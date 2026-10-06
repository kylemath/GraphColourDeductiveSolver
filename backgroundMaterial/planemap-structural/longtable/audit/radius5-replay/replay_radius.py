#!/usr/bin/env python3
"""Independent audit replay of radius certificates (stdlib only; imports no team code).

Definitions (MathConjectureR §1; MathConfinementAttack Step 1):
  state      proper 4-colouring of T - h, h a degree-5 hole, up to renaming of colours;
  filled     the link of h uses at most 3 colours;
  radius     least number of whole-component Kempe swaps of T - h (singletons allowed) to a
             filled state, found by breadth-first search over canonical states;
  DL         link (in cyclic order x0..x4) uses 4 colours with repeat at x_j, x_{j+2}; with
             m = x_{j+1}, a = x_{j+3}, b = x_{j+4}: m ~ a in the {c(m),c(a)} subgraph of T - h and
             m ~ b in the {c(m),c(b)} subgraph.
Core class checks: sphere triangulation (2n-4 faces, 3n-6 edges, every edge in exactly two faces,
every vertex link a single cycle, Euler), minimum degree 5, no separating triangle (every 3-clique
is a face).

usage:
  replay_radius.py selftest
      T4 regression (MathConjectureR faces, hole 4): radius histogram over all states must be
      {0:22, 1:25, 2:15, 3:4, 4:2}; a radius-4 state must certify at 4 and fail at 5.
  replay_radius.py cert GRAPH.json HOLE STATE.json EXPECTED
      GRAPH.json = {"faces": [[a,b,c], ...]}; STATE.json = {"v": colour, ...} on T - HOLE.
      Prints JSON; "pass" is true iff core class, proper, DL, and radius == EXPECTED.
  replay_radius.py iso GRAPH1.json HOLE1 GRAPH2.json HOLE2
      Isomorphism of (T1, h1) and (T2, h2) as plane triangulations with the hole fixed
      (reflection allowed), by canonical planar codes.
"""
import json, sys
from itertools import combinations
from collections import deque

CAP = 5_000_000

T4_FACES = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),
            (3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),
            (8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]


def graph_from_faces(faces):
    faces = [tuple(int(x) for x in f) for f in faces]
    V = sorted({v for f in faces for v in f})
    adj = {v: set() for v in V}
    for a, b, c in faces:
        assert len({a, b, c}) == 3, ('degenerate face', (a, b, c))
        adj[a] |= {b, c}; adj[b] |= {a, c}; adj[c] |= {a, b}
    return V, adj, faces


def core_check(V, adj, faces):
    n = len(V); E = sum(len(s) for s in adj.values()) // 2
    out = dict(order=n, edges=E, faces=len(faces))
    fs = {frozenset(f) for f in faces}
    edge_faces = {}
    for f in faces:
        for e in combinations(f, 2):
            edge_faces[frozenset(e)] = edge_faces.get(frozenset(e), 0) + 1
    out['faces_distinct'] = len(fs) == len(faces)
    out['every_edge_in_two_faces'] = all(edge_faces.get(frozenset((u, w)), 0) == 2 for u in V for w in adj[u])
    out['edges_equal_face_edges'] = len(edge_faces) == E
    # vertex links are single cycles
    def link_cycle(v):
        nb = {u: set() for u in adj[v]}
        for f in faces:
            if v in f:
                a, b = [x for x in f if x != v]
                nb[a].add(b); nb[b].add(a)
        if any(len(s) != 2 for s in nb.values()):
            return None
        start = min(nb); cyc = [start]; prev = None; cur = start
        while True:
            nxt = [x for x in nb[cur] if x != prev]
            nxt = nxt[0] if prev is not None else min(nb[cur])
            if nxt == start: break
            cyc.append(nxt); prev, cur = cur, nxt
            if len(cyc) > len(nb): return None
        return cyc if len(cyc) == len(nb) else None
    links = {v: link_cycle(v) for v in V}
    out['links_are_cycles'] = all(links[v] is not None for v in V)
    out['euler'] = n - E + len(faces) == 2
    out['counts'] = len(faces) == 2 * n - 4 and E == 3 * n - 6
    out['min_degree'] = min(len(adj[v]) for v in V)
    sep = [t for t in combinations(V, 3)
           if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]] and frozenset(t) not in fs]
    out['separating_triangles'] = len(sep)
    out['core'] = (out['faces_distinct'] and out['every_edge_in_two_faces'] and out['edges_equal_face_edges']
                   and out['links_are_cycles'] and out['euler'] and out['counts']
                   and out['min_degree'] >= 5 and not sep)
    return out, links


