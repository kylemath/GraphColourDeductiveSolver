"""Equal-split overload configurations (exploratory).  Under the rule "a vertex of degree >= 7 sends 1/b to each adjacent
5 with b neighbours of degree >= 7", a receiver u of degree D is overloaded iff sum over its 5-neighbours of 1/b > D - 6.
This enumerates MINIMAL overloaded sender sets S (|S| = k) at u: each sender word (D, w_{i+1}, s_i, s_{i-1}, w_{i-1})
over {5, 6, B}, B = a vertex of degree >= 7 whose degree is left free: B vertices are NOT in the configuration (they
are ring vertices), so a reducible configuration here is reducible for every degree of every B.  A sender must have a
non-R completion (B in {7,8,9}, wlp.isR5).  I = u + senders + their non-B link vertices; ring = N(I) minus I in the
layered free completion (non-I vertices get degree 9 there).  Assignments with a degree-5 vertex of I whose whole link
is in I and reducible are dropped.  Writes eq_D<D>_k<k>.txt (ring <= RMAX).  Usage: python3 pairs2.py D k [RMAX=16]"""
import sys, os, itertools, collections
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
D, K = int(sys.argv[1]), int(sys.argv[2]); RMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 16
ARGV = list(sys.argv)
src = open(os.path.join(HERE, 'pairs.py')).read()
pre = src[:src.index('out = {}; nchk = 0')].replace("os.path.dirname(os.path.abspath(__file__))", repr(HERE))
sys.argv = ['pairs.py', str(D), '1']; exec(pre); sys.argv = ARGV; D, K = int(ARGV[1]), int(ARGV[2])
B = 0
def nonR_completion(w):
    pos = [j for j, x in enumerate(w) if x == B]
    for c in itertools.product((7, 8, 9), repeat=len(pos)):
        ww = list(w)
        for j, x in zip(pos, c): ww[j] = x
        if not isR5(ww): return True
    return False
out = {}
for S in itertools.combinations(range(D), K):
    if S[0] != 0: continue
    wl = sorted({(i + e) % D for i in S for e in (-1, 0, 1)}); sl = sorted({(i + e) % D for i in S for e in (-1, 0)})
    free_w = [i for i in wl if i not in S]
    for wd in itertools.product((5, 6, B), repeat=len(free_w)):
        link = [9] * D
        for i in S: link[i] = 5
        for i, d_ in zip(free_w, wd): link[i] = d_
        for sd in itertools.product((5, 6, B), repeat=len(sl)):
            sdeg = dict(zip(sl, sd)); dem = []; ok = True
            for i in S:
                w = (D, link[(i + 1) % D], sdeg[i], sdeg[(i - 1) % D], link[(i - 1) % D])
                if not nonR_completion(w): ok = False; break
                dem.append(Fr(1, 1 + sum(1 for x in w[1:] if x == B)))
            if not ok or sum(dem) <= D - 6 or any(sum(dem) - x > D - 6 for x in dem): continue
            sig = (tuple(link), tuple(sdeg.get(i, 1) for i in range(D)), tuple(1 if i in wl else 0 for i in range(D)))
            def tr(sig, k, refl):
                lk, sv, iw = sig
                if refl: lk = lk[::-1]; iw = iw[::-1]; sv = tuple(sv[(-i - 2) % D] for i in range(D))
                return (lk[k:] + lk[:k], sv[k:] + sv[:k], iw[k:] + iw[:k])
            cs = min(tr(sig, k, r) for k in range(D) for r in (0, 1))
            if cs in out: continue
            bl = {i: (9 if link[i] == B else link[i]) for i in range(D)}
            adj, name = build([bl[i] for i in range(D)], {('s', i): (9 if v == B else v) for i, v in sdeg.items()})
            inv = {v: x for x, v in name.items()}
            I = [inv[('u',)]] + [inv[('w', i)] for i in wl if link[i] != B] + [inv[('s', i)] for i in sl if sdeg[i] != B]
            deg = {inv[('u',)]: D}
            deg.update({inv[('w', i)]: link[i] for i in wl if link[i] != B}); deg.update({inv[('s', i)]: sdeg[i] for i in sl if sdeg[i] != B})
            red = False
            for x in I:
                if deg[x] == 5 and adj[x] <= set(I):
                    N = list(adj[x]); o = [N[0]]
                    while len(o) < 5: o.append(next(y for y in adj[o[-1]] & adj[x] if y not in o))
                    if isR5([deg[y] for y in o]): red = True; break
            c = None if red else extract(adj, I, deg)
            out[cs] = (c, red, tuple(sorted(dem)))
lines = []; side = []
for cs, (c, red, dem) in sorted(out.items(), key=lambda kv: (kv[1][0][0] if kv[1][0] else 99)):
    if c is None or c[0] > RMAX: continue
    f = lambda t: ''.join('B' if x == B else ('.' if x in (1, 9) else str(x)) for x in t)
    nm = 'e%d_%s_%s_%s' % (D, f(cs[0]), f(cs[1]), ''.join(map(str, cs[2])))
    lines.append('%s %d %d %s %s' % ((nm,) + c)); side.append('%s %s' % (nm, '+'.join(str(x) for x in dem)))
print('D=%d k=%d minimal overloaded classes %d, already-R %d, not extractable %d, written (ring <= %d) %d; rings %s; demand types %s' % (
    D, K, len(out), sum(1 for v in out.values() if v[1]), sum(1 for v in out.values() if v[0] is None and not v[1]), RMAX, len(lines),
    sorted(collections.Counter(v[0][0] for v in out.values() if v[0]).items()),
    dict(collections.Counter('+'.join(str(x) for x in v[2]) for v in out.values()))))
open(os.path.join(HERE, 'eq_D%d_k%d.txt' % (D, K)), 'w').write('\n'.join(lines) + '\n')
open(os.path.join(HERE, 'eq_D%d_k%d.dem' % (D, K)), 'w').write('\n'.join(side) + '\n')
