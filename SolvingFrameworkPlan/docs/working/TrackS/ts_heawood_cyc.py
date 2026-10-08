#!/usr/bin/env python3
"""Track S: Heawood sums S_t = sum_f eps_t(f) along all-DL pi-cycles; reports sum_t S_t / L and the W(f) multiset.
usage: ts_heawood_cyc.py GRAPHFILE [--all | name:hole ...]"""
import sys, json
from collections import Counter
from ts_lib import load_graphs, HoleData, Geo
from ts_qcyc import cycles
from ts_wind import eps
a = sys.argv
if a[2] == '--all':
    G = load_graphs(a[1]); specs = [(nm, h) for nm, rot in G.items() for h in range(len(rot)) if len(rot[h]) == 5]
else:
    G = load_graphs(a[1], {s.rsplit(':', 1)[0] for s in a[2:]}); specs = [(s.rsplit(':', 1)[0], int(s.rsplit(':', 1)[1])) for s in a[2:]]
for nm, h in specs:
    hd = HoleData(G[nm], h)
    cs = cycles(hd)
    if not cs: continue
    geo = Geo(G[nm], h)
    for c in cs:
        E = [eps(hd, geo, q) for q in c]; S = [sum(e.values()) for e in E]
        W = Counter(sum(e[f] for e in E) for f in E[0])
        print(json.dumps(dict(g=nm, h=h, L=len(c), sumS=sum(S), perstep=sum(S) / len(c), W=sorted(W.items()),
                              N=[hd.info[q]['N'] for q in c], S=S)), flush=True)
