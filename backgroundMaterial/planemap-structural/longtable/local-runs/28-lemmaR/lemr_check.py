#!/usr/bin/env python3
"""[exploratory] NightLemmaR: Lemma R on the excursion-level output of picyc.lemr (gentri orders 17-24, both orientations, every
degree-5 hole with a positive pi-cycle, every link pattern). Forms: K = hits from DL R3 states of positive cycles (Job K);
D = hits from DL R3 states that are DD-step endpoints (NightF6Flow); A = hits from any DL DD-step endpoint (any R-type).
Checks: hit excursions have u = 1 and at most one hit each (no double counting); rem = sum over free excursions of (u - 3f);
Lemma R on targets with w <= 0; targets with a positive excursion (u > 3f); capped single-source credit."""
import json, sys, glob, os
from collections import Counter
here = os.path.dirname(os.path.abspath(__file__))
forms = {'K': lambda c: (c >> 3) == 3, 'D': lambda c: (c >> 3) == 3 and (c >> 2) & 1, 'A': lambda c: (c >> 2) & 1}
st = {f: Counter() for f in forms}; viol = {f: [] for f in forms}; bad = Counter(); prev = Counter(); posexc_free = Counter()
for fn in sorted(glob.glob(os.path.join(here, 'out*.jsonl'))):
    run = os.path.basename(fn)[3:-6]
    for l in open(fn):
        if '"lemr": [{' not in l: continue
        d = json.loads(l)
        for T in d['lemr']:
            w, exc = T['w'], T['exc']
            if not exc or sum(u - 3 * f for u, f, h in exc) != 5 * w: bad['identity'] += 1
            for i, (u, f, h) in enumerate(exc):
                if h and u != 1: bad['hit with u != 1'] += 1
                if len(h) > 1: bad['two sources on one excursion'] += 1
            for fo, sel in forms.items():
                hit = [any(sel(c) and not (c >> 1) & 1 for c in h) for u, f, h in exc]
                if not any(hit): continue
                s = st[fo]; s['targets'] += 1
                if w > 0: s['positive targets'] += 1; continue
                s['nonpositive targets'] += 1
                rem = sum(u - 3 * f for (u, f, h), x in zip(exc, hit) if not x)
                pos = [(u, f) for (u, f, h), x in zip(exc, hit) if not x and u > 3 * f]
                if pos: s['nonpositive targets with a positive free excursion'] += 1
                if rem == 0: s['rem = 0'] += 1
                if rem > 0:
                    viol[fo].append((run, d['name'], d['hole'], d['linkdeg'], 'w', w, 'L', T['L'], 'rem', rem, 'exc', [(u, f, int(x)) for (u, f, h), x in zip(exc, hit)]))
                if fo == 'D':
                    n = len(exc)
                    for i, x in enumerate(hit):
                        if x: pu, pf, ph = exc[i - 1]; prev[('prev exc hit' if hit[i - 1] else 'prev exc free', 'prev u', pu if pu < 4 else '>=4')] += 1
                    for u, f in pos: posexc_free[(u, f)] += 1
for k, v in bad.items(): print('BAD', k, v)
print('consistency failures:', sum(bad.values()))
for fo in forms:
    print('form %s:' % fo, dict(st[fo]), 'violations on nonpositive targets:', len(viol[fo]))
    for v in viol[fo][:6]: print('   ', v)
print('form D, excursion before a hit excursion:', sorted(prev.items(), key=str))
print('form D, positive free excursions (u, f) in nonpositive targets:', sorted(posexc_free.items()))
