#!/usr/bin/env python3
"""Track Q: truly local excess -- for a window W of consecutive cycle states, recompute the ground set and the parts
from the states in W only (any graph carrying just these |W| states with these partitions), then the mcf LP bound
(and MILP if --milp).  Shows whether the excess needs the closure of the cycle.
usage: tq_local.py DATA.json K1,K2,... [--milp]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tq_exact import build
from tq_mcf import solve_mcf
d0 = json.load(open(sys.argv[1])); ks = [int(x) for x in sys.argv[2].split(',')]; milp = '--milp' in sys.argv
n = d0['n']; E = {frozenset(e) for e in d0['E']}; cols = d0['cols']; L = len(cols)
for k in ks:
    for s in (range(L) if k < L else [0]):
        W = [(s + i) % L for i in range(k)]
        cs = [cols[i] for i in W]; U, parts, forced = build(n, E, cs)
        r = solve_mcf(dict(n=n, cols=cs, forced=forced), U, parts, None, 900, not milp)
        print(json.dumps(dict(src=d0['src'], k=k, start=s, startN=d0['Nprof'][s], U=len(U), e=round(r.get('e', float('nan')), 4), secs=r['secs'])), flush=True)
