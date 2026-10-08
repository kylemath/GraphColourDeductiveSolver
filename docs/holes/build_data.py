#!/usr/bin/env python3
"""Build docs/holes/data.js for the 'Diamonds and Holes' page.

Everything on the page that is a number or a graph comes from this script, which reads committed
repo files (paths below, relative to the repo root) and asserts what it can:

  * The four Lean occurrence structures (DiamondP/MOcc.lean, C2122P/MOcc.lean): the free completions
    of the Birkhoff diamond and of RSST 2.122 are rebuilt from their `Nx` fields and drawn.  The script
    checks that TrackB/occ_sched.h (the schedule frame.c uses) states exactly the same `Nx` facts.
  * A Python port of TrackB/frame.c (Occ matcher from occ_sched.h, appearance test with clean tips,
    NoSep by triangle count, minimum degree).  The port is checked against frame.c's recorded counts:
    on all 10,221 min-degree-5 4-connected triangulations of orders 12-24 (TrackB/out/
    all-mindeg5-12-24.txt) it must find exactly the frame-class counts of TrackB/out/count-small.log.
  * FrameWit22 (TrackC/FrameWit22-faces.json, the face list behind FrameWit22Map.lean): rebuilt as a
    rotation system, checked to be a triangulated sphere in the frame class by the port, and checked
    isomorphic (as a map, possibly mirrored) to the census's only order-22 frame graph p22#196.
  * The C60 dual: the first (only) order-32 graph of the committed IPR list ipr_32_52.pc.
  * Hole-type (link word) statistics by order from the exhaustive frame-class census lists
    (Census29/out/frame-22..32.txt, Census33/out/frame-33.txt). Order 34: when the uncommitted 117 MB
    Census34/out/frame-34.txt is present, the script computes the counts and writes the committed summary
    Census34/out/wordcounts-34.json (with the source SHA-256); otherwise it reads that JSON. Set
    HOLES_IGNORE_FRAME34=1 to force the JSON path.
  * TrackB's discharging set S (TrackB/out/discharge-frameonly.json).

Usage: python3 docs/holes/build_data.py   (writes docs/holes/data.js)
"""
import json, math, os, re, random, sys, hashlib
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
W = os.path.join(ROOT, 'SolvingFrameworkPlan', 'docs', 'working')
LEAN = os.path.join(W, 'StudioMathLean', 'Mathlib', 'Combinatorics', 'SimpleGraph', 'PlaneMap')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.js')


def rel(p):
    return os.path.relpath(p, ROOT)


def log(*a):
    print(*a, file=sys.stderr)


# ---------------------------------------------------------------- rotation systems
def parse_rot(s):
    return [list(map(int, r.split(','))) for r in s.split(';')]


def rot_from_faces(faces, n):
    """Faces (a,b,c) listed with a consistent orientation -> rotation lists (next(v,a)=b for face v,a,b)."""
    nxt = [dict() for _ in range(n)]
    for f in faces:
        for i in range(3):
            v, a, b = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            assert a not in nxt[v], ('vertex', v, 'two faces after', a)
            nxt[v][a] = b
    rot = []
    for v in range(n):
        start = min(nxt[v]); r = [start]
        while True:
            u = nxt[v][r[-1]]
            if u == start: break
            r.append(u)
        assert len(r) == len(nxt[v]), ('link of', v, 'is not one cycle')
        rot.append(r)
    return rot


def check_triangulated_sphere(rot):
    n = len(rot)
    A = [set(r) for r in rot]
    for v in range(n):
        assert len(A[v]) == len(rot[v]), 'repeated neighbour'
        for u in rot[v]: assert v in A[u] and u != v, 'asymmetric'
    pos = [{u: i for i, u in enumerate(r)} for r in rot]
    # faces = orbits of the face permutation on darts; triangulated means every orbit has length 3
    seen = set(); faces = []
    for v in range(n):
        for u in rot[v]:
            if (v, u) in seen: continue
            f = [(v, u)]; seen.add((v, u))
            while True:
                a, b = f[-1]  # the face after dart a->b continues with b -> prev_b(a)
                c = rot[b][(pos[b][a] - 1) % len(rot[b])]
                d = (b, c)
                if d == f[0]: break
                f.append(d); seen.add(d)
            assert len(f) == 3, 'non-triangular face'
            faces.append(tuple(x for x, _ in f))
    E = sum(len(r) for r in rot) // 2
    assert n - E + len(faces) == 2, 'Euler characteristic is not 2'
    return faces


