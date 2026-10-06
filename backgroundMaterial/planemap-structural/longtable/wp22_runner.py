#!/usr/bin/env python3
"""wp22_runner.py -- sharded, resumable, capped runner for WP22 (S2).  Same style as the WP20 shard runner, own code.

  wp22_runner.py plan   RUN_DIR --mode s2a [--tags 40] [--tag-cpu 120] [--max-steps N] [--cpu-cap 6000]
  wp22_runner.py plan   RUN_DIR --mode s2b [--orders 3,4,5] [--reduced] [--shard-cpu 3600] [--cpu-cap C]
  wp22_runner.py plan   RUN_DIR --mode s2c --cert-dir DIR [--cert-dir DIR ...] [--shard-cpu 3600] [--cpu-cap C]
  wp22_runner.py run    RUN_DIR [--workers W] [--cpu-cap S] [--timeout S] [--max-attempts N] [--retry-failed]
  wp22_runner.py status RUN_DIR [--verify]
  wp22_runner.py merge  RUN_DIR OUT_PREFIX        (refuses unless every shard is done and verified)
  wp22_runner.py record OUT_FILE --run RUN_DIR [--run RUN_DIR ...] [--workers W] [--start T] [--end T]
  wp22_runner.py worker RUN_DIR SHARD_ID          (internal)

One shard = one S2a tag | one S2b (graph, hole) | one S2c certificate file.  Every shard runs in its own subprocess
(own process group); the scheduler keeps at most W alive, retries a shard whose process died (SIGKILL, crash, wall
timeout) up to max-attempts, and writes shard files atomically (temp file, fsync, rename).  A ledger (ledger.json,
atomically rewritten) holds the SHA-256 of every finished shard; a missing or hash-mismatching shard is recomputed
on the next `run`.  SIGTERM/SIGINT on the scheduler kills the workers, saves the ledger and exits 128+signal.
CPU cap: the scheduler sums CPU seconds (ps, process trees) of finished and running shards; it does not LAUNCH a
shard whose per-shard CPU budget would take the reserved total over the cap, and kills everything if the measured
total exceeds the cap.  Capped shards are left 'capped' and `merge` refuses: a capped run is inconclusive.
A shard file is a deterministic function of the plan (no timing, no hostname); timing lives in the ledger.
Package hashes: the plan records the SHA-256 of the producer files and the pre-registration; workers and merge
refuse to run if any differs from the plan.
"""
import argparse
import fcntl
import hashlib
import json
import os
import platform
import resource
import signal
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

EXIT_CAPPED = 3
PRODUCERS = ["wp22_radius.py", "wp22_search.py", "wp22_census.py", "wp22_s2c.py", "wp22_runner.py"]
DECLS = ["WP22-S2-preregistration.md", "WP22-interface.md"]
DEFAULT_CERT_DIRS = [os.path.join(HERE, "../../../SolvingFrameworkPlan/docs/working/MathChainSearch/certs_len_ge6"),
                     os.path.join(HERE, "../../../SolvingFrameworkPlan/docs/working/MathChainSearch/lt_certs")]


