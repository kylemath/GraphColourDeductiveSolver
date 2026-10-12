"""Quick-and-dirty triangulation utilities: rotation from edge list, flips, vertex insertion,
random min-degree-5 triangulations of larger order (not uniform; exploratory only)."""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mass_core import validate_triangulation

def nxt(rot, a, b):  # third vertex of face on dart (a,b)
    return rot[b][(rot[b].index(a) + 1) % len(rot[b])]

def rotation_from_edges(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    cyc = []
    for v in range(n):
        N = adj[v]; link = {w: [x for x in adj[w] if x in N] for w in N}
        assert all(len(l) == 2 for l in link.values()), ("non-induced link", v)
        start = min(N); order = [start]; prev = None; cur = start
        while True:
            a, b = link[cur]; nx_ = a if a != prev else b
            if nx_ == start: break
            order.append(nx_); prev, cur = cur, nx_
        assert len(order) == len(N)
        cyc.append(order)
    rot = [None] * n; rot[0] = cyc[0]; stack = [0]
    while stack:
        v = stack.pop()
        for w in rot[v]:
            if rot[w] is not None: continue
            need = rot[v][(rot[v].index(w) - 1) % len(rot[v])]
            c = cyc[w]
            if c[(c.index(v) + 1) % len(c)] != need: c = c[::-1]
            rot[w] = c; stack.append(w)
    validate_triangulation(rot)
    return rot

def _insert_between(lst, p, q, new):
    k = len(lst)
    for i in range(k):
        if {lst[i], lst[(i + 1) % k]} == {p, q}:
            lst.insert(i + 1, new); return
    raise ValueError

def flip(rot, a, b):
    x = nxt(rot, a, b); y = nxt(rot, b, a)
    if x == y or y in rot[x]: return False
    rot2 = [list(r) for r in rot]
    rot2[a].remove(b); rot2[b].remove(a)
    _insert_between(rot2[x], a, b, y); _insert_between(rot2[y], a, b, x)
    try: validate_triangulation_loose(rot2)
    except AssertionError: return False
    rot[:] = rot2; return True

def validate_triangulation_loose(rot):
    n = len(rot); seen = set(); faces = 0
    for v, ns in enumerate(rot):
        assert len(set(ns)) == len(ns) and v not in ns and len(ns) >= 3
        assert all(v in rot[w] for w in ns)
        for w in ns:
            if (v, w) in seen: continue
            d, L = (v, w), 0
            while d not in seen:
                seen.add(d); L += 1; d = (d[1], nxt(rot, d[0], d[1]))
            assert d == (v, w) and L == 3; faces += 1
    assert n - sum(map(len, rot)) // 2 + faces == 2

def insert_vertex(rot, a, b):
    c = nxt(rot, a, b); v = len(rot)
    rot2 = [list(r) for r in rot] + [[a, b, c]]
    _insert_between(rot2[a], b, c, v); _insert_between(rot2[b], a, c, v); _insert_between(rot2[c], a, b, v)
    try: validate_triangulation_loose(rot2)
    except AssertionError:
        rot2[v] = [a, c, b]; validate_triangulation_loose(rot2)
    rot[:] = rot2; return v

def grow(rot, target_n, rng, mix=200):
    rot = [list(r) for r in rot]
    while len(rot) < target_n:
        for _ in range(1000):
            a = rng.randrange(len(rot)); b = rng.choice(rot[a])
            snap = [list(r) for r in rot]
            v = insert_vertex(rot, a, b)
            ok = True
            for _ in range(2):  # raise degree of v from 3 to 5
                cand = []
                for x in rot[v]:
                    y = nxt(rot, v, x)  # face v,x,y ; edge x-y opposite v
                    if len(rot[x]) >= 6 and len(rot[y]) >= 6: cand.append((x, y))
                rng.shuffle(cand)
                if not any(flip(rot, x, y) for x, y in cand): ok = False; break
            if ok and min(map(len, rot)) >= 5: break
            rot[:] = snap
        else:
            raise RuntimeError("stuck")
        mixflips(rot, rng, mix)
    validate_triangulation(rot)
    return rot

def mixflips(rot, rng, k):
    for _ in range(k):
        a = rng.randrange(len(rot)); b = rng.choice(rot[a])
        if len(rot[a]) >= 6 and len(rot[b]) >= 6: flip(rot, a, b)
