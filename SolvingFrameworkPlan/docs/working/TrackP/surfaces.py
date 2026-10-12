#!/usr/bin/env python3
"""Track F [exploratory]: triangulations of closed surfaces (torus, Klein bottle, projective plane, genus 2, ...),
random growth + edge-flip walks with min degree >= 5.  A triangulation is a list of 3-sets of vertices (simplicial:
simple graph, every edge in exactly two faces, every vertex link a single cycle).  Output lines 'name n r0;...;r_{n-1}'
where r_v is the cyclic link order of v (orientation per vertex arbitrary; only the hole's cyclic order is used)."""
import random, itertools, collections, sys

def edges_of(F):
    E = collections.defaultdict(list)
    for i, f in enumerate(F):
        for a, b in itertools.combinations(sorted(f), 2): E[(a, b)].append(i)
    return E

def link_cycle(F, v):
    nb = collections.defaultdict(list)
    for f in F:
        if v in f:
            a, b = sorted(set(f) - {v}); nb[a].append(b); nb[b].append(a)
    if not nb or any(len(x) != 2 for x in nb.values()): return None
    start = min(nb); cyc = [start]; prev = None; cur = start
    while True:
        nx = nb[cur][0] if prev is None else [x for x in nb[cur] if x != prev][0]
        if nx == start: break
        if nx in cyc: return None
        cyc.append(nx); prev, cur = cur, nx
    return cyc if len(cyc) == len(nb) else None

def validate(n, F, chi=None):
    if any(len(set(f)) != 3 for f in F): return 'degenerate'
    if len({frozenset(f) for f in F}) != len(F): return 'dup face'
    E = edges_of(F)
    if any(len(x) != 2 for x in E.values()): return 'edge-face'
    for v in range(n):
        if link_cycle(F, v) is None: return 'link'
    if chi is not None and n - len(E) + len(F) != chi: return 'euler'
    return None

def orientable(F):
    F = [tuple(f) for f in F]; E = collections.defaultdict(list)
    for i, f in enumerate(F):
        for a, b in itertools.combinations(f, 2): E[frozenset((a, b))].append(i)
    o = [None] * len(F); o[0] = F[0]
    for start in range(len(F)):
        if o[start] is None: o[start] = F[start]
        st = [start]
        while st:
            i = st.pop(); a, b, c = o[i]
            for x, y in ((a, b), (b, c), (c, a)):
                for k in E[frozenset((x, y))]:
                    if k == i: continue
                    z = [v for v in F[k] if v not in (x, y)][0]; want = (y, x, z)
                    if o[k] is None: o[k] = want; st.append(k)
                    else:
                        cyc = [o[k][t:] + o[k][:t] for t in range(3)]
                        if want not in cyc: return False
    return True

def relabel(F):
    vs = sorted({v for f in F for v in f}); m = {v: i for i, v in enumerate(vs)}
    return len(vs), [tuple(m[v] for v in f) for f in F]

def torus(r, s):
    vid = lambda i, j: (i % r) * s + (j % s); F = []
    for i in range(r):
        for j in range(s):
            F.append((vid(i, j), vid(i + 1, j), vid(i + 1, j + 1))); F.append((vid(i, j), vid(i + 1, j + 1), vid(i, j + 1)))
    return r * s, F

def klein(r, s):
    def vid(i, j):
        if i == r: i, j = 0, -j
        return (i % r) * s + (j % s)
    F = []
    for i in range(r):
        for j in range(s):
            a, b, c, d = vid(i, j), vid(i + 1, j), vid(i + 1, j + 1), vid(i, j + 1)
            F.append((a, b, c)); F.append((a, c, d))
    return r * s, F

RP2_6 = [(0,1,2),(0,2,3),(0,3,4),(0,4,5),(0,5,1),(1,2,4),(2,3,5),(3,4,1),(4,5,2),(5,1,3)]

def connected_sum(T1, T2, rng):
    n1, F1 = T1; n2, F2 = T2
    f1 = rng.choice(F1); f2 = rng.choice(F2)
    F2s = [tuple(v + n1 for v in f) for f in F2]; f2s = tuple(v + n1 for v in f2)
    m = {f2s[0]: f1[0], f2s[1]: f1[1], f2s[2]: f1[2]}
    F = [f for f in F1 if f != f1] + [tuple(m.get(v, v) for v in f) for f in F2s if f != f2s]
    return relabel(F)

