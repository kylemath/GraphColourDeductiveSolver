"""New binding w2 frame (explore r37): w2 link 7665675 = (u, w1, s1, e, y, s2, w3), s-word 5.66577 = (w0, p1, x2, x3,
x4, s3, w4) (k36 top k=2 row 7665675/5966577).  e = 5 with link (w2 7, s1 6, x2 6, x3 6, y 6): lone.
Hats around e: h(w2,s1)=w1=6, h(s1,x2)=q, h(x2,x3)=a, h(x3,y)=b, h(y,w2)=s2=7.  Privates: s1->p1, x2->c, x3->d,
y->x4 (=5).  T routes: e -> y -> s2 (big) is a T route; e -> s1 -> w1 (6) is not.
Rule-S routes not paired at w2 (bigs other than s2 reached through a 6-neighbour): p1, q, a, b, c, d.
Question: is there an admissible 2-ball (all wheels non-R) with p1, q, a, b, c, d all <= 6?  usage: python3 eroute2.py"""
import itertools
from defs import isR5, isR6
L = (5, 6, 7, 8, 9)
W = lambda w: (isR5 if len(w) == 5 else isR6)(w)
ok = []; nall = 0
for p1, q, a, b, c, d in itertools.product(L, repeat=6):
    if isR6((7, 7, 6, p1, 6, 5)): continue          # w1: u, w2, s1, p1, s0, w0
    if isR6((6, 7, 5, 6, q, p1)): continue          # s1: w1, w2, e, x2, q, p1
    if isR6((5, 6, a, c, q, 6)): continue           # x2: e, x3, a, c, q, s1
    if isR6((5, 6, b, d, a, 6)): continue           # x3: e, y, b, d, a, x2
    if isR6((7, 5, 6, b, 5, 7)): continue           # y: w2, e, x3, b, x4, s2
    nall += 1
    if max(p1, q, a, b, c, d) <= 6: ok.append((p1, q, a, b, c, d))
print('admissible 2-balls of e:', nall, ' with no unpaired S route (p1,q,a,b,c,d all <= 6):', len(ok))
for z in ok[:30]: print('  p1 q a b c d =', z)
# which slots carry the route when the adversary keeps bigs to a minimum
import collections
names = ('p1', 'q', 'a', 'b', 'c', 'd'); cnt = collections.Counter(); mins = collections.Counter()
for p1, q, a, b, c, d in itertools.product(L, repeat=6):
    v = (p1, q, a, b, c, d)
    if isR6((7, 7, 6, p1, 6, 5)) or isR6((6, 7, 5, 6, q, p1)) or isR6((5, 6, a, c, q, 6)) or isR6((5, 6, b, d, a, 6)) or isR6((7, 5, 6, b, 5, 7)): continue
    bs = tuple(n for n, x in zip(names, v) if x >= 7); cnt[len(bs)] += 1
    if len(bs) == 1: mins[(bs[0], ''.join(map(str, v)))] += 1
print('number of big slots among p1,q,a,b,c,d:', dict(sorted(cnt.items())))
bys = collections.Counter(k[0] for k in mins); print('single-big 2-balls by slot:', dict(bys))
for k in sorted(mins)[:40]: print('  ', k[0], 'p1 q a b c d =', k[1])
two = collections.Counter(); ex = {}
for p1, q, a, b, c, d in itertools.product(L, repeat=6):
    v = (p1, q, a, b, c, d)
    if isR6((7, 7, 6, p1, 6, 5)) or isR6((6, 7, 5, 6, q, p1)) or isR6((5, 6, a, c, q, 6)) or isR6((5, 6, b, d, a, 6)) or isR6((7, 5, 6, b, 5, 7)): continue
    bs = tuple(n for n, x in zip(names, v) if x >= 7)
    if len(bs) == 2: two[bs] += 1; ex.setdefault(bs, []).append(''.join(map(str, v)))
print('two-big 2-balls by slot pair:', dict(two))
for k in two: print('  ', k, ex[k][:6])
