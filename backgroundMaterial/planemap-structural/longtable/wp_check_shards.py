#!/usr/bin/env python3
"""Resumable, sharded driver for the independent checker d1_check21.py.

usage: wp_check_shards.py OUTPUT.json PLANTRI_STDOUT DECLARATION.md --ledger-dir DIR
           [--range-size 200] [--workers 2] [--timeout 1800] [--retries 2]
           [--checker d1_check21.py] [--limit K]  [extra flags passed to the checker, e.g. --plantri P]

It runs the checker as subprocesses, one per fixed-size index range (plus one whole-file
"global" run, `--range 0 0`, which does the structural checks once), at most --workers at a
time.  No multiprocessing.Pool.  Each job result is written atomically (temp file, fsync,
rename) into DIR as range-LO-HI.json / global.json with its own SHA-256, and DIR/ledger.json
indexes them.  A re-run skips jobs whose result file is intact, status ok, and whose recorded
checker/output/input/declaration hashes still equal the current files.

Verdict (the last line):
  CHECK OK (all N ranges)                 exit 0   every range ok and the global checks ok
  CHECK FAILED: ranges ...                exit 1   some range (or the global check) mismatched
  PARTIAL: k of N ranges checked          exit 2   anything else; never a pass
Standard library only; reads no producer code.
"""
import sys, os, json, hashlib, argparse, subprocess, signal, time, tempfile

STOP = [False]
HERE = os.path.dirname(os.path.abspath(__file__))


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def canon_json(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":")).encode()


def self_hash(entry):
    d = {k: v for k, v in entry.items() if k != "result_sha256"}
    return hashlib.sha256(canon_json(d)).hexdigest()


def fsync_dir(d):
    try:
        fd = os.open(d, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        pass


def atomic_write(path, data):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=d)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        fsync_dir(d)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def count_graphs(path):
    with open(path) as f:
        return sum(1 for l in f if l.strip())


class Job:
    def __init__(self, kind, lo, hi, ledger_dir):
        self.kind, self.lo, self.hi = kind, lo, hi
        self.name = "global" if kind == "global" else "range-%07d-%07d" % (lo, hi)
        self.res_path = os.path.join(ledger_dir, self.name + ".json")
        self.log_path = os.path.join(ledger_dir, self.name + ".log")
        self.entry = None        # final entry (ok/mismatch/...) or None = pending
        self.attempts = 0
        self.proc = None
        self.t0 = 0.0
        self.logf = None
        self.tmp_log = None
        self.timed_out = False

    def label(self):
        return "global" if self.kind == "global" else "range %d..%d" % (self.lo, self.hi)


def load_valid(job, ctx):
    """a previously recorded result that may be trusted: intact, ok, hashes current"""
    try:
        with open(job.res_path, "rb") as f:
            e = json.loads(f.read())
        if e.get("result_sha256") != self_hash(e):
            return None
        if e.get("status") != "ok" or e.get("kind") != job.kind or e.get("range") != [job.lo, job.hi]:
            return None
        for k in ("checker_sha256", "output_sha256", "input_sha256", "decl_sha256"):
            if e.get(k) != ctx[k]:
                return None
        if e.get("extra_args") != ctx["extra_args"] or e.get("range_size") != ctx["range_size"]:
            return None
        if sha_file(job.log_path) != e.get("log_sha256"):
            return None
        return e
    except (OSError, ValueError, AttributeError, TypeError):
        return None


def write_ledger(jobs, ctx, ledger_path):
    led = dict(header(ctx))
    led["jobs"] = []
    for j in jobs:
        if j.entry is None:
            led["jobs"].append({"kind": j.kind, "range": [j.lo, j.hi], "status": "pending",
                                "attempts": j.attempts})
        else:
            led["jobs"].append(j.entry)
    led["ledger_sha256"] = hashlib.sha256(canon_json({k: v for k, v in led.items()
                                                      if k != "ledger_sha256"})).hexdigest()
    atomic_write(ledger_path, json.dumps(led, indent=1, sort_keys=True).encode())


