#!/usr/bin/env python3
"""MathRadiusCensus / run_census.py [exploratory tooling]: sharded, atomic, resumable radius census.

Usage: run_census.py N [--gen-parts K] [--block B] [--workers W] [--outdir DIR] [--report]
  Stage 1 (generator): K shards of `gen_tri N --all --part i K`  -> DIR/gen_N_p<i>.txt   (atomic rename on exit code 0)
  Stage 2 (merge):     dedup the shards by canonical hex          -> DIR/graphs_N.txt     (sorted by hex; atomic)
  Stage 3 (census):    blocks of B graphs: `census graphs_N.txt --range a b` -> DIR/cen_N_b<j>.jsonl (atomic)
  DIR/manifest.json is rewritten atomically after every change; a re-run skips finished stages/shards and redoes interrupted ones.
  --report prints the merged result (PARTIAL if anything is unfinished); exit code 3 if a KILL flag is present.
KILL flag: any state of any hole whose Kempe class contains no filled state (unreached > 0): a targetless class.
Known counts of min-degree-5 triangulations (all, incl. separating triangles) used as a validity check of the generator."""
import argparse, json, os, subprocess, sys, time, threading
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); LOCK = threading.Lock()
# 12..20 from the task statement except 20 (see PREREG: 73 is the literature value, the task text said 71); 21,22 recalled from Brinkmann-McKay
KNOWN = {12:1, 13:0, 14:1, 15:1, 16:3, 17:4, 18:12, 19:23, 20:73, 21:192, 22:651}

def atomic_write(path, text):
    tmp = path + ".tmp%d" % os.getpid()
    with open(tmp, "w") as f: f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)
def load(p):
    try: return json.load(open(p))
    except Exception: return {}
def save(st, a):
    with LOCK: atomic_write(a.outdir + "/manifest.json", json.dumps(st, indent=1, sort_keys=True))
def run_stage(cmd, out):
    tmp = out + ".part"
    with open(tmp, "w") as fo: rc = subprocess.call(cmd, stdout=fo, stderr=subprocess.DEVNULL)
    if rc == 0: os.replace(tmp, out)
    return rc
def with_retry(name, cmd, out, st, a):
    for attempt in range(3):
        t0 = time.time(); rc = run_stage(cmd, out)
        if rc == 0:
            st[name] = {"status": "done", "seconds": round(time.time() - t0, 1)}; save(st, a); return
        st[name] = {"status": "failed", "rc": rc, "attempt": attempt}; save(st, a)

def merge(a, st):
    seen = {}
    for i in range(a.gen_parts):
        for line in open(f"{a.outdir}/gen_{a.N}_p{i}.txt"):
            if line.startswith("G"): seen.setdefault(line.split()[2], line)
    atomic_write(f"{a.outdir}/graphs_{a.N}.txt", "".join(seen[h] for h in sorted(seen)))
    st["merge"] = {"status": "done", "graphs": len(seen)}; save(st, a)

def report(a, st):
    gpath = f"{a.outdir}/graphs_{a.N}.txt"
    ng = st.get("merge", {}).get("graphs")
    partial = False
    if ng is None: print(f"N={a.N}: generator/merge unfinished: PARTIAL"); return 1
    print(f"N={a.N}: {ng} graphs generated (known count {KNOWN.get(a.N,'?')}) -> {'MATCH' if KNOWN.get(a.N)==ng else 'CHECK'}")
    nblk = (ng + a.block - 1) // a.block; kill = 0; capped = 0
    tot = dict(holes=0, states=0, dl=0); hist = {}; histc4 = {}; maxdl = -1; maxdl4 = -1; wit = None; seen_g = set()
    for j in range(nblk):
        if st.get(f"b{j}", {}).get("status") != "done": partial = True; print("  unfinished block", j); continue
        for line in open(f"{a.outdir}/cen_{a.N}_b{j}.jsonl"):
            r = json.loads(line); seen_g.add(r["g"])
            if r.get("capped"): capped += 1; continue
            tot["holes"] += 1; tot["states"] += r["ncol"]; tot["dl"] += r["ndl"]
            if r["unreached"]: kill += 1; print("  KILL FLAG (targetless class): graph", r["g"], "hole", r["v"], "unreached", r["unreached"], "unreached_dl", r["unreached_dl"])
            for rad, c in enumerate(r["hist_dl"]):
                hist[rad] = hist.get(rad, 0) + c
                if not r["sep"]: histc4[rad] = histc4.get(rad, 0) + c
            if r["maxdl"] > maxdl: maxdl = r["maxdl"]; wit = (r["g"], r["v"], r.get("wit"))
            if not r["sep"] and r["maxdl"] > maxdl4: maxdl4 = r["maxdl"]
    print(f"  {'PARTIAL' if partial else ('COMPLETE-WITH-CAPS' if capped else 'COMPLETE')}: holes={tot['holes']} canonical colourings={tot['states']} DL states={tot['dl']}")
    print("  DL radius histogram (all min-degree-5):", {k: hist[k] for k in sorted(hist) if hist[k]})
    print("  DL radius histogram (4-connected only):", {k: histc4[k] for k in sorted(histc4) if histc4[k]})
    print("  max DL radius: all", maxdl, " 4-connected", maxdl4, " witness (graph,hole,colouring):", wit)
    print("  capped holes (inconclusive):", capped); print("  KILL flags:", kill)
    return 3 if kill else 0

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("N", type=int); ap.add_argument("--gen-parts", type=int, default=1)
    ap.add_argument("--block", type=int, default=50); ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--outdir"); ap.add_argument("--report", action="store_true"); a = ap.parse_args()
    a.outdir = a.outdir or os.path.join(HERE, f"run_N{a.N}"); os.makedirs(a.outdir, exist_ok=True)
    st = load(a.outdir + "/manifest.json")
    if a.report: sys.exit(report(a, st))
    todo = [i for i in range(a.gen_parts) if st.get(f"g{i}", {}).get("status") != "done"]
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda i: with_retry(f"g{i}", [os.path.join(HERE, "gen_tri"), str(a.N), "--all", "--part", str(i), str(a.gen_parts)],
                                          f"{a.outdir}/gen_{a.N}_p{i}.txt", st, a), todo))
    if any(st.get(f"g{i}", {}).get("status") != "done" for i in range(a.gen_parts)): print("generator shards unfinished"); sys.exit(1)
    if st.get("merge", {}).get("status") != "done" or not os.path.exists(f"{a.outdir}/graphs_{a.N}.txt"): merge(a, st)
    ng = st["merge"]["graphs"]; nblk = (ng + a.block - 1) // a.block
    todo = [j for j in range(nblk) if st.get(f"b{j}", {}).get("status") != "done"]
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda j: with_retry(f"b{j}", [os.path.join(HERE, "census"), f"{a.outdir}/graphs_{a.N}.txt", "--range", str(j * a.block), str((j + 1) * a.block)],
                                          f"{a.outdir}/cen_{a.N}_b{j}.jsonl", st, a), todo))
    sys.exit(report(a, st))
if __name__ == "__main__": main()
