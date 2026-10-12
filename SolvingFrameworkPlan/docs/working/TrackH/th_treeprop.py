#!/usr/bin/env python3
"""Track H: Conjecture TP ('tree propagation fails'): on the sphere, for a DL -> DL pi-step c -> pi(c), it is impossible
that both c and pi(c) have connected {alpha,mu}- and {A,B}-graphs (i.e. partition-1 trees; in the dual: the {2,3}
Tait subgraph is a single cycle through the hole).  TP implies rigid isolation.  Counts DL->DL steps by the pair
(#am, #AB at c ; #am', #AB' at pi(c)) == ((1,1),(1,1)).
usage: th_treeprop.py GRAPHFILE MAXGRAPHS STRIDE [HOLEFIELD]"""
import sys
from collections import Counter
from th_engine import Hole

def p1(H, col, roles):
    al, mu, A, B = roles; out = []
    for pr in [(al, mu), (A, B)]:
        left = {v for v in H.V if col[v] in pr}; k = 0
        while left:
            s = next(iter(left)); left -= H.comp(col, s, pr); k += 1
        out.append(k)
    return tuple(out)

gf, maxg, stride = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
tot = Counter(); k = 0; bad = []
for ln, l in enumerate(open(gf)):
    if ln % stride: continue
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; k += 1
    if k > maxg: break
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        H = Hole(rot, h); S = len(H.states); info = [None] * S; cnt = [None] * S
        for i in range(S):
            r, col = H.analyse_state(i); info[i] = r
            if r['kind'] == 'DL': cnt[i] = p1(H, col, r['roles'])
        for i in range(S):
            if info[i]['kind'] != 'DL' or info[i]['pi'] is None: continue
            t = info[i]['pi']
            if info[t]['kind'] != 'DL': continue
            tot['DLDL'] += 1
            a, b = cnt[i] == (1, 1), cnt[t] == (1, 1)
            tot['trees_at_c'] += a; tot['trees_at_pic'] += b; tot['both'] += a and b
            if a and b and len(bad) < 5: bad.append((p[0], h, i, t))
print(gf, dict(tot), bad)
