"""EXPLORATORY (not a declared WP). Long Table, 2026-10-05.

Exhaustive VH_C reading on plantri 5.8 output: 4-connected triangulations (plantri -c4m4 n -a)
whose vertices of degree < 5 all lie on one face. For every such face phi, look for a degree-5
vertex off phi with a legal fan whose every start has a pure Kempe fill (hole fixed). If none,
fall back to the phi-avoiding mixed search (slides may not land on phi).

Usage: plantri -c4m4 N -a | python3 vhphi_plantri.py N OUT.json [WORKERS]
Orders <= 18 only (19-24 are spent holdouts).
"""
from __future__ import annotations

import json
import sys
import time
from multiprocessing import Pool

import vhphi_explore as E


def parse(line):
    n_str, body = line.split()
    rows = body.split(",")
    rot = [[ord(ch) - 97 for ch in r] for r in rows]
    return rot


def faces_of(rot):
    n = len(rot)
    fs = set()
    for v in range(n):
        d = len(rot[v])
        for i in range(d):
            a, b = rot[v][i], rot[v][(i + 1) % d]
            fs.add(frozenset((v, a, b)))
    return fs


cache_pure = {}


def pure_good(rot, adj, v):
    fans, _ = E.pure_good_fans(rot, adj, v)
    return fans


def examine(args):
    idx, line = args
    rot = parse(line)
    n = len(rot)
    adj = [set(r) for r in rot]
    low = {v for v in range(n) if len(rot[v]) < 5}
    if len(low) > 3:
        return None
    phis = [f for f in faces_of(rot) if low <= f]
    if not phis:
        return None
    deg5 = [v for v in range(n) if len(rot[v]) == 5]
    good = {}
    remaining = list(phis)
    # visit degree-5 vertices, stop once every phi has a pure-good vertex off it
    for v in deg5:
        if not remaining:
            break
        if not any(v not in f for f in remaining):
            continue
        g = pure_good(rot, adj, v)
        good[v] = g
        if g:
            remaining = [f for f in remaining if v in f]
    rec = {"idx": idx, "n": n, "low": sorted(low), "nphi": len(phis),
           "tested": {str(k): v for k, v in good.items()}}
    if not remaining:
        rec["verdict"] = "pure-pass"
        return rec
    # mixed fallback for each remaining phi
    fails = []
    for f in remaining:
        ok_any = False
        inconclusive = False
        for v in deg5:
            if v in f:
                continue
            for fan_i, ok in E.mixed_good_fans(rot, adj, v, set(f)):
                if ok:
                    ok_any = True
                    break
                if ok is None:
                    inconclusive = True
            if ok_any:
                break
        if not ok_any:
            fails.append({"phi": sorted(f), "inconclusive": inconclusive})
    rec["remaining_after_pure"] = [sorted(f) for f in remaining]
    rec["verdict"] = "mixed-pass" if not fails else "FAIL"
    rec["fails"] = fails
    if fails:
        rec["line"] = line.strip()
    return rec


def main():
    n = int(sys.argv[1])
    assert n <= 18
    out = sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    lines = [l for l in sys.stdin if l.strip()]
    t0 = time.time()
    results = []
    with Pool(workers) as pool:
        for rec in pool.imap_unordered(examine, enumerate(lines), chunksize=64):
            if rec is not None:
                results.append(rec)
                if rec["verdict"] != "pure-pass":
                    print("NONPURE", json.dumps(rec)[:400], flush=True)
    results.sort(key=lambda r: r["idx"])
    summary = {}
    for r in results:
        key = (len(r["low"]), r["verdict"])
        summary[str(key)] = summary.get(str(key), 0) + 1
    json.dump({"order": n, "input_graphs": len(lines), "members": len(results),
               "summary": summary, "results": results}, open(out, "w"))
    print("order", n, "graphs", len(lines), "members", len(results), "summary", summary,
          f"{time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
