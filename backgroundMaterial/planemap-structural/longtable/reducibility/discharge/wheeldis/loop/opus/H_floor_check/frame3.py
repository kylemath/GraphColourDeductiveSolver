"""H_floor_check: build R*(6,6) + w2's worst frame (+ mirror at w4) as an oriented triangle patch, check it,
read off rule-T routes, and evaluate w2's row bound and the (6,6) floor.  usage: python3 frame.py DISDIR
(DISDIR holds studio17/wheels17_verdicts.txt and wheeldis/{wlpdefs.py (wlp.py lines 1-45), out/fans_dfast.out})"""
import sys, os, collections
from fractions import Fraction as F
DIS = sys.argv[1]
src = open(os.path.join(DIS, 'wheeldis', 'wlpdefs.py')).read()
g = {'__file__': os.path.join(DIS, 'wheeldis', 'wlpdefs.py')}; sys.argv = ['x']; exec(src, g)
isR5, isR6 = g['isR5'], g['isR6']
w = ['w%d' % i for i in range(7)]; s = ['s%d' % i for i in range(7)]
faces = []
for i in range(7):
    j = (i + 1) % 7
    faces += [('u', w[i], w[j]), (w[j], w[i], s[i])]
deg = dict(u=7, **{w[i]: d for i, d in enumerate([5, 6, 7, 5, 7, 6, 5])},
           **{s[i]: d for i, d in enumerate([6, 6, 7, 7, 6, 7, 5])})   # filling (s1, s4) = (6, 6)
for i in (0, 3, 6): faces.append((w[i], s[i - 1], s[i]))               # link fives
for i, p in ((1, 'p1'), (5, 'p5')): faces += [(w[i], s[i - 1], p), (w[i], p, s[i])]; deg[p] = 7
# w2 frame (round 2): link (u, w1, s1, e, f, s2, w3) = 7665675, s-word (w0, p1, x2, x3, x4, s3, w4) = 5 7 6 6 5 7 7;
# f (= e') is a 6 with private pi.  s2's frame: link (w3, w2, f, x4, q1, q2, s3) = 5765557, s (u, e, pi, r1, r2, r3, w4) = 7575757
faces += [('w2', 's1', 'e'), ('w2', 'e', 'f'), ('w2', 'f', 's2'),
          ('e', 's1', 'x2'), ('e', 'x2', 'x3'), ('e', 'x3', 'f'), ('f', 'x3', 'pi'), ('f', 'pi', 'x4'), ('f', 'x4', 's2'),
          ('s2', 'x4', 'q1'), ('s2', 'q1', 'q2'), ('s2', 'q2', 's3'),
          ('x4', 'pi', 'r1'), ('x4', 'r1', 'q1'), ('q1', 'r1', 'r2'), ('q1', 'r2', 'q2'), ('q2', 'r2', 'r3'), ('q2', 'r3', 's3')]
deg.update(e=5, f=6, x2=6, x3=6, x4=5, pi=7, q1=5, q2=5, r1=5, r2=7, r3=5)
# 1. each directed edge once (consistent orientation, no face repeated)
de = collections.Counter((a, b) for (x, y, z) in faces for (a, b) in ((x, y), (y, z), (z, x)))
assert max(de.values()) == 1, [k for k, v in de.items() if v > 1]
# 2. rotations of closed vertices are single cycles of the stated degree
def rot(v):
    nxt = {}
    for f_ in faces:
        if v in f_:
            k = f_.index(v); nxt[f_[(k + 1) % 3]] = f_[(k + 2) % 3]
    return nxt
def cyc(v):
    n = rot(v); a = next(iter(n)); out = [a]
    while n.get(out[-1]) is not None and n[out[-1]] != a: out.append(n[out[-1]])
    closed = n.get(out[-1]) == a and len(out) == len(n)
    return out, closed
closedv = ['u'] + [x for x in w if x != 'w4'] + ['e', 'f', 's2', 'x4', 'q1', 'q2']
for v in closedv:
    c, ok = cyc(v); assert ok and len(c) == deg[v], (v, c, deg[v])
    print('%-3s deg %d  link %s  letters %s' % (v, deg[v], ' '.join(c), ''.join(str(min(deg[x], 9)) for x in c)))
# w2's link and s-word as in the k36 frame
c, _ = cyc('w2'); k = c.index('u'); c = c[k:] + c[:k]
if c[1] != 'w1': c = [c[0]] + c[1:][::-1]
third = {}
for (x, y, z) in faces:
    for a, b, cc in ((x, y, z), (y, z, x), (z, x, y)): third.setdefault(frozenset((a, b)), set()).add(cc)
sw = [next(iter(third[frozenset((c[i], c[(i + 1) % 7]))] - {'w2'})) for i in range(7)]
print('w2 link', ''.join(str(deg[x]) for x in c), [*c], ' s-word', ''.join(str(deg[x]) for x in sw), sw)
# 3. rule-T routes of every closed five: big B in its link, a 6 x next to B in its link, z = third(B, x) - {v}
def routes(v):
    cl, _ = cyc(v); out = []
    for i, B in enumerate(cl):
        if deg[B] < 7: continue
        for x in (cl[i - 1], cl[(i + 1) % len(cl)]):
            if deg[x] == 6:
                z = third[frozenset((B, x))] - {v}; out.append((B, x, z, [deg.get(q) for q in z]))
    return out
for v in ('w0', 'w3', 'w6', 'e', 'x4', 'q1', 'q2'):
    cl, _ = cyc(v)
    print('five %-3s link %s bigs %s  T routes %s  R5? %s' % (v, ''.join(str(deg[x]) for x in cl),
          [x for x in cl if deg[x] >= 7], routes(v), isR5([deg[x] for x in cl])))
c, _ = cyc('s2'); k = c.index('w3'); c = c[k:] + c[:k]
if c[1] != 'w2': c = [c[0]] + c[1:][::-1]
sw2 = [next(iter(third[frozenset((c[i], c[(i + 1) % 7]))] - {'s2'})) for i in range(7)]
print('s2 link', ''.join(str(deg[x]) for x in c), c, ' s-word', ''.join(str(deg[x]) for x in sw2), sw2)
print('f 6-wheel', [deg[x] for x in cyc('f')[0]], 'R6?', isR6([deg[x] for x in cyc('f')[0]]))