def faces_of(rot):
    return check_triangulated_sphere(rot)


# ---------------------------------------------------------------- Lean Occ structures and occ_sched.h
def lean_occ(name):
    src = open(os.path.join(LEAN, name + 'Occ.lean')).read()
    m = re.search(r'structure Occ .*?ring : Fin (\d+) .*?int : Fin (\d+)', src)
    R, L = int(m.group(1)), int(m.group(2))
    dm = re.search(r'deg : .*?\(!\[([\d, ]+)\]', src)
    deg = [int(x) for x in dm.group(1).split(',')]
    facts = []
    for f in re.finditer(r'r\d+_\d+ : Nx T \((int|ring) (\d+)\) \((int|ring) (\d+)\) \((int|ring) (\d+)\)', src):
        g = f.groups()
        idx = lambda k, i: int(i) if k == 'int' else L + int(i)
        facts.append((idx(g[0], g[1]), idx(g[2], g[3]), idx(g[4], g[5])))
    assert len(deg) == L == 4
    return dict(R=R, L=L, deg=deg, facts=facts, file=rel(os.path.join(LEAN, name + 'Occ.lean')))


def parse_sched():
    src = open(os.path.join(W, 'TrackB', 'occ_sched.h')).read()
    confs = {}
    for nm in ['DiamondP', 'DiamondM', 'C2122P', 'C2122M']:
        arr = lambda key: re.search(nm + '_' + key + r'\[\]?\[?\d*\]? = \{(.*?)\};', src, re.S).group(1)
        deg = [int(x) for x in re.search(nm + r'_deg\[4\] = \{(.*?)\}', src).group(1).split(',')]
        steps = [tuple(map(int, t.split(','))) for t in re.findall(r'\{([\d,]+)\}', arr('steps'))]
        facts = [tuple(map(int, t.split(','))) for t in re.findall(r'\{([\d,]+)\}', arr('facts'))]
        confs[nm] = dict(deg=deg, steps=steps, facts=facts, L=10 if 'Diamond' in nm else 11)
    return confs


# ---------------------------------------------------------------- Python port of TrackB/frame.c
class G:
    def __init__(self, rot):
        self.rot = rot; self.n = len(rot); self.deg = [len(r) for r in rot]
        self.A = [set(r) for r in rot]
        self.pos = [{u: i for i, u in enumerate(r)} for r in rot]

    def nxt(self, x, y): return self.rot[x][(self.pos[x][y] + 1) % self.deg[x]]
    def prv(self, x, y): return self.rot[x][(self.pos[x][y] - 1) % self.deg[x]]


def has_occ(g, c):
    for i0 in range(g.n):
        if g.deg[i0] != c['deg'][0]: continue
        for i1 in g.rot[i0]:
            if g.deg[i1] != c['deg'][1]: continue
            asg = [-1] * 16; asg[0] = i0; asg[1] = i1; ok = True
            for t, xs, as_, out in c['steps']:
                x, a = asg[xs], asg[as_]
                if a not in g.A[x]: ok = False; break
                asg[out] = g.nxt(x, a) if t == 0 else g.prv(x, a)
            if not ok: continue
            for xi, yi, zi in c['facts']:
                x, y, z = asg[xi], asg[yi], asg[zi]
                if y not in g.A[x] or g.nxt(x, y) != z: ok = False; break
            if not ok: continue
            if any(g.deg[asg[a]] != c['deg'][a] for a in range(4)): continue
            if len(set(asg[:c['L']])) != c['L']: continue
            return True
    return False


