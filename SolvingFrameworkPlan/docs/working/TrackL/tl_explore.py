#!/usr/bin/env python3
"""Track L exploration [data]: at DL N = 9 states with the extra chain in P1, tally the extra-chain type (am = sigma-type,
AB) against (pi c rigid, pi^-1 c rigid); at in-shape states, which of X, Y, Xt, Yt the free {2,3}-cycle C' meets.
usage: tl_explore.py GRAPHFILE STRIDE OFFSET MAXGRAPHS"""
import sys
from collections import Counter
from tl_lib import HoleData, TaitState, read_graphs

gf, stride, off, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
T = Counter()
for name, rot in read_graphs(gf, stride, off, maxg):
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        hd = HoleData(rot, h); T['holes'] += 1
        for i in range(hd.S):
            r = hd.info[i]
            if r['kind'] != 'DL' or r['N'] != 9: continue
            ex = hd.extra(i)
            if ex not in ([0], [1]): T['nine_extra_P23'] += 1; continue
            typ = 'am' if ex == [0] else 'AB'
            pr = r['pi'] is not None and hd.rigid(r['pi'])
            qr = r['pinv'] is not None and hd.rigid(r['pinv'])
            T[(typ, 'pi_rigid' if pr else '-', 'pinv_rigid' if qr else '-')] += 1
            if not (pr and qr): continue
            ts = TaitState(hd, i)
            Hc = ts.components(ts.H); assert len(Hc) == 2
            Cp = [c for c in Hc if not (c & ts.H0)][0]
            feat = tuple(int(bool(Cp & S)) for S in (ts.X, ts.Y, ts.Xt, ts.Yt))
            T[('inshape', typ, 'meets X,Y,Xt,Yt', feat)] += 1
print(gf, dict(sorted(T.items(), key=str)), flush=True)
