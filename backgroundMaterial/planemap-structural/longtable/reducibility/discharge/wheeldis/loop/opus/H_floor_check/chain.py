"""H_floor_check round 2: rule-T floor with w2's frame link 7665675 (k36 orientation), via the chain
w0 -T0-> w2 <- e (lone five, only route e -> (e') -> s2) and s2's own row.  sep3 `c` = k36's acceptance check.
usage: python3 -I chain.py WHEELDIS_DIR   (a copy of the branch's wheeldis tree with bin/sep3 compiled)"""
import sys, os, re, itertools, collections
from fractions import Fraction as F
WD = os.path.abspath(sys.argv[1]); os.chdir(WD)
YF = os.path.join(WD, 'out', 'wlp3_j28_13.txt'); hdr = open(YF).readline().split()
args = [a for a in hdr[2:] if a == 'w7plus' or (a.startswith(('pat=', 'cpat=')) and os.path.exists(a.split('=', 1)[1]))]
args += ['pat=loop/n9/win%s.out' % x for x in ('9', '25', '25b', '27', '29', '31')] + ['tag=h2']
src = open(os.path.join(WD, 'wlp3.py')).read(); __file__ = os.path.join(WD, 'wlp3.py'); sys.argv = ['wlp3'] + args
exec(src[:src.index('A_ub, b_ub = [], []')])
def check(d, lk, sv):
    SEP.stdin.write('c %d %s %s\n' % (d, ''.join(map(str, lk)), ''.join(map(str, sv)))); SEP.stdin.flush()
    return SEP.stdout.readline().strip() == '1'
assert check(7, [5,6,7,5,7,6,5], [6,5,7,7,5,7,5]) and check(7, [5,6,7,5,7,6,5], [6,6,7,7,6,7,5])
L5 = (5, 6, 7, 8, 9)
def share(lk, sv, i):
    """sound lower bound (in units of 1 - t) on what link five lk[i] pays the centre (letter 7)"""
    nl = [7, lk[(i + 1) % 7], sv[i], sv[(i - 1) % 7], lk[(i - 1) % 7]]
    bigs = [j for j in range(5) if nl[j] >= 7]
    if bigs == [0]:
        if any(nl[d % 5] == 6 and lk[(i + 2 * d) % 7] >= 7 for d in (1, -1)): return F(0)
        return F(1)
    if any(nl[(j + d) % 5] == 6 for j in bigs for d in (1, -1)): return F(0)
    return F(1, len(bigs)) if len({root(nl, j) for j in bigs}) == 1 else F(0)
def killed37(lk, sv):   # round 37: degree 7, link 7665575, five in the slot between the 7 and its adjacent 6
    for s in range(7):
        for dr in (1, -1):
            l = [lk[(s + dr * k) % 7] for k in range(7)]
            if l == [7, 6, 6, 5, 5, 7, 5] and sv[s if dr == 1 else (s - 1) % 7] == 5: return True
    return False
# w2 frames: link (u7, w1 6, s1 6, e 5, e' 6, s2 7, w3 5), s (w0 5, p1, x2, x3, x4, s3 7, w4 7), e lone (x2, x3 <= 6)
W2 = collections.defaultdict(list)
for p, x2, x3, x4 in itertools.product(L5, (5, 6), (5, 6), L5):
    lk = [7, 6, 6, 5, 6, 7, 5]; sv = [5, p, x2, x3, x4, 7, 7]
    if isR5([7, 6, x3, x2, 6]) or not check(7, lk, sv): continue
    W2[(x3, x4)].append(p)          # x3 is read again by e''s wheel, x4 by s2's frame
print('# w2 frames 7665675 with e lone, accepted: (x3, x4) ->', {k: len(v) for k, v in sorted(W2.items())})
# s2 frames: link (w3 5, w2 7, e' 6, x4, q1, q2, s3 7), s (u 7, e 5, pi, r1, r2, r3, w4 7); pi = e''s private
best = collections.defaultdict(lambda: (F(-1),))
cnt = collections.Counter()
for (x3, x4) in sorted(W2):
    for q1, q2, pi, r1, r2, r3 in itertools.product(L5, repeat=6):
        if isR6([7, 5, x3, pi, x4, 7]): cnt['e\' R6'] += 1; continue
        lk = [5, 7, 6, x4, q1, q2, 7]; sv = [7, 5, pi, r1, r2, r3, 7]
        c2 = sum(share(lk, sv, i) for i in range(7) if lk[i] == 5)
        if c2 <= best[(x3, x4)][0] and c2 < F(1): continue
        if killed37(lk, sv): cnt['k37'] += 1; continue
        if not check(7, lk, sv): cnt['c rej'] += 1; continue
        cnt['kept'] += 1
        if c2 > best[(x3, x4)][0]: best[(x3, x4)] = (c2, lk, sv)
print('#', dict(cnt))
def floor(c2): return (2 * c2 - F(9, 10)) / (F(91, 10) + 2 * c2)
for k, b in sorted(best.items(), key=lambda kv: -kv[1][0]):
    print('(x3, x4) = %s: best s2 c2 = %s  floor %s = %.5f  s2 link %s s %s' % (k, b[0], floor(b[0]), float(floor(b[0])),
          ''.join(map(str, b[1])), ''.join(map(str, b[2]))))
SEP.stdin.close(); SEP.wait()
