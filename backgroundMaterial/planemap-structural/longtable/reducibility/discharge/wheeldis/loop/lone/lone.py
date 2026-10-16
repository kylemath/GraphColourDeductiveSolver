"""EXPLORE round 7 (exploratory): the 'lone fives' family.  A five is lone at a receiver u if u is its only neighbour of
degree >= 7.  At t = 0 a receiver of degree d with more than d - 6 lone fives is a positive cluster that no rule moving
charge from a 5 to its big neighbours can discharge, so every such arrangement must contain a forbidden (reducible)
pattern.  This asks bin/sep3 (wlp3's receiver oracle, same patterns as wlp3: pat=, cpat=, w7plus) for the arrangements
with the most lone fives that contain no forbidden pattern.
Usage: python3 loop/lone/lone.py d=7,8,9,10,11,12 many=50 out=FILE [pat=FILE ...] [cpat=FILE ...] [w7plus]
Prints per d the max number of lone fives over pattern-free arrangements and lists those with > d - 6."""
import sys, os
W3 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lp', 'wlp3s.py')
opt = {a.split('=', 1)[0]: a.split('=', 1)[1] for a in sys.argv[1:] if a.split('=', 1)[0] in ('d', 'many', 'out')}
DL = [int(x) for x in opt.get('d', '7,8,9,10,11,12').split(',')]; MANY = int(opt.get('many', '50')); OUTF = opt.get('out')
rest = [a for a in sys.argv[1:] if a.split('=', 1)[0] not in ('d', 'many', 'out')]
sys.argv = [W3, 'tag=lone'] + rest; __file__ = W3
src = open(W3).read(); exec(src[:src.index('A_ub, b_ub = []')])
yv = np.array([1.0 if all(x <= 6 for x in r[1:]) else 0.0 for r in roots])
out = []
for d in DL:
    res, nodes = sep(d, yv, d - 6 + 0.5, MANY)
    best = sep(d, yv, -1.0, 1)[0]
    mx = best[0][0] if best else 0
    out.append('d=%d: max lone fives in a pattern-free arrangement = %g (limit d-6 = %d); %d listed with > %d' % (d, mx, d - 6, len(res), d - 6))
    for v, lk, sv, p in res: out.append('  %g receiver d=%d link %s s %s' % (v, d, lk, sv))
print('\n'.join(out))
if OUTF: open(OUTF, 'w').write('\n'.join(out) + '\n')
SEP.stdin.close(); SEP.wait()
