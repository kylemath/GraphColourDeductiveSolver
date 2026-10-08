#!/usr/bin/env python3
"""Track H: how often are unfilled states 'rigid' on closed triangulated surfaces?
Rigid = pair-graph component counts (am, AB, aA, mB, aB, mA) = (1, 1, 2, 1, 2, 1) (the minimum for a DL state obeying D;
both general-graph LPC counterexamples consist only of rigid states).  On the sphere (Euler identity) rigid <=> all six
pair graphs are forests <=> every bicoloured cycle of the dual Tait colouring passes through the hole.
Also counts 'near-rigid' states (sum of counts = 9, one above the minimum 8) and states of Kempe degree <= 2.
usage: th_rigidscan.py GRAPHFILE MAXGRAPHS STRIDE OUT.jsonl   (every degree-5 vertex of every STRIDE-th graph)"""
import sys, json
from th_engine import Hole

def counts(H, col, roles):
    al, mu, A, B = roles; cs = []
    for pr in [(al, mu), (A, B), (al, A), (mu, B), (al, B), (mu, A)]:
        left = {v for v in H.V if col[v] in pr}; k = 0
        while left:
            s = next(iter(left)); left -= H.comp(col, s, pr); k += 1
        cs.append(k)
    return cs

gf, maxg, stride, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
fo = open(out, 'a'); k = 0
for ln, l in enumerate(open(gf)):
    if ln % stride: continue
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
    k += 1
    if k > maxg: break
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        H = Hole(rot, h)
        tot = dict(unfilled=0, DL=0, rigid=0, rigidDL=0, near=0, nearDL=0)
        for i in range(len(H.states)):
            r, col = H.analyse_state(i)
            if r['kind'] == 'F': continue
            cs = counts(H, col, r['roles']); tot['unfilled'] += 1; dl = r['kind'] == 'DL'; tot['DL'] += dl
            if cs == [1, 1, 2, 1, 2, 1]: tot['rigid'] += 1; tot['rigidDL'] += dl
            if sum(cs) == 9 and cs[2] >= 2 and cs[4] >= 2: tot['near'] += 1; tot['nearDL'] += dl
        fo.write(json.dumps(dict(graph=p[0], hole=h, **tot)) + '\n'); fo.flush()
