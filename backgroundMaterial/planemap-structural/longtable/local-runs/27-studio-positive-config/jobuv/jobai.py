#!/usr/bin/env python3
"""Job AI: the actual {A,B}-cycles at positions 4, 6, 8 (R3k2, R3k1, R3k0) of every period of (5,5,5,5,6) Gamma-cycles, orders 25-27, both orientations.
Cycle basis = fundamental cycles of a BFS spanning forest of the {A,B}-subgraph of T - v. Per cycle: length, ring vertices on it (x_i, w_i, m), and the split of T - C
(size of the side containing v vs the rest). Per step 4, 5, 6, 7: the swapped component's intersection with each cycle and the fate of the cycle in the next state
(survives = its vertex set is still a cycle of the next state's {A,B}-subgraph; else rerouted if the next {A,B} rank >= 1, dies if it is 0)."""
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
from jobag import canon
def ab_cycles(H, k, A, B):
    V = {u for u in H.sp.order if H.col(k, u) in (A, B)}
    par = {}; depth = {}; cyc = []
    for r in sorted(V):
        if r in par: continue
        par[r] = None; depth[r] = 0; q = [r]
        for u in q:
            for w in H.rot[u]:
                if w in V and w not in par: par[w] = u; depth[w] = depth[u] + 1; q.append(w)
    seen = set()
    for u in V:
        for w in H.rot[u]:
            if w not in V or par.get(u) == w or par.get(w) == u or (min(u, w), max(u, w)) in seen: continue
            seen.add((min(u, w), max(u, w)))
            a, b = u, w; pa, pb = [a], [b]
            while a != b:
                if depth[a] >= depth[b]: a = par[a]; pa.append(a)
                else: b = par[b]; pb.append(b)
            cyc.append(pa + pb[-2::-1])
    return cyc
def side_split(H, C):
    Cs = set(C); h = H.h; seen = {h}; st = [h]
    while st:
        u = st.pop()
        for w in H.rot[u]:
            if w not in Cs and w not in seen: seen.add(w); st.append(w)
    return len(seen) - 1, len(H.rot) - len(Cs) - len(seen)
def analyse(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); h = hole
    t6 = next(t for t in range(5) if len(H.rot[H.L[t]]) >= 6); p = H.L[t6]; y = H.w[(t6 + 4) % 5]; z = H.w[t6]
    m = [w for w in H.rot[p] if w != h and w not in (H.L[(t6 + 1) % 5], H.L[(t6 + 4) % 5], y, z)][0]
    names = {H.L[i]: 'x%d' % i for i in range(5)} | {H.w[i]: 'w%d' % i for i in range(5)} | {m: 'm'}
    rel = lambda v: names.get(v)
    out = []
    for c, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        n = len(zc); fr = [H.frame(x) for x in zc]
        s0 = next(i for i in range(n) if fr[i][1] == 3 and (t6 - fr[i][0]) % 5 == 4); zc = zc[s0:] + zc[:s0]; fr = fr[s0:] + fr[:s0]
        per = []
        for b in range(0, n, 10):
            rec = {}
            for pos in (4, 5, 6, 7, 8):
                x = zc[b + pos]; j, ty, hi, (al, mu, A, B) = fr[b + pos]
                C = ab_cycles(H, x, A, B)
                rec[pos] = dict(rank=len(C), cycles=[dict(len=len(cc), ring=[rel(v) for v in cc if rel(v)], y=y in cc, z=z in cc, p=p in cc, m=m in cc, split=side_split(H, cc), verts=cc) for cc in C],
                                fixed=(ty == 3 and H.sigma(x) == x))
                if pos < 8:   # the step pos -> pos+1 swaps the {alpha,A}-component of x_{j+2}
                    s = H.sp.states[x]; i2 = H.sp.idx[H.L[(j + 2) % 5]]; K = next(K for K in H.sp.components(s, al, A) if K >> i2 & 1); Kv = set(H.sp.mask_vertices(K))
                    xn = zc[(b + pos + 1) % n]; jn, tyn, hin, (aln, mun, An, Bn) = fr[(b + pos + 1) % n]
                    fate = []
                    for cc in C:
                        still = all(H.col(xn, v) in (An, Bn) for v in cc)
                        fate.append(dict(meets=len(Kv & set(cc)), fate='survives' if still else None))
                    rec[pos]['step'] = dict(Ksize=len(Kv), fates=fate)
            for pos in (4, 5, 6, 7):
                nr = rec[pos + 1]['rank']
                for f in rec[pos]['step']['fates']:
                    if f['fate'] is None: f['fate'] = 'rerouted' if nr >= 1 else 'dies'
            per.append(rec)
        out.append(dict(run=lab, name=name, hole=hole, L=n, periods=per))
    return out
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) == (5, 5, 5, 5, 6) and any(z['gamma'] for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    with Pool(12) as P: res = [x for xs in P.map(analyse, sorted(holes)) for x in xs]
    json.dump(res, open('jobai.json', 'w'))
    C = Counter(); fates = defaultdict(Counter); killer = Counter(); prev = Counter(); yz = Counter(); lens = Counter(); ringv = Counter(); splits = Counter()
    for x in res:
        for P_ in x['periods']:
            for pos in (4, 6, 8):
                r = P_[pos]; C[(pos, r['rank'])] += 1
                for cc in r['cycles']: lens[cc['len']] += 1; ringv[tuple(sorted(cc['ring']))] += 1; splits[('v side', cc['split'][0], 'far side', cc['split'][1])] += 1
            for pos in (4, 5, 6, 7):
                for f in P_[pos]['step']['fates']: fates[pos][(f['fate'], 'meets K' if f['meets'] else 'misses K')] += 1
            # fixed-point periods: rank 0 at 6 and/or 8
            for pos in (6, 8):
                if P_[pos]['rank'] == 0:
                    q = pos - 1
                    while q >= 4 and P_[q]['rank'] == 0: q -= 1
                    if q >= 4:
                        killer[(pos, 'killed at step %d' % q)] += 1
                        for cc in P_[q]['cycles']: prev[(pos, q, cc['len'], tuple(sorted(cc['ring'])), 'y' if cc['y'] else '-', 'z' if cc['z'] else '-')] += 1
            cyc_any = [cc for pos in (4, 6, 8) for cc in P_[pos]['cycles']]
            if cyc_any: yz['some cycle at 4/6/8 passes through y or z' if any(cc['y'] or cc['z'] for cc in cyc_any) else 'NO cycle at 4/6/8 through y or z'] += 1
    print('(5,5,5,5,6) Gamma-cycle records %d, periods %d' % (len(res), sum(len(x['periods']) for x in res)))
    print('A/B rank at positions 4, 6, 8:', sorted(C.items()))
    print('cycle lengths:', sorted(lens.items())); print('split of T - C (vertices on v\'s side, far side):', sorted(splits.items())[:12])
    print('ring vertices on the cycles (most common):', ringv.most_common(8))
    print('fate of each A/B cycle at steps 4..7 (fate, meets swapped component?):'); [print('   step', k, dict(v)) for k, v in sorted(fates.items())]
    print('HEADLINE fixed-point periods: rank 0 at position 6/8, the step after the last rank>=1 position that killed it:', dict(killer))
    print('    the cycle at that preceding position (pos0, pos, len, ring vertices, y?, z?):'); [print('      ', k, v) for k, v in prev.most_common(10)]
    print('periods with a cycle at 4/6/8: through y or z?', dict(yz))
