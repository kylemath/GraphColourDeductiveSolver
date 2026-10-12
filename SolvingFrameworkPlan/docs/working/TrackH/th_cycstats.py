#!/usr/bin/env python3
"""Track H: per all-DL pi-cycle statistics of sigma along the cycle, over a list of (graph line, hole) items.
Per cycle: string of sigma-triviality (T = K_{am}(x_{j+2}) contains every a/m vertex, i.e. sigma is a renaming),
sigma-exit string (s = sigma(c) not DL), (#am comps, #AB comps) per state, and the class [N, F, viol(D)].
usage: th_cycstats.py ITEMS.txt OUT.jsonl   (ITEMS: 'name n rot hole' lines)"""
import sys, json
from th_engine import Hole

def comps(H, col, pair):
    left = {v for v in H.V if col[v] in pair}; k = 0
    while left:
        s = next(iter(left)); left -= H.comp(col, s, pair); k += 1
    return k

out = open(sys.argv[2], 'a')
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) < 4: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; h = int(p[3])
    try:
        H = Hole(rot, h).build()
    except AssertionError:
        continue
    for cyc in H.allDL_cycles():
        mem = H.class_members(cyc[0]); info = H.info
        tri, sig, nc = '', '', []
        for i in cyc:
            r = info[i]; col = H.col(i); al, mu, A, B = r['roles']
            na, nb = comps(H, col, (al, mu)), comps(H, col, (A, B)); nc.append((na, nb))
            tri += 'T' if na == 1 else '.'
            sig += 's' if info[r['sigma']]['kind'] != 'DL' else '.'
        F = sum(1 for i in mem if info[i]['kind'] == 'F')
        viol = sum(1 for i in mem if info[i]['kind'] != 'F' and not (info[i]['D1'] and info[i]['D2']))
        out.write(json.dumps(dict(graph=p[0], hole=h, L=len(cyc), N=len(mem), F=F, viol=viol, triv=tri, sig=sig, nc=nc)) + '\n'); out.flush()
