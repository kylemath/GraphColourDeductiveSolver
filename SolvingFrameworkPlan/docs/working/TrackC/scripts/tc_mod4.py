"""Track C scoping data: the mod-4 chain-count formula (F) and the local swap lemma (W).

F : for an unfilled state s at a degree-5 hole h of a triangulated sphere with n vertices,
      2 N(s) == cw(s) + (n-1) - hand(s) + 2 (L1(s) + L2(s))   (mod 4)
    N = number of Kempe chains of T - h (sum over the six colour pairs),
    cw = number of faces avoiding h whose Tait triple (c(u)^c(v), c(v)^c(w), c(w)^c(u)),
         read in the rotation order of the face, is a cyclic shift of (1,2,3),
    hand = [ (al^mu, al^A, al^B) is a cyclic shift of (1,2,3) ].
W : for a Kempe swap of a component K of T - h, delta cw == 2 m_h(K) (mod 4), where m_h(K) is
    the number of link edges x_t x_{t+1} with both ends in K (1 for pi at a DL state, 0 for
    link-free swaps). Expected on every orientable triangulated surface.
Uses the independent reviewer's library TrackI-review/ri_core.py (read-only).
Usage: nice -n 10 python3 -I tc_mod4.py
"""
import sys, random, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'TrackI-review'))
from ri_core import *  # noqa

CYC = ((1, 2, 3), (2, 3, 1), (3, 1, 2))

def orient(s):
    faces = list(s.faces); f0 = faces[0]; a, b, c = tuple(f0)
    ori = {f0: (a, b, c)}; st = [f0]
    while st:
        f = st.pop(); x, y, z = ori[f]
        for (u, v) in ((x, y), (y, z), (z, x)):
            for g in s.ef[frozenset((u, v))]:
                if g in ori: continue
                (w,) = tuple(g - {u, v}); ori[g] = (v, u, w); st.append(g)
    return ori

def cwcount(ori, h, ix, c):
    k = 0
    for f, (x, y, z) in ori.items():
        if h in (x, y, z): continue
        if (c[ix[x]] ^ c[ix[y]], c[ix[y]] ^ c[ix[z]], c[ix[z]] ^ c[ix[x]]) in CYC: k += 1
    return k

def oriented_link(s, ori, h):
    Lr = s.link(h)
    f = next(f for f in ori if h in ori[f]); x, y, z = ori[f]
    t = (x, y, z).index(h); a = (x, y, z)[(t + 1) % 3]; b = (x, y, z)[(t + 2) % 3]
    i = Lr.index(a)
    return Lr if Lr[(i + 1) % 5] == b else Lr[::-1]

def residue(s, ori, h, L, nbr, ix, c, n):
    st = hole_state(nbr, c, L)
    if st is None: return None, None
    N = N_total(nbr, c); cw = cwcount(ori, h, ix, c)
    hand = int((st['al'] ^ st['mu'], st['al'] ^ st['A'], st['al'] ^ st['B']) in CYC)
    return st, (2 * N - cw - (n - 1) + hand - 2 * (st['L1'] + st['L2'])) % 4

def run(surfaces, seed, steps, label):
    rng = random.Random(seed); F = Counter(); Wpi = Counter(); W0 = Counter(); thm6 = Counter()
    for s in surfaces:
        n = len(s.V); ori = orient(s)
        for h in [h for h in s.V if len(s.adj[h]) == 5][:3]:
            Lr = oriented_link(s, ori, h)
            V, ix, nbr = graph_minus(s, h); L = [ix[v] for v in Lr]; Ls = set(L)
            c = random_colouring(nbr, rng)
            if c is None: continue
            for _ in range(steps):
                st, r = residue(s, ori, h, L, nbr, ix, c, n)
                if st is not None:
                    F[r] += 1
                    if st['DL']:
                        c2, K = pi_move(nbr, c, st)
                        if c2 is not None:
                            st2 = hole_state(nbr, c2, L)
                            Wpi[(cwcount(ori, h, ix, c2) - cwcount(ori, h, ix, c)) % 4] += 1
                            thm6[((N_total(nbr, c2) - N_total(nbr, c)) % 2 == int(bool(st2 and st2['DL'])))] += 1
                v = rng.randrange(len(c)); o = rng.choice([q for q in range(4) if q != c[v]])
                K = component(nbr, c, v, c[v], o); c2 = kempe_swap(nbr, c, v, o)
                if not (K & Ls):
                    W0[(cwcount(ori, h, ix, c2) - cwcount(ori, h, ix, c)) % 4] += 1
                c = c2
    print(label, 'F residues', dict(F), '| W at pi (dcw mod 4)', dict(Wpi),
          '| W link-free', dict(W0), '| Thm6 holds', dict(thm6), flush=True)

if __name__ == '__main__':
    rng = random.Random(1)
    run([random_surface(tetra(), rng.randint(12, 34), rng, 200, target_min5=True) for _ in range(60)], 11, 300, 'sphere-min5')
    run([random_surface(tetra(), rng.randint(12, 34), rng, 200) for _ in range(60)], 12, 300, 'sphere-min3')
    cen = os.path.join(HERE, '..', '..', 'Census29', 'out')
    gs = []
    for k in (22, 24, 26, 28, 30, 32):
        p = os.path.join(cen, 'frame-%d.txt' % k)
        if os.path.exists(p):
            lines = open(p).read().split('\n')
            lines = [l for l in lines if l.strip()]
            for l in rng.sample(lines, min(8, len(lines))):
                gs.append(parse_census_line(l)[1])
    run(gs, 13, 300, 'census-frame')
    run([random_surface(torus_grid(3, 4), rng.randint(12, 26), rng, 100) for _ in range(30)], 14, 300, 'torus')