def subdivide(n, F, rng):
    i = rng.randrange(len(F)); a, b, c = F[i]; v = n
    F = F[:i] + F[i + 1:] + [(a, b, v), (b, c, v), (c, a, v)]
    return n + 1, F

class Tri:
    def __init__(self, n, F):
        self.n = n; self.F = [tuple(f) for f in F]; self.rebuild()
    def rebuild(self):
        self.E = edges_of(self.F); self.adj = collections.defaultdict(set)
        for (a, b) in self.E: self.adj[a].add(b); self.adj[b].add(a)
    def deg(self, v): return len(self.adj[v])
    def flip(self, a, b, mindeg=5, check=True):
        """flip edge ab; returns True if done."""
        key = (min(a, b), max(a, b)); fs = self.E.get(key)
        if not fs or len(fs) != 2: return False
        f1, f2 = self.F[fs[0]], self.F[fs[1]]
        c = [v for v in f1 if v not in (a, b)][0]; d = [v for v in f2 if v not in (a, b)][0]
        if c == d or d in self.adj[c]: return False
        if check and (self.deg(a) - 1 < mindeg or self.deg(b) - 1 < mindeg): return False
        i1, i2 = fs
        self.F[i1] = (a, c, d); self.F[i2] = (b, c, d); self.rebuild(); return True
    def mindeg(self): return min(self.deg(v) for v in range(self.n))

def raise_mindeg(T, rng, mindeg=5, steps=200000):
    """flip walk decreasing energy sum max(0, mindeg - deg)."""
    def en(): return sum(max(0, mindeg - T.deg(v)) for v in range(T.n))
    e = en(); t = 0
    while e > 0 and t < steps:
        t += 1
        low = [v for v in range(T.n) if T.deg(v) < mindeg]; v = rng.choice(low)
        # flip an edge of the link of v (opposite edge) to raise deg v: edge (x, y) in link of v, opposite vertex w != v
        lc = link_cycle(T.F, v); k = rng.randrange(len(lc)); x, y = lc[k], lc[(k + 1) % len(lc)]
        if T.deg(x) - 1 < 3 or T.deg(y) - 1 < 3: continue
        old = [f for f in T.F]
        if not T.flip(x, y, check=False): continue
        e2 = en()
        if e2 <= e or rng.random() < 0.05: e = e2
        else: T.F = old; T.rebuild()
    return e == 0

def random_walk(T, rng, steps, mindeg=5):
    E = list(T.E.keys())
    for _ in range(steps):
        a, b = rng.choice(list(T.E.keys())); T.flip(a, b, mindeg)
    return T

def to_line(name, n, F):
    rot = [link_cycle(F, v) for v in range(n)]
    return f"{name} {n} " + ";".join(",".join(map(str, r)) for r in rot)

def make(surface, n_target, rng):
    if surface == 'torus':
        r = rng.choice([4, 5, 6]); s = max(4, n_target // r); n, F = torus(r, s); chi = 0
    elif surface == 'klein':
        r = rng.choice([4, 5, 6]); s = max(5, n_target // r); n, F = klein(r, s); chi = 0
    elif surface == 'rp2':
        n, F = 6, list(RP2_6); chi = 1
    elif surface == 'genus2':
        n, F = connected_sum(torus(3, 4), torus(3, 4), rng); chi = -2
    elif surface == 'rp2x3':   # non-orientable genus 3 (connected sum of three projective planes)
        n, F = connected_sum(connected_sum((6, list(RP2_6)), (6, list(RP2_6)), rng), (6, list(RP2_6)), rng); chi = -1
    else: raise ValueError(surface)
    assert validate(n, F, chi) is None, (surface, validate(n, F, chi))
    while n < n_target: n, F = subdivide(n, F, rng)
    T = Tri(n, F)
    if not raise_mindeg(T, rng): return None
    random_walk(T, rng, 20 * n)
    if T.mindeg() < 5: return None
    err = validate(T.n, T.F, chi)
    if err: return None
    want_or = surface in ('torus', 'genus2')
    if orientable(T.F) != want_or: return None
    return T

if __name__ == '__main__':
    surface, count, nmin, nmax, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    rng = random.Random(seed); k = 0; tries = 0
    while k < count and tries < 50 * count:
        tries += 1; T = make(surface, rng.randint(nmin, nmax), rng)
        if T is None or not any(T.deg(v) == 5 for v in range(T.n)): continue
        print(to_line(f"{surface}_{seed}_{k}", T.n, T.F)); k += 1
