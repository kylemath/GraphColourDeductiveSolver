#!/usr/bin/env python3
"""Track L [data]: lock-path words at sphere DL N = 9 states with extra chain in P1.
Lock1 path = the path from x1 to x3 in the muA-chain of x1; Lock2 path = x1 to x4 in the muB-chain.  Every edge of a
lock path is dual to a colour-3 (Lock1) / colour-2 (Lock2) Tait edge, hence lies on H = H0 u C'.  Word, read from x1:
'h' = edge on H0, 'c' = edge on C'.
Tallies (extra type, pi rigid?, pi^-1 rigid?, Lock1 word, Lock2 word).
usage: tl_sphladder.py GRAPHFILE STRIDE OFFSET MAXGRAPHS"""
import sys
from collections import Counter, deque
from tl_lib import HoleData, TaitState, read_graphs


def path(hd, col, s, t, pair):
    prev = {s: None}; dq = deque([s])
    while dq:
        u = dq.popleft()
        if u == t: break
        for w in hd.Hh.adj[u]:
            if w not in prev and col[w] in pair: prev[w] = u; dq.append(w)
    assert t in prev
    P = [t]
    while prev[P[-1]] is not None: P.append(prev[P[-1]])
    return P[::-1]


import os
ALL = os.environ.get('TL_ALL') == '1'
SUMMARY = os.environ.get('TL_SUM') == '1'


def main():
    gf, stride, off, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    T = Counter()
    for name, rot in read_graphs(gf, stride, off, maxg):
        for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
            hd = HoleData(rot, h); T['holes'] += 1
            for i in range(hd.S):
                r = hd.info[i]
                if r['kind'] != 'DL' or r['N'] != 9: continue
                ex = hd.extra(i)
                if ex not in ([0], [1]): continue
                pr = r['pi'] is not None and hd.rigid(r['pi'])
                qr = r['pinv'] is not None and hd.rigid(r['pinv'])
                if not (pr or qr) and not ALL: continue
                ts = TaitState(hd, i); col = hd.col[i]; x = r['x']
                al, mu, A, B = r['roles']
                eid = {frozenset(e): k for k, e in enumerate(ts.prim)}
                Hc = ts.components(ts.H)
                H0 = ts.H0
                words = []
                for tgt, pair in ((x[3], (mu, A)), (x[4], (mu, B))):
                    P = path(hd, col, x[1], tgt, pair)
                    w = ''
                    for a, b in zip(P, P[1:]):
                        k = eid[frozenset((a, b))]
                        assert k in ts.H
                        w += 'h' if k in H0 else 'c'
                    words.append(w)
                def prop(w):
                    return ('h1' if w[0] == 'h' else 'c1') + ('/pairs' if all(w[2 * t + 1] == w[2 * t + 2] for t in range((len(w) - 1) // 2)) else '/nopairs')
                if SUMMARY:
                    T[('am' if ex == [0] else 'AB', 'pi' if pr else '-', 'pinv' if qr else '-', 'L1:' + prop(words[0]), 'L2:' + prop(words[1]))] += 1
                else:
                    T[('am' if ex == [0] else 'AB', 'pi' if pr else '-', 'pinv' if qr else '-', 'L1:' + words[0], 'L2:' + words[1])] += 1
    print(gf, 'holes', T.pop('holes', 0), flush=True)
    for k in sorted(T, key=str): print('  ', k, T[k])


if __name__ == '__main__':
    main()
