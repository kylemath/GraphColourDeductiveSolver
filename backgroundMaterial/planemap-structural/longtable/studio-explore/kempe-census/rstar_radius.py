#!/usr/bin/env python3
"""[exploratory] Path 8: R*-radius per order = max over graphs of (min over degree-5 holes of rho), from the radius
census out-N.jsonl (one record per degree-5 hole orbit). Also the same restricted to fullerene duals (all degrees 5
or 6), and the local pattern (sorted link degrees) of the best vertex in the graphs attaining the order's maximum.
Graphs are regenerated from plantri by index. usage: plantri -m5 -c4 N -a | rstar_radius.py N"""
import json, os, sys
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1])
lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
best = {}
for l in open(os.path.join(H, "out-%d.jsonl" % n)):
    r = json.loads(l)
    i, rho = r["index"], r["rho"]
    key = 99 if rho is None else rho
    if i not in best or key < best[i][0]:
        best[i] = (key, r["hole"])


def rot(line):
    return [[ord(c) - 97 for c in x] for x in line.split()[1].split(",")]


def summary(idx):
    if not idx:
        return {"graphs": 0}
    hist = Counter(best[i][0] for i in idx)
    mx = max(hist)
    pats = Counter()
    for i in idx:
        if best[i][0] == mx:
            R = rot(lines[i])
            pats[str(sorted(len(R[w]) for w in R[best[i][1]]))] += 1
    return {"graphs": len(idx), "min_rho_hist": {str(k): v for k, v in sorted(hist.items())}, "rstar_radius": mx,
            "best_vertex_link_degrees_at_max": dict(pats.most_common(10))}


allidx = sorted(best)
full = [i for i in allidx if all(len(x) in (5, 6) for x in rot(lines[i]))]
print(json.dumps({"order": n, "all": summary(allidx), "fullerene_duals": summary(full)}))
