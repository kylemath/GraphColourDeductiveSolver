#!/usr/bin/env python3
"""Job AD from Job Z records (exits from all DD endpoints; charge-back form), (5,5,5,5,6) and (5,5,5,6,6), orders 25-27, both orientations.
For every positive cycle Z with def'(Z) > 0: its nonpositive sigma-neighbours T (w, L, rem, #exits from Z into T, credits); (i) min over Z of max_T |rem(T)| / def'(Z);
(ii) weakest neighbour profile; (iii) tightest single-target assignment: sharing and spare; (iv) whether EVERY / SOME target hit by Z's own exits can take def'(Z) alone."""
import json, sys
from fractions import Fraction
from collections import defaultdict, Counter
def canon(ld, cap=8):
    d = [min(x, cap) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
recs = []; ratio = []; prof = Counter(); iv = Counter(); tight = []
for lab in ['z25', 'z25m', 'z26', 'z26m', 'z27', 'z27m']:
    for l in open('out/%s.jsonl' % lab):
        if '"jobs": {"pos": [{' not in l: continue
        r = json.loads(l); pat = canon(r['linkdeg'])
        if pat not in ((5, 5, 5, 5, 6), (5, 5, 5, 6, 6)): continue
        js = r['jobs']; tg = {t[0]: dict(Lam=t[1], L=t[2], rem=t[6], nh=t[4]) for t in js['targets']}; pos = {z['id']: z for z in js['pos']}
        src = defaultdict(lambda: defaultdict(int)); zx = defaultdict(lambda: defaultdict(list))
        for s, t, cr, ty in js['exits']:
            if t in tg: src[t][s] += cr; zx[s][t].append(cr)
        charge = defaultdict(Fraction)
        for t, d in tg.items():
            if d['nh'] > 0 and d['rem'] > 0:
                tot = sum(src[t].values())
                for s, cr in src[t].items(): charge[s] += Fraction(d['rem'] * cr, tot)
        defs = {zid: z['def'] + charge[zid] for zid, z in pos.items() if z['def'] + charge[zid] > 0}
        cap = {t: Fraction(-d['rem']) for t, d in tg.items() if d['rem'] < 0}
        for zid, dp in defs.items():
            z = pos[zid]; nb = [t for t in z['nbrN'] if t in tg]
            rows = [(t, tg[t]['Lam'] // 5, tg[t]['L'], tg[t]['rem'], len(zx[zid][t]), zx[zid][t]) for t in nb]
            best = max((cap.get(t, 0) for t in nb), default=0); ratio.append((float(best / dp), lab, r['name'], r['hole'], zid, str(dp), rows))
            prof['has w<=-2 neighbour' if any(tg[t]['Lam'] <= -10 for t in nb) else 'NO w<=-2 neighbour'] += 1
            hit = [t for t, v in zx[zid].items() if v and t in cap]
            iv['every exit-target can take def alone' if hit and all(cap[t] >= dp for t in hit) else ('some exit-target can' if any(cap[t] >= dp for t in hit) else ('no exit-target can (or no exits)'))] += 1
            recs.append(dict(run=lab, name=r['name'], hole=r['hole'], pattern=','.join(map(str, pat)), Z=zid, gamma=z['gamma'], L=z['L'], w=z['Lambda'] // 5, def_prime=str(dp), neighbours=rows))
        # (iii): tightest assignment per hole: greedy by largest spare, record sharing
        if defs:
            used = defaultdict(Fraction); share = defaultdict(list)
            for zid, dp in sorted(defs.items(), key=lambda kv: -kv[1]):
                nb = [t for t in pos[zid]['nbrN'] if t in cap]
                t = max(nb, key=lambda t: cap[t] - used[t]) if nb else None
                if t is None: continue
                used[t] += dp; share[t].append(zid)
            for t, zs in share.items(): tight.append((float(cap[t] - used[t]), len(zs), lab, r['name'], r['hole'], t, [str(defs[z]) for z in zs]))
json.dump(recs, open('jobad-records.json', 'w'), indent=0)
ratio.sort()
print('positive cycles with def\' > 0 at (5,5,5,5,6)/(5,5,5,6,6), orders 25-27, both orientations: %d (Gamma %d)' % (len(recs), sum(1 for x in recs if x['gamma'])))
print('(i) min over Z of max_T |rem(T)| / def\'(Z): %.2f at %s' % (ratio[0][0], ratio[0][1:6])); print('    5 smallest:', [(round(x[0], 2),) + x[1:6] for x in ratio[:5]])
print('    distribution (ratio buckets):', sorted(Counter(min(int(x[0]), 20) for x in ratio).items()))
print('(ii) neighbour profile:', dict(prof))
print('(iii) tightest targets after a greedy single-target assignment (spare, #positive cycles sharing, ...):', sorted(tight)[:6])
print('    max sharing:', max((x[1] for x in tight), default=0))
print('(iv) exit targets:', dict(iv))
