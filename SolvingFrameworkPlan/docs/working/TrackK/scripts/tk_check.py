"""Track K: step-by-step data check of the hand proof of Conjecture F (FProof.md).
For every unfilled state s at a degree-5 hole h it builds the filled-in map T° (T - h plus the
two diagonals x1x3, x1x4 from the mu-vertex, as a map: parallel edges kept apart) and checks
  S1  N(T-h) = N(T°) + 2 - L1 - L2                         (exact)
  S2  cw(T°) = cw(s) + 3*hand(s)                            (exact)
  S3  per partition i: k_i == |X|+|Y|+e(XY) (mod 2)          (any orientable surface)
  S4  per partition i: r_i = k_i + 1                         (sphere; r_i = #chains of P_i)
  S5  the signed face counts of the four colour triangles agree (= d), cw - ccw = 4d,
      deg(A) == d (mod 2)
  S6  F0 on T°: 2N(T°) == cw(T°) + |V(T°)| (mod 4)
  S7  F itself (tc_mod4 residue) == 0                        (sphere)
  S8  torus: F residue == 2*G mod 4, G = sum_i (r_i - k_i) - 3 + 3g  (exact explanation)
Also the no-hole statement F0 on random full colourings.
Uses TrackI-review/ri_core.py and TrackC/scripts/tc_mod4.py read-only.
Usage: nice -n 10 python3 -I tk_check.py [scale]
"""
import sys, os, random
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(W, 'TrackI-review')); sys.path.insert(0, os.path.join(W, 'TrackC', 'scripts'))
from ri_core import *  # noqa
from tc_mod4 import orient, oriented_link, CYC, residue  # noqa

PARTS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))

def tait_cw(a, b, c): return (a ^ b, b ^ c, c ^ a) in CYC
def pos(a, b, c):
    (d,) = set(range(4)) - {a, b, c}; p = (d, a, b, c)
    return sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0

def ncomp(n, edges, col, p, q):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for u, v in edges:
        if {col[u], col[v]} == {p, q}: par[f(u)] = f(v)
    return len({f(v) for v in range(n) if col[v] in (p, q)})

def analyse(nv, faces, edges, col):
    """faces: oriented triples (u,v,w) with tags for darts; edges: list of (u,v) with multiplicity.
    Returns dict of all quantities for a closed oriented triangulated map."""
    out = {}
    out['N'] = sum(ncomp(nv, edges, col, p, q) for p, q in PAIRS)
    out['cw'] = sum(tait_cw(col[u], col[v], col[w]) for (u, v, w), _ in faces)
    out['F'] = len(faces)
    # signed counts per colour triangle
    sc = Counter()
    for (u, v, w), _ in faces:
        t = frozenset((col[u], col[v], col[w])); sc[t] += 1 if pos(col[u], col[v], col[w]) else -1
    out['signed'] = sc
    # dual: darts -> face index; twin by (v,u,tag)
    dart = {}
    for i, ((u, v, w), tags) in enumerate(faces):
        for (a, b), tg in zip(((u, v), (v, w), (w, u)), tags):
            dart.setdefault((a, b, tg), []).append(i)
    ks, rs, par_ok = [], [], []
    for (P, Q) in PARTS:
        cls = {P[0]: 0, P[1]: 0, Q[0]: 1, Q[1]: 1}
        par = list(range(len(faces)))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for (a, b, tg), fl in dart.items():
            if cls[col[a]] != cls[col[b]]:
                g = dart[(b, a, tg)]
                assert len(fl) == 1 and len(g) == 1
                par[f(fl[0])] = f(g[0])
        k = len({f(i) for i in range(len(faces))})
        r = ncomp(nv, edges, col, *P) + ncomp(nv, edges, col, *Q)
        X, Y = P
        exy = sum(1 for u, v in edges if {col[u], col[v]} == {X, Y})
        nxy = sum(1 for v in range(nv) if col[v] in (X, Y))
        ks.append(k); rs.append(r); par_ok.append((k - nxy - exy) % 2 == 0)
    out['k'] = ks; out['r'] = rs; out['S3'] = all(par_ok)
    return out

def S5ok(o, col, nv, edges):
    vals = set(o['signed'].get(frozenset(t), 0) for t in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)))
    if len(vals) != 1: return False, None
    d = vals.pop()
    if o['cw'] - (o['F'] - o['cw']) != 4 * d: return False, d
    degA = sum(1 for u, v in edges if 0 in (col[u], col[v]))
    return (degA - d) % 2 == 0, d

