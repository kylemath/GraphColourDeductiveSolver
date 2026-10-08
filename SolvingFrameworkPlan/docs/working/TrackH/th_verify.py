#!/usr/bin/env python3
"""Track H: independent verification of an LPC counterexample candidate (pure Python, th_engine):
the class of the all-DL pi-cycle is listed; per state: kind, D1, D2, and Theorem P quantities (odd-G-degree counts of
K_aA, K_aB, K_am at x_{j+2}) with the expected parities (P1: oA odd iff not inA; P2: oB odd iff not inB; P3: oM odd).
usage: th_verify.py FILE NAME HOLE"""
import sys
from collections import Counter
from th_engine import read_graphs, Hole
g = read_graphs(sys.argv[1])[sys.argv[2]]; h = int(sys.argv[3]); H = Hole(g, h).build()
print('n', len(g), 'edges', sum(len(a) for a in g) // 2, 'states', len(H.states), 'class sizes', sorted(Counter(H.cls).values()))
for cyc in H.allDL_cycles():
    mem = H.class_members(cyc[0])
    print('cycle length', len(cyc), 'class size', len(mem), 'class == cycle states', set(mem) == set(cyc))
    ok = dict(D=0, P1=0, P2=0, P3=0, LP=0)
    for i in mem:
        r = H.info[i]
        if r['kind'] == 'F': print('  filled state', i); continue
        ok['D'] += r['D1'] and r['D2']
        ok['P1'] += (r['oA'] % 2 == 1) == (not r['inA']); ok['P2'] += (r['oB'] % 2 == 1) == (not r['inB']); ok['P3'] += r['oM'] % 2 == 1
        ok['LP'] += (r['oA'] % 2 == r['L2']) and (r['oB'] % 2 == r['L1'])
    print('  states satisfying', ok, 'of', len(mem), '; kinds', Counter(H.info[i]['kind'] for i in mem))
