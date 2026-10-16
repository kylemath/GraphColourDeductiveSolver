"""G9 probe 2 (exploratory): tables for loop/g9/defectc9 over the alphabet {5,6,7,8,9}, 9 = the centre letter (degree
>= 9; only the centre has it).  As defect_tables8.py; a word with a 9 is reducible only where a rule with a free vertex
covers it (5-wheel: a D fan with F at that position; 6-wheel: 2.122); 7-/8-wheels with a 9 were never tested -> not
reducible.  Index base 5 (digit = letter - 5).  Line order: bad5 bad6 d7 t7 d8 t8.  Usage: python3 defect_tables9.py OUT"""
import sys, os, itertools, collections
WD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUTF = sys.argv[1]
src = open(os.path.join(WD, 'defect.py')).read().replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = %r' % WD)
sys.argv = ['defect.py', '5', '1', '1', '/dev/null', 'strict7']
exec(src[:src.index("CENTRE, K, CMIN, OUT")])
D8 = set(); T8 = set()
for fn in ('bigwheels_dfast.out', 'bigwheels1516_dfast_partial.out'):
    for line in open(os.path.join(WD, 'out', fn)):
        f = line.split()
        if not f or not f[0].startswith('c8_') or ('D=true' not in line and 'D=false' not in line): continue
        w = tuple(map(int, f[0][3:])); T8.add(w)
        if 'D=true' in line: D8.add(w)
A = (5, 6, 7, 8, 9)
fam = ((5, lambda w: isR5(w)), (6, lambda w: bad6(w)), (7, lambda w: canon(w) in D7), (7, lambda w: canon(w) in T7),
       (8, lambda w: canon(w) in D8), (8, lambda w: canon(w) in T8))
lines = []
for nm, (n, f) in zip(('bad5', 'bad6', 'd7', 't7', 'd8', 't8'), fam):
    bits = ['1' if f(list(w)) else '0' for w in itertools.product(A, repeat=n)]
    lines.append(' '.join(bits))
    w9 = [b for w, b in zip(itertools.product(A, repeat=n), bits) if 9 in w]
    print('%s: words %d true %d; with a 9: %d true %d' % (nm, len(bits), bits.count('1'), len(w9), w9.count('1')))
open(OUTF, 'w').write('\n'.join(lines) + '\n')
# restriction to 5..8 must equal defect_tables8.txt
old = [l.split() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'defect_tables8.txt'))]
for i, (n, f) in enumerate(fam):
    new = [b for w, b in zip(itertools.product(A, repeat=n), lines[i].split()) if 9 not in w]
    print('line %d restricted to 5..8 equals defect_tables8.txt: %s' % (i + 1, new == old[i]))
print('canonical 5-wheels with a 9 that are reducible (fans):', sorted(''.join(map(str, w)) for w in {canon(w) for w in itertools.product(A, repeat=5) if 9 in w} if isR5(list(w))))