def run(surfaces, seed, steps, label, g):
    rng = random.Random(seed); C = Counter()
    for s in surfaces:
        n = len(s.V); ori = orient(s)
        for h in [h for h in s.V if len(s.adj[h]) == 5][:3]:
            Lr = oriented_link(s, ori, h)
            V, ix, nbr = graph_minus(s, h); L = [ix[v] for v in Lr]
            base_faces = [(tuple(ix[x] for x in t), ('E', 'E', 'E')) for f, t in ori.items() if h not in t]
            base_edges = [(ix[u], ix[v]) for e in s.ef for u, v in [tuple(e)] if h not in e]
            c = random_colouring(nbr, rng)
            if c is None: continue
            for _ in range(steps):
                st, res = residue(s, ori, h, L, nbr, ix, c, n)
                if st is not None:
                    x = st['x']; C['states'] += 1
                    par13 = x[3] in nbr[x[1]]; par14 = x[4] in nbr[x[1]]
                    C['parallel diag'] += par13 or par14
                    fan = [((x[1], x[2], x[3]), ('E', 'E', 'D')), ((x[1], x[3], x[4]), ('D', 'E', 'D')),
                           ((x[4], x[0], x[1]), ('E', 'E', 'D'))]
                    faces = base_faces + fan
                    edges = base_edges + [(x[1], x[3]), (x[1], x[4])]
                    o = analyse(len(V), faces, edges, c)
                    Nh = N_total(nbr, c)
                    hand = int((st['al'] ^ st['mu'], st['al'] ^ st['A'], st['al'] ^ st['B']) in CYC)
                    cw = o['cw'] - sum(tait_cw(c[a], c[b], c[d]) for (a, b, d), _ in fan)
                    C['S1 fail'] += Nh != o['N'] + 2 - st['L1'] - st['L2']
                    C['S2 fail'] += o['cw'] != cw + 3 * hand
                    C['S3 fail'] += not o['S3']
                    ok5, d = S5ok(o, c, len(V), edges); C['S5 fail'] += not ok5
                    if g == 0:
                        C['S4 fail'] += any(r != k + 1 for r, k in zip(o['r'], o['k']))
                        C['S6 fail'] += (2 * o['N'] - o['cw'] - len(V)) % 4 != 0
                        C['S7 fail'] += res != 0
                    else:
                        G = sum(o['r']) - sum(o['k']) - 3 + 3 * g
                        C['S8 fail'] += res != (2 * G) % 4
                        C['torus residue %d' % res] += 1
                        C['torus G=%d' % G] += 1
                v = rng.randrange(len(c)); oc = rng.choice([q for q in range(4) if q != c[v]])
                c = kempe_swap(nbr, c, v, oc)
    print(label, dict(sorted(C.items())), flush=True)
    return C

def run_nohole(surfaces, seed, per, label, g):
    rng = random.Random(seed); C = Counter()
    for s in surfaces:
        ori = orient(s); V = s.V; ix = {v: i for i, v in enumerate(V)}
        nbr = [[ix[w] for w in s.adj[v]] for v in V]
        faces = [(tuple(ix[x] for x in t), ('E', 'E', 'E')) for t in ori.values()]
        edges = [tuple(ix[u] for u in e) for e in s.ef]
        c = random_colouring(nbr, rng)
        if c is None: continue
        for _ in range(per):
            o = analyse(len(V), faces, edges, c); C['colourings'] += 1
            C['S3 fail'] += not o['S3']
            ok5, d = S5ok(o, c, len(V), edges); C['S5 fail'] += not ok5
            r = (2 * o['N'] - o['cw'] - len(V)) % 4
            if g == 0:
                C['F0 fail'] += r != 0
                C['S4 fail'] += any(rr != k + 1 for rr, k in zip(o['r'], o['k']))
                C['N==n+1+d fail'] += (o['N'] - len(V) - 1 - d) % 2 != 0
            else:
                G = sum(o['r']) - sum(o['k']) - 3 + 3 * g
                C['torus F0 residue %d' % r] += 1
                C['S8 fail'] += r != (2 * G) % 4
            v = rng.randrange(len(c)); oc = rng.choice([q for q in range(4) if q != c[v]])
            c = kempe_swap(nbr, c, v, oc)
    print(label, dict(sorted(C.items())), flush=True)

if __name__ == '__main__':
    sc = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    m = lambda x: max(1, int(x * sc))
    rng = random.Random(7)
    sph5 = [random_surface(tetra(), rng.randint(12, 34), rng, 200, target_min5=True) for _ in range(m(40))]
    sph3 = [random_surface(tetra(), rng.randint(8, 34), rng, 200) for _ in range(m(40))]
    tor = [random_surface(torus_grid(3, 4), rng.randint(12, 26), rng, 100) for _ in range(m(25))]
    run_nohole(sph3, 21, 60, 'nohole-sphere', 0)
    run_nohole(tor, 22, 60, 'nohole-torus', 1)
    run(sph5, 23, 200, 'hole-sphere-min5', 0)
    run(sph3, 24, 200, 'hole-sphere-min3', 0)
    cen = os.path.join(W, 'Census29', 'out'); gs = []
    for k in (22, 26, 30, 32):
        p = os.path.join(cen, 'frame-%d.txt' % k)
        if os.path.exists(p):
            lines = [l for l in open(p).read().split('\n') if l.strip()]
            for l in rng.sample(lines, min(m(6), len(lines))): gs.append(parse_census_line(l)[1])
    run(gs, 25, 200, 'hole-census-frame', 0)
    run(tor, 26, 200, 'hole-torus', 1)
