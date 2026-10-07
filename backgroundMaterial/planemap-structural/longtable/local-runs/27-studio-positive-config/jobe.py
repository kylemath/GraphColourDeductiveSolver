#!/usr/bin/env python3
"""jobe.py LABEL=FILE ...: Job E summary (C1-Gamma and sigma-C at (5,5,5,5,6) and (5,5,5,6,6) holes)."""
import sys, json
from collections import Counter, defaultdict
S = defaultdict(Counter); firstG = {}; firstS = {}; tk = defaultdict(Counter)
for a in sys.argv[1:]:
    lab, f = a.split('=')
    for l in open(f):
        r = json.loads(l)
        if r['kind'] != 'hole' or 'pattern' not in r: continue
        p = r['pattern']; s = S[(lab, p)]; s['holes'] += 1; s['poshole'] += r['npos'] > 0
        sc = r['sigC']; s['comps'] += sc['ncomp']; s['sigC_fail_comps'] += sc['fail']; s['sigC_fail_holes'] += sc['fail'] > 0
        s['max_comp_cycles'] = max(s['max_comp_cycles'], sc['max_ncycles'])
        if sc['fail'] and (lab, p) not in firstS: firstS[(lab, p)] = (r['name'], r['hole'], r['linkdeg'], sc)
        if r['npos']: s['poshole_sigC_ok'] += sc['fail'] == 0
        for g in r['gamma']:
            s['gamma'] += 1; s['gammaholes_'] += 0; s['r3'] += g['R3']; s['r3ok'] += g['r3_sigma_lockless']; s['r3same'] += g['r3_sigma_same_cycle']; s['other_type'] += g['other']; s['R2'] += g['R2']
            s['gammaL%d' % g['L']] += 1
            for t, km, c in g['type_kmask']: tk[(lab, p)][(t, km)] += c
            if g['first_r3_fail'] and (lab, p) not in firstG: firstG[(lab, p)] = (r['name'], r['hole'], r['linkdeg'], g['L'], g['w'], g['first_r3_fail'])
        s['gammaholes'] += 1 if r['gamma'] else 0
for k in sorted(S):
    s = S[k]
    print(k[0], k[1], 'holes', s['holes'], 'positive holes', s['poshole'], '| sigC: components', s['comps'], 'failing comps', s['sigC_fail_comps'], 'failing holes', s['sigC_fail_holes'], 'max cycles/comp', s['max_comp_cycles'])
    print('    Gamma-cycles', s['gamma'], 'at', s['gammaholes'], 'holes; lengths', sorted((int(x[6:]), v) for x, v in s.items() if x.startswith('gammaL')),
          '| R3 states', s['r3'], 'sigma lockless', s['r3ok'], 'C1Gamma failures', s['r3'] - s['r3ok'], '| sigma lands on same cycle', s['r3same'], '| R2', s['R2'], 'other-type', s['other_type'])
    if k in firstG: print('    FIRST C1Gamma FAILURE', firstG[k])
    if k in firstS: print('    FIRST sigC FAILURE', firstS[k])
    print('    (type, kmask) counts on Gamma-cycles:', sorted(tk[k].items()))
