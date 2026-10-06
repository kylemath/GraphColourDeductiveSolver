#!/usr/bin/env python3
"""lattack_witness.py -- explicit planar witness for a chain of length 6 (team L-Attack), self-contained re-check.
Does NOT import lattack_verify: all checks re-implemented below (union of two checks).  Standard library only.
Graph: 20-vertex plane triangulation (36 oriented faces), hole v=16 (degree 5), colouring of T-v with colours 0..3."""
import itertools
FACES = [[1, 16, 5], [2, 4, 6], [2, 33, 22], [3, 16, 8], [4, 2, 22], [4, 14, 21], [4, 22, 14], [5, 31, 1], [5, 33, 6], [6, 4, 11], [6, 10, 20], [6, 11, 34], [6, 20, 5], [6, 33, 2], [8, 13, 17], [8, 14, 3], [9, 14, 8], [10, 1, 31], [10, 6, 34], [11, 10, 34], [11, 17, 13], [13, 1, 10], [13, 8, 16], [13, 10, 11], [14, 17, 21], [16, 1, 13], [16, 3, 5], [17, 9, 8], [17, 11, 21], [17, 14, 9], [20, 31, 5], [21, 11, 4], [22, 3, 14], [31, 20, 10], [33, 3, 22], [33, 5, 3]]
V = 16
COL = dict([[1, 2], [2, 2], [3, 2], [4, 0], [5, 0], [6, 3], [8, 3], [9, 2], [10, 0], [11, 2], [13, 1], [14, 1], [17, 0], [20, 1], [21, 3], [22, 3], [31, 3], [33, 1], [34, 1]])

A3_FACES = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 1), (1, 6, 2), (2, 7, 3), (3, 8, 4), (4, 9, 5), (5, 10, 1), (6, 7, 2), (6, 11, 7), (7, 8, 3), (7, 12, 8), (8, 9, 4), (8, 13, 9), (9, 10, 5), (9, 14, 10), (10, 6, 1), (10, 15, 6), (11, 12, 7), (12, 13, 8), (13, 14, 9), (14, 15, 10), (15, 11, 6), (16, 11, 15), (16, 12, 11), (16, 13, 12), (16, 14, 13), (16, 15, 14)]
A3_V = 0
A3_COL = dict([(1, 0), (2, 1), (3, 0), (4, 2), (5, 3), (6, 2), (7, 3), (8, 1), (9, 0), (10, 1), (11, 0), (12, 2), (13, 3), (14, 2), (15, 3), (16, 1)])