def appear(g, dc):
    """bit0: some appearance with centre-0 degree dc; bit1: some appearance with clean tips (frame.c)."""
    r = 0
    for c0 in range(g.n):
        if g.deg[c0] != dc: continue
        for c2 in g.rot[c0]:
            if g.deg[c2] != 5: continue
            cm = [t for t in g.rot[c0] if t != c2 and c2 in g.A[t]]
            for t1 in cm:
                for t3 in cm:
                    if t1 == t3 or t3 in g.A[t1] or g.deg[t1] != 5 or g.deg[t3] != 5: continue
                    r |= 1
                    if not any(x in g.A[t3] and x != c0 and x != c2 for x in g.rot[t1]): r |= 2
    return r


def ntriangles(g):
    t = 0
    for a in range(g.n):
        for b in g.rot[a]:
            if b <= a: continue
            for c in g.rot[b]:
                if c > b and c in g.A[a]: t += 1
    return t


def frame_check(rot, confs):
    g = G(rot)
    s = sum(g.deg); assert s == 6 * g.n - 12, 'not a triangulation'
    res = dict(n=g.n, mindeg5=min(g.deg) >= 5)
    res['nosep'] = ntriangles(g) == 2 * g.n - 4
    res['occ'] = {k: has_occ(g, c) for k, c in confs.items()}
    a5, a6 = appear(g, 5), appear(g, 6)
    res['appfree'] = not ((a5 | a6) & 2)
    res['rsstfree'] = not ((a5 | a6) & 1)
    res['occfree'] = not any(res['occ'].values())
    res['frame'] = res['mindeg5'] and res['nosep'] and res['occfree']
    return res


# ---------------------------------------------------------------- words
CAP = 8


def canon(w):
    c = []
    for s in (w, w[::-1]):
        for i in range(len(s)): c.append(tuple(s[i:] + s[:i]))
    return min(c)


def fmt(w):
    return ''.join(str(d) if d < CAP else '8+' for d in w)


def parse_word(s):
    out = []; i = 0
    while i < len(s):
        if s[i] == '8': out.append(8); i += 2 if s[i + 1:i + 2] == '+' else 1
        else: out.append(int(s[i])); i += 1
    return tuple(out)


def has_run(w):
    """Cyclic runs 555 / 565 at positions (j, j+1, j+2)."""
    runs = []
    for j in range(5):
        a, b, c = w[j], w[(j + 1) % 5], w[(j + 2) % 5]
        if a == 5 and c == 5 and b in (5, 6): runs.append((j, '5%d5' % b))
    return runs


def graph_words(rot):
    deg = [len(r) for r in rot]
    return [canon([min(deg[u], CAP) for u in r]) for v, r in enumerate(rot) if deg[v] == 5]


# ---------------------------------------------------------------- map isomorphism (planar, possibly mirrored)
def map_code(rot, v0, u0, mirror):
    lab = {v0: 0}; order = [v0]; first = {v0: u0}; code = []
    i = 0
    while i < len(order):
        v = order[i]; r = rot[v]; k = r.index(first[v]); d = len(r)
        seq = [r[(k + (-j if mirror else j)) % d] for j in range(d)]
        code.append(-1)
        for u in seq:
            if u not in lab:
                lab[u] = len(order); order.append(u); first[u] = v
            code.append(lab[u])
        i += 1
    return tuple(code)


def iso_maps(r1, r2):
    if len(r1) != len(r2): return False
    c1 = map_code(r1, 0, r1[0][0], False)
    for v in range(len(r2)):
        for u in r2[v]:
            for m in (False, True):
                if map_code(r2, v, u, m) == c1: return True
    return False