class Hole:
    def __init__(self, V, adj, h, link):
        self.h = h; self.order = [v for v in V if v != h]
        self.idx = {v: i for i, v in enumerate(self.order)}
        self.nb = [[self.idx[w] for w in adj[v] if w != h] for v in self.order]
        self.link = [self.idx[x] for x in link]          # cyclic order around h

    def canon(self, col):
        ren = {}; return tuple(ren.setdefault(c, len(ren)) for c in col)

    def comp(self, col, s, p, q):
        seen = {s}; st = [s]
        while st:
            a = st.pop()
            for b in self.nb[a]:
                if b not in seen and col[b] in (p, q):
                    seen.add(b); st.append(b)
        return seen

    def neighbours(self, col):
        for p in range(4):
            for q in range(p + 1, 4):
                done = set()
                for s in range(len(col)):
                    if col[s] in (p, q) and s not in done:
                        K = self.comp(col, s, p, q); done |= K
                        new = list(col)
                        for v in K: new[v] = q if col[v] == p else p
                        yield self.canon(new)

    def filled(self, col):
        return len({col[x] for x in self.link}) <= 3

    def dl(self, col):
        L = self.link; lc = [col[x] for x in L]
        if len(set(lc)) != 4: return False
        j = next(j for j in range(5) if lc[j] == lc[(j + 2) % 5])
        m, a, b = L[(j + 1) % 5], L[(j + 3) % 5], L[(j + 4) % 5]
        return (a in self.comp(col, m, col[m], col[a])) and (b in self.comp(col, m, col[m], col[b]))

    def proper(self, col):
        return all(col[u] != col[w] for u in range(len(col)) for w in self.nb[u])

    def radius(self, col):
        s = self.canon(col); dist = {s: 0}; q = deque([s]); layers = [1]
        while q:
            c = q.popleft(); d = dist[c]
            if self.filled(c): return d, layers, len(dist)
            for t in self.neighbours(c):
                if t not in dist:
                    if len(dist) >= CAP: return None, layers, len(dist)
                    dist[t] = d + 1; q.append(t)
                    if d + 1 >= len(layers): layers.append(0)
                    layers[d + 1] += 1
        return float('inf'), layers, len(dist)       # Kempe class exhausted, no fill: targetless


def cert(faces, h, state, expected):
    V, adj, faces = graph_from_faces(faces)
    core, links = core_check(V, adj, faces)
    out = dict(core=core, hole=h, hole_degree=len(adj[h]))
    H = Hole(V, adj, h, links[h])
    col = [int(state[str(v)]) if str(v) in state else int(state[v]) for v in H.order]
    out['state_covers_T_minus_h'] = sorted(int(k) for k in state) == H.order
    out['colours_in_0_3'] = all(0 <= c < 4 for c in col)
    out['proper'] = H.proper(col)
    out['link_colours'] = [col[x] for x in H.link]
    out['link_degrees'] = [len(adj[x]) for x in links[h]]
    out['filled'] = H.filled(col)
    out['doubly_locked'] = H.dl(col)
    r, layers, explored = H.radius(col)
    out['radius'] = r; out['bfs_layers'] = layers; out['states_explored'] = explored
    out['expected'] = expected
    out['pass'] = bool(core['core'] and len(adj[h]) == 5 and out['state_covers_T_minus_h'] and out['colours_in_0_3']
                       and out['proper'] and out['doubly_locked'] and r == expected)
    return out


