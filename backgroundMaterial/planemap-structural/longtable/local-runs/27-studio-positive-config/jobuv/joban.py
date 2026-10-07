#!/usr/bin/env python3
"""Job AN (closing permutation). For every Gamma-cycle (orders 25-27, all patterns, both orientations): follow L pi-steps with ABSOLUTE colours (each step = the Kempe swap of
the step component, colours exchanged on it), and read rho with c_L = rho(c_0). At (5,5,5,5,6)/(5,5,5,5,7): start c_0 at an R3k2 state (period position 4) and test whether rho fixes
c_0(p) and 3-cycles the other three. Rank vector per period: ranks of the three alpha-free pairs at positions 4, 6, 8, named by that period's own R3k2 labels
(alpha = c(p), mu = c(x_{j+1}), A, B): r_AB (= r34), r_muB (= r24), r_muA (= r23). Period map: distribution of (v_b -> v_{b+1})."""
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
from jobag import canon, rank
from jobam import stepK
def cyctype(perm):
    seen = set(); t = []
    for a in range(4):
        if a in seen: continue
        n = 0; b = a
        while b not in seen: seen.add(b); b = perm[b]; n += 1
        t.append(n)
    t = tuple(sorted(t, reverse=True))
    return {(1, 1, 1, 1): 'identity', (2, 1, 1): 'transposition', (3, 1): '3-cycle', (4,): '4-cycle', (2, 2): 'double transposition'}[t]
def job(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); pat = canon([len(H.rot[x]) for x in H.L]); out = []
    hi = [t for t in range(5) if len(H.rot[H.L[t]]) >= 6]; t6 = hi[0] if len(hi) == 1 else None
    allv = [u for u in range(len(H.rot)) if u != H.h]
    for c, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        n = len(zc)
        if t6 is not None:
            fr = [H.frame(x) for x in zc]
            s = next((i for i in range(n) if fr[i][1] == 3 and (t6 - fr[i][0]) % 5 == 2), None)
            if s is not None: zc = zc[s:] + zc[:s]
        col = {v: H.col(zc[0], v) for v in H.sp.order}; c0 = dict(col)
        for t in range(n):
            K = stepK(H, zc[t]); cs = {col[v] for v in K}; assert len(cs) == 2, cs
            a, b = sorted(cs)
            for v in K: col[v] = b if col[v] == a else a
            # sanity: absolute colouring after the step has the partition of the next state
            if t == n - 1 or t < 3:
                nxt = zc[(t + 1) % n]; mp = {}
                assert all(mp.setdefault(H.col(nxt, v), col[v]) == col[v] for v in H.sp.order)
        rho = {}
        for v in H.sp.order: rho.setdefault(c0[v], col[v])
        perm = [rho[a] for a in range(4)]; ct = cyctype(perm)
        rec = dict(pattern=pat, L=n, rho=perm, type=ct)
        if t6 is not None:
            p = H.L[t6]; rec['fixes_p'] = perm[c0[p]] == c0[p]
            # rank vectors per period (positions 4, 6, 8 relative to an R3k2 start = position 0 here)
            vecs = []
            for b in range(0, n, 10):
                x2 = zc[b]; j, ty, hi2, (al, mu, A, B) = H.frame(x2)
                v = tuple(rank(H, zc[(b + d) % n], allv, pr) for d in (0, 2, 4) for pr in ((A, B), (mu, B), (mu, A)))
                vecs.append(v)
            rec['vecs'] = vecs
        out.append(rec)
    return [dict(r, run=lab, name=name, hole=hole) for r in out]
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if any(zz['gamma'] for zz in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    with Pool(12) as P: res = [x for xs in P.map(job, sorted(holes)) for x in xs]
    json.dump(res, open('joban.json', 'w'))
    C = defaultdict(Counter)
    for r in res: C[','.join(map(str, r['pattern']))][r['type']] += 1
    print('Gamma-cycle records (orders 25-27, both orientations):', len(res))
    print('closing permutation rho by pattern:'); [print('   %-12s %s' % (k, dict(v))) for k, v in sorted(C.items(), key=lambda kv: -sum(kv[1].values()))]
    for pat in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 7)):
        R = [r for r in res if tuple(r['pattern']) == pat]
        fx = Counter((r['type'], r['fixes_p']) for r in R); orb = Counter(r['L'] * {'identity': 1, 'transposition': 2, '3-cycle': 3, '4-cycle': 4, 'double transposition': 2}[r['type']] for r in R)
        print('\n=== %s: (rho type, fixes c(p)) %s; true orbit lengths in colouring space %s' % (pat, dict(fx), sorted(orb.items())))
        trans = Counter()
        for r in R:
            vs = r['vecs']
            for i in range(len(vs)): trans[(vs[i], vs[(i + 1) % len(vs)])] += 1
        print('   period map on (rAB, rmuB, rmuA at pos 4 | 6 | 8), most common transitions v_b -> v_{b+1}:')
        for (a, b), k in trans.most_common(10): print('     %s -> %s  x%d' % (a, b, k))
        same = sum(k for (a, b), k in trans.items() if a == b); print('   v_{b+1} = v_b in %d of %d transitions' % (same, sum(trans.values())))
