#!/usr/bin/env python3
"""Job AU. (i) degree-6 Gamma-cycles: k = 4 / k = 3 failures and k <= 2 fixed points by cycle length L (census orders 25-27 from jobm-gamma-sequences.jsonl + jobr27, and the
Job AS constructions from their battery json). (ii) L = 20 degree-6 Gamma-cycles: orientation-REVERSING automorphisms of T fixing h, and whether one maps s(t) to s(c - t).
(iii) L = 20 cycles with one break (one failing R3k4): does the breaking period have the larger Lock2 witness ({mu,B}-component of x_{j+1}) or the larger |K_{c(p),c(m)}(p)| at R3k4?"""
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
from jobag import canon
from jobao import part
K1 = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}
def part_i():
    tab = defaultdict(Counter)
    for fn in ('../jobm-gamma-sequences.jsonl', '../jobr27/jobm-gamma-sequences.jsonl'):
        for l in open(fn):
            r = json.loads(l)
            if r['pattern'] != '5,5,5,5,6': continue
            for seq in r['jobm']:
                L = len(seq); t = tab[('census', L)]; t['cycles'] += 1
                for x in seq:
                    if x[0] != 3: continue
                    k = K1[x[1]]
                    if k in (3, 4) and x[2] != 'L': t['k%d failures' % k] += 1
                    if k <= 2 and x[2] == 'X': t['k<=2 fixed points'] += 1
    for fn in ('../jobas/jobas-battery.json', '../jobas/jobas-battery-long.json'):
        for r in json.load(open(fn)):
            if tuple(sorted(r['link_degrees'])) != (5, 5, 5, 5, 6) or not r.get('universal_period'): continue
            t = tab[('construction', r['L'])]; t['cycles'] += 1
            for tup, c in r['period_tuples']:
                if not tup[0].startswith('L'): t['k4 failures'] += c
                if not tup[1].startswith('L'): t['k3 failures'] += c
                t['k<=2 fixed points'] += c * sum(1 for e in tup[2:] if e == 'fixed')
    return tab
def reflections(H):
    rot = H.rot; n = len(rot); h = H.h; out = []
    for r in range(5):
        phi = {h: h}; dmap = {(h, H.L[0]): (h, H.L[r])}; q = [(h, H.L[0])]; ok = True
        while q and ok:
            u, v = q.pop(); a, b = dmap[(u, v)]
            if phi.setdefault(v, b) != b: ok = False; break
            ru, ra = rot[u], rot[a]
            if len(ru) != len(ra): ok = False; break
            i, k = ru.index(v), ra.index(b)
            for t in range(len(ru)):
                v2, b2 = ru[(i + t) % len(ru)], ra[(k - t) % len(ra)]     # reversed cyclic order: orientation-reversing
                if (u, v2) in dmap:
                    if dmap[(u, v2)] != (a, b2): ok = False; break
                else: dmap[(u, v2)] = (a, b2); q.append((u, v2))
                if (v2, u) not in dmap: dmap[(v2, u)] = (b2, a); q.append((v2, u))
                elif dmap[(v2, u)] != (b2, a): ok = False; break
        if ok and len(phi) == n and len(set(phi.values())) == n: out.append(phi)
    return out
def job(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); refl = reflections(H); out = []
    t6 = next(t for t in range(5) if len(H.rot[H.L[t]]) >= 6)
    for c, z in enumerate(H.cycles):
        if not all(H.DL[x] for x in z) or len(z) != 20: continue
        P = [part(H, x) for x in z]; rev = False
        for phi in refl:
            img0 = frozenset(frozenset(phi[v] for v in cl) for cl in P[0])
            if img0 in P:
                cc = P.index(img0)
                if all(frozenset(frozenset(phi[v] for v in cl) for cl in P[t]) == P[(cc - t) % 20] for t in range(20)): rev = True
        fr = [H.frame(x) for x in z]; r4 = [i for i in range(20) if fr[i][1] == 3 and (t6 - fr[i][0]) % 5 == 4]
        feats = []
        for i in r4:
            x = z[i]; j, ty, hi, (al, mu, A, B) = fr[i]; s = H.sp.states[x]
            m1 = H.sp.idx[H.L[(j + 1) % 5]]
            lock2 = next(bin(K).count('1') for K in H.sp.components(s, mu, B) if K >> m1 & 1)
            sg = H.sigma(x); lk = H.locks(sg); fail = not (not H.filled(sg) and lk and not lk[0] and not lk[1])
            feats.append(dict(pos=i, fail=fail, lock2=lock2))
        out.append(dict(run=lab, name=name, hole=hole, n_reflections=len(refl), time_reversal_symmetry=rev, r4=feats))
    return out
if __name__ == '__main__':
    tab = part_i()
    print('(i) degree-6 Gamma-cycles by L:')
    for k in sorted(tab): print('   ', k, dict(tab[k]))
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) == (5, 5, 5, 5, 6) and any(z['gamma'] and z['L'] == 20 for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    with Pool(12) as P: res = [x for xs in P.map(job, sorted(holes)) for x in xs]
    json.dump(dict(tab={'%s|%s' % k: v for k, v in tab.items()}, cycles=res), open('jobau.json', 'w'))
    print('(ii) L = 20 degree-6 Gamma-cycles: %d; holes with an orientation-reversing automorphism fixing h: %d; cycles with a time-reversal symmetry s(t) -> s(c - t): %d'
          % (len(res), sum(1 for r in res if r['n_reflections']), sum(r['time_reversal_symmetry'] for r in res)))
    one = [r for r in res if len(r['r4']) == 2 and sum(f['fail'] for f in r['r4']) == 1]
    print('(iii) L = 20 cycles with exactly one failing R3k4: %d' % len(one))
    c = Counter()
    for r in one:
        a, b = r['r4']; f, g = (a, b) if a['fail'] else (b, a)
        c['failing larger' if f['lock2'] > g['lock2'] else ('failing smaller' if f['lock2'] < g['lock2'] else 'tie')] += 1
    print('    Lock2 witness |K_{mu,B}(x_{j+1})| at the two R3k4 states: %s' % dict(c))
    # |K_{c(p),c(m)}(p)| from Job N visit rows (cycles with exactly two k = 4 visits = L = 20 at degree 6)
    c = Counter(); ck3 = Counter()
    for fn in ('../jobn-visits.jsonl', '../jobr27/jobn-visits.jsonl'):
        for l in open(fn):
            r = json.loads(l)
            if r['pattern'] != '5,5,5,5,6': continue
            for cyc in r['jobn']:
                for kk, cc in ((4, c), (3, ck3)):
                    v = [row for row in cyc if row[1] == kk]
                    if len(v) != 2 or v[0][2] + v[1][2] != 1: continue
                    f, g = (v[0], v[1]) if not v[0][2] else (v[1], v[0])
                    cc['failing larger' if f[10] > g[10] else ('failing smaller' if f[10] < g[10] else 'tie')] += 1
                    cc[('fail', f[10], 'other', g[10])] += 1
    print('    |K_{c(p),c(m)}(p)| (Job N) at the two k = 4 visits, one failing:', dict(c))
    print('    same at the two k = 3 visits, one failing:', dict(ck3))
