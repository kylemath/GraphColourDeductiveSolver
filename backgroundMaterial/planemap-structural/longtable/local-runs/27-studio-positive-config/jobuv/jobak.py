#!/usr/bin/env python3
"""Job AK parts 2-4 (+ addendum a) on (5,5,5,5,6) Gamma-cycle periods, orders 25-27, both orientations. NightW2 bookkeeping: at R3k2 (pos 4) alpha = 1, mu = 2, A = 3, B = 4;
the {2,3}-graph at R3k0 (pos 8) = that state's own {A,B}-graph; the {3,4}-graph at R3k2 = its own {A,B}-graph; at pos 5 the {2,3}-graph = pos 5's own {A,B}-graph; at pos 6
the {2,3}-graph = pos 6's own {mu,B}-graph. K4..K7 = vertex sets swapped at steps 4..7."""
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
from uv_lib import Hole
from jobag import canon
from jobai import ab_cycles
def rank_pair(H, k, a, b):
    from jobag import rank
    return rank(H, k, [u for u in range(len(H.rot)) if u != H.h], (a, b))
def separates(H, C, targets):
    Cs = set(C); seen = {H.h}; st = [H.h]
    while st:
        u = st.pop()
        for w in H.rot[u]:
            if w not in Cs and w not in seen: seen.add(w); st.append(w)
    return any(t not in Cs and t not in seen for t in targets)
