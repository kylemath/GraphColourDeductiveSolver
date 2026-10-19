"""Write the common registry snapshot (Studio run A's patterns + twoeng k3x + k42map windows) as slot-mask patterns
for sepb: one line per pattern 'd n slot mask ...' (slot w_i = i, s_i = d + i; mask bit k = letter 5 + k), and the
RBIG 7-words (w7plus).  Uses wlp3.py's own loader (parse / fullparse), read-only."""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = HERE
WD = os.path.abspath(os.path.join(HERE, '../../..'))
os.environ['WLP_SEPF'] = '1'
args = open(os.path.join(WD, 'out/job28/j28_13.args')).read().split()
args += ['pat=loop/n9/win%s.out' % k for k in ('9', '25', '25b', '27', '29', '31')]
args += ['pat=out/job30/addA_dfast18.out', 'pat=out/job30/k3x_D.out', 'cpat=out/job30/k3x_C.cfast',
         'pat=loop/studio/k42map/k42map_D.out', 'cpat=loop/studio/k42map/k42map_C.cfast']
K43 = 'k43' in sys.argv[1:]   # also the round-43 batch after round 44's drop (366 windows, Team B two-engine b4_k43)
if K43:
    args += ['pat=loop/teamB/b3_pfh/k43/k43_366_kc.out', 'cpat=loop/teamB/b3_pfh/k43/k43_366_kc.out']
SUF = '_k43' if K43 else ''
missing = [a for a in args if a.startswith(('pat=', 'cpat=')) and not os.path.exists(os.path.join(WD, a.split('=', 1)[1]))]
print('missing files (skipped):', missing)
args = [a for a in args if a not in missing]
sys.argv = ['wlp3'] + args
src = open(os.path.join(WD, 'wlp3.py')).read()
__file__ = os.path.join(WD, 'wlp3.py')
cut = src.index("print('patterns:'")
os.chdir(WD)
exec(src[:cut])
print('patterns:', dict(PSRC))
LI = {5: 0, 6: 1, 7: 2, 8: 3, 9: 4}
out = []
for d, P in PATS:
    sm = {}
    ok = True
    for i, m in P:
        slots = [(i, 1), ((i + 1) % d, (m >> 0) & 31), (d + i, (m >> 5) & 31), (d + (i - 1) % d, (m >> 10) & 31),
                 ((i - 1) % d, (m >> 15) & 31)]
        for sl, mm in slots:
            sm[sl] = sm.get(sl, 31) & mm
            if sm[sl] == 0:
                ok = False
    if ok:
        out.append((d, sorted(sm.items())))
for d, F in FULLP:
    sm = {}
    for sl, mm in F:
        sm[sl] = sm.get(sl, 31) & mm
    out.append((d, sorted(sm.items())))
with open(os.path.join(OUTD, 'reg_patterns%s.txt' % SUF), 'w') as fo:
    for d, sm in out:
        fo.write('%d %d %s\n' % (d, len(sm), ' '.join('%d %d' % x for x in sm)))
import itertools
RB7 = {canon(tuple(map(int, x))) for x in RBIG if len(x) == 7}
print('RBIG 7-words', len(RB7))
with open(os.path.join(OUTD, 'rbig7%s.txt' % SUF), 'w') as fo:
    for wd in itertools.product((5, 6, 7, 8, 9), repeat=7):
        if canon(wd) in RB7:
            fo.write(''.join(map(str, wd)) + '\n')
from collections import Counter
print('written', len(out), 'patterns by d', Counter(d for d, _ in out))
