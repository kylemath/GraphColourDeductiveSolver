#!/usr/bin/env python3
"""Job BB (2) summary: one-period Phi test from out/bb{25,26,27}{,m}.jsonl (picyc.bb --jobbb). Per candidate, per (open run / Gamma) and (break / no break):
pairs available, #(Phi(u0) >= Phi(u10)) = failures of the strict form 'B => Phi(u0) < Phi(u10)', #(Phi(u0) > Phi(u10)) = failures of the <= form."""
import json, sys
from collections import Counter
NAMES = ['|K_pm(p)| at R3k4', 'Lock2 witness at R3k4'] + ['|K_%d| (step %d component)' % (i, i) for i in range(10)]
tot = [[[0] * 12 for _ in range(4)] for _ in range(3)]; P = Counter(); special = []
for o in (25, 26, 27):
    for suf in ('', 'm'):
        for l in open('../out/bb%d%s.jsonl' % (o, suf)):
            if '"jobbb"' not in l: continue
            r = json.loads(l); b = r['jobbb']
            P['pairs open'] += b['pairs'][0]; P['pairs Gamma'] += b['pairs'][1]; P['breaks open'] += b['breaks'][0]; P['breaks Gamma'] += b['breaks'][1]
            P['B != not-J(u9) open'] += b['J_mismatch'][0]; P['B != not-J(u9) Gamma'] += b['J_mismatch'][1]
            for k in range(12):
                v = b['cand'][k]
                for gi in range(4):
                    for t in range(3): tot[t][gi][k] += v[3 * gi + t]
            if r['name'] == 'p25#16945' and r['hole'] == 3 and suf == 'm': special.append(b)
print('pairs (R3k4 u0 with u0..u10 DL):', dict(P))
lab = ['open, no break', 'open, BREAK', 'Gamma, no break', 'Gamma, BREAK']
print('%-30s | %-34s | %-34s | %s' % ('candidate Phi', 'open runs with a break: n / fail< / fail<=', 'Gamma with a break: n / fail< / fail<=', 'no-break pairs with Phi0<Phi10 (open, Gamma)'))
for k in range(12):
    n1, s1, l1 = tot[0][1][k], tot[1][1][k], tot[2][1][k]; n3, s3, l3 = tot[0][3][k], tot[1][3][k], tot[2][3][k]
    nb_open = tot[0][0][k] - tot[1][0][k]; nb_g = tot[0][2][k] - tot[1][2][k]
    print('%-30s | %8d %8d %8d %8s | %8d %8d %8d %8s | %d/%d, %d/%d' % (NAMES[k], n1, s1, l1, '', n3, s3, l3, '', nb_open, tot[0][0][k], nb_g, tot[0][2][k]))
print('p25#16945 mirror h3 (separately):', special)