def all_states(V, adj, h):
    order = [v for v in V if v != h]; pos = {v: i for i, v in enumerate(order)}
    prev = [[pos[w] for w in adj[v] if w != h and pos[w] < pos[v]] for v in order]
    col = [0] * len(order); res = []
    def rec(i, used):
        if i == len(order): res.append(tuple(col)); return
        forb = {col[w] for w in prev[i]}
        for c in range(min(used + 1, 4)):
            if c not in forb: col[i] = c; rec(i + 1, max(used, c + 1))
    rec(0, 0)
    return order, res


def selftest():
    V, adj, faces = graph_from_faces(T4_FACES)
    core, links = core_check(V, adj, faces)
    H = Hole(V, adj, 4, links[4])
    order, states = all_states(V, adj, 4)
    assert order == H.order
    hist = {}; r4 = None
    for s in states:
        r = H.radius(list(s))[0]; hist[r] = hist.get(r, 0) + 1
        if r == 4 and r4 is None: r4 = s
    st = {str(v): r4[i] for i, v in enumerate(H.order)}
    ok4 = cert(T4_FACES, 4, st, 4)['pass']; ok5 = cert(T4_FACES, 4, st, 5)['pass']
    res = dict(t4_core=core['core'], t4_states=len(states), t4_hist={str(k): v for k, v in sorted(hist.items())},
               expected_hist={'0': 22, '1': 25, '2': 15, '3': 4, '4': 2},
               radius4_state_certifies_at_4=ok4, radius4_state_fails_at_5=not ok5)
    res['selftest_pass'] = (res['t4_core'] and res['t4_hist'] == res['expected_hist'] and len(states) == 68
                            and ok4 and not ok5)
    return res


def orient(faces):
    """Consistently oriented faces (by propagation across edges), then rotation next[v][a] = b."""
    faces = [tuple(f) for f in faces]
    ef = {}
    for f in faces:
        for e in combinations(f, 2): ef.setdefault(frozenset(e), []).append(f)
    o = {frozenset(faces[0]): faces[0]}; q = [faces[0]]
    while q:
        p, r, s = q.pop()
        for (x, y) in ((p, r), (r, s), (s, p)):
            for g in ef[frozenset((x, y))]:
                k = frozenset(g)
                if k in o: continue
                z = (set(g) - {x, y}).pop(); o[k] = (y, x, z); q.append((y, x, z))
    assert len(o) == len(faces), 'faces not connected'
    nxt = {}
    for (p, r, s) in o.values():
        for (a, b, c) in ((p, r, s), (r, s, p), (s, p, r)):
            assert b not in nxt.setdefault(a, {}), 'inconsistent orientation'
            nxt[a][b] = c
    return nxt


def code(nxt, h, u0):
    num = {h: 0}; order = [h]; first = {h: u0}; out = []; i = 0
    while i < len(order):
        v = order[i]; i += 1; s = first[v]; w = s; row = []
        while True:
            if w not in num: num[w] = len(order); order.append(w); first[w] = v
            row.append(num[w]); w = nxt[v][w]
            if w == s: break
        out.append(tuple(row))
    return tuple(out)


def iso_code(faces, h):
    nxt = orient(faces)
    prv = {v: {b: a for a, b in d.items()} for v, d in nxt.items()}
    return min(code(r, h, u) for r in (nxt, prv) for u in nxt[h])


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'selftest':
        print(json.dumps(selftest()))
    elif mode == 'cert':
        g = json.load(open(sys.argv[2])); st = json.load(open(sys.argv[4]))
        print(json.dumps(cert(g['faces'], int(sys.argv[3]), st, int(sys.argv[5])), default=str))
    elif mode == 'iso':
        f1 = json.load(open(sys.argv[2]))['faces']; f2 = json.load(open(sys.argv[4]))['faces']
        c1 = iso_code(f1, int(sys.argv[3])); c2 = iso_code(f2, int(sys.argv[5]))
        print(json.dumps(dict(isomorphic_with_hole_fixed=c1 == c2, order1=len(c1), order2=len(c2))))
