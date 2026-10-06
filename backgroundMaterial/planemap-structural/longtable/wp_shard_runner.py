#!/usr/bin/env python3
"""Resumable, crash-tolerant shard runner for the CPU-heavy producer runs (Shard-Runner package v1).

  wp_shard_runner.py plan   RUN_DIR --mode graphs --input LIST.txt --decl DECL.md --phase P1 --order N
                            [--wp WP20] [--shard-size 100] [--first F] [--graph-limit M]
                            [--cpu-cap SECONDS] [--timeout SECONDS] [--max-attempts 3]
  wp_shard_runner.py plan   RUN_DIR --mode chains --seeds SEEDS.txt --chains 12 --steps 400
                            --seed-tag WP21 [--chain-cpu 6000] [--cpu-cap ...] [--timeout ...]
  wp_shard_runner.py run    RUN_DIR [--workers W] [--cpu-cap S] [--timeout S] [--max-attempts N]
                            [--retry-failed]
  wp_shard_runner.py status RUN_DIR [--verify]
  wp_shard_runner.py merge  RUN_DIR OUT.json            (graphs mode; refuses unless every shard is done)
  wp_shard_runner.py merge  RUN_DIR OUT_PREFIX          (chains mode: writes PREFIX{,-evaluated.txt,-log.json}.json)
  wp_shard_runner.py merge  RUN_DIR OUT --partial       (writes OUT, must contain "PARTIAL", "partial": true)
  wp_shard_runner.py worker RUN_DIR SHARD_ID            (internal: one shard in its own process)

Producers are called unchanged (d1_confirm.analyse_graph, wp21_search.chain), so results are
identical to the plain runs.  No multiprocessing.Pool: the scheduler runs every shard in its own
subprocess (own process group) and keeps at most W running.  See shard-runner-report.md.
"""
import argparse
import fcntl
import hashlib
import json
import os
import resource
import signal
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT_CAP = 10 ** 9
EXIT_CAPPED = 3
EMPTY_WIT = lambda: {"sep_bad": [], "d1_kills": [], "p_kills": []}


