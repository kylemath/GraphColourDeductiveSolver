#!/usr/bin/env python3
"""[exploratory] Conjecture K3 sweep: every degree-5 hole class with rho >= 4 in the exhaustive radius census (out-N.jsonl
records that carry the graph), orders given; k3.cpp at each, testing all unfilled states at distance >= 4.
usage: k3scan.py ORDERS... [--workers K]"""
import json, os, subprocess, sys, tempfile
from collections import Counter
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__))
def faces(line):
    rot = [[ord(c) - 97 for c in x] for x in line.split()[1].split(",")]; seen, F = set(), []
    for v, nb in enumerate(rot):
        for i in range(len(nb)):
            f = (v, nb[(i + 1) % len(nb)], nb[i]); k = min((f, f[1:] + f[:1], f[2:] + f[:2]))
            if k not in seen: seen.add(k); F.append(f)
    return len(rot), F
def work(rec):
    n, F = faces(rec["graph"])
    with tempfile.NamedTemporaryFile("w", suffix=".tri", delete=False) as fh:
        fh.write("%d %d\n" % (n, len(F)) + "".join("%d %d %d\n" % f for f in F)); p = fh.name
    try:
        o = json.loads(subprocess.run([os.path.join(H, "k3"), p, str(rec["hole"]), "4"], capture_output=True, text=True).stdout)
    finally:
        os.unlink(p)
    return {"index": rec["index"], "hole": rec["hole"], "rho": rec["rho"], **o}
def main():
    w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 6
    orders = [int(x) for x in sys.argv[1:] if x.isdigit() and "--workers" not in x][: (sys.argv.index("--workers") - 1) if "--workers" in sys.argv else None]
    for n in orders:
        recs = [r for r in (json.loads(l) for l in open(os.path.join(H, "out-%d.jsonl" % n))) if "graph" in r]
        hist, maxk, ge4, first, tested = Counter(), 0, 0, None, 0
        with Pool(w) as pool, open(os.path.join(H, "k3-%d.jsonl" % n), "w") as fo:
            for r in pool.imap_unordered(work, recs, chunksize=8):
                fo.write(json.dumps(r) + "\n")
                if "error" in r: continue
                tested += r["tested_states"]; hist.update(r["leastk_hist"]); maxk = max(maxk, r["max_k"]); ge4 += r["k_ge4"]
                if r["k_ge4"] and first is None: first = {"order": n, "index": r["index"], "hole": r["hole"], **r["first_k_ge4"]}
        print(json.dumps({"order": n, "holes": len(recs), "tested_states_dist_ge4": tested, "leastk_hist": dict(hist), "max_k": maxk, "k_ge4": ge4, "first_counterexample": first}), flush=True)
if __name__ == "__main__":
    main()
