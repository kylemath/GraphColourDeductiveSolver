"""Receiver-centred candidates (exploratory): a vertex u of degree D with k LONE-BIG senders (degree-5 neighbours whose
link has u as the only vertex of degree >= 7; types 55667, 55676, 56667, 66667 at D = 7, the same with 8 at D = 8).
Configuration I = u + the senders + their links (all degrees exact; degrees 5/6 except u); ring = N(I) minus I in the
layered free completion (b8b/rings.py), which must be an induced cycle.  Assignments in which some degree-5 vertex of I
with its whole link in I has a reducible word (wheel census / fans) are dropped (already R).
Writes pairs_D<D>_k<k>.txt (dfast format, ring <= RMAX, canonical up to symmetry by sorted degree signature).
Usage: python3 pairs.py D k [RMAX=16]"""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
from rings import Layered
D, K = int(sys.argv[1]), int(sys.argv[2]); RMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 16
src = open(os.path.join(HERE, 'wlp.py')).read().replace('__file__', repr(os.path.join(HERE, 'wlp.py')))
sys.argv = ['wlp']; exec(src[:src.index('# sender rows')])          # canon, isR5 (census + certified C + fans)
LONE = {canon(w) for w in itertools.product((5, 6), repeat=4) for w in [w + (D,)] if not isR5(w)}
print('lone sender types at D=%d:' % D, sorted(LONE))

def build(link, r2):
    """link: degrees of w_0..w_{D-1}; r2: dict (kind, i) -> degree for ring-2 vertices, kind 's' (shared by w_i,w_{i+1})
    or ('p', i, j).  Returns (adj, names)."""
    L = Layered(D); L.add_ring(list(link))
    W = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('u',)}
    for i, w in enumerate(W): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(W)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    L.add_ring([r2.get(name[z], 9) for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name

def extract(adj, I, deg):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev = cur
    if len(order) != len(RS): return None
    for x in I: assert len(adj[x]) == deg[x], (x, len(adj[x]), deg[x])
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return len(order), len(Il), f(ra), f(ia)

out = {}; nchk = 0
for S in itertools.combinations(range(D), K):
    if S[0] != 0: continue
    # vertices of I (by symbolic name): u, w_i (i in S and neighbours), s_{i-1}, s_i
    wl = sorted({(i + e) % D for i in S for e in (-1, 0, 1)})
    sl = sorted({(i + e) % D for i in S for e in (-1, 0)})
    free_w = [i for i in wl if i not in S]
    for wd in itertools.product((5, 6), repeat=len(free_w)):
        link = [9] * D
        for i in S: link[i] = 5
        for i, d_ in zip(free_w, wd): link[i] = d_
        for sd in itertools.product((5, 6), repeat=len(sl)):
            sdeg = dict(zip(sl, sd))
            ok = True
            for i in S:
                w = (D, link[(i + 1) % D], sdeg[i], sdeg[(i - 1) % D], link[(i - 1) % D])
                if canon(w) not in LONE: ok = False; break
            if not ok: continue
            sig = (tuple(link), tuple(sdeg.get(i, 0) for i in range(D)), tuple(1 if i in wl else 0 for i in range(D)))
            # symmetry: rotations / reflections of the D-cycle
            def tr(sig, k, refl):
                lk, sv, iw = sig
                if refl:
                    lk = lk[::-1]; iw = iw[::-1]; sv = tuple(sv[(-i - 2) % D] for i in range(D))
                return (lk[k:] + lk[:k], sv[k:] + sv[:k], iw[k:] + iw[:k])
            cs = min(tr(sig, k, r) for k in range(D) for r in (0, 1))
            if cs in out: continue
            adj, name = build(link, {('s', i): sdeg[i] for i in sl})
            inv = {v: x for x, v in name.items()}
            I = [inv[('u',)]] + [inv[('w', i)] for i in wl] + [inv[('s', i)] for i in sl]
            deg = {inv[('u',)]: D}; deg.update({inv[('w', i)]: link[i] for i in wl}); deg.update({inv[('s', i)]: sdeg[i] for i in sl})
            # drop if a degree-5 vertex of I has its whole link inside I with a reducible word
            red = False
            for x in I:
                if deg[x] == 5 and adj[x] <= set(I):
                    # cyclic order of x's link
                    N = list(adj[x]); o = [N[0]]
                    while len(o) < 5:
                        o.append(next(y for y in adj[o[-1]] & adj[x] if y not in o))
                    if isR5([deg[y] for y in o]): red = True; break
            c = None if red else extract(adj, I, deg)
            out[cs] = (c, red, S); nchk += 1
for cs, (c, red, S) in sorted(out.items()):
    if c is None: print('  %s senders %s link %s s %s inI %s' % ('already-R' if red else 'NOT-EXTRACTABLE', S, *[''.join(map(str, x)) for x in cs]))
lines = []
for cs, (c, red, S) in sorted(out.items(), key=lambda kv: (kv[1][0][0] if kv[1][0] else 99)):
    if c is None or c[0] > RMAX: continue
    nm = 'p%d_%s_%s_%s' % (D, ''.join(map(str, cs[0])), ''.join(map(str, cs[1])), ''.join(map(str, cs[2])))
    lines.append('%s %d %d %s %s' % ((nm,) + c))
import collections
print('classes', len(out), 'already-R', sum(1 for v in out.values() if v[1]), 'not extractable',
      sum(1 for v in out.values() if v[0] is None and not v[1]), 'written (ring <= %d)' % RMAX, len(lines),
      'rings', sorted(collections.Counter(v[0][0] for v in out.values() if v[0]).items()))
open(os.path.join(HERE, 'pairs_D%d_k%d.txt' % (D, K)), 'w').write('\n'.join(lines) + '\n')
