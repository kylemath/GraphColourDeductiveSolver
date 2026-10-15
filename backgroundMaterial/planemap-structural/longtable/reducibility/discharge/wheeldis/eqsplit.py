"""The equal-split rule (exploratory): every vertex of degree >= 7 sends 1/b to each adjacent degree-5 vertex v, where b
is the number of neighbours of v of degree >= 7.  Every 5 then ends at exactly 0.  This script computes the maximum
demand sum(1/b) on a receiver of degree d under the wheel-level R of wlp.py (options as wlp.py, e.g. bigw),
with lone-big senders (b = 1) capped by capD=k if given, and the uniform bound for all d >= 9 (Karp max cycle mean
of the letter-9 transfer matrix).  Usage: python3 eqsplit.py bigw cap7=1 cap8=2"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'wlp.py')).read().replace('__file__', repr(os.path.join(HERE, 'wlp.py')))
exec(src[:src.index('A_ub, b_ub = [], []')])
yv = np.array([1.0 / sum(1 for x in r if x >= 7) for r in roots])
out = ['# equal-split rule, options %s' % ' '.join(sorted(OPT))]
for d in (7, 8):
    f = best_words_cap if d in CAP else best_words
    top = f(d, yv, 3, -1.0)
    out.append('d=%d: max demand %.4f vs d-6 = %d; worst: %s' % (d, top[0][0], d - 6, ' '.join(''.join(map(str, r)) for r in top[0][1])))
for d in range(9, 25):
    v, p = best_arrangement(d, yv)
    out.append('d=%d: max demand %.4f vs d-6 = %d %s' % (d, v, d - 6, 'OK' if v <= d - 6 + 1e-9 else 'FAIL') + ('' if v <= d - 6 + 1e-9 else '  worst: ' + ' '.join(''.join(map(str, r)) for r in p)))
src2 = src[src.index('def karp'):src.index('yv = res.x')]
exec(src2)
M = np.full((NS, NS), -np.inf)
for a, b, r in TRI[9]: M[a, b] = yv[ix[r]] if r is not None else 0.0
lam = karp(M)
out.append('letter-9 max cycle mean (demand per link position) = %.6f; d*lam <= d-6 for all d >= %.2f' % (lam, 6 / (1 - lam) if lam < 1 else float('inf')))
print('\n'.join(out))
open(os.path.join(HERE, 'out', 'eqsplit_%s.txt' % ('_'.join(sorted(OPT)) or 'base')), 'w').write('\n'.join(out) + '\n')
