#!/usr/bin/env python3
"""Track S: the primal identity V5 (Lemma S4 of README) in arbitrary graphs (no embedding):
for a DL state t with #aA(t) = 2 and pi(t), pi^-1(t) defined:  P2(pi t) = P2(pi^-1 t) xor delta(K_aA(x_j)),
and P2(pi t) cap P2(t) = empty.  Also reports, along every all-DL pi-cycle, whether it is a Q-cycle (P2 = (2,1) everywhere).
usage: ts_v5_general.py GRAPHFILE [hole]   (graph lines 'name n adj;adj;...', default hole 0)"""
import sys, json
from collections import Counter
from ts_lib import HoleData
from ts_qcyc import cycles


def P2(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']
    return {(v, w) for v in hd.Hh.V for w in hd.Hh.adj[v] if v < w and {col[v], col[w]} in ({al, A}, {mu, B})}


h = int(sys.argv[2]) if len(sys.argv) > 2 else 0
C = Counter()
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
    hd = HoleData(rot, h); info = hd.info
    pre = {}
    for i in range(hd.S):
        if info[i]['kind'] == 'DL' and info[i]['pi'] is not None: pre[info[i]['pi']] = i
    for t in range(hd.S):
        r = info[t]
        if r['kind'] != 'DL' or r['pi'] is None or t not in pre or r['c6'][2] != 2: continue
        u, q = r['pi'], pre[t]
        if info[u]['kind'] == 'F': continue
        x = r['x']; col = hd.col[t]; al, mu, A, B = r['roles']
        K0 = hd.Hh.comp(col, x[0], (al, A))
        d = {(v, w) for v in hd.Hh.V for w in hd.Hh.adj[v] if v < w and ((v in K0) != (w in K0))}
        C['V5_n'] += 1; C['V5_fail'] += P2(hd, u) != (P2(hd, q) ^ d)
        C['disj_fail'] += bool(P2(hd, u) & P2(hd, t))
    for c in cycles(hd):
        C['cycles'] += 1; C['Qcycles'] += all(info[q]['c6'][2] + info[q]['c6'][3] == 3 for q in c)
    print(p[0], dict(C), flush=True)
print('TOTAL', json.dumps(dict(C)))