# ---------------------------------------------------------------- layouts
def sphere_layout(rot, seed=1, iters=4000):
    """Spring layout on the unit sphere; asserted to be an embedding (all faces positively oriented)."""
    n = len(rot); faces = faces_of(rot)
    rng = np.random.default_rng(seed)
    best = None
    for attempt in range(12):
        X = rng.normal(size=(n, 3)); X /= np.linalg.norm(X, axis=1)[:, None]
        E = np.array([(v, u) for v in range(n) for u in rot[v] if u > v])
        for it in range(iters):
            D = X[:, None, :] - X[None, :, :]
            d2 = (D ** 2).sum(-1) + np.eye(n)
            F = (D / d2[..., None] ** 1.5).sum(1) * 0.02
            S = np.zeros_like(X)
            diff = X[E[:, 1]] - X[E[:, 0]]
            np.add.at(S, E[:, 0], diff); np.add.at(S, E[:, 1], -diff)
            X = X + F + 0.05 * S
            X /= np.linalg.norm(X, axis=1)[:, None]
        F = np.array(faces)
        sg = np.einsum('ij,ij->i', X[F[:, 0]], np.cross(X[F[:, 1]], X[F[:, 2]]))
        if (sg > 0).all() or (sg < 0).all():
            if (sg < 0).all(): X[:, 0] *= -1
            best = X; break
    assert best is not None, 'sphere layout did not embed'
    F = np.array(faces)
    sg = np.einsum('ij,ij->i', best[F[:, 0]], np.cross(best[F[:, 1]], best[F[:, 2]]))
    assert (sg > 0).all()
    return best, faces


def flat_layout(rot, X, v, centre):
    """Open the sphere at vertex v: stereographic projection from X[v], so v goes to infinity and its link
    becomes the outer boundary. Asserted to be a straight-line embedding of T - v: every face avoiding v has
    the same orientation, and the boundary (the link of v) is a simple polygon."""
    N = X[v]; a = np.cross(N, [1.0, 0, 0])
    if np.linalg.norm(a) < 0.1: a = np.cross(N, [0, 1.0, 0])
    a /= np.linalg.norm(a); c = np.cross(N, a)
    P = np.array([[(p @ a) / (1 - p @ N), (p @ c) / (1 - p @ N)] if i != v else [0.0, 0.0] for i, p in enumerate(X)])
    faces = faces_of(rot)
    sgn = set()
    for f in faces:
        if v in f: continue
        A, B, C = P[list(f)]
        s = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
        assert abs(s) > 1e-9
        sgn.add(s > 0)
    assert len(sgn) == 1, 'flat drawing is not an embedding'
    L = [P[u] for u in rot[v]]
    def cross(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    k = len(L)
    for i in range(k):
        for j in range(i + 2, k):
            if i == 0 and j == k - 1: continue
            p1, p2, q1, q2 = L[i], L[(i + 1) % k], L[j], L[(j + 1) % k]
            assert not (cross(p1, p2, q1) * cross(p1, p2, q2) < 0 and cross(q1, q2, p1) * cross(q1, q2, p2) < 0), 'boundary not simple'
    P = P - P[centre]  # translate so the chosen hole sits at the centre (a translation keeps the embedding)
    faces_off = [f for f in faces if v not in f]

    def valid(Q):
        sg = set()
        for f in faces_off:
            A, B, C = Q[list(f)]
            s = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
            if abs(s) < 1e-9: return False
            sg.add(s > 0)
        return len(sg) == 1

    # Stereographic projection shrinks the middle. Spread it with a radial power r -> r^g about the centre hole,
    # choosing g to maximise the shortest edge among the exponents that keep a straight-line embedding.
    edges = [(x, u) for x in range(len(rot)) for u in rot[x] if u > x and v not in (x, u)]
    best = None
    for g in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4]:
        r = np.linalg.norm(P, axis=1)
        Q = P * ((r + 1e-12) ** (g - 1))[:, None]; Q[centre] = 0; Q[v] = 0
        if not valid(Q): continue
        ml = min(np.linalg.norm(Q[x] - Q[u]) for x, u in edges) / max(np.linalg.norm(Q[u]) for u in range(len(rot)) if u != v)
        if best is None or ml > best[0]: best = (ml, g, Q)
    assert best is not None and valid(best[2])
    P = best[2]
    R = max(np.linalg.norm(P[u]) for u in range(len(rot)) if u != v)
    P = P / R
    P[v] = [0.0, 0.0]
    return P


def far_hole(rot, X, centre):
    """The degree-5 vertex farthest (on the sphere layout) from the centre hole: the map is opened there."""
    return max((u for u in range(len(rot)) if len(rot[u]) == 5 and u != centre), key=lambda u: -float(X[u] @ X[centre]))