# ----------------------------------------------------------------------------- helpers
def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def fsync_dir(d):
    fd = os.open(d, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write(path, data):
    """temp file in the same directory, fsync, rename into place, fsync the directory."""
    d = os.path.dirname(os.path.abspath(path))
    tmp = os.path.join(d, ".%s.tmp.%d" % (os.path.basename(path), os.getpid()))
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.rename(tmp, path)
    fsync_dir(d)


def jdump(obj):
    return json.dumps(obj).encode()


def shard_path(run, sid):
    return os.path.join(run, "shards", "shard-%05d.json" % sid)


def load_plan(run):
    with open(os.path.join(run, "plan.json")) as f:
        return json.load(f)


def load_ledger(run):
    with open(os.path.join(run, "ledger.json")) as f:
        return json.load(f)


def cpu_s(t):
    s = 0.0
    for x in [float(y) for y in t.replace("-", ":").split(":")]:
        s = s * 60 + x
    return s


def tree_cpu(pids):
    """Summed CPU seconds (via ps) of the given pids and all their descendants."""
    rows = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,time="], capture_output=True, text=True).stdout.split("\n")
    kids, cpu = {}, {}
    for r in rows:
        p = r.split()
        if len(p) == 3:
            try:
                kids.setdefault(int(p[1]), []).append(int(p[0]))
                cpu[int(p[0])] = cpu_s(p[2])
            except ValueError:
                pass
    out = {}
    for root in pids:
        tot, stack = 0.0, [root]
        while stack:
            q = stack.pop()
            tot += cpu.get(q, 0.0)
            stack.extend(kids.get(q, []))
        out[root] = tot
    return out


def read_lines(path):
    raw = open(path, "rb").read()
    return raw, [l for l in raw.decode().splitlines() if l.strip()]


def producer_files(plan):
    if plan["mode"] == "graphs":
        return ["d1_confirm.py"]
    return ["d1_confirm.py", "wp21_search.py"]


def current_hashes(plan):
    ph = {f: sha_file(os.path.join(HERE, f)) for f in producer_files(plan)}
    dh = sha_file(plan["decl"]) if plan.get("decl") and os.path.exists(plan["decl"]) else ""
    return ph, dh


# ----------------------------------------------------------------------------- plan
def cmd_plan(a):
    run = os.path.abspath(a.run)
    plan = {"version": 1, "mode": a.mode, "cpu_cap": a.cpu_cap, "timeout": a.timeout,
            "max_attempts": a.max_attempts}
    if a.mode == "graphs":
        if not (a.input and a.decl and a.phase and a.order):
            sys.exit("plan graphs needs --input --decl --phase --order")
        raw, lines = read_lines(a.input)
        sel = list(range(len(lines)))[a.first:]
        if a.graph_limit:
            sel = sel[:a.graph_limit]
        shards = []
        for k in range(0, len(sel), a.shard_size):
            part = sel[k:k + a.shard_size]
            shards.append({"id": len(shards), "lo": part[0], "hi": part[-1] + 1})
        plan.update({"input": os.path.abspath(a.input), "input_sha256": sha_bytes(raw),
                     "decl": os.path.abspath(a.decl), "wp": a.wp, "phase": a.phase, "order": a.order,
                     "shard_size": a.shard_size, "first": a.first, "graph_limit": a.graph_limit,
                     "n_graphs": len(sel), "shards": shards})
    else:
        if not (a.seeds and a.chains):
            sys.exit("plan chains needs --seeds --chains")
        raw = open(a.seeds, "rb").read()
        plan.update({"seeds": os.path.abspath(a.seeds), "seeds_sha256": sha_bytes(raw),
                     "decl": os.path.join(HERE, "WP21-declaration.md"),
                     "chains": a.chains, "steps": a.steps, "seed_tag": a.seed_tag,
                     "chain_cpu": a.chain_cpu,
                     "shards": [{"id": c, "chain": c} for c in range(a.chains)]})
    os.makedirs(os.path.join(run, "shards"), exist_ok=True)
    os.makedirs(os.path.join(run, "logs"), exist_ok=True)
    ph, dh = current_hashes(plan)
    plan["producer_sha256"], plan["declaration_sha256"] = ph, dh
    pp = os.path.join(run, "plan.json")
    if os.path.exists(pp):
        old = load_plan(run)
        keep = ("cpu_cap", "timeout", "max_attempts")
        if {k: v for k, v in old.items() if k not in keep} != {k: v for k, v in plan.items() if k not in keep}:
            sys.exit("a different plan already exists in %s (use a new run directory)" % run)
        print("plan already present and identical; %d shards" % len(plan["shards"]))
        return
    atomic_write(pp, json.dumps(plan, indent=1).encode())
    led = {"plan_sha256": sha_file(pp), "state": "partial", "cpu_done": 0.0, "cpu_wasted": 0.0,
           "scheduler_pid": None, "updated": time.time(),
           "shards": {str(s["id"]): {"id": s["id"], "range": [s.get("lo"), s.get("hi")] if a.mode == "graphs"
                                     else [s["chain"], s["chain"] + 1],
                                     "status": "pending", "attempts": 0, "sha256": "", "wall_seconds": 0.0,
                                     "cpu_seconds": 0.0, "error": "", "history": [],
                                     "producer_sha256": ph, "declaration_sha256": dh}
                      for s in plan["shards"]}}
    atomic_write(os.path.join(run, "ledger.json"), json.dumps(led, indent=1).encode())
    print("planned %d shards (%s) in %s" % (len(plan["shards"]), a.mode, run))


# ----------------------------------------------------------------------------- worker
def cmd_worker(a):
    run = os.path.abspath(a.run)
    plan = load_plan(run)
    sid = a.shard
    # die with the scheduler (no orphan keeps burning CPU if the scheduler is SIGKILLed)
    ppid = os.getppid()

    def watch():
        while True:
            time.sleep(1.0)
            if os.getppid() != ppid:
                os._exit(77)
    threading.Thread(target=watch, daemon=True).start()
    ph, dh = current_hashes(plan)
    if ph != plan["producer_sha256"] or dh != plan["declaration_sha256"]:
        print("ERROR producer or declaration hash differs from the plan", flush=True)
        sys.exit(4)
    # test hook: delay (seconds) before computing; WP_SHARD_TEST_SLEEP_IDS restricts it to some shard ids
    slp = float(os.environ.get("WP_SHARD_TEST_SLEEP", "0") or 0)
    ids = os.environ.get("WP_SHARD_TEST_SLEEP_IDS", "")
    if slp and (not ids or str(sid) in ids.split(",")):
        time.sleep(slp)
    t0 = time.time()
    sh = next(s for s in plan["shards"] if s["id"] == sid)
    if plan["mode"] == "graphs":
        import d1_confirm as P
        raw, lines = read_lines(plan["input"])
        if sha_bytes(raw) != plan["input_sha256"]:
            print("ERROR input file changed since plan", flush=True)
            sys.exit(4)
        graphs, wit = [], EMPTY_WIT()
        for idx in range(sh["lo"], sh["hi"]):
            g, w = P.analyse_graph((idx, lines[idx]))
            graphs.append(g)
            for k in wit:
                wit[k].extend(w[k])
        payload = {"shard": sid, "lo": sh["lo"], "hi": sh["hi"], "graphs": graphs, "witnesses": wit}
    else:
        import wp21_search as W
        seeds = [l.strip() for l in open(plan["seeds"]) if l.strip()]
        job = W.make_jobs(seeds, plan["chains"], plan["steps"], plan["seed_tag"], plan["chain_cpu"])[sh["chain"]]
        cid, evaluated, best, secs = W.chain(job)
        payload = {"shard": sid, "chain": cid, "evaluated": evaluated, "best": best}
    data = jdump(payload)
    atomic_write(shard_path(run, sid), data)
    ru = resource.getrusage(resource.RUSAGE_SELF)
    print("RESULT " + json.dumps({"sha256": sha_bytes(data), "wall": time.time() - t0,
                                  "cpu": ru.ru_utime + ru.ru_stime}), flush=True)


# ----------------------------------------------------------------------------- scheduler
class Scheduler:
    def __init__(self, run, workers, a):
        self.run = run
        self.plan = load_plan(run)
        if a.cpu_cap is not None:
            self.plan["cpu_cap"] = a.cpu_cap
        if a.timeout is not None:
            self.plan["timeout"] = a.timeout
        if a.max_attempts is not None:
            self.plan["max_attempts"] = a.max_attempts
        self.workers = workers
        self.retry_failed = a.retry_failed
        self.led = load_ledger(run)
        self.stop_sig = None
        self.running = {}   # sid -> dict(proc, t0, log)
        self.last_flush = 0

    def flush(self):
        self.led["updated"] = time.time()
        atomic_write(os.path.join(self.run, "ledger.json"), json.dumps(self.led, indent=1).encode())

    def shard_ok(self, e):
        p = shard_path(self.run, e["id"])
        return e["status"] == "done" and e["sha256"] and os.path.exists(p) and sha_file(p) == e["sha256"]

    def overall(self):
        sh = self.led["shards"].values()
        if all(e["status"] == "done" for e in sh):
            return "complete"
        if any(e["status"] == "capped" for e in sh) or self.led.get("capped"):
            return "capped"
        if any(e["status"] == "failed" for e in sh):
            return "failed"
        return "partial"

    def prepare(self):
        ph, dh = current_hashes(self.plan)
        if ph != self.plan["producer_sha256"] or dh != self.plan["declaration_sha256"]:
            sys.exit("producer or declaration hash differs from the plan; refusing to run")
        self.led["capped"] = False
        sd = os.path.join(self.run, "shards")
        for fn in os.listdir(sd):                  # leftover temp files of dead workers
            if fn.startswith(".") and ".tmp." in fn:
                try:
                    if not pid_alive(int(fn.rsplit(".", 1)[1])):
                        os.remove(os.path.join(sd, fn))
                except (ValueError, OSError):
                    pass
        for e in self.led["shards"].values():
            if e["status"] == "done":
                if not self.shard_ok(e):
                    e["error"] = "shard file missing or hash mismatch; recomputing"
                    e["status"], e["sha256"] = "pending", ""
            elif e["status"] in ("running", "capped", "timeout"):
                e["status"] = "pending"          # stale entry of a dead scheduler / earlier cap
            elif e["status"] == "failed" and self.retry_failed:
                e["status"], e["attempts"], e["error"] = "pending", 0, ""
        self.flush()

    def launch(self, sid):
        e = self.led["shards"][str(sid)]
        e["status"], e["error"] = "running", ""
        e["attempts"] += 1
        logp = os.path.join(self.run, "logs", "shard-%05d.log" % sid)
        lf = open(logp, "w")
        proc = subprocess.Popen([sys.executable, os.path.abspath(__file__), "worker", self.run, str(sid)],
                                stdout=lf, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                start_new_session=True)
        lf.close()
        self.running[sid] = {"proc": proc, "t0": time.time(), "log": logp, "cpu": 0.0}
        self.flush()

    def kill(self, sid, sig_first=signal.SIGTERM):
        r = self.running[sid]
        p = r["proc"]
        for sg in (sig_first, signal.SIGKILL):
            try:
                os.killpg(p.pid, sg)
            except ProcessLookupError:
                break
            try:
                p.wait(timeout=3)
                break
            except subprocess.TimeoutExpired:
                continue
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.wait()

    def finish(self, sid, why=None):
        """Account for a shard whose process has ended (or has just been killed)."""
        r = self.running.pop(sid)
        e = self.led["shards"][str(sid)]
        wall = time.time() - r["t0"]
        rc = r["proc"].returncode
        res = None
        try:
            for ln in open(r["log"]).read().splitlines():
                if ln.startswith("RESULT "):
                    res = json.loads(ln[7:])
        except Exception:
            pass
        if why is None and rc == 0 and res:
            p = shard_path(self.run, sid)
            if os.path.exists(p) and sha_file(p) == res["sha256"]:
                e.update(status="done", sha256=res["sha256"], wall_seconds=round(wall, 2),
                         cpu_seconds=round(res["cpu"], 2), error="")
                e["history"].append("done")
                self.led["cpu_done"] += res["cpu"]
                return
            why = "result file missing or hash mismatch"
        if why is None:
            why = ("killed by signal %d" % -rc) if rc < 0 else ("exit code %d" % rc)
            try:
                tail = open(r["log"]).read().strip().splitlines()[-1:]
                if tail:
                    why += ": " + tail[0][:300]
            except Exception:
                pass
        self.led["cpu_wasted"] += r["cpu"]
        e["error"] = why
        e["wall_seconds"] = round(wall, 2)
        e["history"].append(why[:80])
        if why.startswith("timeout"):
            e["status"] = "timeout"
        else:
            e["status"] = "pending"
        if e["attempts"] >= self.plan["max_attempts"]:
            e["status"] = "failed"
            e["error"] = "gave up after %d attempts; last: %s" % (e["attempts"], why)
        elif e["status"] == "timeout":
            e["status"] = "pending"        # retried; the history keeps the timeout

    def cpu_total(self):
        return self.led["cpu_done"] + self.led["cpu_wasted"] + sum(r["cpu"] for r in self.running.values())

    def handle_signal(self, signum, frm):
        self.stop_sig = signum

    def shutdown(self, reason):
        for sid in list(self.running):
            self.kill(sid)
            r = self.running.pop(sid)
            e = self.led["shards"][str(sid)]
            self.led["cpu_wasted"] += r["cpu"]
            e["status"] = "capped" if reason == "capped" else "pending"
            e["attempts"] = max(0, e["attempts"] - (0 if reason == "capped" else 1))
            e["error"] = "stopped: " + reason
        if reason == "capped":
            self.led["capped"] = True
            for e in self.led["shards"].values():
                if e["status"] == "pending":
                    e["status"] = "capped"
                    e["error"] = "not run: CPU cap reached"
        self.led["state"] = self.overall() if reason != "signal" else "partial"
        self.led["scheduler_pid"] = None
        self.flush()

    def loop(self):
        lockf = open(os.path.join(self.run, "lock"), "w")
        try:
            fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            sys.exit("another scheduler holds the lock on %s" % self.run)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)
        self.prepare()
        self.led["scheduler_pid"] = os.getpid()
        self.led["cpu_cap"] = self.plan["cpu_cap"]
        queue = [e["id"] for e in sorted(self.led["shards"].values(), key=lambda e: e["id"])
                 if e["status"] == "pending"]
        last_ps = 0
        cap = self.plan["cpu_cap"]
        self.flush()
        while True:
            if self.stop_sig:
                self.shutdown("signal")
                return 128 + self.stop_sig
            # reap
            for sid in list(self.running):
                r = self.running[sid]
                if r["proc"].poll() is not None:
                    self.finish(sid)
                    self.flush()
                    if self.led["shards"][str(sid)]["status"] == "pending":
                        queue.insert(0, sid)     # retry soon
                elif time.time() - r["t0"] > self.plan["timeout"]:
                    self.kill(sid)
                    self.finish(sid, why="timeout after %.0fs" % self.plan["timeout"])
                    self.flush()
                    if self.led["shards"][str(sid)]["status"] == "pending":
                        queue.insert(0, sid)
            # cpu accounting
            if self.running and time.time() - last_ps > 1.0:
                last_ps = time.time()
                try:
                    cp = tree_cpu([r["proc"].pid for r in self.running.values()])
                    for r in self.running.values():
                        r["cpu"] = cp.get(r["proc"].pid, r["cpu"])
                except Exception:
                    pass
            if cap is not None and self.cpu_total() > cap:
                print("CAPPED: CPU %.0fs exceeds cap %.0fs" % (self.cpu_total(), cap), flush=True)
                self.shutdown("capped")
                return EXIT_CAPPED
            while queue and len(self.running) < self.workers:
                self.launch(queue.pop(0))
            if not self.running and not queue:
                break
            time.sleep(0.1)
        self.led["state"] = self.overall()
        self.led["scheduler_pid"] = None
        self.flush()
        return 0 if self.led["state"] == "complete" else 1


