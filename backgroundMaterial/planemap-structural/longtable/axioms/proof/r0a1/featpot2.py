"""Shared-weight potential search, richer features (normal form, H = 0..n-1, v = 0): per side (in = f1 side,
out): #chords of M, sum of chord spans (b-a for a<b, v-chords span = position of far end or n - it, both
given), #even/#odd H-edges, sum of positions of M's H-edges by parity, one-hot k.  LP over all arcs of all
census classes.  usage: featpot2.py n1 n2 ..."""
import sys, json
import numpy as np
from scipy.optimize import linprog
from r0lib import G5, analyse
from featpot import sides
rows = []
NF = 17
for n in map(int, sys.argv[1:]):
    for l in open(f'out/census_n{n}_p.jsonl'):
        r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
        sd = sides(g); A = analyse(g)
        def feat(M):
            f = np.zeros(NF)
            for e in range(g.m):
                if not (M >> e & 1): continue
                a, b = sorted(g.E[e])
                if e in g.fidx:
                    s = g.fidx[e]; f[12 + s] += 1
                    if s in (1, 3, 4):
                        side = 0 if s == 1 else 1; f[2 * side] += 1
                        f[8 + side] += b; f[10 + side] += n - b
                elif b - a == 1:
                    f[4 + (a % 2)] += 1; f[6 + (a % 2)] += a / n
                else:
                    side = sd[e]; f[2 * side] += 1; f[1 + 2 * side] += (b - a) / n
            return f
        F = [feat(M) for M in A['P']]
        for i, j in A['arcs']: rows.append(F[i] - F[j])
res = linprog(np.zeros(NF), A_ub=np.array(rows), b_ub=-np.ones(len(rows)), bounds=[(None, None)] * NF, method='highs')
print(len(rows), 'arcs; LP status', res.status, (np.round(res.x, 2) if res.status == 0 else ''))