def analyse(args):
    lab, name, hole = args
    H = Hole(name, hole, lab.endswith('m')); h = hole
    t6 = next(t for t in range(5) if len(H.rot[H.L[t]]) >= 6); p = H.L[t6]; y = H.w[(t6 + 4) % 5]; z = H.w[t6]
    m = [w for w in H.rot[p] if w != h and w not in (H.L[(t6 + 1) % 5], H.L[(t6 + 4) % 5], y, z)][0]
    out = []
    for c, zc in enumerate(H.cycles):
        if not all(H.DL[x] for x in zc): continue
        n = len(zc); fr = [H.frame(x) for x in zc]
        s0 = next(i for i in range(n) if fr[i][1] == 3 and (t6 - fr[i][0]) % 5 == 4); zc = zc[s0:] + zc[:s0]; fr = fr[s0:] + fr[:s0]
        for b in range(0, n, 10):
            st = {q: zc[b + q] for q in range(4, 9)}; F = {q: fr[b + q] for q in range(4, 9)}
            K = {}
            for q in (4, 5, 6, 7):
                j, ty, hi, (al, mu, A, B) = F[q]; s = H.sp.states[st[q]]; i2 = H.sp.idx[H.L[(j + 2) % 5]]
                K[q] = set(H.sp.mask_vertices(next(KK for KK in H.sp.components(s, al, A) if KK >> i2 & 1)))
            A4, B4 = F[4][3][2], F[4][3][3]; A8, B8 = F[8][3][2], F[8][3][3]
            r4 = rank_pair(H, st[4], A4, B4); r6 = rank_pair(H, st[6], F[6][3][2], F[6][3][3]); r8 = rank_pair(H, st[8], A8, B8)
            rec = dict(run=lab, name=name, hole=hole, cycle=c, period=b // 10, r4=r4, r6=r6, r8=r8, K={q: sorted(K[q]) for q in K}, p=p, m=m, y=y, z=z)
            # Lock1 chain at R3k2: {mu,A}-component of x_{j+1}
            j4, _, _, (al4, mu4, _, _) = F[4]; s4 = H.sp.states[st[4]]; im = H.sp.idx[H.L[(j4 + 1) % 5]]
            lock1 = set(H.sp.mask_vertices(next(KK for KK in H.sp.components(s4, mu4, A4) if KK >> im & 1)))
            if r4 == 0:   # (2) a {2,3}-cycle at R3k0
                C8 = ab_cycles(H, st[8], A8, B8)
                rec['H'] = [dict(meets4=bool(set(cc) & K[4]), meets5=bool(set(cc) & K[5]), meets7=bool(set(cc) & K[7]), meets7not4=bool(set(cc) & (K[7] - K[4])), meetsLock1=bool(set(cc) & lock1), len=len(cc)) for cc in C8]
                # (3) F4: C5 = {2,3}-cycle at pos 5 (= pos-5 own {A,B})
                j5, _, _, (_, _, A5, B5) = F[5]; C5 = ab_cycles(H, st[5], A5, B5)
                rec['C5'] = [dict(len=len(cc), through_p=p in cc, near_y=bool(set(cc) & set(H.rot[y])), inter_K4=len(set(cc) & K[4]), separates_h_from_K4=separates(H, cc, K[4])) for cc in C5]
                j6, _, _, (_, mu6, _, B6) = F[6]; rec['kill'] = rank_pair(H, st[6], mu6, B6) == 0
                if rec['kill']: rec['C8'] = [dict(len=len(cc), inter_K7=len(set(cc) & K[7])) for cc in C8]
            if r8 == 0:   # mirror: a {3,4}-cycle at R3k2 meets K4 \ K7 ?
                C4 = ab_cycles(H, st[4], A4, B4)
                rec['Hmirror'] = [dict(meets4not7=bool(set(cc) & (K[4] - K[7])), meets4=bool(set(cc) & K[4]), meets7=bool(set(cc) & K[7])) for cc in C4]
            if r4 + r6 + r8 == 1:   # (4) dump
                rec['dump'] = dict(rotation=H.rot, link=H.L, colourings={q: {str(v): 'abcd'[H.col(st[q], v)] for v in sorted(H.sp.order)} for q in range(4, 9)})
            out.append(rec)
    return out
if __name__ == '__main__':
    holes = set()
    for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
        for l in open('../out/%s.jsonl' % lab):
            if '"jobs": {"pos": [{' not in l: continue
            r = json.loads(l)
            if canon(r['linkdeg']) == (5, 5, 5, 5, 6) and any(z['gamma'] for z in r['jobs']['pos']): holes.add((lab, r['name'], r['hole']))
    with Pool(12) as P: res = [x for xs in P.map(analyse, sorted(holes)) for x in xs]
    json.dump([{k: v for k, v in r.items() if k != 'dump'} for r in res], open('jobak-periods.json', 'w'))
    json.dump([dict(run=r['run'], name=r['name'], hole=r['hole'], cycle=r['cycle'], period=r['period'], ranks=(r['r4'], r['r6'], r['r8']), **r['dump']) for r in res if 'dump' in r], open('jobak-66dump.json', 'w'))
    print('periods', len(res))
    Hs = [h for r in res for h in r.get('H', [])]; print('(2) periods with rank(k2)=0: %d; their {2,3}-cycles at R3k0: %d' % (sum(1 for r in res if r['r4'] == 0), len(Hs)))
    print('    meets K4 %d, K5 %d, K7 %d, K7\\K4 %d, the pulled-back Lock1@R3k2 chain %d' % tuple(sum(h[k] for h in Hs) for k in ('meets4', 'meets5', 'meets7', 'meets7not4', 'meetsLock1')))
    perH = Counter(any(h['meets7not4'] for h in r['H']) for r in res if r['r4'] == 0); print('    Hypothesis H per period (some {2,3}-cycle meets K7\\K4):', dict(perH), '; every cycle:', sum(h['meets7not4'] for h in Hs), '/', len(Hs))
    Hm = [h for r in res for h in r.get('Hmirror', [])]; perHm = Counter(any(h['meets4not7'] for h in r['Hmirror']) for r in res if r['r8'] == 0)
    print('    mirror: periods with rank(k0)=0: %d; {3,4}-cycles at R3k2 meeting K4\\K7: %d / %d; per period %s' % (sum(1 for r in res if r['r8'] == 0), sum(h['meets4not7'] for h in Hm), len(Hm), dict(perHm)))
    C5 = [c for r in res for c in r.get('C5', [])]; print('(3) F4 periods: %d; C5 cycles %d: through p %d, near y %d, separates h from a K4 vertex %d; |C5 & K4| distribution %s; length %s'
          % (sum(1 for r in res if r['r4'] == 0), len(C5), sum(c['through_p'] for c in C5), sum(c['near_y'] for c in C5), sum(c['separates_h_from_K4'] for c in C5), sorted(Counter(c['inter_K4'] for c in C5).items()), sorted(Counter(c['len'] for c in C5).items())))
    kl = [r for r in res if r.get('kill')]; c8 = [c for r in kl for c in r['C8']]
    print('    kill cases (r23(6) = 0): %d; C8 |C8 & K7| distribution %s' % (len(kl), sorted(Counter(c['inter_K7'] for c in c8).items())))
    print('(4) rank-sum-1 periods dumped: %d (jobak-66dump.json)' % sum(1 for r in res if 'dump' in r))
