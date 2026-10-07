#!/usr/bin/env python3
"""[Track E, C0] Barnette paired-states signed sum on small Eulerian triangulations (own code, stdlib only).

Reading of OpenAIStructuralAnalogies.md §0 being validated:
  T Eulerian triangulation (faces 2-coloured black/white), black face t0 outer, roots = V(t0).
  A = black faces != t0, X = non-root vertices, |A| = |X| = k-1.
  state r: bijection A -> X with r(t) in V(t).  pair (r,s): r(t) != s(t) for all t.
  delta(v,w) = +1 if the black face of edge vw is on the left of v->w (faces CCW), else -1.
  J(r,s) = (1/3) sum_t delta(r(t), s(t));   phase i^J.
  Q_s = {edge of t opposite s(t)}.
Checks:
  (a) J is an integer for every pair; every directed cycle of D = {r(t)->s(t)} has delta-sum +-3 (disk identity);
  (b) for every s with Q_s cyclic: sum_r i^J = 0 (cancellation);  for Q_s a forest: <= 1 partner;
  (c) Z(x) = sum_pairs i^J exp(x w(s)) with random integer incidence weights a(t,v): the Taylor moments
      M_j = sum_pairs i^J w(s)^j vanish for j < c_min and M_{c_min} != 0 (c_min = fewest cycles of D);
  (d) per undirected D group, sum over the 2^c orientations equals prod_C (phase_+ e^{xL+} + phase_- e^{xL-}) with
      phase ratio -1 between the two orientations of every cycle (checked at x = 0 moments via exact group sums).
Triangulations: all Eulerian (all degrees even) simple triangulations, n = 6..12, found by random edge-flip walks
(dedup by canonical code) -- a sampling enumerator, so "all" is not certified; counts are reported.
"""
import random, itertools, sys, json
from fractions import Fraction

def faces_to_rot(F):
    nxt = {}
    for t in F:
        for i in range(3): nxt.setdefault(t[i], {})[t[(i + 1) % 3]] = t[(i + 2) % 3]
    rot = {}
    for v in nxt:
        s = min(nxt[v]); r = [s]
        while nxt[v][r[-1]] != s: r.append(nxt[v][r[-1]])
        rot[v] = r
    return rot

def canon(F):
    rot = faces_to_rot(F); best = None
    for v in rot:
        for w in rot[v]:
            lab = {v: 0, w: 1}; order = [(v, w)]; code = []
            q = [(v, w)]
            i = 0
            seen_v = [v, w]
            # BFS over vertices: each vertex visited with a reference neighbour
            refs = {v: w, w: v}
            qi = 0; verts = [v, w]
            while qi < len(verts):
                x = verts[qi]; qi += 1
                r = rot[x]; p = r.index(refs[x]); seq = r[p:] + r[:p]
                for y in seq:
                    if y not in lab: lab[y] = len(lab); refs[y] = x; verts.append(y)
                    code.append(lab[y])
                code.append(-1)
            code = tuple(code)
            if best is None or code < best: best = code
    return best

def octahedron():
    # vertices 0 top 5 bottom, 1..4 equator
    F = []
    for i in range(4):
        a, b = 1 + i, 1 + (i + 1) % 4
        F.append((0, a, b)); F.append((5, b, a))
    return F

def flip(F, rnd):
    F = list(F); idx = rnd.randrange(len(F)); t = F[idx]; k = rnd.randrange(3)
    a, b, c = t[k], t[(k + 1) % 3], t[(k + 2) % 3]
    # other face with directed edge b->a
    j = next(j for j, u in enumerate(F) if any(u[m] == b and u[(m + 1) % 3] == a for m in range(3)))
    u = F[j]; m = next(m for m in range(3) if u[m] == b and u[(m + 1) % 3] == a); d = u[(m + 2) % 3]
    # new edge c-d must not exist; degrees of a,b >= 4 after
    edges = set()
    for f in F:
        for i in range(3): edges.add(frozenset((f[i], f[(i + 1) % 3])))
    if frozenset((c, d)) in edges or c == d: return None
    deg = {}
    for f in F:
        for x in f: deg[x] = deg.get(x, 0) + 1
    if deg[a] <= 3 or deg[b] <= 3: return None
    G = [f for i, f in enumerate(F) if i not in (idx, j)]
    G.append((a, d, c)); G.append((b, c, d))
    return G

def grow(F, rnd):
    # insert vertex in a random face (degree-3 vertex), returns new F
    F = list(F); idx = rnd.randrange(len(F)); a, b, c = F.pop(idx); n = 1 + max(x for f in F + [(a, b, c)] for x in f)
    F += [(a, b, n), (b, c, n), (c, a, n)]; return F

def eulerian(F):
    deg = {}
    for f in F:
        for x in f: deg[x] = deg.get(x, 0) + 1
    return all(d % 2 == 0 for d in deg.values())

def enum_eulerian(n, steps, seed):
    rnd = random.Random(seed); F = octahedron()
    while len({x for f in F for x in f}) < n: F = grow(F, rnd)
    found = {}
    for _ in range(steps):
        G = flip(F, rnd)
        if G is None: continue
        F = G
        if eulerian(F):
            c = canon(F)
            if c not in found: found[c] = F
    return list(found.values())

