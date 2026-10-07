#!/usr/bin/env python3
"""[exploratory] NightP1 section 2: slack of charge-back P1 on the Studio Job S records (orders 25-27, both orientations).
Input: ../27-studio-positive-config/jobs-records.jsonl (per hole: pos cycles {id, Lambda, gamma, L, CrN, def, nbrN}; targets [id, Lam, L, hit, nh, nd, rem]).
Charge-back sources of the 12 rem > 0 targets are read from ../27-studio-positive-config/jobcb-summary.txt (each has ONE source, so the charge is the whole rem).
For every hole with some def' > 0 (def' = def + charge):
  - best single-neighbour ratio  rho(Z) = max_{T in nbrN, rem(T) < 0} |rem(T)| / def'(Z);
  - optimal single-target assignment maximising the minimum residual slack min_T (|rem(T)| - assigned(T)) (exhaustive; groups are tiny);
  - Hall ratio  min over nonempty X of  sum_{T in N(X)} |rem(T)| / sum_X def'.
Output: p1-slack.txt. Runs in < 1 s, one core."""
import json, re, itertools, os
from fractions import Fraction
from collections import defaultdict, Counter
here = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(here, '..', '27-studio-positive-config')
charge = defaultdict(lambda: defaultdict(Fraction))   # (run, name, hole) -> source -> charge
cur = None
for l in open(os.path.join(src, 'jobcb-summary.txt')):
    m = re.match(r'== sx(\S+):', l)
    if m: cur = 's' + m.group(1); continue
    m = re.match(r"\s+rem>0: \('([^']+)', (\d+), (\d+), \{.*'rem': (\d+)\}, \{(.*)\}\)", l)
    if m and cur:
        nm, h, t, rem, srcs = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
        cr = {int(a): int(b) for a, b in re.findall(r'(\d+): (\d+)', srcs)}; tot = sum(cr.values())
        for s, c in cr.items(): charge[(cur, nm, h)][s] += Fraction(rem * c, tot)
out = []; P = out.append
rows = []; C = Counter()
for l in open(os.path.join(src, 'jobs-records.jsonl')):
    r = json.loads(l); js = r['jobs']; key = (r['run'], r['name'], r['hole'])
    tg = {t[0]: dict(Lam=t[1], L=t[2], hit=t[3], nh=t[4], rem=t[6]) for t in js['targets']}
    ch = charge.get(key, {})
    defs = []
    for z in js['pos']:
        dp = z['def'] + ch.get(z['id'], 0)
        nb = [t for t in z['nbrN'] if t in tg and tg[t]['rem'] < 0]
        C['pos'] += 1
        if dp > 0: defs.append((z, dp, nb))
    if not defs: continue
    C['holes_def'] += 1; C['def_cycles'] += len(defs)
    # best single-neighbour ratio per deficit cycle
    for z, dp, nb in defs:
        best = max(nb, key=lambda t: -tg[t]['rem']) if nb else None
        rho = Fraction(-tg[best]['rem']) / dp if best is not None else Fraction(0)
        rows.append(dict(run=r['run'], name=r['name'], hole=r['hole'], pat=r['pattern'], z=z['id'], gamma=z['gamma'], L=z['L'], Lam=z['Lambda'], CrN=z['CrN'],
                         dp=dp, nnb=len(nb), best=best, bestrem=tg[best]['rem'] if best is not None else None, bestnh=tg[best]['nh'] if best is not None else None,
                         bestLam=tg[best]['Lam'] if best is not None else None, rho=rho,
                         rank=sorted([tg[t]['Lam'] for t in tg]).index(tg[best]['Lam']) if best is not None else None))
    # optimal assignment maximising min residual slack over used targets, and over all targets
    cap = {t: Fraction(-tg[t]['rem']) for t in tg if tg[t]['rem'] < 0}
    bestmin = None; bestA = None
    for choice in itertools.product(*[nb for _, _, nb in defs]):
        used = defaultdict(Fraction)
        for (z, dp, nb), t in zip(defs, choice): used[t] += dp
        mn = min(cap[t] - used[t] for t in used)
        if bestmin is None or mn > bestmin: bestmin, bestA = mn, choice
    # minimum over targets used of (cap - assigned) / cap, and shared targets
    shared = sum(1 for t, k in Counter(bestA).items() if k > 1) if bestA else 0
    # Hall ratio
    hall = None
    for k in range(1, len(defs) + 1):
        for X in itertools.combinations(defs, k):
            NX = set(t for _, _, nb in X for t in nb); s = sum(dp for _, dp, _ in X)
            v = sum(cap[t] for t in NX) / s
            if hall is None or v < hall: hall = v
    rows[-1]['hole_minslack'] = bestmin
    for rr in rows[-len(defs):]: rr['hole_minslack'] = bestmin; rr['hall'] = hall; rr['ndef'] = len(defs); rr['shared'] = shared
