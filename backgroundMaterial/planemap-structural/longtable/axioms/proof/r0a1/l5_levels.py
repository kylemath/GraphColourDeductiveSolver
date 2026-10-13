"""The L = 5 level model of Lemma L5 as its own SAT problem (equivalent to R0 at L = 5 in normal form):
levels l(1..n-1) in {0..4}, l(1) = 0, l(n-1) = 4; H-edge rules (o-edges (odd i, i+1): both in {0,1}, both in
{2,3}, or both 4; e-edges (even i, i+1): both 0, both in {1,2}, or both in {3,4}); chords join equal levels
1, 2 or 3, or levels in {0,4}; v-chords f4, f1, f3 end at levels 1, 2, 3; circle-rule planarity.
Variants: 'noparity' replaces the H-edge rules by |dl| <= 1; 'nonplanar' drops planarity; 'free1/3/4' drops
the level condition on that v-chord's end; 'crossI' / 'crossO' allows crossings on the f1 page / the f3,f4 page.
usage: l5_levels.py n [noparity] [nonplanar] [free1] [free3] [free4] [crossI] [crossO]"""
import sys, itertools
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose4
n = int(sys.argv[1]); par = 'noparity' not in sys.argv; planar = 'nonplanar' not in sys.argv
P = IDPool(); cl = []
lv = {(x, l): P.id(('l', x, l)) for x in range(1, n) for l in range(5)}
for x in range(1, n):
    cl += CardEnc.equals([lv[x, l] for l in range(5)], 1, vpool=P, encoding=EncType.pairwise).clauses
cl.append([lv[1, 0]]); cl.append([lv[n - 1, 4]])
O = [{0, 1}, {2, 3}, {4}]; E_ = [{0}, {1, 2}, {3, 4}]
for i in range(1, n - 1):
    groups = (O if i % 2 == 1 else E_) if par else None
    for a in range(5):
        for b in range(5):
            ok = any(a in g and b in g for g in groups) if par else abs(a - b) <= 1
            if not ok: cl.append([-lv[i, a], -lv[i + 1, b]])
cls = lambda l: 'A' if l in (0, 4) else l
ch = {(a, b): P.id(('c', a, b)) for a in range(1, n) for b in range(a + 2, n)}
vc = {(s, j): P.id(('v', s, j)) for s in (1, 3, 4) for j in range(2, n - 1)}
for x in range(1, n):
    lits = [ch[min(x, y), max(x, y)] for y in range(1, n) if abs(x - y) >= 2] + [vc[s, x] for s in (1, 3, 4) if (s, x) in vc]
    cl += CardEnc.equals(lits, 1, vpool=P, encoding=EncType.seqcounter).clauses
for s in (1, 3, 4):
    cl += CardEnc.equals([vc[s, j] for j in range(2, n - 1)], 1, vpool=P, encoding=EncType.seqcounter).clauses
for (a, b), c in ch.items():
    for la in range(5):
        for lb in range(5):
            if cls(la) != cls(lb): cl.append([-c, -lv[a, la], -lv[b, lb]])
need = {4: 1, 1: 2, 3: 3}
for (s, j), c in vc.items():
    if 'free%d' % s not in sys.argv: cl.append([-c, lv[j, need[s]]])
if planar:
    VPOS = {4: n + .25, 1: n + .5, 3: n + .75}
    sl = {s: P.id(('vs', s)) for s in (1, 3, 4)}
    cl += [[sl[1], sl[3]], [-sl[1], -sl[3]], [-sl[3], sl[4]], [sl[3], -sl[4]], [sl[1]]]   # page I = True (f1's side)
    items = [((a, b), c, P.id(('sd', a, b))) for (a, b), c in ch.items()] + [((j, VPOS[s]), c, sl[s]) for (s, j), c in vc.items()]
    def cross(c, d):
        a1, b1 = c; a2, b2 = d
        if len({a1, b1, a2, b2}) < 4: return False
        return (a1 < a2 < b1) != (a1 < b2 < b1)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            (c1, p1, s1), (c2, p2, s2) = items[i], items[j]
            if not cross(c1, c2): continue
            if s1 == s2:
                if not (('crossI' in sys.argv and s1 == sl[1]) or ('crossO' in sys.argv and s1 in (sl[3], sl[4]))):
                    cl.append([-p1, -p2])
                continue
            if 'crossO' not in sys.argv: cl.append([-p1, -p2, s1, s2])      # forbids both on page O
            if 'crossI' not in sys.argv: cl.append([-p1, -p2, -s1, -s2])    # forbids both on page I
s = Glucose4(bootstrap_with=cl); r = s.solve()
tag = ('' if par else 'noparity ') + ('planar' if planar else 'nonplanar') + ''.join(' ' + a for a in sys.argv[2:] if a.startswith(('free', 'cross')))
out = f'n={n} L=5 level model {tag}: {"SAT" if r else "UNSAT"}'
if r:
    m = set(x for x in s.get_model() if x > 0)
    out += '  levels ' + ''.join(str(next(l for l in range(5) if lv[x, l] in m)) for x in range(1, n))
    out += '  chords ' + str([k for k, v in ch.items() if v in m] + [k for k, v in vc.items() if v in m])
print(out, flush=True)
