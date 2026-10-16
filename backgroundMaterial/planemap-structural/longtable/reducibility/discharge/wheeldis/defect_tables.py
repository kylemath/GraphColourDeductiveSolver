"""Write bin/defect_tables.txt for bin/defectc (README §7, test G): for every word over {5,6,7} read in cyclic order,
bad5[w] (5-wheel in R_opt), bad6[w] (6-wheel in R_opt, incl. the six 565xxx C-candidates), d7[w] (7-wheel tested D),
t7[w] (7-wheel tested at all).  Usage: python3 defect_tables.py"""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'defect.py')).read().replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = %r' % HERE)
sys.argv = ['defect.py', '5', '1', '1', '/dev/null', 'strict7']
exec(src[:src.index("CENTRE, K, CMIN, OUT")])
print('C-candidate 7-wheels:', len(C7), 'C-tested negative:', len(NC7))
lines = []
for n, f in ((5, lambda w: isR5(w)), (6, lambda w: bad6(w)), (7, lambda w: canon(w) in D7), (7, lambda w: canon(w) in T7)):
    lines.append(' '.join('1' if f(list(w)) else '0' for w in itertools.product((5, 6, 7), repeat=n)))
os.makedirs(os.path.join(HERE, 'bin'), exist_ok=True)
open(os.path.join(HERE, 'bin', 'defect_tables.txt'), 'w').write('\n'.join(lines) + '\n')
print([l.count('1') for l in lines])
