"""H_floor_check round 2: guaranteed (y-independent) share c(1-t) of w2's load over every w2 arrangement at s1 = 6
(k36 enumeration: link (u7, w1 6, s1 6, e, e', s2 7, w3 5), s-word (w0 5, p, x2, x3, x4, s3 7, w4 7)).
Share rules (sound lower bounds on what a link five v pays w2, any feasible (Y, T, t)):
  lone five (only big = w2), every 6 next to w2 in v's link has z small (z = next link vertex of w2): 1 - t
  every big of v carries the same rooted word and no 6 of v sits next to any big of v: (1 - t)/#bigs
  otherwise 0.  Floor from w2 and mirror w4: T0, T6 <= 1 + t - c(1 - t);  2.7 t >= 0.7 - T0 - T6.
No c-check / wheel filter here except isR5 on w2's link fives; candidates must be checked separately.
usage: python3 -I frame2.py DISDIR"""
import sys, os, itertools, collections
from fractions import Fraction as F
DIS = sys.argv[1]
g = {'__file__': os.path.join(DIS, 'wheeldis', 'wlpdefs.py')}; sys.argv = ['x']; exec(open(os.path.join(DIS, 'wheeldis', 'wlpdefs.py')).read(), g)
isR5, isR6, root = g['isR5'], g['isR6'], g['root']
L5 = (5, 6, 7, 8, 9)
def share(lk, sv, i):
    v = [lk[i], lk[(i + 1) % 7], sv[i], sv[(i - 1) % 7], lk[(i - 1) % 7]]   # v's link from w2: w2, a, b, c, e
    nl = [7] + v[1:]                                                       # w2 = letter 7
    bigs = [j for j in range(5) if nl[j] >= 7]
    if bigs == [0]:
        for d in (1, -1):
            if nl[d % 5] == 6 and lk[(i + 2 * d) % 7] >= 7: return F(0), 'lone, T route'
        return F(1), 'lone'
    if any(nl[(j + d) % 5] == 6 for j in bigs for d in (1, -1)): return F(0), 'multi-big with 6 next to a big'
    if len({root(nl, j) for j in bigs}) == 1: return F(1, len(bigs)), 'symmetric %d bigs' % len(bigs)
    return F(0), 'multi-big, distinct words'
def floor(c): return (2 * c - F(13, 10)) / (F(47, 10) + 2 * c)
rows = []
for e, e2, p, x2, x3, x4 in itertools.product(L5, repeat=6):
    lk = [7, 6, 6, e, e2, 7, 5]; sv = [5, p, x2, x3, x4, 7, 7]
    fv = [i for i in range(7) if lk[i] == 5]
    if any(isR5([7, lk[(i + 1) % 7], sv[i], sv[(i - 1) % 7], lk[(i - 1) % 7]]) for i in fv): continue
    c = sum(share(lk, sv, i)[0] for i in fv)
    rows.append((c, ''.join(map(str, lk)), ''.join(map(str, sv))))
by = collections.defaultdict(list)
for r in rows: by[r[1]].append(r)
print('# s1 = 6 arrangements kept by isR5:', len(rows))
for lw in sorted(by, key=lambda k: -max(r[0] for r in by[k]))[:12]:
    b = max(by[lw]); print('link %s  max c %s  floor %s = %.5f  e.g. s %s (%d with that c)' %
          (lw, b[0], floor(b[0]), float(floor(b[0])), b[2], sum(1 for r in by[lw] if r[0] == b[0])))
for lw in ('7665675',):
    print('\n## link', lw)
    for c, l, s in sorted(by[lw], reverse=True)[:6]:
        print('  s %s c %s:' % (s, c), [(i, share(list(map(int, l)), list(map(int, s)), i)) for i in range(7) if l[i] == '5'])
