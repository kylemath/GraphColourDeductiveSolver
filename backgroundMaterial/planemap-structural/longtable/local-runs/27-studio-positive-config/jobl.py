#!/usr/bin/env python3
"""jobl.py: Job L from jobi-cycles.jsonl (per-exit keys) and jobk-records.jsonl (sigma-hop counts). Debt D = 5w; credit C = sum (3f - 1) over lockless exits,
split by target winding (C_neg: w(T) <= 0, C_pos: w(T) > 0); per k (kmask) counts of R3 states and lockless exits."""
import json, re
from collections import defaultdict, Counter
hops = defaultdict(list)
for l in open('jobk-records.jsonl'):
    r = json.loads(l); run = r['run'].replace('k', 'i')
    for p in r['jobk_pos']: hops[(run, r['name'], r['hole'], p['L'], p['w'])].append(p['sigma_chain_to_negative'])
rows = []
for l in open('jobi-cycles.jsonl'):
    r = json.loads(l)
    for g in r['jobg']:
        D = 5 * g['w']; C = Cn = Cp = 0; perk = defaultdict(lambda: [0, 0])
        for key, v in g['exits'].items():
            m = re.match(r'(lockless|onelock|DL|filled)_k(\d+)', key); kind, km = m.group(1), int(m.group(2)); perk[km][0] += v
            if kind == 'lockless':
                perk[km][1] += v; f = int(re.search(r'_f(\d+)', key).group(1)); wT = int(re.search(r'_wT(-?\d+)', key).group(1)); c = (3 * f - 1) * v
                C += c; Cn += c if wT <= 0 else 0; Cp += c if wT > 0 else 0
        h = hops.get((r['run'], r['name'], r['hole'], g['L'], g['w']), [None])
        rows.append(dict(run=r['run'], name=r['name'], hole=r['hole'], pattern=r['pattern'], linkdeg=r['linkdeg'], gamma=g['gamma'], L=g['L'], w=g['w'], D=D, C=C, C_neg=Cn, C_pos=Cp,
                         perk={str(k): v for k, v in sorted(perk.items())}, hop=h[0]))
json.dump(rows, open('jobl-cycles.json', 'w'), indent=0)
for pat in ['5,5,5,5,6', '5,5,5,6,6']:
    for gam in [True, False]:
        R = [x for x in rows if x['pattern'] == pat and x['gamma'] == gam]
        if not R: continue
        mn = min(R, key=lambda x: x['C_neg'] / x['D']); mc = min(R, key=lambda x: x['C'] / x['D'])
        fails = [x for x in R if x['C_neg'] < x['D']]
        print('== %s %s: cycles %d; min C_neg/D %.3f at %s %s h%d (L %d, D %d, C_neg %d, C %d); min C/D %.3f at %s %s h%d; C_neg < D in %d; C < D in %d; C_pos > 0 in %d'
              % (pat, 'Gamma' if gam else 'nonGamma positive', len(R), mn['C_neg'] / mn['D'], mn['run'], mn['name'], mn['hole'], mn['L'], mn['D'], mn['C_neg'], mn['C'],
                 mc['C'] / mc['D'], mc['run'], mc['name'], mc['hole'], len(fails), sum(1 for x in R if x['C'] < x['D']), sum(1 for x in R if x['C_pos'] > 0)))
        for x in fails[:4]: print('   C_neg < D:', x['run'], x['name'], 'h', x['hole'], x['linkdeg'], 'L', x['L'], 'D', x['D'], 'C_neg', x['C_neg'], 'C_pos', x['C_pos'], 'perk [R3, lockless]', x['perk'], 'hop', x['hop'])
        if not gam: print('   sigma-hops to a negative cycle:', dict(Counter(x['hop'] for x in R)), '; C_neg/D distribution:', sorted(round(x['C_neg'] / x['D'], 2) for x in R))