# ---------------------------------------------------------------- configuration drawings
def config_drawing(conf, label):
    """Free completion of an Occ structure: interior 0..3, ring L..L+R-1. Build the faces from Nx facts,
    then draw: ring on a circle in ring order, interior by Tutte barycentres."""
    L, R = conf['L'], conf['R']
    nv = L + R
    faces = set()
    for x, y, z in conf['facts']:
        faces.add(tuple(sorted((x, y, z))))
    adj = {v: set() for v in range(nv)}
    for f in faces:
        for i in range(3):
            for j in range(3):
                if i != j: adj[f[i]].add(f[j])
    for a in range(L):
        assert len(adj[a]) == conf['deg'][a], (label, 'interior degree', a)
    ringc = [L + t for t in range(R)]
    for t in range(R):  # consecutive ring vertices adjacent (ring is a cycle)
        u, w = ringc[t], ringc[(t + 1) % R]
        assert w in adj[u], (label, 'ring not a cycle at', t)
    M = np.zeros((nv, nv)); bb = np.zeros((nv, 2))
    for t in range(R):
        a = math.pi / 2 + 2 * math.pi * t / R
        v = ringc[t]; M[v, v] = 1; bb[v] = (math.cos(a), -math.sin(a))
    for a in range(L):
        M[a, a] = len(adj[a])
        for u in adj[a]: M[a, u] -= 1
    P = np.linalg.solve(M, bb)
    # inner faces only (faces touching an interior vertex)
    edges = sorted({tuple(sorted((u, w))) for u in adj for w in adj[u]})
    edges += [tuple(sorted((ringc[t], ringc[(t + 1) % R]))) for t in range(R)]
    edges = sorted(set(edges))
    names = ['int %d' % a for a in range(L)] + ['ring %d' % t for t in range(R)]
    return dict(label=label, L=L, R=R, deg=conf['deg'], pos=[[round(float(x), 4), round(float(y), 4)] for x, y in P],
                faces=sorted(faces), edges=edges, names=names, file=conf['file'],
                nfacts=len(conf['facts']))


