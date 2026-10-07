#!/usr/bin/env python3
"""Job BC summary from out/bc{25,26,27}{,m}.jsonl and out/bcx{,m}.jsonl (picyc.bc --jobbc histograms)."""
import json
from collections import Counter
H = Counter(); D = Counter()
for f in ['bc%d%s' % (o, s) for o in (25, 26, 27) for s in ('', 'm')] + ['bcx', 'bcxm']:
    src = 'cons/adv' if f.startswith('bcx') else 'census'
    for l in open('../out/%s.jsonl' % f):
        if '"jobbc"' not in l: continue
        r = json.loads(l); b = r['jobbc']; D['dual checked'] += b['dual_checked']; D['dual fail'] += b['dual_fail']; D['name fail'] += b['name_fail']
        for k, v in b['hist'].items(): H[(src,) + tuple(k.split(' ', 4))] += v
print('(iv) pair dualities checked at every window state:', dict(D))
EV = ['s3 C12 merge', 's4 C12 split', 's5 C13 merge', 's6 C13 split', 's7 C14 merge', 's8 C14 split']
for kind in ('G6', 'G7', 'O6', 'O7'):
    for src in ('census', 'cons/adv'):
        rows = [(k, v) for k, v in H.items() if k[0] == src and k[1] == kind]
        if not rows: continue
        n = sum(v for _, v in rows); ne = Counter(); miss5 = Counter(); w2 = Counter(); w2s = Counter(); evf = Counter()
        for k, v in rows:
            ev = k[2][2:]; F = k[4]; e = ev.count('1'); ne[e] += v
            for i in range(6):
                if ev[i] == '1': evf[EV[i]] += v
            if e == 5: miss5[EV[ev.index('0')]] += v
            if F == 'FFF': w2[ev] += v
            if F[0] == 'F' and F[2] == 'F': w2s[ev] += v
        print('== %s %s windows (positions 3..9 all DL): %d' % ({'G': 'Gamma', 'O': 'open'}[kind[0]] + ' degree ' + kind[1], src, n, ) if False else '== %s degree %s, %s: %d windows' % ({'G': 'Gamma', 'O': 'open-run'}[kind[0]], kind[1], src, n))
        print('    (i) number of events achieved:', dict(sorted(ne.items())))
        print('        per event:', dict(evf))
        print('    (ii) windows with 5 of 6 events, the missing event:', dict(miss5))
        print('    (iii) W2 failures (4, 6, 8 all fixed): %d, event patterns %s' % (sum(w2.values()), dict(w2)))
        print('          W2* failures (4 and 8 fixed): %d, event patterns %s' % (sum(w2s.values()), dict(w2s)))
