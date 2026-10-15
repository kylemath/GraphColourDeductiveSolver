"""Summarise dfast verdicts on the equal-split overload configurations (pairs2.py) by demand type and ring."""
import os, collections, glob
HERE = os.path.dirname(os.path.abspath(__file__))
dem = {}
for fn in glob.glob(os.path.join(HERE, 'eq_D7_k*.dem')):
    for line in open(fn):
        if line.strip(): nm, t = line.split(); dem[nm] = t
C = collections.Counter(); R = collections.Counter(); ex = {}
for line in open(os.path.join(HERE, 'out', 'eq_D7_dfast.out')):
    f = line.split(); nm = f[0]; r = int(f[1][2:]); v = 'D' if 'D=true' in line else 'notD'
    C[(dem[nm], v)] += 1; R[(r, v)] += 1
    if v == 'notD' and dem[nm] not in ex: ex[dem[nm]] = nm + ' r=%d' % r
out = ['# equal-split overload configurations at a 7 (k = 2 all, k = 3 ring <= 14), dfast',
       'by demand type: ' + str(dict(sorted(C.items()))), 'by ring: ' + str(dict(sorted(R.items()))),
       'one notD example per type:'] + ['  %s  %s' % kv for kv in sorted(ex.items())]
print('\n'.join(out)); open(os.path.join(HERE, 'out', 'eq_D7_summary.txt'), 'w').write('\n'.join(out) + '\n')