def main(FACES=FACES, V=V, COL=COL, steps=8):
    # 1. combinatorial map checks: every directed edge in exactly one face, orientable closed surface, Euler = 2
    de = {}
    for f in FACES:
        for i in range(3):
            e = (f[i], f[(i + 1) % 3]); assert e not in de, ("directed edge twice", e); de[e] = f
    assert all((b, a) in de for (a, b) in de), "boundary edge"
    verts = {x for f in FACES for x in f}; E = len(de) // 2
    assert len(verts) - E + len(FACES) == 2, "Euler"
    assert all(len(set(f)) == 3 for f in FACES)
    adj = {u: set() for u in verts}
    for (a, b) in de: adj[a].add(b)
    # vertex links must be single cycles (genuine sphere, not pinched)
    for u in verts:
        nxt = {f[(i + 1) % 3]: f[(i + 2) % 3] for f in FACES for i in range(3) if f[i] == u}
        x = next(iter(nxt)); c = 1; y = nxt[x]
        while y != x: y = nxt[y]; c += 1
        assert c == len(nxt) == len(adj[u]), "pinched link at %d" % u
    # no multi-edges by construction (adjacency sets); triangulation simple => each edge in two faces, checked above
    assert len(adj[V]) == 5
    # 2. link in cyclic order
    nxt = {f[(i + 1) % 3]: f[(i + 2) % 3] for f in FACES for i in range(3) if f[i] == V}
    link = [next(iter(nxt))]
    while len(link) < 5: link.append(nxt[link[-1]])
    assert nxt[link[-1]] == link[0]
    # 3. colouring proper on T - v
    for u in verts - {V}:
        for w in adj[u] - {V}: assert COL[u] != COL[w]
    # 4. chain
    def comp(col, s, pair):
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w != V and w not in seen and col[w] in pair: seen.add(w); st.append(w)
        return seen
    def path(col, s, t, pair):
        par = {s: None}; q = [s]
        for u in q:
            for w in adj[u]:
                if w != V and w not in par and col[w] in pair: par[w] = u; q.append(w)
        if t not in par: return None
        p = [t]
        while par[p[-1]] is not None: p.append(par[p[-1]])
        return p[::-1]
    col = dict(COL); k = 0
    while True:
        cs = [col[x] for x in link]
        assert len(set(cs)) == 4, ("link lost a colour at step", k)
        js = [j for j in range(5) if cs[j] == cs[(j + 2) % 5]]; assert len(js) == 1; j = js[0]
        m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
        p1 = path(col, m, a, {col[m], col[a]}); p2 = path(col, m, b, {col[m], col[b]})
        print("step", k, "link colours", cs, "repeat idx", j, "locks:", "P=%s" % p1, "Q=%s" % p2)
        if p1 is None or p2 is None: print("NOT doubly locked at step", k); break
        for p, pr in ((p1, {col[m], col[a]}), (p2, {col[m], col[b]})):
            assert all(col[x] in pr for x in p) and all(p[i + 1] in adj[p[i]] for i in range(len(p) - 1))
        k += 1
        al, c = col[link[j]], col[link[(j + 3) % 5]]
        K = comp(col, link[(j + 2) % 5], {al, c})
        assert link[j] not in K  # Theorem A, step 2 (consistency check)
        col = {u: ((c if col[u] == al else al) if u in K else col[u]) for u in col}
        if k == steps: break
    print("chain length (doubly locked iterates s..F^(n-1)s):", k)
if __name__ == "__main__":
    print("== W6: 20-vertex witness found by lattack_search (hc tag b) ==")
    main()
    print("== A3 period check (self-contained) ==")
    _adj = {}
    for f in A3_FACES:
        for a in f: _adj.setdefault(a, set()).update(x for x in f if x != a)
    _nx = {f[(i + 1) % 3]: f[(i + 2) % 3] for f in A3_FACES for i in range(3) if f[i] == A3_V}
    _link = [next(iter(_nx))]
    while len(_link) < 5: _link.append(_nx[_link[-1]])
    def _comp(col, s, pair):
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for w in _adj[u]:
                if w != A3_V and w not in seen and col[w] in pair: seen.add(w); st.append(w)
        return seen
    def _locked(col):
        cs = [col[x] for x in _link]
        if len(set(cs)) != 4: return False
        j = [j for j in range(5) if cs[j] == cs[(j + 2) % 5]][0]
        m, a, b = _link[(j + 1) % 5], _link[(j + 3) % 5], _link[(j + 4) % 5]
        return a in _comp(col, m, {col[m], col[a]}) and b in _comp(col, m, {col[m], col[b]})
    def _F(col):
        cs = [col[x] for x in _link]; j = [j for j in range(5) if cs[j] == cs[(j + 2) % 5]][0]
        al, c = cs[j], cs[(j + 3) % 5]; K = _comp(col, _link[(j + 2) % 5], {al, c})
        return {u: ((c if col[u] == al else al) if u in K else col[u]) for u in col}
    s = dict(A3_COL); seen = {}; k = 0
    while True:
        key = tuple(sorted(s.items()))
        if key in seen: print("F-orbit is periodic: state", k, "= state", seen[key], "; all", k, "states doubly locked => chain length infinite"); break
        assert _locked(s); seen[key] = k; s = _F(s); k += 1
    print("== A3: 17-vertex stacked antiprism (degrees 5,6), 45 steps (cap) ==")
    main(A3_FACES, A3_V, A3_COL, steps=45)