# ----------------------------------------------------------------------------- helpers
def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def atomic_write(path, data):
    d = os.path.dirname(os.path.abspath(path))
    tmp = os.path.join(d, ".%s.tmp.%d" % (os.path.basename(path), os.getpid()))
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.rename(tmp, path)
    fd = os.open(d, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def jdump(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def shard_path(run, sid):
    return os.path.join(run, "shards", "shard-%05d.json" % sid)


def load_plan(run):
    with open(os.path.join(run, "plan.json")) as f:
        return json.load(f)


def load_ledger(run):
    with open(os.path.join(run, "ledger.json")) as f:
        return json.load(f)


def pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def cpu_s(t):
    s = 0.0
    for x in [float(y) for y in t.replace("-", ":").split(":")]:
        s = s * 60 + x
    return s


def tree_cpu(pids):
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


def package_hashes(plan_files=None):
    ph = {f: sha_file(os.path.join(HERE, f)) for f in PRODUCERS}
    dh = {f: sha_file(os.path.join(HERE, f)) for f in DECLS}
    return ph, dh


# ----------------------------------------------------------------------------- plan
def cmd_plan(a):
    run = os.path.abspath(a.run)
    plan = {"version": 1, "mode": a.mode, "cpu_cap": a.cpu_cap, "timeout": a.timeout, "max_attempts": a.max_attempts,
            "shard_cpu": a.shard_cpu}
    if a.mode == "s2a":
        import wp22_search as S
        tags = S.tags()[:a.tags]
        plan.update({"tags": tags, "tag_cpu": a.tag_cpu, "max_steps": a.max_steps, "shard_cpu": a.tag_cpu,
                     "shards": [{"id": i, "tag": t} for i, t in enumerate(tags)]})
        if plan["cpu_cap"] is None:
            plan["cpu_cap"] = 6000.0
    elif a.mode == "s2b":
        import wp22_census as C
        orders = tuple(int(x) for x in a.orders.split(","))
        gs = C.groups(a.reduced, orders)
        plan.update({"orders": list(orders), "reduced": bool(a.reduced),
                     "shards": [{"id": i, "graph": g, "r": r, "hole": h, "weight": w}
                                for i, (g, r, h, w) in enumerate(gs)]})
    else:
        import wp22_s2c as X
        dirs = [os.path.abspath(d) for d in (a.cert_dir or DEFAULT_CERT_DIRS)]
        files = X.list_certs(dirs)
        if not files:
            sys.exit("no certificate files found in %s" % dirs)
        plan.update({"cert_dirs": dirs, "shards": [{"id": i, "file": f, "file_sha256": sha_file(f)}
                                                   for i, f in enumerate(files)]})
    os.makedirs(os.path.join(run, "shards"), exist_ok=True)
    os.makedirs(os.path.join(run, "logs"), exist_ok=True)
    ph, dh = package_hashes()
    plan["producer_sha256"], plan["declaration_sha256"] = ph, dh
    pp = os.path.join(run, "plan.json")
    if os.path.exists(pp):
        old = load_plan(run)
        keep = ("cpu_cap", "timeout", "max_attempts")
        if {k: v for k, v in old.items() if k not in keep} != {k: v for k, v in plan.items() if k not in keep}:
            sys.exit("a different plan already exists in %s (use a new run directory)" % run)
        print("plan already present and identical; %d shards" % len(plan["shards"]))
        return
    atomic_write(pp, json.dumps(plan, indent=1, sort_keys=True).encode())
    led = {"plan_sha256": sha_file(pp), "state": "partial", "cpu_done": 0.0, "cpu_wasted": 0.0, "capped": False,
           "scheduler_pid": None, "updated": time.time(),
           "shards": {str(s["id"]): {"id": s["id"], "status": "pending", "attempts": 0, "sha256": "", "pid": None,
                                     "wall_seconds": 0.0, "cpu_seconds": 0.0, "error": "", "history": []}
                      for s in plan["shards"]}}
    atomic_write(os.path.join(run, "ledger.json"), json.dumps(led, indent=1).encode())
    print("planned %d shards (%s) in %s" % (len(plan["shards"]), a.mode, run))


# ----------------------------------------------------------------------------- worker
def compute_shard(plan, sh):
    """the deterministic payload of one shard."""
    import time as _t
    mode = plan["mode"]
    if mode == "s2a":
        import wp22_search as S
        res = S.search_tag(sh["tag"], plan["tag_cpu"], plan["max_steps"])
        return {"mode": "s2a", "shard": sh["id"], "result": res}
    if mode == "s2b":
        import wp22_census as C
        deadline = _t.process_time() + plan["shard_cpu"]
        recs, summ = C.census_hole(sh["graph"], sh["r"], sh["hole"], deadline=deadline)
        summ["weight"] = sh["weight"]
        return {"mode": "s2b", "shard": sh["id"], "summary": summ, "records": recs}
    import wp22_s2c as X
    if sha_file(sh["file"]) != sh["file_sha256"]:
        print("ERROR certificate file changed since plan", flush=True)
        sys.exit(4)
    deadline = _t.process_time() + plan["shard_cpu"]
    recs, summ = X.cert_records(sh["file"], deadline=deadline, name=os.path.basename(sh["file"]))
    return {"mode": "s2c", "shard": sh["id"], "summary": summ, "records": recs}


def cmd_worker(a):
    run = os.path.abspath(a.run)
    plan = load_plan(run)
    sid = a.shard
    ppid = os.getppid()

    def watch():
        while True:
            time.sleep(1.0)
            if os.getppid() != ppid:
                os._exit(77)
    threading.Thread(target=watch, daemon=True).start()
    ph, dh = package_hashes()
    if ph != plan["producer_sha256"] or dh != plan["declaration_sha256"]:
        print("ERROR package file hash differs from the plan", flush=True)
        sys.exit(4)
    slp = float(os.environ.get("WP22_TEST_SLEEP", "0") or 0)       # test hook: delay before computing
    ids = os.environ.get("WP22_TEST_SLEEP_IDS", "")
    if slp and (not ids or str(sid) in ids.split(",")):
        time.sleep(slp)
    t0 = time.time()
    sh = next(s for s in plan["shards"] if s["id"] == sid)
    payload = compute_shard(plan, sh)
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
        for k in ("cpu_cap", "timeout", "max_attempts"):
            if getattr(a, k) is not None:
                self.plan[k] = getattr(a, k)
        self.workers = workers
        self.retry_failed = a.retry_failed
        self.led = load_ledger(run)
        self.stop_sig = None
        self.running = {}

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
        ph, dh = package_hashes()
        if ph != self.plan["producer_sha256"] or dh != self.plan["declaration_sha256"]:
            sys.exit("package file hash differs from the plan; refusing to run")
        self.led["capped"] = False
        sd = os.path.join(self.run, "shards")
        for fn in os.listdir(sd):
            if fn.startswith(".") and ".tmp." in fn:
                try:
                    if not pid_alive(int(fn.rsplit(".", 1)[1])):
                        os.remove(os.path.join(sd, fn))
                except (ValueError, OSError):
                    pass
        for e in self.led["shards"].values():
            e["pid"] = None
            if e["status"] == "done":
                if not self.shard_ok(e):
                    e["error"] = "shard file missing or hash mismatch; recomputing"
                    e["status"], e["sha256"] = "pending", ""
            elif e["status"] in ("running", "capped", "timeout"):
                e["status"] = "pending"
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
        e["pid"] = proc.pid
        self.running[sid] = {"proc": proc, "t0": time.time(), "log": logp, "cpu": 0.0}
        self.flush()

    def kill(self, sid):
        p = self.running[sid]["proc"]
        for sg in (signal.SIGTERM, signal.SIGKILL):
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
        r = self.running.pop(sid)
        e = self.led["shards"][str(sid)]
        e["pid"] = None
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
        e["status"] = "pending"
        if e["attempts"] >= self.plan["max_attempts"]:
            e["status"] = "failed"
            e["error"] = "gave up after %d attempts; last: %s" % (e["attempts"], why)

    def cpu_total(self):
        return self.led["cpu_done"] + self.led["cpu_wasted"] + sum(r["cpu"] for r in self.running.values())

    def reserved(self):
        """CPU already spent plus the per-shard budget of every running shard (not less than what it has used)."""
        b = self.plan.get("shard_cpu") or 0.0
        return self.led["cpu_done"] + self.led["cpu_wasted"] + sum(max(r["cpu"], b) for r in self.running.values())

    def handle_signal(self, signum, frm):
        self.stop_sig = signum

    def shutdown(self, reason):
        for sid in list(self.running):
            self.kill(sid)
            r = self.running.pop(sid)
            e = self.led["shards"][str(sid)]
            e["pid"] = None
            self.led["cpu_wasted"] += r["cpu"]
            e["status"] = "capped" if reason == "capped" else "pending"
            e["attempts"] = max(0, e["attempts"] - (0 if reason == "capped" else 1))
            e["error"] = "stopped: " + reason
        if reason == "capped":
            self.mark_capped()
        self.led["state"] = self.overall() if reason != "signal" else "partial"
        self.led["scheduler_pid"] = None
        self.flush()

    def mark_capped(self):
        self.led["capped"] = True
        for e in self.led["shards"].values():
            if e["status"] == "pending":
                e["status"] = "capped"
                e["error"] = "not run: CPU cap reached"

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
        cap = self.plan["cpu_cap"]
        last_ps = 0
        self.flush()
        while True:
            if self.stop_sig:
                self.shutdown("signal")
                return 128 + self.stop_sig
            for sid in list(self.running):
                r = self.running[sid]
                if r["proc"].poll() is not None:
                    self.finish(sid)
                    self.flush()
                    if self.led["shards"][str(sid)]["status"] == "pending":
                        queue.insert(0, sid)
                elif time.time() - r["t0"] > self.plan["timeout"]:
                    self.kill(sid)
                    self.finish(sid, why="timeout after %.0fs" % self.plan["timeout"])
                    self.flush()
                    if self.led["shards"][str(sid)]["status"] == "pending":
                        queue.insert(0, sid)
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
                if cap is not None and self.reserved() + (self.plan.get("shard_cpu") or 0.0) > cap:
                    print("CAPPED: launching another shard could exceed the cap %.0fs" % cap, flush=True)
                    for sid in queue:
                        self.led["shards"][str(sid)]["status"] = "pending"
                    queue = []
                    self.mark_capped()
                    break
                self.launch(queue.pop(0))
            if not self.running and not queue:
                break
            time.sleep(0.1)
        self.led["state"] = self.overall()
        self.led["scheduler_pid"] = None
        self.flush()
        return 0 if self.led["state"] == "complete" else (EXIT_CAPPED if self.led["state"] == "capped" else 1)


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
    counts, damaged = {}, []
    for e in led["shards"].values():
        st = e["status"]
        if st == "done":
            p = shard_path(run, e["id"])
            if not os.path.exists(p) or (verify and sha_file(p) != e["sha256"]):
                st = "damaged"
                damaged.append(e["id"])
        if st == "running" and not (led.get("scheduler_pid") and pid_alive(led["scheduler_pid"])):
            st = "pending"
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


def status_text(run, verify=False):
    d = status_data(run, verify)
    return ("shards done %d/%d  state %s  counts %s  damaged %s  cpu_done %.1fs cpu_wasted %.1fs cap %s"
            % (d["done"], d["total"], d["state"], json.dumps(d["counts"], sort_keys=True), d["damaged"],
               d["cpu_done"], d["cpu_wasted"], d["cpu_cap"]))


def cmd_status(a):
    run = os.path.abspath(a.run)
    print(status_text(run, a.verify))
    sys.exit(0 if status_data(run, a.verify)["state"] == "complete" else 1)


def read_shards(run, plan, led):
    out, missing = [], []
    for s in plan["shards"]:
        e = led["shards"][str(s["id"])]
        p = shard_path(run, s["id"])
        if e["status"] == "done" and os.path.exists(p) and sha_file(p) == e["sha256"]:
            out.append(json.load(open(p)))
        else:
            missing.append(s["id"])
    if missing:
        sys.exit("MERGE REFUSED: shards not done or damaged: %s (state %s)" % (missing[:20], status_data(run)["state"]))
    return out


def merge_s2a(plan, payloads):
    rows, hist, restart_hist, kills = [], {}, {}, []
    best_all = None
    for pl in payloads:
        r = pl["result"]
        b = r.get("best")
        rows.append({"tag": r["tag"], "steps": r["steps"], "evals": r["evals"], "restarts": r["restarts"],
                     "stopped": r["stopped"], "capped": r["capped"], "unresolved_evals": r["unresolved_evals"],
                     "best_r": b["r"] if b else None, "best_ball": b["ball"] if b else None,
                     "best_order": b["order"] if b else None, "best_status": b["status"] if b else None,
                     "kill2": len(r["kill2"])})
        for k, v in r["r_hist"].items():
            hist[k] = hist.get(k, 0) + v
        for rb in r["per_restart_best"]:
            restart_hist[str(rb[0])] = restart_hist.get(str(rb[0]), 0) + 1
        kills.extend({"tag": r["tag"], "certificate": c} for c in r["kill2"])
        if b and (best_all is None or (b["r"], b["ball"]) > (best_all["r"], best_all["ball"])):
            best_all = {"tag": r["tag"], "r": b["r"], "ball": b["ball"], "cert": b["cert"]}
    num = lambda d: dict(sorted(d.items(), key=lambda kv: int(kv[0])))
    out = {"phase": "S2a", "tags": len(rows), "per_tag": rows, "max_r_over_tags": best_all["r"] if best_all else None,
           "best": best_all, "r_hist_all_evaluations": num(hist), "per_restart_best_hist": num(restart_hist),
           "tags_capped_at_cpu": sum(1 for x in rows if x["capped"]), "kill2": kills,
           "any_kill2": bool(kills), "plan_sha256_note": "see ledger"}
    return {"": out}


def merge_s2b(plan, payloads):
    recs = []
    per, hist = [], {}
    for pl in payloads:
        recs.extend(pl["records"])
        s = pl["summary"]
        per.append({k: v for k, v in s.items() if k != "kill2_candidates"})
        for k, v in s["radius_hist"].items():
            hist[k] = hist.get(k, 0) + v
    recs.sort(key=lambda r: (r["graph"], r["v"], r["state"]))
    kills = [c for pl in payloads for c in pl["summary"]["kill2_candidates"]]
    byg = {}
    for p in per:
        g = byg.setdefault(p["graph"], {})
        for k, v in p["radius_hist"].items():
            g[k] = g.get(k, 0) + v
    key = lambda d: dict(sorted(d.items(), key=lambda kv: (kv[0] == "inf", kv[0] == "None", kv[0])))
    summ = {"phase": "S2b", "reduced": plan["reduced"], "holes": len(per), "doubly_locked_states": len(recs),
            "radius_hist_all": key(hist), "radius_hist_by_graph": {g: key(v) for g, v in sorted(byg.items())},
            "max_radius": max((r["radius"] for r in recs if isinstance(r["radius"], int)), default=None),
            "capped_states": sum(p["capped"] for p in per), "kill2_candidates": kills, "per_hole": per}
    return {".jsonl": "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n" for r in recs),
            "": summ}


def merge_s2c(plan, payloads):
    recs, per, hist = [], [], {}
    for pl in payloads:
        recs.extend(pl["records"])
        per.append(pl["summary"])
        for k, v in pl["summary"]["radius_hist_dl"].items():
            hist[k] = hist.get(k, 0) + v
    summ = {"phase": "S2c", "label": "descriptive, post hoc, not a kill criterion", "certificates": len(per),
            "dl_states": sum(p["doubly_locked_states"] for p in per),
            "radius_hist_dl": dict(sorted(hist.items(), key=lambda kv: kv[0])),
            "max_radius_dl": max((p["max_radius_dl"] for p in per if p["max_radius_dl"] is not None), default=None),
            "capped_states": sum(p["capped"] for p in per),
            "kill2_candidates": [(p["cert"], p["kill2_candidates"]) for p in per if p["kill2_candidates"]],
            "per_certificate": per}
    return {".jsonl": "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n" for r in recs),
            "": summ}