P('P1 slack on Studio Job S records + charge-back (orders 25-27, both orientations)')
P('positive cycles %d; holes with some def\' > 0: %d; deficit cycles: %d' % (C['pos'], C['holes_def'], C['def_cycles']))
P('')
P('Per-run: #deficit cycles, min best-single-neighbour ratio rho = |rem(T*)|/def\', min Hall ratio, min optimal residual slack')
for run in ['s25', 's25m', 's26', 's26m', 's27', 's27m']:
    R = [x for x in rows if x['run'] == run]
    if not R: continue
    P('  %-5s %3d  rho_min %-8s hall_min %-8s minslack %s' % (run, len(R), str(round(float(min(x['rho'] for x in R)), 3)), str(round(float(min(x['hall'] for x in R)), 3)),
                                                         str(min(x['hole_minslack'] for x in R))))
P('')
P('Holes with more than one deficit cycle: %d; of these, optimal assignment shares a target in %d' % (
    len(set((x['run'], x['name'], x['hole']) for x in rows if x['ndef'] > 1)), len(set((x['run'], x['name'], x['hole']) for x in rows if x['ndef'] > 1 and x['shared']))))
P('')
P('Best neighbour T*: unhit (nh = 0) in %d of %d; T* = most negative cycle among the hole\'s listed targets in %d' % (
    sum(1 for x in rows if x['bestnh'] == 0), len(rows), sum(1 for x in rows if x['rank'] == 0)))
P('Deficit cycles that are Gamma: %d; def\' distribution: %s' % (sum(1 for x in rows if x['gamma']), sorted(Counter(str(x['dp']) for x in rows).items(), key=lambda a: float(Fraction(a[0])))))
P('def\' = Lambda(Z) (no lockless credit at all, after charge-back): %d of %d' % (sum(1 for x in rows if x['dp'] == x['Lam']), len(rows)))
P('rho distribution (floor): %s' % sorted(Counter(min(int(x['rho']), 50) for x in rows).items()))
P('')
P('Tightest 15 deficit cycles by rho (single best neighbour):')
for x in sorted(rows, key=lambda x: x['rho'])[:15]:
    P('  %-5s %-11s h%-2d %s Z%-3d gamma=%d L=%-3d Lam=%-3d CrN=%-3d def\'=%-5s #nb=%d  T*=%d Lam(T*)=%d rem(T*)=%d nh=%d  rho=%.2f  hole minslack=%s hall=%.2f' % (
        x['run'], x['name'], x['hole'], x['pat'], x['z'], x['gamma'], x['L'], x['Lam'], x['CrN'], x['dp'], x['nnb'], x['best'], x['bestLam'], x['bestrem'], x['bestnh'],
        float(x['rho']), x['hole_minslack'], float(x['hall'])))
P('')
P('Tightest 10 holes by optimal residual slack:')
seen = set()
for x in sorted(rows, key=lambda x: x['hole_minslack']):
    k = (x['run'], x['name'], x['hole'])
    if k in seen: continue
    seen.add(k); P('  %-5s %-11s h%-2d ndef=%d minslack=%s hall=%.2f' % (k + (x['ndef'], x['hole_minslack'], float(x['hall']))))
    if len(seen) == 10: break
open(os.path.join(here, 'p1-slack.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
