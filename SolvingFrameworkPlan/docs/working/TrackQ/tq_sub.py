#!/usr/bin/env python3
"""Track Q: which cycle states force the excess?  Ground set U fixed (admissible at all L states); connectivity
constraints imposed only for the states in a subset W.  LP (mcf) value and, if wanted, MILP value.
usage: tq_sub.py DATA.json [--milp]"""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tq_mcf import solve_mcf
d = json.load(open(sys.argv[1])); milp = '--milp' in sys.argv
U = [tuple(e) for e in d['U']]; parts = [(t, p, q, frozenset(P)) for t, p, q, P in d['parts']]; L = len(d['cols']); Np = d['Nprof']
def val(W):
    ps = [x for x in parts if x[0] in W]
    r = solve_mcf(d, U, ps, None, 600, not milp)
    return round(r.get('e', float('nan')), 4)
res = {}
for k in range(1, L + 1):
    for s in (range(L) if k < L else [0]):
        W = {(s + i) % L for i in range(k)}
        print(json.dumps(dict(src=d['src'], k=k, start=s, startN=Np[s], e=val(W))), flush=True)
    if k >= 3 and all(True for _ in [0]): pass
for name, W in (('rigid', {i for i in range(L) if Np[i] == '8'}), ('inshape', {i for i in range(L) if Np[i] == '9'})):
    print(json.dumps(dict(src=d['src'], set=name, e=val(W))), flush=True)