def cmd_merge(a):
    run = os.path.abspath(a.run)
    plan, led = load_plan(run), load_ledger(run)
    ph, dh = package_hashes()
    if ph != plan["producer_sha256"] or dh != plan["declaration_sha256"]:
        sys.exit("MERGE REFUSED: package file hash differs from the plan")
    payloads = read_shards(run, plan, led)
    if plan["mode"] == "s2a":
        outs = merge_s2a(plan, payloads)
    elif plan["mode"] == "s2b":
        outs = merge_s2b(plan, payloads)
    else:
        outs = merge_s2c(plan, payloads)
    for suffix, content in outs.items():
        path = a.out + suffix + ("" if suffix else "-summary") + (".json" if suffix == "" else "")
        data = content.encode() if isinstance(content, str) else \
            json.dumps(content, sort_keys=True, indent=1).encode() + b"\n"
        atomic_write(path, data)
        print("wrote %s sha256 %s" % (path, sha_bytes(data)))


# ----------------------------------------------------------------------------- record
def sh(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, shell=True, cwd=HERE).stdout.strip()
    except Exception:
        return "?"


def cmd_record(a):
    mem = sh("sysctl -n hw.memsize") or sh("grep MemTotal /proc/meminfo")
    cpu = sh("sysctl -n machdep.cpu.brand_string") or platform.processor()
    lines = ["WP22 RECORD", "machine: %s (%s)" % (platform.node(), platform.platform()), "cpu brand: %s" % cpu,
             "cores: %s" % (os.cpu_count()), "memory: %s" % mem, "python: %s" % sys.version.replace("\n", " "),
             "git head: %s" % sh("git rev-parse HEAD"), "git status of package files: %s" %
             sh("git status --short -- " + " ".join(PRODUCERS + DECLS)).replace("\n", " | "),
             "workers: %s" % a.workers, "start: %s" % a.start, "end: %s" % a.end,
             "record written: %s" % time.strftime("%Y-%m-%d %H:%M:%S %z")]
    ph, dh = package_hashes()
    lines += ["package sha256:"] + ["  %s  %s" % (v, k) for k, v in sorted({**ph, **dh}.items())]
    for run in a.run or []:
        run = os.path.abspath(run)
        plan = load_plan(run)
        st = status_text(run, True)
        lines += ["run %s (%s): %s" % (run, plan["mode"], st), "  plan.json sha256 %s" % sha_file(
            os.path.join(run, "plan.json"))]
        led = load_ledger(run)
        for sid in sorted(led["shards"], key=int):
            e = led["shards"][sid]
            lines.append("  shard %s %s sha256 %s cpu %.1fs attempts %d" % (sid, e["status"], e["sha256"],
                                                                         e["cpu_seconds"], e["attempts"]))
    for pth in a.hash_file or []:
        if os.path.exists(pth):
            lines.append("output %s sha256 %s" % (pth, sha_file(pth)))
    atomic_write(a.out, ("\n".join(lines) + "\n").encode())
    print("wrote", a.out)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("plan")
    p.add_argument("run")
    p.add_argument("--mode", choices=["s2a", "s2b", "s2c"], required=True)
    p.add_argument("--tags", type=int, default=40)
    p.add_argument("--tag-cpu", type=float, default=120.0)
    p.add_argument("--max-steps", type=int, default=None, help="work cap per tag (tests); default none")
    p.add_argument("--orders", default="3,4,5")
    p.add_argument("--reduced", action="store_true")
    p.add_argument("--cert-dir", action="append")
    p.add_argument("--shard-cpu", type=float, default=3600.0)
    p.add_argument("--cpu-cap", type=float, default=None)
    p.add_argument("--timeout", type=float, default=3 * 3600)
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
    p.set_defaults(f=cmd_merge)
    p = sp.add_parser("record")
    p.add_argument("out")
    p.add_argument("--run", action="append")
    p.add_argument("--workers", default="?")
    p.add_argument("--start", default="?")
    p.add_argument("--end", default="?")
    p.add_argument("--hash-file", action="append")
    p.set_defaults(f=cmd_record)
    p = sp.add_parser("worker")
    p.add_argument("run")
    p.add_argument("shard", type=int)
    p.set_defaults(f=cmd_worker)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