def cmd_run(a):
    run = os.path.abspath(a.run)
    s = Scheduler(run, a.workers, a)
    rc = s.loop()
    print(status_text(run))
    sys.exit(rc)


# ----------------------------------------------------------------------------- status / merge
def status_data(run, verify=False):
    plan, led = load_plan(run), load_ledger(run)
    total = len(plan["shards"])
    counts = {}
    damaged = []
    for e in led["shards"].values():
        st = e["status"]
        if st == "done":
            p = shard_path(run, e["id"])
            if not os.path.exists(p) or (verify and sha_file(p) != e["sha256"]):
                st = "damaged"
                damaged.append(e["id"])
        if st == "running" and not (led.get("scheduler_pid") and pid_alive(led["scheduler_pid"])):
            st = "pending"                     # stale entry of a dead scheduler
        counts[st] = counts.get(st, 0) + 1
    done = counts.get("done", 0)
    if done == total:
        state = "complete"
    elif counts.get("capped") or led.get("capped"):
        state = "capped"
    elif counts.get("failed"):
        state = "failed"
    else:
        state = "partial"
    return {"done": done, "total": total, "state": state, "counts": counts, "damaged": damaged,
            "cpu_done": led["cpu_done"], "cpu_wasted": led["cpu_wasted"], "cpu_cap": plan["cpu_cap"]}


def pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def status_text(run, verify=False):
    d = status_data(run, verify)
    return ("shards done %d/%d  state %s  counts %s  damaged %s  cpu_done %.1fs cpu_wasted %.1fs cap %s"
            % (d["done"], d["total"], d["state"], json.dumps(d["counts"], sort_keys=True), d["damaged"],
               d["cpu_done"], d["cpu_wasted"], d["cpu_cap"]))


def cmd_status(a):
    print(status_text(os.path.abspath(a.run), a.verify))
    sys.exit(0 if status_data(os.path.abspath(a.run), a.verify)["state"] == "complete" else 1)


def read_shards(run, plan, led, partial):
    """Load shard payloads in shard-id order, each verified against the ledger hash."""
    out, missing = [], []
    for s in plan["shards"]:
        e = led["shards"][str(s["id"])]
        p = shard_path(run, s["id"])
        ok = e["status"] == "done" and os.path.exists(p) and sha_file(p) == e["sha256"]
        if not ok:
            missing.append(s["id"])
            continue
        out.append(json.load(open(p)))
    if missing and not partial:
        sys.exit("MERGE REFUSED: shards not done or damaged: %s (state %s)" %
                 (missing[:20], status_data(run)["state"]))
    return out, missing


def cmd_merge(a):
    run = os.path.abspath(a.run)
    plan, led = load_plan(run), load_ledger(run)
    ph, dh = current_hashes(plan)
    if ph != plan["producer_sha256"] or dh != plan["declaration_sha256"]:
        sys.exit("MERGE REFUSED: producer or declaration hash differs from the plan")
    payloads, missing = read_shards(run, plan, led, a.partial)
    if a.partial:
        if "PARTIAL" not in os.path.basename(a.out):
            sys.exit("a partial output must have PARTIAL in its file name")
    if plan["mode"] == "graphs":
        raw, _ = read_lines(plan["input"])
        if sha_bytes(raw) != plan["input_sha256"]:
            sys.exit("MERGE REFUSED: input file changed since plan")
        graphs, wit = [], EMPTY_WIT()
        for pl in payloads:
            graphs.extend(pl["graphs"])
            for k in wit:
                wit[k].extend(pl["witnesses"][k])
        graphs.sort(key=lambda g: g["index"])
        for k in wit:
            wit[k].sort(key=lambda w: w["index"])        # stable: producer order within a graph
        out = {"wp": plan["wp"], "phase": plan["phase"], "order": plan["order"],
               "declaration_sha256": dh, "input_sha256": plan["input_sha256"],
               "producer_sha256": ph, "graphs": graphs, "witnesses": wit, "truncated": False,
               "wall_seconds": 0.0}
        txt = json.dumps(out)
        if len(txt) > OUT_CAP:
            out["witnesses"] = EMPTY_WIT()
            out["truncated"] = True
        if a.partial:
            out["wp"] = "PARTIAL-" + out["wp"]
            out["partial"] = True
            out["missing_shards"] = missing
        atomic_write(a.out, json.dumps(out).encode())
        print("wrote %s (%d graphs)%s" % (a.out, len(graphs), " PARTIAL, missing %s" % missing if a.partial else ""))
    else:
        import wp21_search as W
        results = [(pl["chain"], pl["evaluated"], pl["best"], 0.0) for pl in payloads]
        if a.partial:
            sys.exit("partial merge is only implemented for graphs mode; use status")
        print(W.assemble(results, a.out, plan["seed_tag"], plan["chains"], plan["steps"]))


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("plan")
    p.add_argument("run")
    p.add_argument("--mode", choices=["graphs", "chains"], required=True)
    p.add_argument("--input")
    p.add_argument("--decl")
    p.add_argument("--wp", default="WP20")
    p.add_argument("--phase")
    p.add_argument("--order", type=int)
    p.add_argument("--shard-size", type=int, default=100)
    p.add_argument("--first", type=int, default=0)
    p.add_argument("--graph-limit", type=int, default=0)
    p.add_argument("--seeds")
    p.add_argument("--chains", type=int)
    p.add_argument("--steps", type=int, default=100)
    p.add_argument("--seed-tag", default="WP21")
    p.add_argument("--chain-cpu", type=float, default=1e12)
    p.add_argument("--cpu-cap", type=float, default=None, help="CPU-seconds cap for the whole phase")
    p.add_argument("--timeout", type=float, default=4 * 3600, help="wall seconds per shard attempt")
    p.add_argument("--max-attempts", type=int, default=3)
    p.set_defaults(f=cmd_plan)
    p = sp.add_parser("run")
    p.add_argument("run")
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--cpu-cap", type=float, default=None)
    p.add_argument("--timeout", type=float, default=None)
    p.add_argument("--max-attempts", type=int, default=None)
    p.add_argument("--retry-failed", action="store_true")
    p.set_defaults(f=cmd_run)
    p = sp.add_parser("status")
    p.add_argument("run")
    p.add_argument("--verify", action="store_true")
    p.set_defaults(f=cmd_status)
    p = sp.add_parser("merge")
    p.add_argument("run")
    p.add_argument("out")
    p.add_argument("--partial", action="store_true")
    p.set_defaults(f=cmd_merge)
    p = sp.add_parser("worker")
    p.add_argument("run")
    p.add_argument("shard", type=int)
    p.set_defaults(f=cmd_worker)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
