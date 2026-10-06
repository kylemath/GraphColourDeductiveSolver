#!/usr/bin/env python3
"""MathNDiscSearch / run_shards.py [exploratory tooling]: sharded, resumable, crash-tolerant disc search.

Usage: run_shards.py N NPARTS [--workers W] [--outdir DIR] [--maxout M] [--tlimit SEC]

For each shard (part i of NPARTS) of disc_gen2, then test_N_fast on its output:
  - each stage writes to a temp file and is renamed atomically only on exit code 0;
  - shard status is kept in DIR/manifest.json (written atomically after every change);
  - a re-run skips finished shards and redoes interrupted ones from scratch;
  - a pool of W worker processes (default: all cores minus one); a crashed shard is retried up to 2 times;
  - `--report` prints the merged result and says PARTIAL if any shard is unfinished.
The shard split is disc_gen2's own (every NPARTS-th target at a fixed depth), so shards are disjoint and complete together.
"""
import argparse, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
import threading
LOCK = threading.Lock()

HERE = os.path.dirname(os.path.abspath(__file__))

def atomic_write(path, text):
    tmp = path + ".tmp%d" % os.getpid()
    with open(tmp, "w") as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)

def load(mpath):
    try:
        return json.load(open(mpath))
    except Exception:
        return {}

def run_stage(cmd, out_path, err_path):
    tmp_o, tmp_e = out_path + ".part", err_path + ".part"
    with open(tmp_o, "w") as fo, open(tmp_e, "w") as fe:
        rc = subprocess.call(cmd, stdout=fo, stderr=fe)
    if rc == 0:
        os.replace(tmp_o, out_path); os.replace(tmp_e, err_path)
    return rc

def shard(i, a, state, lock_path):
    name = "p%d" % i
    d = a.outdir
    gen_out, gen_err = f"{d}/gen_{a.N}_{name}.txt", f"{d}/gen_{a.N}_{name}.err"
    res_out, res_err = f"{d}/res_{a.N}_{name}.txt", f"{d}/res_{a.N}_{name}.err"
    for attempt in range(3):
        t0 = time.time()
        cmd = [os.path.join(HERE, "disc_gen2"), str(a.N), str(i), str(a.nparts), str(a.maxout), str(a.tlimit)]
        rc = run_stage(cmd, gen_out, gen_err)
        if rc != 0:
            state[name] = {"status": "gen_failed", "rc": rc, "attempt": attempt}; save(a, state); continue
        t1 = time.time()
        rc = run_stage([os.path.join(HERE, "test_N_fast"), gen_out], res_out, res_err)
        if rc != 0:
            state[name] = {"status": "test_failed", "rc": rc, "attempt": attempt}; save(a, state); continue
        state[name] = {"status": "done", "gen_seconds": round(t1 - t0, 1), "test_seconds": round(time.time() - t1, 1)}
        save(a, state); return
    # leave failure status in place

def save(a, state):
    with LOCK:
        atomic_write(f"{a.outdir}/manifest.json", json.dumps(state, indent=1, sort_keys=True))

def report(a, state):
    parts = [f"p{i}" for i in range(a.nparts)]
    done = [p for p in parts if state.get(p, {}).get("status") == "done"]
    import re
    tot = {"discs": 0, "rigid_ok": 0, "locked3": 0, "Nholds": 0, "CAND": 0, "trunc": 0}
    for p in done:
        for line in open(f"{a.outdir}/res_{a.N}_{p}.txt"):
            if "summary" in line:
                for k in tot:
                    m = re.search(k + r"=(\d+)", line)
                    if m: tot[k] += int(m.group(1))
    print(f"N={a.N}: {len(done)}/{a.nparts} shards done", "PARTIAL" if len(done) < a.nparts else "COMPLETE")
    print("totals over finished shards:", tot)
    for p in parts:
        if p not in done: print("  unfinished:", p, state.get(p, {}).get("status", "not started"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int); ap.add_argument("nparts", type=int)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--outdir", default=None); ap.add_argument("--maxout", type=int, default=1000000000)
    ap.add_argument("--tlimit", type=float, default=1e9); ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    a.outdir = a.outdir or os.path.join(HERE, f"shards_N{a.N}_of{a.nparts}")
    os.makedirs(a.outdir, exist_ok=True)
    state = load(f"{a.outdir}/manifest.json")
    if not a.report:
        todo = [i for i in range(a.nparts) if state.get(f"p{i}", {}).get("status") != "done"]
        print(f"{len(todo)} shards to run, {a.nparts - len(todo)} already done", flush=True)
        with ThreadPoolExecutor(a.workers) as ex:
            list(ex.map(lambda i: shard(i, a, state, None), todo))
    report(a, state)

if __name__ == "__main__":
    main()
