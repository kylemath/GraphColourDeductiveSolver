#!/usr/bin/env python3
"""Job AG (Lemma Fix), Gamma-cycles at (5,5,5,5,6) and (5,5,5,5,7), orders 25-27, both orientations. Independent Python.
At every R3 state with k in {0,1,2} (k = position of the high-degree link vertex p relative to the repeat j): roles {alpha,mu} = {c(x_j), c(x_{j+1})}, {A,B} = the other pair.
(a) sigma fixed point vs {A,B}-subgraph of T - v acyclic (cycle rank E - V + C = 0); (b) cycle rank of the {A,B}-subgraph induced on the RING (x_0..x_4, w_0..w_4 and p's
middle outer neighbour(s)); (c) cycle rank of the whole {A,B}-subgraph; (d) cycle rank of the {A,B}-subgraph induced on the 2-ball around v."""
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
def canon(ld, cap=8):
    d = [min(x, cap) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
def rank(H, k, verts, cols):
    V = [u for u in verts if H.col(k, u) in cols]; Vs = set(V)
    E = sum(1 for u in V for w in H.rot[u] if w in Vs and w != H.h and u < w)
    seen = set(); C = 0
    for u in V:
        if u in seen: continue
        C += 1; st = [u]; seen.add(u)
        while st:
            a = st.pop()
            for w in H.rot[a]:
                if w in Vs and w not in seen: seen.add(w); st.append(w)
    return E - len(V) + C
def analyse(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); h = hole
    t6 = next(t for t in range(5) if len(H.rot[H.L[t]]) >= 6); p = H.L[t6]; y = H.w[(t6 + 4) % 5]; z = H.w[t6]
    M = [w for w in H.rot[p] if w != h and w not in (H.L[(t6 + 1) % 5], H.L[(t6 + 4) % 5], y, z)]
    ring = set(H.L) | set(H.w) | set(M)
    ball2 = set(H.L) | {w for x in H.L for w in H.rot[x]}; ball2.discard(h)
    allv = [u for u in range(len(H.rot)) if u != h]
    out = []
    for c, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        rows = []
        for x in zc:
            j, ty, hi, (al, mu, A, B) = H.frame(x); k = (t6 - j) % 5
            if ty != 3: rows.append(None); continue
            s = H.sigma(x); fixed = (s == x)
            r_all = rank(H, x, allv, (A, B)); r_ring = rank(H, x, ring, (A, B)); r_b2 = rank(H, x, ball2, (A, B))
            lk = H.locks(s); ex = 'fixed' if fixed else ('lockless' if (not H.filled(s) and not lk[0] and not lk[1]) else 'other')
            rows.append(dict(k=k, fixed=fixed, ex=ex, r_all=r_all, r_ring=r_ring, r_b2=r_b2))
        s0 = next(i for i, r in enumerate(rows) if r and r['k'] == 4); rows = rows[s0:] + rows[:s0]
        out.append(dict(run=lab, name=name, hole=hole, deg=len(H.rot[p]), L=len(rows), rows=rows))
    return out
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7)) and any(z['gamma'] for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    with Pool(12) as P: res = [x for xs in P.map(analyse, sorted(holes)) for x in xs]
    json.dump(res, open('jobag.json', 'w'))
    fails57 = {(x['run'], x['name'], x['hole'], x['L']) for x in json.load(open('jobac.json'))['part1'] if x['pattern'] == '5,5,5,5,7'}
    for deg in (6, 7):
        R = [x for x in res if x['deg'] == deg]; a = Counter(); per = Counter(); vis = Counter()
        for x in R:
            rows = x['rows']; n = len(rows)
            for r in rows:
                if r is None or r['k'] > 2: continue
                a[(r['fixed'], r['r_all'] == 0)] += 1
                vis[(r['k'], r['ex'], 'ring cycle' if r['r_ring'] > 0 else 'ring acyclic', '2-ball cycle' if r['r_b2'] > 0 else '2-ball acyclic')] += 1
            for b in range(0, n, 10):
                ks = [r for r in rows[b:b + 10] if r and r['k'] <= 2]
                per[('some k<=2 state has an A/B cycle in the ring' if any(r['r_ring'] > 0 for r in ks) else 'NO ring A/B cycle at k<=2',
                     'in the 2-ball' if any(r['r_b2'] > 0 for r in ks) else 'NONE in the 2-ball')] += 1
        print('\n=== degree-%d (pattern (5,5,5,5,%d)): Gamma-cycle records %d' % (deg, deg, len(R)))
        print('(a) (sigma fixed point, {A,B} acyclic) at k <= 2 R3 states:', dict(a))
        print('    k, exit kind, ring, 2-ball:'); [print('      ', k, v) for k, v in sorted(vis.items(), key=str)]
        print('periods:', dict(per))
        if deg == 7:
            fr = [x for x in R if (x['run'], x['name'], x['hole'], x['L']) in fails57]
            c = Counter((r['k'], r['ex'], r['r_all'], r['r_ring'], r['r_b2']) for x in fr for r in x['rows'] if r and r['k'] <= 2)
            print('  Lemma S failure records (%d): (k, exit, rank all, rank ring, rank 2-ball):' % len(fr), sorted(c.items()))
