#!/usr/bin/env python3
"""Lemma W (Job X addendum) from out/w*.jsonl: windows R3k3, R3k2, R3k1, R3k0, R3k4' inside DL runs at (5,5,5,5,6): credit >= 10, W1 (k3 or k4' lockless),
W2 (some k <= 2 lockless), W4 (k4' fails => k3 lockless with f = 3); Gamma-cycles vs non-closed runs; distance from a failing window to the run end."""
import json, sys
from collections import Counter
for lab in sys.argv[1:]:
    nw = [0, 0]; wf = {'run': [0] * 4, 'gamma': [0] * 4}; bad = 0; ex = []; dist = Counter()
    for l in open('out/%s.jsonl' % lab):
        if '"jobx": {' not in l: continue
        r = json.loads(l); jx = r['jobx']; nw[0] += jx['windows'][0]; nw[1] += jx['windows'][1]; bad += jx['windows_malformed']
        for i in range(4): wf['run'][i] += jx['wfail_run'][i]; wf['gamma'][i] += jx['wfail_gamma'][i]
        for e in jx['wfail_examples']:
            ex.append((r['name'], r['hole'], e))
            if not e['W1']: dist[('W1', 'gamma' if e['gamma'] else e['dist_to_run_end'])] += 1
            if e['credit'] < 10: dist[('credit<10', 'gamma' if e['gamma'] else e['dist_to_run_end'])] += 1
    print('== %s: windows on non-closed runs %d, on Gamma-cycles %d (malformed %d)' % (lab, nw[0], nw[1], bad))
    print('   failures [credit<10, not W1, not W2, not W4]: runs %s, Gamma %s' % (wf['run'], wf['gamma']))
    print('   distance to run end of failing windows:', sorted(dist.items(), key=str)[:20])
    g = [x for x in ex if x[2]['gamma']]; print('   first failing windows on Gamma-cycles:', g[:3]); print('   first failing on runs:', [x for x in ex if not x[2]['gamma']][:2])
