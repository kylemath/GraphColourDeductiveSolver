#!/usr/bin/env python3
"""[UNTESTED] Path 3 runner (Studio only). For every instance NAME.json written by path3_build.py and every
degree-5 orbit representative v (or every degree-5 vertex with --holes all) it runs the existing engines:

  KMAP_REPS=1 kmap NAME.edges v V CAP  -> kappa(T), kappa(T-v), new classes, and per class of T-v: size,
                                          hit_by_T (= the class contains a restriction of a colouring of T
                                          = the class contains a filled state; these are the same thing)
  kreach NAME.edges V                  -> targetless classes, depth to a filled state (cross-check of kmap)
  kempe  NAME.tri V                    -> rho, unreached DL states (Studio intel fast/kempe.cpp)

and adds rep-level diagnostics on each class representative of T-v (NOT invariants; see path3_kclasses.py
for whole-class checks): number of colours on the link of v; |winding| of the link ring of every vertex of
degree >= 7 (the ring avoids that vertex's colour, so it is a closed walk on a triangle); the parity vector
O_i = #(T-odd vertices of colour i) mod 2.

Sources of the engines (compile once):
  kmap   backgroundMaterial/planemap-structural/longtable/studio-explore/kempe-census/kmap.cpp
  kreach backgroundMaterial/planemap-structural/longtable/studio-explore/sage-qa-runs/kreach.cpp
  kempe  backgroundMaterial/planemap-structural/studiointel/fast/kempe.cpp
All three need n <= 64 (kmap enumerates T itself) and enumerate every colouring: CAP bounds the states.

Usage: python3 run_path3.py OUTDIR --bin ~/studio-scratch/census [--cap 50000000] [--holes reps|all]
                            [--workers 8] [--timeout 7200] [--only SUBSTRING] > OUTDIR/results.jsonl
A KILL line is printed to stderr whenever new_classes > 0 or targetless > 0 or rho is null; such a record is a
CANDIDATE only until path3_kclasses.py (independent code) reproduces it.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor


def runj(cmd, env=None, timeout=None):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        return [{"error": "timeout"}]
    out = []
    for line in p.stdout.splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                out.append({"raw": line})
    return out or [{"error": "no output", "stderr": p.stderr[-300:]}]


def winding(col, ring):
    """ring: cyclic list of vertices avoiding one colour; walk on the triangle of the other three colours."""
    cs = sorted({col[x] for x in ring})
    if len(cs) > 3 or any(x not in col for x in ring):
        return None
    if len(cs) < 3:
        return 0
    pos = {c: i for i, c in enumerate(cs)}
    tot = 0
    for k in range(len(ring)):
        d = (pos[col[ring[(k + 1) % len(ring)]]] - pos[col[ring[k]]]) % 3
        tot += 1 if d == 1 else -1
    return abs(tot) // 3


def diagnostics(info, v, rep):
    col = {int(k): c for k, c in rep["colouring"].items()}
    rot, n = info["rotation"], info["n"]
    deg = [len(r) for r in rot]
    link = rot[v]
    big = {}
    for x in range(n):
        if x != v and deg[x] >= 7 and v not in rot[x]:
            big[x] = winding(col, rot[x])
    odd = [sum(1 for x in col if col[x] == i and deg[x] % 2) % 2 for i in range(4)]
    return {"link_colours": len({col[x] for x in link}), "pole_winding": big, "odd_parity": odd}


def one(job):
    info, v, a = job
    base = os.path.join(a.outdir, info["name"])
    env = dict(os.environ, KMAP_REPS="1")
    km = runj([os.path.join(a.bin, "kmap"), base + ".edges", "v", str(v), str(a.cap)], env, a.timeout)
    kr = runj([os.path.join(a.bin, "kreach"), base + ".edges", str(v)], None, a.timeout)[0]
    ke = runj([os.path.join(a.bin, "kempe"), base + ".tri", str(v)], None, a.timeout)[0]
    rec = {"name": info["name"], "family": info["family"], "n": info["n"], "v": v,
           "link_degrees": [len(info["rotation"][y]) for y in info["rotation"][v]],
           "four_connected": info["four_connected"], "min_degree": info["min_degree"],
           "diamond_proxy": info["diamond_proxy"], "c2122_proxy_at_v": v in info["c2122_proxy_holes"],
           "kmap": km[0], "kreach": kr, "kempe": {k: ke.get(k) for k in ("rho", "unreached_DL", "error", "N")}}
    if len(km) > 1 and "reps" in km[1]:
        rec["classes_T_minus_v"] = [{"size": r["class_size"], "hit_by_T": r["hit_by_T"],
                                     "T_classes_mapping_here": r["T_classes_mapping_here"],
                                     **diagnostics(info, v, r)} for r in km[1]["reps"]]
    kill = (km[0].get("new_classes", 0) or 0) > 0 or (kr.get("targetless_classes", 0) or 0) > 0 \
        or ("rho" in ke and ke["rho"] is None and "error" not in ke)
    rec["CANDIDATE_KILL"] = bool(kill)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--bin", default=os.path.expanduser("~/studio-scratch/census"))
    ap.add_argument("--cap", type=int, default=50000000)
    ap.add_argument("--holes", choices=["reps", "all"], default="reps")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=7200)
    ap.add_argument("--only", default="")
    ap.add_argument("--max-n", type=int, default=64)
    a = ap.parse_args()
    jobs = []
    for p in sorted(glob.glob(os.path.join(a.outdir, "*.json"))):
        info = json.load(open(p))
        if "rotation" not in info or a.only not in info["name"] or info["n"] > a.max_n:
            continue
        if info["min_degree"] < 5:
            print(json.dumps({"name": info["name"], "skipped": "min degree %d" % info["min_degree"]}), flush=True)
            continue
        deg = [len(r) for r in info["rotation"]]
        holes = [r["v"] for r in info["deg5_orbit_reps"]] if a.holes == "reps" else [x for x in range(info["n"]) if deg[x] == 5]
        jobs += [(info, v, a) for v in holes]
    jobs.sort(key=lambda j: j[0]["n"])                       # small first: early failures surface early
    with ThreadPoolExecutor(a.workers) as ex:
        for rec in ex.map(one, jobs):
            print(json.dumps(rec), flush=True)
            if rec["CANDIDATE_KILL"]:
                print("KILL-CANDIDATE %s v=%d" % (rec["name"], rec["v"]), file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
