#!/usr/bin/env python3
import json, glob, sys
from collections import defaultdict
def canon(d):
    d = [min(x, 8) for x in d]; c = []
    for s in (d, d[::-1]):
        for i in range(5): c.append(tuple(s[i:]+s[:i]))
    return min(c)
cap = int(sys.argv[1]) if len(sys.argv) > 1 else 8
P = defaultdict(lambda: dict(holes=0, classes=0, pos=0, dl=0, alldl=0, minfrac=9, maxsw=-10**9, minsw=10**9, orders=set(), maxsw_frac=None))
for fn in sorted(glob.glob('out-*.jsonl')):
    for line in open(fn):
        r = json.loads(line); key = canon([min(x, cap) for x in r['deg']]); p = P[key]
        p['holes'] += 1; p['orders'].add(r['n'])
        for c in r['classes']:
            p['classes'] += 1; p['pos'] += c['npos'] > 0; p['dl'] += c['dl']; p['alldl'] += c['alldl']
            p['minfrac'] = min(p['minfrac'], c['F']/c['size']); p['maxsw'] = max(p['maxsw'], c['sw']); p['minsw'] = min(p['minsw'], c['sw'])
TC = sum(p['classes'] for p in P.values()); TP = sum(p['pos'] for p in P.values()); rate = TP/TC
print('global: classes %d positive classes %d rate %.3e; holes %d; patterns %d; max sum-winding over ALL classes %d' % (TC, TP, rate, sum(p['holes'] for p in P.values()), len(P), max(p['maxsw'] for p in P.values())))
rows = sorted(P.items(), key=lambda kv: -(kv[1]['classes']*rate - kv[1]['pos']))
print('pattern | holes | classes | posclasses | exp | exp-obs | DL states | allDL cycles | min filled frac | max sum-w | min sum-w | orders')
for k, p in rows:
    e = p['classes']*rate
    print('%s | %d | %d | %d | %.2f | %.2f | %d | %d | %.4f | %d | %d | %d-%d' % (''.join(map(str, k)), p['holes'], p['classes'], p['pos'], e, e-p['pos'], p['dl'], p['alldl'], p['minfrac'], p['maxsw'], p['minsw'], min(p['orders']), max(p['orders'])))