def header(ctx):
    return {"ledger_version": 1, "checker_sha256": ctx["checker_sha256"],
            "output_sha256": ctx["output_sha256"], "input_sha256": ctx["input_sha256"],
            "decl_sha256": ctx["decl_sha256"], "graphs": ctx["graphs"],
            "range_size": ctx["range_size"], "extra_args": ctx["extra_args"]}


def start(job, ctx, args):
    job.attempts += 1
    job.timed_out = False
    job.tmp_log = job.log_path + ".run%d" % os.getpid()
    job.logf = open(job.tmp_log, "wb")
    cmd = [sys.executable, ctx["checker"], args.output, args.input, args.decl,
           "--range", str(job.lo), str(job.hi), "--workers", "1", "--die-with-parent", str(os.getpid())]
    if job.kind == "range":
        cmd.append("--no-global")
    cmd += ctx["extra_args"]
    job.t0 = time.monotonic()
    job.proc = subprocess.Popen(cmd, stdout=job.logf, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, start_new_session=True)


def kill_proc(job):
    p = job.proc
    if p is None or p.poll() is not None:
        return
    try:
        p.terminate()
        try:
            p.wait(5)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
    except OSError:
        pass


def close_log(job):
    if job.logf:
        try:
            job.logf.flush()
            os.fsync(job.logf.fileno())
        except OSError:
            pass
        job.logf.close()
        job.logf = None


def parse_unresolved(logpath):
    try:
        with open(logpath, errors="replace") as f:
            for line in f:
                if "unresolved (producer interrupted/non-complete):" in line:
                    return int(line.rsplit(":", 1)[1])
    except (OSError, ValueError):
        pass
    return None


def finish(job, ctx, status, code):
    close_log(job)
    os.replace(job.tmp_log, job.log_path)
    fsync_dir(os.path.dirname(os.path.abspath(job.log_path)))
    e = {"kind": job.kind, "range": [job.lo, job.hi], "status": status, "attempts": job.attempts,
         "exit_code": code, "log_sha256": sha_file(job.log_path),
         "checker_sha256": ctx["checker_sha256"], "output_sha256": ctx["output_sha256"],
         "input_sha256": ctx["input_sha256"], "decl_sha256": ctx["decl_sha256"],
         "extra_args": ctx["extra_args"], "range_size": ctx["range_size"],
         "wall_seconds": round(time.monotonic() - job.t0, 2),
         "unresolved": parse_unresolved(job.log_path),
         "log_file": os.path.basename(job.log_path)}
    e["result_sha256"] = self_hash(e)
    atomic_write(job.res_path, json.dumps(e, indent=1, sort_keys=True).encode())
    job.entry = e


