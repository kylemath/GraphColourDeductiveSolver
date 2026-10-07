#!/usr/bin/env python3
"""[exploratory] NightLemmaR: Lemma R (rem(T) = 5w(T) - sum_hits(1-3f) <= 0 on targets with w <= 0) from Job K records, orders 25-26 and 27.
Flags whether every positive cycle of the hole is a Gamma-cycle (then every DL state is a DD endpoint, so the Job K form = the DD-endpoint form),
and evaluates the capped one-source Lemma S: sum over targets of min(credit into T, max(0, -5w(T))) >= 5w(Z) (single positive cycle holes)."""
import json, sys, os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '27-studio-positive-config')
for lab, fn in (('25-26', 'jobk-records.jsonl'), ('27', 'jobr27/jobk-records.jsonl')):
    tg = nonpos = 0; viol = []; capfail = []; capmin = None
    for l in open(os.path.join(base, fn)):
        r = json.loads(l); allg = all(p['gamma'] for p in r['jobk_pos'])
        for w, L, nh, hs, rem in r['lemmaR']:
            tg += 1
            if w <= 0:
                nonpos += 1
                if rem > 0: viol.append((r['run'], r['name'], r['hole'], r['pattern'], 'w', w, 'L', L, 'hits', nh, 'hitsum', hs, 'rem', rem, 'all sources Gamma', allg))
        if len(r['jobk_pos']) == 1:
            Z = r['jobk_pos'][0]; need = 5 * Z['w']
            cap = sum(min(-hs, max(0, -5 * w)) for w, L, nh, hs, rem in r['lemmaR'])
            raw = sum(-hs for w, L, nh, hs, rem in r['lemmaR'] if w <= 0)
            if raw >= need and cap < need: capfail.append((r['run'], r['name'], r['hole'], need, raw, cap))
            if Z['gamma']: capmin = min(capmin or 9e9, cap / need)
    print('orders %s: targets %d, nonpositive %d, Lemma R violations on nonpositive targets %d' % (lab, tg, nonpos, len(viol)))
    for v in viol: print('   ', v)
    print('   single-positive holes where capping the targets breaks the one-source Lemma S: %d %s; min capped credit / debt on Gamma sources %.3f' % (len(capfail), capfail[:5], capmin))
