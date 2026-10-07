#!/usr/bin/env python3
"""Charge-back P1 (coordinator refinement of Jobs S/Z) from out/sx*.jsonl or out/z*.jsonl (records with 'exits' = [source, target, credit, R-type]):
rem(T) as before; for each nonpositive T with rem(T) > 0, charge rem(T) back to the positive sources that hit T in proportion to their credits (exact rationals);
def'(Z) = def(Z) + charge-back; then P1: each def' > 0 assigned to ONE nonpositive sigma-neighbour T with rem(T) < 0, no T over-assigned (exact search)."""
import json, sys
from fractions import Fraction
from collections import defaultdict, Counter
def assign_single(Z, cap):
    order = sorted(Z, key=lambda z: (-z[1], len(z[2]))); used = defaultdict(Fraction)
    def bt(i):
        if i == len(order): return True
        zid, d, nb = order[i]
        for t in sorted(nb, key=lambda t: -(cap.get(t, 0) - used[t])):
            if cap.get(t, 0) - used[t] >= d:
                used[t] += d
                if bt(i + 1): return True
                used[t] -= d
        return False
    return bt(0)
for lab in sys.argv[1:]:
    T = Counter(); fails = []; pos_rem = []
    for l in open('out/%s.jsonl' % lab):
        if '"jobs": {"pos": [{' not in l: continue
        r = json.loads(l); js = r['jobs']; T['holes'] += 1
        tg = {t[0]: dict(Lam=t[1], L=t[2], hit=t[3], nh=t[4], nd=t[5], rem=t[6]) for t in js['targets']}
        pos = {z['id']: z for z in js['pos']}
        src_cr = defaultdict(lambda: defaultdict(int))
        for s, t, cr, ty in js['exits']:
            if t in tg: src_cr[t][s] += cr
        charge = defaultdict(Fraction)
        for t, d in tg.items():
            if d['nh'] > 0 and d['rem'] > 0:
                tot = sum(src_cr[t].values()); pos_rem.append((r['name'], r['hole'], t, d, dict(src_cr[t])))
                for s, cr in src_cr[t].items(): charge[s] += Fraction(d['rem'] * cr, tot)
        deficits = []
        for zid, z in pos.items():
            dp = z['def'] + charge[zid]
            if dp > 0: deficits.append((zid, dp, [t for t in z['nbrN'] if t in tg and tg[t]['rem'] < 0]))
        T['def_prime_pos'] += len(deficits); T['charged'] += sum(1 for v in charge.values() if v > 0)
        if deficits:
            cap = {t: Fraction(-tg[t]['rem']) for t in tg if tg[t]['rem'] < 0}
            if not assign_single(deficits, cap): fails.append((r['name'], r['hole'], [(z, str(d), nb) for z, d, nb in deficits]))
    print("== %s: holes %d; targets with rem > 0: %d; sources charged back: %d; def' > 0: %d; charge-back P1 single-target FAILS at %d holes %s"
          % (lab, T['holes'], len(pos_rem), T['charged'], T['def_prime_pos'], len(fails), fails[:3]))
    for x in pos_rem: print('   rem>0:', x)