def on_signal(signum, frame):
    STOP[0] = True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("output")
    ap.add_argument("input")
    ap.add_argument("decl")
    ap.add_argument("--ledger-dir", required=True)
    ap.add_argument("--range-size", type=int, default=200)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--timeout", type=float, default=1800.0, help="wall seconds per attempt")
    ap.add_argument("--retries", type=int, default=2, help="extra attempts after a crash, kill or timeout")
    ap.add_argument("--checker", default=os.path.join(HERE, "d1_check21.py"))
    ap.add_argument("--limit", type=int, default=None,
                    help="stop after starting this many new jobs (testing a partial run)")
    args, extra = ap.parse_known_args()
    if args.range_size < 1 or args.workers < 1 or args.retries < 0:
        ap.error("bad numeric option")
    os.makedirs(args.ledger_dir, exist_ok=True)
    for f in os.listdir(args.ledger_dir):     # debris of a killed earlier driver (one driver per ledger dir)
        if ".log.run" in f or f.startswith(".tmp-"):
            try:
                os.unlink(os.path.join(args.ledger_dir, f))
            except OSError:
                pass
    n = count_graphs(args.input)
    ctx = {"checker": os.path.abspath(args.checker), "checker_sha256": sha_file(args.checker),
           "output_sha256": sha_file(args.output), "input_sha256": sha_file(args.input),
           "decl_sha256": sha_file(args.decl), "graphs": n, "range_size": args.range_size,
           "extra_args": extra}
    jobs = [Job("global", 0, 0, args.ledger_dir)]
    for lo in range(0, n, args.range_size):
        jobs.append(Job("range", lo, min(n, lo + args.range_size), args.ledger_dir))
    nranges = len(jobs) - 1
    ledger_path = os.path.join(args.ledger_dir, "ledger.json")
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)

    skipped = 0
    queue = []
    for j in jobs:
        e = load_valid(j, ctx)
        if e is not None:
            j.entry, j.attempts = e, e.get("attempts", 0)
            skipped += 1
        else:
            queue.append(j)
    print("%d graphs, %d ranges of <= %d, ledger %s; %d jobs already ok and skipped, %d to run"
          % (n, nranges, args.range_size, args.ledger_dir, skipped, len(queue)), flush=True)
    write_ledger(jobs, ctx, ledger_path)

    running, started = [], 0
    retry_count = {}
    while (queue or running) and not STOP[0]:
        while queue and len(running) < args.workers and not STOP[0] and \
                (args.limit is None or started < args.limit):
            j = queue.pop(0)
            start(j, ctx, args)
            started += 1
            running.append(j)
        if not running:
            break      # --limit reached
        time.sleep(0.1)
        for j in list(running):
            code = j.proc.poll()
            if code is None and time.monotonic() - j.t0 > args.timeout:
                j.timed_out = True
                kill_proc(j)
                code = j.proc.poll()
            if code is None:
                continue
            running.remove(j)
            close_log(j)
            if j.timed_out:
                status = "timeout"
            elif code == 0:
                status = "ok"
            elif code == 1:
                status = "mismatch"
            else:
                status = "failed"     # crash, kill, incomplete range (exit 2), bad arguments
            retryable = status == "timeout" or (status == "failed" and code != 2)
            if retryable and j.attempts <= args.retries and not STOP[0]:
                print("  %s: attempt %d %s (exit %s), retrying" % (j.label(), j.attempts, status, code),
                      flush=True)
                queue.append(j)
                continue
            if STOP[0] and (j.timed_out is False and code is not None and code < 0):
                # killed by our own shutdown: leave pending, record nothing
                continue
            finish(j, ctx, status, code)
            write_ledger(jobs, ctx, ledger_path)
            print("  %s: %s (attempts %d, %.1fs)" % (j.label(), status, j.attempts, j.entry["wall_seconds"]),
                  flush=True)
    if STOP[0] or running:
        for j in running:
            kill_proc(j)
            close_log(j)
            try:
                os.unlink(j.tmp_log)
            except OSError:
                pass
        print("interrupted: children terminated, ledger left valid", flush=True)
    for j in jobs:       # remove stray temp logs of jobs that never finished
        if j.entry is None and j.tmp_log and os.path.exists(j.tmp_log):
            try:
                os.unlink(j.tmp_log)
            except OSError:
                pass
    write_ledger(jobs, ctx, ledger_path)

    gj = jobs[0]
    rj = jobs[1:]
    bad = [j for j in jobs if j.entry and j.entry["status"] == "mismatch"]
    okr = [j for j in rj if j.entry and j.entry["status"] == "ok"]
    unres = sum((j.entry.get("unresolved") or 0) for j in jobs if j.entry and j.entry["status"] == "ok")
    if bad:
        print("CHECK FAILED: " + ", ".join(j.label() for j in bad))
        return 1
    if len(okr) == nranges and gj.entry and gj.entry["status"] == "ok":
        if unres:
            print("NOTE: %d unresolved (producer interrupted) vertices/graphs, inconclusive, as in the "
                  "unsharded checker" % unres)
        print("CHECK OK (all %d ranges)" % nranges)
        return 0
    notok = [j.label() + " " + (j.entry["status"] if j.entry else "pending")
             for j in jobs if not (j.entry and j.entry["status"] == "ok")]
    print("not ok: " + "; ".join(notok[:20]) + (" ..." if len(notok) > 20 else ""))
    print("PARTIAL: %d of %d ranges checked" % (len(okr), nranges)
          + ("" if gj.entry and gj.entry["status"] == "ok" else " (global checks not ok)"))
    return 2


if __name__ == "__main__":
    sys.exit(main())
