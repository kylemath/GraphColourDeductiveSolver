"""Positive control for sat_planar's circle rule on genuine sphere Hamiltonian states (census windows):
circle = H walked from the e4-neighbour to the e2-neighbour, then v-points e1, e3, e0; require a side
2-colouring of the chords with no same-side crossing and side(e3) != side(e0) = side(e1)."""
import sys, json
from pf_lib import Sphere, nr_windows, bits
import tt_lib
W = '/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/'
ok = bad = 0
G = tt_lib.load_graphs(W + 'Census34/out/maxima_graphs.txt')
for nm, rot in list(G.items()):
    for h in range(len(rot)):
        if len(rot[h]) != 5: continue
        sp = Sphere(rot, h); g = sp.g
        for w in nr_windows(sp):
            for (P, M) in w:
                if g.kH(P, M) != 1: continue
                k = g.vedge(M); f = g.fv; e = [f[(k - 2 + i) % 5] for i in range(5)]
                H = P | M
                seq = []; x = g.other(e[4], 0); ed = e[4]
                while x != 0:
                    seq.append(x); nx = [t for t in g.inc[x] if (H >> t & 1) and t != ed]; ed = nx[0]; x = g.other(ed, x)
                pos = {x: i + 1 for i, x in enumerate(seq)}; n = g.n
                vp = {e[1]: n + .25, e[3]: n + .5, e[0]: n + .75}
                ch = []
                for c in bits(g.ALL & ~H):
                    a, b = g.E[c]
                    pa = vp[c] if a == 0 else pos[a]; pb = vp[c] if b == 0 else pos[b]
                    ch.append((min(pa, pb), max(pa, pb), c))
                A = tt_lib.interlace(ch)
                # add constraint edges: e3 must differ from e0, e1; e0 = e1 -> encode e0~e1 via a dummy
                idx = {c: i for i, (_, _, c) in enumerate(ch)}
                m = len(ch); A = A + [0]
                def link(i, j): A[i] |= 1 << j; A[j] |= 1 << i
                link(idx[e[3]], idx[e[0]]); link(idx[e[3]], idx[e[1]])
                link(idx[e[0]], m); link(idx[e[1]], m)   # dummy node forces side(e0) = side(e1)
                if tt_lib.bipartition(A) is None: bad += 1
                else: ok += 1
print('sphere Ham states satisfying the circle rule:', ok, 'failing:', bad)
