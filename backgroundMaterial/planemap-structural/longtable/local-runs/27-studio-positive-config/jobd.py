#!/usr/bin/env python3
"""jobd.py LABEL=FILE ...: per-class orientation check and Job D (Theorem F5 identity and bounds by link pattern).
Per class sig [size, F, sum w, DD, N0, E2, tau]. Bounds: B1 = 2N0 - DD, B2 = 2N0 + E2 - DD, B3 = 2N0 + 3tau - DD, B4 = 2N0 + E2 + 3tau - DD (= -sum lambda)."""
import sys, json
from collections import defaultdict, Counter
def canon(ld, cap=8):
    d = [min(x, cap) for x in ld]; return min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))
def pat(t): return ','.join(('%d' % x) if x < 8 else '8+' for x in t)
NB = ['2N0-DD', '2N0+E2-DD', '2N0+3tau-DD', '2N0+E2+3tau-DD']
sigs = {}; tot = Counter(); P = defaultdict(lambda: {'n': 0, 'holes': 0, 'min': [None] * 4, 'argmin': [None] * 4, 'fail': [0] * 4, 'first': [None] * 4})
for a in sys.argv[1:]:
    lab, f = a.split('=')
    for l in open(f):
        r = json.loads(l)
        if r['kind'] != 'hole' or 'clsig' not in r: continue
        tot['holes'] += 1; tot['classes'] += len(r['clsig']); tot['cls_bad'] += r['cls_bad']; tot['cyc_split'] += r['cyc_split']; tot['f5_bad'] += r['f5_bad']
        key = (r['name'], r['hole']); sigs.setdefault(key, {})[lab] = sorted(tuple(c[:3]) for c in r['clsig'])
        k = canon(r['linkdeg']); e = P[k]; e['holes'] += 1
        for c in r['clsig']:
            sz, F, w, DD, N0, E2, tau = c; e['n'] += 1
            # identity: sum lambda = 5w = DD - 2N0 - E2 - 3tau
            if 5 * w != DD - 2 * N0 - E2 - 3 * tau: tot['identity_bad'] += 1
            B = [2 * N0 - DD, 2 * N0 + E2 - DD, 2 * N0 + 3 * tau - DD, 2 * N0 + E2 + 3 * tau - DD]
            for i in range(4):
                if e['min'][i] is None or B[i] < e['min'][i]: e['min'][i] = B[i]; e['argmin'][i] = (lab, r['name'], r['hole'], c)
                if B[i] < 0:
                    e['fail'][i] += 1
                    if e['first'][i] is None: e['first'][i] = (lab, r['name'], r['hole'], 'class [size,F,w,DD,N0,E2,tau]=%s' % c)
print('=== totals', dict(tot))
# orientation check: same hole, both orientations (labels X and Xm)
mm = 0; nchk = 0
for key, d in sigs.items():
    labs = sorted(d)
    for x in labs:
        if x + 'm' in d:
            nchk += 1
            if d[x] != d[x + 'm']: mm += 1; print('ORIENTATION MISMATCH', key, x) if mm <= 5 else None
print('=== per-class orientation check: holes compared %d, mismatches in (size, F, sum w) class multisets %d' % (nchk, mm))
print('=== Job D: min over classes of each bound, by link pattern (classes counted over both orientations); "fail" = classes with the bound < 0')
print('%-12s %7s %8s | %s' % ('pattern', 'holes', 'classes', ' | '.join('%-22s' % b for b in NB)))
for k, e in sorted(P.items(), key=lambda kv: -kv[1]['n']):
    print('%-12s %7d %8d | %s  %s' % (pat(k), e['holes'], e['n'], ' | '.join('min %6d fail %6d' % (e['min'][i], e['fail'][i]) for i in range(4)),
          'type: ' + ('F5 (2N0 suffices)' if e['min'][0] >= 0 else 'F6 (2N0+3tau suffices)' if e['min'][2] >= 0 else '2N0+E2+3tau needed' if e['min'][3] >= 0 else 'FLOOR FAILS')))
print('\n=== first failing class per pattern and bound')
for k, e in sorted(P.items(), key=lambda kv: -kv[1]['n']):
    for i in range(3):
        if e['first'][i]: print('%-12s %-14s first fail %s ; min at %s' % (pat(k), NB[i], e['first'][i], e['argmin'][i]))
