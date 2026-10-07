#!/usr/bin/env python3
"""[exploratory] Euler-slack features of ALL states of T - hole for the order-22 F-cycle graph
(studiointel/fcycle/fcycle_order22.json, hole 15). Writes a CSV in the same columns as scan.py (order 22, gi 0, floor 0).
usage: fcycle22.py out.csv.gz"""
import os, sys, json, gzip
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common")); sys.path.insert(0, H)
from kempe_py import Space
from euler_features import features, FEATURES
from scan import COLS
from hard import build
d = json.load(open(os.path.join(H, "..", "..", "..", "studiointel", "fcycle", "fcycle_order22.json")))
adj, link = build(d["faces"], d["hole"])
sp = Space({v: set(w) for v, w in adj.items()}, d["hole"], link=link)
sp.build_graph(); sp.classes(); sp.dist_to_filled()
N = sp.N; A = [[j for j in range(N) if sp.nbm[i] >> j & 1] for i in range(N)]
size = [0] * sp.ncl; fil = [0] * sp.ncl
for k in range(len(sp.states)): size[sp.cl[k]] += 1; fil[sp.cl[k]] += sp.filled(k)
with gzip.open(sys.argv[1], "wt") as fh:
    fh.write(",".join(COLS) + "\n")
    for k, s in enumerate(sp.states):
        c = sp.cl[k]; f, fr = features(A, list(s), sp.linki)
        r = [22, 0, d["hole"], 0, int(sp.filled(k)), sp.dist[k], size[c], fil[c]] + [f[x] for x in FEATURES]
        fh.write(",".join(repr(x) if isinstance(x, float) else str(x) for x in r) + "\n")
print("states", len(sp.states), "classes", sp.ncl, file=sys.stderr)
