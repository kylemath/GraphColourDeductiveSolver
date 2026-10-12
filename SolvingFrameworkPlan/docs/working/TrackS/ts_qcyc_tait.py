#!/usr/bin/env python3
"""Track S: all-DL pi-cycles at every degree-5 hole, with Tait component counts (kH, kF13, kF12) computed in the dual
(valid on any closed surface).  Flags Tait-Q-cycles: k(F13) = 1 at every state (the good-matching cycles of README §2).
usage: ts_qcyc_tait.py GRAPHFILE stride off maxg"""
import sys, json
from ts_lib import HoleData
from tl_lib import TaitState
from ts_qcyc import cycles
a = sys.argv; s, off, mx = int(a[2]), int(a[3]), int(a[4]); ng = nh = 0; ncyc = nq = 0
for ln, l in enumerate(open(a[1])):
    if ln % s != off: continue
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
    ng += 1
    for h in range(len(rot)):
        if len(rot[h]) != 5: continue
        nh += 1
        try:
            hd = HoleData(rot, h)
        except Exception as ex:
            continue
        for c in cycles(hd):
            ks = []
            for q in c:
                St = TaitState(hd, q); T = St.T
                ks.append('%d%d%d' % (T.ncomp(St.H), T.ncomp(St.F13), T.ncomp(St.F12)))
            ncyc += 1; isq = all(k[1] == '1' for k in ks); nq += isq
            print(json.dumps(dict(g=p[0], h=h, L=len(c), TaitQ=isq, nQ=sum(k[1] == '1' for k in ks),
                                  N=[hd.info[q]['N'] for q in c], word=' '.join(ks))), flush=True)
    if ng >= mx: break
print(json.dumps(dict(graphs=ng, holes=nh, cycles=ncyc, taitQ=nq)), flush=True)
