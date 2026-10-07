#!/usr/bin/env python3
"""Job BQ summary from out/bq{adv,c25,c26,c27}{,m}.jsonl (picyc.bq --jobbq): B' slack = 2 N0 + E2 + 3 tau - 2 |R_rho| per sigma u sigma' group."""
import json
from collections import Counter, defaultdict
BIG = 1 << 39
for group, tags in (('census orders 25-27', ['c25', 'c26', 'c27']), ('adversarial (61 AW hits, AS, AQ)', ['adv'])):
    T = Counter(); mnpos = defaultdict(lambda: (BIG, None)); mnall = defaultdict(lambda: (BIG, None)); hist = Counter()
    for t in tags:
        for suf in ('', 'm'):
            for l in open('../out/bq%s%s.jsonl' % (t, suf)):
                if '"jobbq"' not in l: continue
                r = json.loads(l); b = r['jobbq']; p = r['pattern']; ex = (r['name'], r['hole'], suf or 'plantri')
                T['holes'] += 1; T['groups'] += b['groups']; T['negative groups'] += b['neg']; T['holes with a negative group'] += b['neg'] > 0; T['identity fails'] += b['identity_fail']
                if b['min_slack_posgroups'] < mnpos[p][0]: mnpos[p] = (b['min_slack_posgroups'], ex)
                if b['min_slack'] < mnall[p][0]: mnall[p] = (b['min_slack'], ex)
                for k, v in b['hist'].items(): hist[int(k)] += v
    print('=' * 20, group, dict(T))
    ps = sorted(mnpos, key=lambda p: mnpos[p][0]); g = min((mnpos[p] for p in mnpos), key=lambda x: x[0]) if mnpos else None
    print("  HEADLINE 1: min B' slack over groups CONTAINING a positive cycle:", g)
    print("  HEADLINE 2: min B' slack over all groups (incl. Sigma-lambda = 0 / no-positive):", min(mnall.values(), key=lambda x: x[0]))
    print('  min slack over positive-containing groups, by pattern (lowest 15):', [(p, mnpos[p][0]) for p in ps[:15]])
    print('  min slack over all groups, by pattern (negative only):', {p: v[0] for p, v in mnall.items() if v[0] < 0})
    print('  slack histogram (buckets -1 = negative, 0..9, 10 = 10..99, 100 = >= 100):', dict(sorted(hist.items())))
