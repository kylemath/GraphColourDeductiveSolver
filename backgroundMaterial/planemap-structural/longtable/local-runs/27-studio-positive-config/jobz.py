#!/usr/bin/env python3
"""Job Z: Lemma S with sigma-exits from EVERY DD-endpoint state (R1, R2, R3 and unclassified), all patterns, Gamma-cycles; credit 3f - 1; CrN = targets w <= 0.
Per pattern: Gamma records, min CrN/D (D = Lambda), cycles with CrN < D, share of CrN from non-R3 exits; also positive non-Gamma cycles."""
import json, sys
from collections import defaultdict
def canon(ld, cap=8):
    d = [min(x, cap) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
def pat(t): return ','.join(('%d' % x) if x < 8 else '8+' for x in t)
for lab in sys.argv[1:]:
    P = defaultdict(lambda: {'n': 0, 'min': None, 'fail': [], 'crN': 0, 'crNo': 0, 'nG': 0, 'nfailNG': 0})
    for l in open('out/%s.jsonl' % lab):
        if '"jobs": {"pos": [{' not in l: continue
        r = json.loads(l); p = pat(canon(r['linkdeg']))
        for z in r['jobs']['pos']:
            e = P[(p, z['gamma'])]; e['n'] += 1; e['crN'] += z['CrN']; e['crNo'] += z['CrN_nonR3']; ratio = z['CrN'] / z['Lambda']
            if e['min'] is None or ratio < e['min'][0]: e['min'] = (round(ratio, 3), r['name'], r['hole'], z['L'], z['Lambda'], z['CrN'], z['CrN_nonR3'], z['CrP'])
            if z['CrN'] < z['Lambda']: e['fail'].append((r['name'], r['hole'], z['L'], z['Lambda'], z['CrN'], z['CrN_nonR3'], z['CrP']))
    print('== %s' % lab)
    for (p, g), e in sorted(P.items(), key=lambda kv: (not kv[0][1], -kv[1]['n'])):
        if not g and not e['fail']: continue
        print('   %-12s %-9s records %4d  min CrN/D %s  CrN<D in %d  non-R3 share of CrN %.1f%%  first fails %s'
              % (p, 'Gamma' if g else 'nonGamma', e['n'], e['min'], len(e['fail']), 100.0 * e['crNo'] / max(1, e['crN']), e['fail'][:2] if g else ''))
