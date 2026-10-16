"""G9 (exploratory): tables for loop/g9/defectc8 over the alphabet {5,6,7,8}.  Same sources as defect_tables.py
(exec of defect.py's header, option strict7), extended to words with a letter 8 and to 8-wheels:
  bad5[w]  5-wheel in R_opt: Job 17 D/C c5 words (these include letter 8) or a D fan (F = free, matches 8) / diamond;
  bad6[w]  6-wheel in R_opt: Job 17 c6 words (letters 5-7 only), the six 565xxx, or 2.122 (three consecutive 5s);
           a 6-wheel with a letter 8 is reducible only through 2.122 (otherwise untested -> NOT reducible here);
  d7[w]    7-wheel tested D (bigwheels*_dfast.out, def_w7_r16.out; words over 5-8) or cfast C-candidate (strict7);
  t7[w]    7-wheel tested at all;
  d8[w]    8-wheel tested D (c8_ lines of bigwheels*_dfast.out; words over 5-8);  t8[w] 8-wheel tested at all.
Untested words count as NOT reducible (conservative).  Index = base-4 code of the word read in cyclic order,
digit = letter - 5, first letter most significant.  Line order: bad5 bad6 d7 t7 d8 t8.
Usage: python3 defect_tables8.py OUT"""
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
        if not f or not f[0].startswith('c8_'): continue
        if 'D=true' not in line and 'D=false' not in line: continue
        w = tuple(map(int, f[0][3:])); T8.add(w)
        if 'D=true' in line: D8.add(w)
print('C7 (cfast C-candidate 7-wheels):', len(C7), ' with an 8:', sum(1 for w in C7 if 8 in w))
print('D7', len(D7), 'T7', len(T7), 'D8', len(D8), 'T8', len(T8))
A = (5, 6, 7, 8)
fam = ((5, lambda w: isR5(w)), (6, lambda w: bad6(w)), (7, lambda w: canon(w) in D7), (7, lambda w: canon(w) in T7),
       (8, lambda w: canon(w) in D8), (8, lambda w: canon(w) in T8))
lines = []; names = ('bad5', 'bad6', 'd7', 't7', 'd8', 't8'); rep = []
for nm, (n, f) in zip(names, fam):
    bits = []; st = collections.Counter()
    for w in itertools.product(A, repeat=n):
        b = f(list(w)); bits.append('1' if b else '0')
        st[(8 in w, b)] += 1
    lines.append(' '.join(bits))
    rep.append('%s: words %d, true %d; words with an 8: %d, true among them %d' % (nm, len(bits), bits.count('1'), st[(True, True)] + st[(True, False)], st[(True, True)]))
open(OUTF, 'w').write('\n'.join(lines) + '\n')
print('\n'.join(rep))
# canonical words with an 8 in each family that are reducible / untested (for the report)
for n, nm in ((5, 'bad5'), (6, 'bad6'), (7, '7'), (8, '8')):
    cw = sorted({canon(w) for w in itertools.product(A, repeat=n) if 8 in w})
    if n == 5: r = [w for w in cw if isR5(list(w))]; print('5-wheels with 8: canonical %d, R %d (via Job17 C or fans)' % (len(cw), len(r)))
    if n == 6: r = [w for w in cw if bad6(list(w))]; print('6-wheels with 8: canonical %d, R %d (2.122 only)' % (len(cw), len(r)))
    if n == 7: print('7-wheels with 8: canonical %d, D %d, tested %d, untested %d' % (len(cw), sum(w in D7 for w in cw), sum(w in T7 for w in cw), sum(w not in T7 for w in cw)))
    if n == 8: print('8-wheels: canonical %d, D %d, tested %d, untested %d' % (len(cw) + 0, sum(w in D8 for w in cw), sum(w in T8 for w in cw), sum(w not in T8 for w in cw)))
# consistency with bin/defect_tables.txt (restriction to {5,6,7})
old = [l.split() for l in open(os.path.join(WD, 'bin', 'defect_tables.txt'))]
for i, (n, f) in enumerate(fam[:4]):
    new = ['1' if f(list(w)) else '0' for w in itertools.product((5, 6, 7), repeat=n)]
    print('restriction to 5-7 of %s equals bin/defect_tables.txt line %d: %s' % (names[i], i + 1, new == old[i]))
