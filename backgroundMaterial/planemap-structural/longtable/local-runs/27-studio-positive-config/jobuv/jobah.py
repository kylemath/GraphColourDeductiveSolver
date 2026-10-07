#!/usr/bin/env python3
"""Job AH: at every state of each Gamma-cycle at (5,5,5,5,6)/(5,5,5,5,7) (orders 25-27, both orientations): cycle ranks (E - V + C) of the global {A,B}-, {mu,A}- and
{mu,B}-subgraphs of T - v ({alpha,mu} = {c(x_j), c(x_{j+1})} for the state's own j), the step's swapped pair / component in terms of p, m (middle outer neighbour(s)), y, z,
and per-step rank changes. Periods start at R3k4 (positions 0..9: R3k4 R1k1 R3k3 R1k0 R3k2 R1k4 R3k1 R1k3 R3k0 R1k2). Independent Python."""
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
from jobag import rank, canon
def analyse(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); h = hole
    t6 = next(t for t in range(5) if len(H.rot[H.L[t]]) >= 6); p = H.L[t6]; y = H.w[(t6 + 4) % 5]; z = H.w[t6]
    M = [w for w in H.rot[p] if w != h and w not in (H.L[(t6 + 1) % 5], H.L[(t6 + 4) % 5], y, z)]
    allv = [u for u in range(len(H.rot)) if u != h]; out = []
    for c, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        rows = []
        for x in zc:
            j, ty, hi, (al, mu, A, B) = H.frame(x); k = (t6 - j) % 5
            xj2 = H.L[(j + 2) % 5]; s = H.sp.states[x]; i2 = H.sp.idx[xj2]
            K = next(K for K in H.sp.components(s, al, A) if K >> i2 & 1); Kv = set(H.sp.mask_vertices(K))
            pair = ''.join(nm for nm, v in (('p', p), ('m', M[0]), ('y', y), ('z', z)) if H.col(x, v) in (al, A))
            comp = ''.join(nm for nm, v in (('p', p), ('m', M[0]), ('y', y), ('z', z)) if v in Kv)
            fixed = (ty == 3 and H.sigma(x) == x)
            rows.append(dict(ty=ty, k=k, AB=rank(H, x, allv, (A, B)), muA=rank(H, x, allv, (mu, A)), muB=rank(H, x, allv, (mu, B)), pair=pair, comp=comp or '-', fixed=fixed, K=len(Kv)))
        s0 = next(i for i, r in enumerate(rows) if r['ty'] == 3 and r['k'] == 4); rows = rows[s0:] + rows[:s0]
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
    json.dump(res, open('jobah.json', 'w'))
    fails57 = {(x['run'], x['name'], x['hole'], x['L']) for x in json.load(open('jobac.json'))['part1'] if x['pattern'] == '5,5,5,5,7'}
    for deg, sel in ((6, lambda x: True), (7, lambda x: (x['run'], x['name'], x['hole'], x['L']) in fails57), (7, lambda x: True)):
        R = [x for x in res if x['deg'] == deg and sel(x)]
        tag = 'degree 6' if deg == 6 else ('degree 7, the 15 Lemma S failure records' if len(R) < 40 else 'degree 7, all')
        seqfix = Counter(); seqrest = Counter(); m468 = None; zero468 = 0; dAB = defaultdict(Counter); pairs = Counter(); twozero = 0; n468 = 0
        for x in R:
            rows = x['rows']; n = len(rows)
            for b in range(0, n, 10):
                per = rows[b:b + 10]; sq = tuple(r['AB'] for r in per)
                (seqfix if any(r['fixed'] for r in per) else seqrest)[sq] += 1
                s468 = per[4]['AB'] + per[6]['AB'] + per[8]['AB']; n468 += 1
                if m468 is None or s468 < m468[0]: m468 = (s468, x['run'], x['name'], x['hole'])
                zero468 += (per[4]['AB'] == 0 and per[6]['AB'] == 0 and per[8]['AB'] == 0)
            for i in range(n):
                a, bb = rows[i], rows[(i + 1) % n]
                dAB[i % 10][bb['AB'] - a['AB']] += 1; pairs[(i % 10, a['pair'], a['comp'])] += 1
                if i % 10 in (4, 6) and bb['AB'] == 0 and a['AB'] > 0:
                    c2 = rows[(i + 2) % n]
                    if c2['AB'] == 0: twozero += 1
        print('\n=== %s: Gamma-cycle records %d, periods %d' % (tag, len(R), n468))
        print('(i) A/B rank sequence over the period (positions 0..9), periods WITH a fixed point (top 6):', seqfix.most_common(6))
        print('    periods WITHOUT a fixed point (top 6):', seqrest.most_common(6))
        print('(ii) A/B rank at positions 4, 6, 8 (R3k2, R3k1, R3k0) all zero in %d periods; min rank(4)+rank(6)+rank(8) = %s' % (zero468, m468))
        print('(iii) per step i (state i -> i+1) the swap (pair carrying colours of p,m,y,z; component contents) and the A/B rank change:')
        for i in range(10):
            pr = [(k[1], k[2]) for k in pairs if k[0] == i]
            print('     step %d %s  dAB %s' % (i, sorted(set(pr)), sorted(dAB[i].items())))
        print('    a step 4 or 6 lowering the A/B rank to 0 followed two states later by rank 0 again: %d' % twozero)
        mins = (min(r['muA'] for x in R for r in x['rows']), min(r['muB'] for x in R for r in x['rows']))
        print('    min {mu,A} rank, min {mu,B} rank over all states:', mins)