# ---------------------------------------------------------------- main
def main():
    data = {}
    random.seed(0)
    # 1. Lean configurations vs occ_sched.h
    confs = parse_sched()
    lean = {}
    for nm in ['DiamondP', 'DiamondM', 'C2122P', 'C2122M']:
        lc = lean_occ(nm); lean[nm] = lc
        assert lc['deg'] == confs[nm]['deg'], nm
        assert sorted(lc['facts']) == sorted(confs[nm]['facts']), nm + ': occ_sched.h facts differ from Lean'
        assert 4 + lc['R'] == confs[nm]['L'], nm
    log('Lean Occ structures agree with occ_sched.h (4 configurations)')
    data['configs'] = {
        'diamond': config_drawing(lean['DiamondP'], 'Birkhoff diamond'),
        'c2122': config_drawing(lean['C2122P'], 'RSST configuration 2.122'),
    }

    # 2. port of frame.c vs recorded counts
    expect = {}
    for line in open(os.path.join(W, 'TrackB', 'out', 'count-small.log')):
        m = re.match(r'COUNT n=(\d+) total=(\d+) mindeg5=(\d+) nosep=(\d+) occfree=(\d+) appfree=(\d+) rsstfree=(\d+)', line)
        if m: expect[int(m.group(1))] = tuple(map(int, m.groups()[1:]))
    got = {}
    for line in open(os.path.join(W, 'TrackB', 'out', 'all-mindeg5-12-24.txt')):
        p = line.split()
        if len(p) < 3: continue
        rot = parse_rot(p[2]); r = frame_check(rot, confs)
        n = len(rot); c = got.setdefault(n, [0] * 6)
        c[0] += 1; c[1] += r['mindeg5']; c[2] += r['mindeg5'] and r['nosep']
        ok = r['mindeg5'] and r['nosep']
        c[3] += ok and r['occfree']; c[4] += ok and r['appfree']; c[5] += ok and r['rsstfree']
        if ok: assert r['occfree'] == r['appfree'], ('occ/app mismatch', p[0])
    for n, c in sorted(got.items()):
        assert tuple(c) == expect[n], ('frame.c port disagrees at n=%d' % n, c, expect[n])
    port_check = {'graphs': sum(c[0] for c in got.values()), 'orders': [min(got), max(got)],
                  'frame_by_order': {n: c[3] for n, c in sorted(got.items()) if c[3]}}
    log('frame.c port matches count-small.log on', port_check['graphs'], 'graphs', port_check['frame_by_order'])
    # negative control: the icosahedron (order 12) has diamonds
    ico = parse_rot(open(os.path.join(W, 'TrackB', 'out', 'all-mindeg5-12-24.txt')).readline().split()[2])
    ri = frame_check(ico, confs); assert not ri['frame'] and ri['occ']['DiamondP'] and ri['occ']['DiamondM'] and not ri['occ']['C2122P']
    data['portCheck'] = port_check

    # 3. FrameWit22
    fj = json.load(open(os.path.join(W, 'TrackC', 'FrameWit22-faces.json')))
    faces22 = [tuple(f) for f in fj['faces']]
    rot22 = rot_from_faces(faces22, 22)
    check_triangulated_sphere(rot22)
    r22 = frame_check(rot22, confs)
    assert r22['frame'] and r22['appfree'] and r22['rsstfree'], r22
    deg22 = [len(r) for r in rot22]
    assert sorted(deg22).count(5) == 12 and sorted(deg22).count(6) == 10
    p22 = parse_rot(open(os.path.join(W, 'Census29', 'out', 'frame-22.txt')).read().split()[2])
    assert iso_maps(rot22, p22), 'FrameWit22 is not the census order-22 frame graph'
    X22, F22 = sphere_layout(rot22, seed=3)
    words22 = []
    for v in range(22):
        if deg22[v] == 5:
            raw = [min(deg22[u], CAP) for u in rot22[v]]
            words22.append(dict(v=v, raw=fmt(raw), word=fmt(canon(raw))))
    five = [v for v in range(22) if deg22[v] == 5]
    # degree-5 vertices: components of the subgraph they induce
    comp = {}; tri = []
    for v in five:
        if v in comp: continue
        st = [v]; comp[v] = len(tri); cc = [v]
        while st:
            x = st.pop()
            for u in rot22[x]:
                if deg22[u] == 5 and u not in comp: comp[u] = comp[v]; st.append(u); cc.append(u)
        tri.append(sorted(cc))
    assert all(len(t) == 3 for t in tri) and len(tri) == 4
    centre22 = five[0]
    open22 = far_hole(rot22, X22, centre22)
    P22 = flat_layout(rot22, X22, open22, centre22)
    data['wit22'] = dict(n=22, rot=rot22, faces=F22, xyz=np.round(X22, 4).tolist(),
                         flat=np.round(P22, 4).tolist(), openAt=open22, centreAt=centre22,
                         holes=words22, fiveTriangles=tri, check=r22,
                         iso='p22#196', source=rel(os.path.join(W, 'TrackC', 'FrameWit22-faces.json')),
                         lean=[rel(os.path.join(LEAN, 'FrameWit22Map.lean')), rel(os.path.join(LEAN, 'FrameWit22.lean'))])
    log('FrameWit22: frame class, 12x deg5 / 10x deg6, isomorphic to p22#196; words', {w['word'] for w in words22})

    # 4. C60 dual from the IPR list
    pc = open(os.path.join(ROOT, 'backgroundMaterial', 'planemap-structural', 'studiointel', 'ipr', 'ipr_32_52.pc'), 'rb').read()
    assert pc[:15] == b'>>planar_code<<'
    ipr_all = []; i = 15
    while i < len(pc):
        n = pc[i]; i += 1; rot = []
        for v in range(n):
            r = []
            while pc[i] != 0: r.append(pc[i] - 1); i += 1
            i += 1; rot.append(r)
        ipr_all.append(rot)
    k60 = [j for j, r in enumerate(ipr_all) if len(r) == 32]
    assert len(k60) == 1, 'expected exactly one IPR dual of order 32 (C60)'
    rot60 = ipr_all[k60[0]]; n = 32
    check_triangulated_sphere(rot60)
    r60 = frame_check(rot60, confs); assert r60['frame'] and r60['rsstfree'], r60
    d60 = [len(r) for r in rot60]
    assert d60.count(5) == 12 and d60.count(6) == 20
    assert all(d60[u] == 6 for v in range(32) if d60[v] == 5 for u in rot60[v]), 'not IPR'
    X60, F60 = sphere_layout(rot60, seed=5)
    centre60 = next(v for v in range(32) if d60[v] == 5)
    open60 = far_hole(rot60, X60, centre60)
    P60 = flat_layout(rot60, X60, open60, centre60)
    data['c60'] = dict(n=32, rot=rot60, faces=F60, xyz=np.round(X60, 4).tolist(), flat=np.round(P60, 4).tolist(),
                       openAt=open60, centreAt=centre60, holes=[dict(v=v, raw='66666', word='66666') for v in range(32) if d60[v] == 5],
                       check=r60, source=rel(os.path.join(ROOT, 'backgroundMaterial', 'planemap-structural', 'studiointel', 'ipr', 'ipr_32_52.pc')) + ' (the one order-32 graph, index %d)' % k60[0])
    log('C60 dual: frame class, IPR, 12 holes all 66666')

    # 5. word universe
    univ = sorted({canon(list(w)) for w in __import__('itertools').product([5, 6, 7, 8], repeat=5)})
    assert len(univ) == 136
    excl = [w for w in univ if has_run(w)]
    assert len(excl) == 19 and len(univ) - len(excl) == 117
    disc = json.load(open(os.path.join(W, 'TrackB', 'out', 'discharge-frameonly.json')))
    S_allowed = set(disc['S_allowed'])
    assert len(S_allowed) == 59 and all(not has_run(parse_word(s)) for s in S_allowed)
    assert all(fmt(canon(list(parse_word(s)))) == s for s in S_allowed)
    assert len(disc['S_forbidden']) == 19 and {fmt(w) for w in excl} == set(disc['S_forbidden'])

    # 6. census words by order
    lists = [(k, os.path.join(W, 'Census29', 'out', 'frame-%d.txt' % k)) for k in range(22, 33)]
    lists.append((33, os.path.join(W, 'Census33', 'out', 'frame-33.txt')))
    p34 = os.path.join(W, 'Census34', 'out', 'frame-34.txt')
    j34 = os.path.join(W, 'Census34', 'out', 'wordcounts-34.json')
    have34 = os.path.exists(p34) and not os.environ.get('HOLES_IGNORE_FRAME34')  # env var: test the committed-JSON path
    if have34: lists.append((34, p34))
    expect_graphs = {22: 1, 23: 1, 24: 4, 25: 2, 26: 11, 27: 24, 28: 104, 29: 296, 30: 1178, 31: 4294,
                     32: 16016, 33: 58194, 34: 209702}
    expect_holes34 = 3612341
    census = {}
    rng = random.Random(7)
    verified = 0
    for k, path in lists:
        holes = {}; graphs = {}; mono = {}; ng = 0; nh = 0; sha = hashlib.sha256()
        with open(path) as fh:
            for line in fh:
                p = line.split()
                if len(p) < 3: continue
                sha.update(line.encode())
                rot = parse_rot(p[2]); assert len(rot) == k
                ws = graph_words(rot); ng += 1; nh += len(ws)
                for w in ws:
                    assert not has_run(w), ('555/565 run in frame graph', p[0])
                    holes[w] = holes.get(w, 0) + 1
                for w in set(ws): graphs[w] = graphs.get(w, 0) + 1
                if len(set(ws)) == 1:
                    w = ws[0]; mono.setdefault(w, p[0])
                # re-verify with the frame.c port: all graphs to order 28, a deterministic sample after
                if k <= 28 or rng.random() < (0.01 if k <= 32 else 0.0005):
                    r = frame_check(rot, confs)
                    assert r['frame'] and r['appfree'] and r['rsstfree'], ('not frame', p[0])
                    verified += 1
        assert ng == expect_graphs[k], (k, ng)
        if k == 34: assert nh == expect_holes34, nh
        census[k] = dict(graphs=ng, holes=nh,
                         words={fmt(w): [c, graphs[w]] for w, c in sorted(holes.items(), key=lambda x: -x[1])},
                         monotype={fmt(w): nm for w, nm in sorted(mono.items())},
                         file=rel(path), committed=(k != 34), sha256=sha.hexdigest())
        log('order', k, ng, 'graphs', nh, 'holes', len(holes), 'words; monotype', sorted(fmt(w) for w in mono))
    if have34:
        c = census[34]
        summ = dict(note='Generated by docs/holes/build_data.py from Census34/out/frame-34.txt (not committed, 117 MB). '
                         'Hole type = cyclic link-degree word of a degree-5 vertex, up to rotation/reflection, degrees >= 8 as 8+. '
                         'words: type -> [holes, graphs containing it]; monotype: type -> first graph whose holes all have that type.',
                    order=34, source='SolvingFrameworkPlan/docs/working/Census34/out/frame-34.txt', source_sha256=c['sha256'],
                    graphs=c['graphs'], holes=c['holes'], words=c['words'], monotype=c['monotype'])
        with open(j34, 'w') as fh: json.dump(summ, fh, indent=1); fh.write('\n')
        log('wrote', rel(j34))
    else:
        summ = json.load(open(j34))
        assert summ['order'] == 34 and summ['graphs'] == expect_graphs[34] and summ['holes'] == expect_holes34
        assert sum(v[0] for v in summ['words'].values()) == summ['holes']
        assert all(not has_run(parse_word(w)) for w in summ['words'])
        census[34] = dict(graphs=summ['graphs'], holes=summ['holes'], words=summ['words'], monotype=summ['monotype'],
                          file=rel(j34), committed=True, sha256=summ['source_sha256'])
        log('order 34 from', rel(j34))
    # the order-32 graph forcing 66666 is the C60 dual itself
    m32 = census[32]['monotype'].get('66666')
    assert m32
    with open(os.path.join(W, 'Census29', 'out', 'frame-32.txt')) as fh:
        line = next(l for l in fh if l.split()[0] == m32)
    assert iso_maps(parse_rot(line.split()[2]), rot60), 'order-32 66666 graph is not the C60 dual'
    data['census'] = census
    data['censusVerified'] = verified

    # IPR list: every hole 66666 (whole committed list 32..52)
    nipr = 0; iprh = 0; iprOrders = {}
    for rot in ipr_all:
        n = len(rot)
        ws = graph_words(rot); nipr += 1; iprh += len(ws)
        assert ws and all(fmt(w) == '66666' for w in ws)
        iprOrders[n] = iprOrders.get(n, 0) + 1
    assert nipr == 1267 and iprh == 15204
    data['ipr'] = dict(graphs=nipr, holes=iprh, orders=iprOrders)

    seen = set()
    for k in census: seen |= set(census[k]['words'])
    monoAll = {}
    for k in sorted(census):
        for w, nm in census[k]['monotype'].items(): monoAll.setdefault(w, (k, nm))
    words = []
    for w in univ:
        s = fmt(w)
        words.append(dict(w=s, digits=list(w), excluded=bool(has_run(w)), runs=has_run(w),
                          inS=s in S_allowed, seen=s in seen,
                          mono=(list(monoAll[s]) if s in monoAll else ('IPR duals' if s == '66666' else None))))
    data['words'] = words
    data['monotypeFirst'] = {w: list(v) for w, v in monoAll.items()}
    data['trackB'] = dict(discharging=59, withRuns=78, packing=9, hittingCensus=7, adversarialHitting=13)
    js = 'window.HOLES_DATA = ' + json.dumps(data, separators=(',', ':')) + ';\n'
    open(OUT, 'w').write('/* generated by docs/holes/build_data.py; do not edit */\n' + js)
    log('wrote', rel(OUT), len(js), 'bytes; frame-port re-verified', verified, 'census graphs')


if __name__ == '__main__':
    main()
