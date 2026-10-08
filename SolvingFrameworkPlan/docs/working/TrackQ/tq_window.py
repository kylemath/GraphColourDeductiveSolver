#!/usr/bin/env python3
"""Track Q: exact minimum excess when only a subset W of the cycle states is constrained (ground set and parts
recomputed from W alone).  Windows = cyclic intervals of length k, and 'rigid only' / 'in-shape only'.
Reported e_W = min |E| - (3nv - 8) (exact, CP-SAT OPTIMAL).  usage: tq_window.py DATA.json [workers]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tq_exact import build
from tq_arb import cpsat
d0 = json.load(open(sys.argv[1])); W = int(sys.argv[2]) if len(sys.argv) > 2 else 2
n = d0['n']; E = {frozenset(e) for e in d0['E']}; cols = d0['cols']; L = len(cols); base = 3 * (n - 1) - 8
def solve(sub):
    cs = [cols[i] for i in sub]
    U, parts, forced = build(n, E, cs)
    d = dict(n=n, cols=cs, forced=forced)
    r = cpsat(d, U, parts, None, 1200, W, [1 if frozenset(e) in E else 0 for e in U])
    return r['status'], (r.get('obj', 0) - base), len(U)
Nprof = d0['Nprof']
res = {}
for k in list(range(1, L + 1)):
    starts = range(L) if k < L else [0]
    out = []
    for s in starts:
        sub = [(s + i) % L for i in range(k)]
        st, e, u = solve(sub); out.append((s, Nprof[s], e, st[:3]))
    print(json.dumps(dict(src=d0['src'], k=k, windows=out)), flush=True)
for name, sub in (('rigid', [i for i in range(L) if Nprof[i] == '8']), ('inshape', [i for i in range(L) if Nprof[i] == '9'])):
    st, e, u = solve(sub); print(json.dumps(dict(src=d0['src'], set=name, e=e, status=st)), flush=True)