def face_colouring(F):
    # 2-colour faces so adjacent faces differ; returns dict face-index -> 0 black / 1 white
    e2f = {}
    for i, f in enumerate(F):
        for k in range(3): e2f.setdefault(frozenset((f[k], f[(k + 1) % 3])), []).append(i)
    col = {0: 0}; st = [0]
    while st:
        i = st.pop()
        for k in range(3):
            for j in e2f[frozenset((F[i][k], F[i][(k + 1) % 3]))]:
                if j == i: continue
                if j not in col: col[j] = 1 - col[i]; st.append(j)
                elif col[j] == col[i]: return None
    return col

def sep_triangles(F):
    adj = {}
    for f in F:
        for a, b in itertools.combinations(f, 2): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    fs = {frozenset(f) for f in F}; c = 0
    for a, b, d in itertools.combinations(sorted(adj), 3):
        if b in adj[a] and d in adj[a] and d in adj[b] and frozenset((a, b, d)) not in fs: c += 1
    return c

def analyse(F, rnd, t0i=0):
    col = face_colouring(F); assert col is not None
    black = [F[i] for i in range(len(F)) if col[i] == 0]
    black = black[t0i:] + black[:t0i]
    left = {}
    for i, f in enumerate(F):
        for k in range(3): left[(f[k], f[(k + 1) % 3])] = col[i]
    delta = lambda v, w: 1 if left[(v, w)] == 0 else -1
    t0 = black[0]; A = black[1:]; roots = set(t0)
    X = sorted({x for f in F for x in f} - roots)
    assert len(A) == len(X)
    # states
    states = []
    def rec(i, used, cur):
        if i == len(A): states.append(tuple(cur)); return
        for v in A[i]:
            if v in roots or v in used: continue
            cur.append(v); used.add(v); rec(i + 1, used, cur); used.discard(v); cur.pop()
    rec(0, set(), [])
    a = {(ti, v): rnd.randint(-20, 20) for ti, t in enumerate(A) for v in t}
    w = lambda s: sum(a[(ti, s[ti])] for ti in range(len(A)))
    def Qcyclic(s):
        par = {}
        def f(x):
            while par.setdefault(x, x) != x: x = par[x]
            return x
        for ti, t in enumerate(A):
            u, v = [y for y in t if y != s[ti]]
            ru, rv = f(u), f(v)
            if ru == rv: return True
            par[ru] = rv
        return False
    res = dict(n=len({x for f in F for x in f}), k1=len(A), states=len(states))
    pairs = 0; badJ = 0; cyc_bad = 0; cancel_fail = 0; forest_multi = 0; tree_terms = 0
    groups = {}  # undirected D -> list of (J, w(s))
    cmin = None
    phase_sum_by_s = {}
    cyc_pairs = 0
    for s in states:
        cy = Qcyclic(s); acc = [0, 0, 0, 0]; partners = 0
        for r in states:
            if any(r[t] == s[t] for t in range(len(A))): continue
            pairs += 1; partners += 1; cyc_pairs += cy
            ds = sum(delta(r[t], s[t]) for t in range(len(A)))
            if ds % 3: badJ += 1; continue
            J = ds // 3; acc[J % 4] += 1
            # cycles of D: map r(t) -> s(t)
            nxt = {r[t]: s[t] for t in range(len(A))}; seen = set(); ncyc = 0
            for x0 in nxt:
                if x0 in seen: continue
                ncyc += 1; x = x0; dsum = 0
                while x not in seen:
                    seen.add(x); y = nxt[x]; dsum += delta(x, y); x = y
                if abs(dsum) != 3: cyc_bad += 1
            cmin = ncyc if cmin is None else min(cmin, ncyc)
            key = frozenset(frozenset((r[t], s[t])) for t in range(len(A)))
            groups.setdefault(key, []).append((J, w(s), ncyc))
        re_, im_ = acc[0] - acc[2], acc[1] - acc[3]
        if cy and (re_ or im_): cancel_fail += 1
        if not cy:
            if partners > 1: forest_multi += 1
            if partners == 1: tree_terms += 1
    # moments
    def moment(j, items):
        re_ = im_ = 0
        for J, ws, _ in items:
            v = ws ** j
            if J % 4 == 0: re_ += v
            elif J % 4 == 1: im_ += v
            elif J % 4 == 2: re_ -= v
            else: im_ -= v
        return (re_, im_)
    allitems = [x for g in groups.values() for x in g]
    moms = [moment(j, allitems) for j in range((cmin or 0) + 1)]
    # group check: each group size 2^c and group moment j<c vanish
    gfail = 0
    for g in groups.values():
        c = g[0][2]
        if len(g) != 2 ** c: gfail += 1; continue
        for j in range(c):
            if moment(j, g) != (0, 0): gfail += 1; break
    res.update(sep_tri=sep_triangles(F), degs=sorted(len(v) for v in faces_to_rot(F).values()), t0=t0i, cyclicQ_pairs=cyc_pairs, pairs=pairs, J_nonint=badJ, cycles_not_pm3=cyc_bad, cyclicQ_cancel_fail=cancel_fail,
               forest_s_multi_partner=forest_multi, tree_terms=tree_terms, cmin=cmin,
               lower_moments_zero=all(m == (0, 0) for m in moms[:-1]) if moms else None,
               leading_moment=moms[-1] if moms else None, groups=len(groups), group_fail=gfail)
    return res

if __name__ == '__main__':
    rnd = random.Random(1)
    out = []
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    for n in range(6, NMAX + 1):
        Ts = enum_eulerian(n, 40000 if n < 10 else 150000, n) if n > 6 else [octahedron()]
        for F in Ts:
            for t0i in range(len(F) // 2):   # every black face as the outer face
                r = analyse(F, rnd, t0i); out.append(r); print(json.dumps(r)); sys.stdout.flush()
