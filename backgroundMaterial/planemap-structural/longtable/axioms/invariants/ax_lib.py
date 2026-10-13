"""Axiom-discovery library (Long Table, 13 Oct 2026). Independent matching-form engine
plus candidate planar axioms evaluated on closed orbits.

Graph line format (TrackU engine): "n m a0 b0 a1 b1 ... f0 f1 f2 f3 f4" where f_i are EDGE ids
at the degree-5 vertex v in cyclic order. Vertex v = the common endpoint of the f's.
"""
import json, itertools
import networkx as nx


def parse_line(line):
    t = list(map(int, line.split()))
    n, m = t[0], t[1]
    E = [(t[2 + 2 * i], t[3 + 2 * i]) for i in range(m)]
    fv = t[2 + 2 * m: 7 + 2 * m]
    return n, E, fv


def from_json(d):
    E = [tuple(e) for e in d["edges"]]
    return d["n"], E, list(d["fv"])


class G5:
    def __init__(self, n, E, fv):
        self.n, self.E, self.fv = n, E, fv
        self.m = len(E)
        a, b = E[fv[0]]; c, d = E[fv[1]]
        self.v = a if a in (c, d) else b
        self.inc = [[] for _ in range(n)]
        for i, (x, y) in enumerate(E):
            self.inc[x].append(i); self.inc[y].append(i)
        self.fidx = {e: s for s, e in enumerate(fv)}

    def other(self, e, x):
        a, b = self.E[e]; return b if a == x else a

    # ---- perfect matchings ----
    def pms(self, allowed=None, limit=200000):
        n, E, inc = self.n, self.E, self.inc
        allowed = set(range(self.m)) if allowed is None else set(allowed)
        out = []; used = [False] * n; cur = []
        def rec():
            if len(out) >= limit: return
            best = None; bc = 99
            for x in range(n):
                if not used[x]:
                    c = sum(1 for e in inc[x] if e in allowed and not used[self.other(e, x)])
                    if c < bc: bc, best = c, x
                    if c == 0: return
            if best is None:
                out.append(frozenset(cur)); return
            x = best; used[x] = True
            for e in inc[x]:
                if e in allowed:
                    y = self.other(e, x)
                    if not used[y]:
                        used[y] = True; cur.append(e); rec(); cur.pop(); used[y] = False
            used[x] = False
        rec(); return out

    def kidx(self, M):
        for s, e in enumerate(self.fv):
            if e in M: return s
        raise ValueError

    def ncomp(self, S):
        g = nx.Graph(); g.add_nodes_from(range(self.n))
        g.add_edges_from(self.E[e] for e in S)
        return nx.number_connected_components(g)

    def loops(self, M):
        """E-M at v: return list of loops, each (fstart, fend, vertex list, edge list) traversed
        from v leaving via fstart. None if E-M not a connected figure-eight."""
        S = set(range(self.m)) - set(M)
        if self.ncomp(S) != 1: return None
        v = self.v; seen = set(); res = []
        for s in range(5):
            f = self.fv[s]
            if f in M or f in seen: continue
            verts = []; edges = [f]; seen.add(f); x = self.other(f, v); e = f
            while x != v:
                verts.append(x)
                nxt = [g for g in self.inc[x] if g in S and g != e]
                e = nxt[0]; edges.append(e); seen.add(e); x = self.other(e, x)
            res.append((s, self.fidx[e], verts, edges))
        return res

    def dl(self, M):
        k = self.kidx(M); L = self.loops(M)
        if L is None or len(L) != 2: return None
        want = {frozenset({(k - 1) % 5, (k + 1) % 5}): 'X', frozenset({(k + 2) % 5, (k - 2) % 5}): 'Y'}
        out = {}
        for (s0, s1, verts, edges) in L:
            key = frozenset({s0, s1})
            if key not in want: return None
            out[want[key]] = (s0, s1, verts, edges)
        if len(out['X'][2]) % 2 != 0 or len(out['Y'][2]) % 2 != 1: return None
        return k, out

    def orbits(self):
        P = self.pms()
        good = {M: self.dl(M) for M in P}
        good = {M: d for M, d in good.items() if d is not None}
        succ = {}
        for M, (k, _) in good.items():
            f = self.fv[(k - 2) % 5]
            c = [N for N in P if f in N and not (N & M)]
            if len(c) == 1 and c[0] in good: succ[M] = c[0]
        cyc = []; done = set()
        for M in succ:
            if M in done: continue
            path = []; x = M; pos = {}
            while x in succ and x not in pos and x not in done:
                pos[x] = len(path); path.append(x); x = succ[x]
            if x in pos: cyc.append(path[pos[x]:])
            done.update(path)
        return P, good, cyc

    def word(self, cyc):
        L = len(cyc)
        return [self.ncomp(cyc[t - 1] | cyc[t]) for t in range(L)]


def law_ok(w):
    L = len(w)
    return sum(1 for t in range(L) if (w[t] - w[t - 1]) % 2 == 0)  # number of violations


# ---------------- axioms ----------------

def planar(g5):
    g = nx.Graph(); g.add_edges_from(g5.E)
    return nx.check_planarity(g)[0]


def planar_rot(g5):
    """Planar with the given cyclic order at v (or its mirror): replace v by a 5-wheel gadget."""
    g = nx.Graph(); v = g5.v; base = g5.n
    for i, (a, b) in enumerate(g5.E):
        if i in g5.fidx:
            s = g5.fidx[i]; w = a if b == v else b
            g.add_edge(base + s, w)
        else:
            g.add_edge(a, b)
    hub = base + 5
    for s in range(5):
        g.add_edge(base + s, base + (s + 1) % 5); g.add_edge(hub, base + s)
    return nx.check_planarity(g)[0]


def ham_diagram(g5, P, M):
    """Chord diagram at a Hamiltonian state H=P∪M with v blown up (TrackT §1).
    returns (pos dict endpoint->list of positions, chords list of (e, p, q)), constraint pairs."""
    k = g5.kidx(M); v = g5.v; fv = g5.fv
    e = lambda i: fv[(k - 2 + i) % 5]
    H = set(P) | set(M)
    # walk H from v leaving via e2, returning via e4
    seq = []; x = g5.other(e(2), v); last = e(2)
    while x != v:
        seq.append(x)
        nxt = [f for f in g5.inc[x] if f in H and f != last]
        last = nxt[0]; x = g5.other(last, x)
    assert last == e(4), "H does not return via e4"
    # positions: 0..len(seq)-1 for cubic vertices, then blow-up e1,e3,e0
    pos = {x: i for i, x in enumerate(seq)}
    N = len(seq)
    vpos = {e(0): N, e(3): N + 1, e(1): N + 2}  # circle: ... seq[-1] -(e4)- e0 e3 e1 -(e2)- seq[0]
    chords = []
    for f in range(g5.m):
        if f in H: continue
        a, b = g5.E[f]
        pa = vpos[f] if a == v else pos[a]
        pb = vpos[f] if b == v else pos[b]
        chords.append((f, min(pa, pb), max(pa, pb)))
    cons = [(e(0), e(1), 0), (e(0), e(3), 1)]  # 0 = same side, 1 = opposite
    return chords, cons


def cross(c, d):
    a, b = c[1], c[2]; x, y = d[1], d[2]
    return (a < x < b < y) or (x < a < y < b)


def signed_graph(chords, cons):
    """edges with parity: crossing chords must differ (1); constraints given."""
    idx = {c[0]: i for i, c in enumerate(chords)}
    ed = []
    for i in range(len(chords)):
        for j in range(i + 1, len(chords)):
            if cross(chords[i], chords[j]): ed.append((i, j, 1))
    for (a, b, p) in cons:
        ed.append((idx[a], idx[b], p))
    return len(chords), ed


def parity_consistent(nv, ed):
    adj = [[] for _ in range(nv)]
    for a, b, p in ed: adj[a].append((b, p)); adj[b].append((a, p))
    col = [-1] * nv
    for s in range(nv):
        if col[s] >= 0: continue
        col[s] = 0; st = [s]
        while st:
            x = st.pop()
            for y, p in adj[x]:
                if col[y] < 0: col[y] = col[x] ^ p; st.append(y)
                elif col[y] != col[x] ^ p: return False
    return True


def shortest_odd_cycle(nv, ed):
    """length (#edges) of the shortest 'unbalanced' closed walk in the signed graph (odd parity sum);
    BFS on the double cover. None if balanced."""
    adj = [[] for _ in range(nv)]
    for a, b, p in ed: adj[a].append((b, p)); adj[b].append((a, p))
    best = None
    from collections import deque
    for s in range(nv):
        dist = {(s, 0): 0}; dq = deque([(s, 0)])
        while dq:
            x, q = dq.popleft()
            d = dist[(x, q)]
            if best is not None and d >= best: break
            for y, p in adj[x]:
                st = (y, q ^ p)
                if st not in dist:
                    dist[st] = d + 1; dq.append(st)
        if (s, 1) in dist:
            L = dist[(s, 1)]
            if best is None or L < best: best = L
    return best


def fig8_diagram(g5, M, dlinfo):
    """Rotation-determined outer circle of the figure-eight Q=E-M: X from its f_{k-1} end to f_{k+1}
    end, then Y from f_{k+2} end to f_{k-2} end (TrackS frame). Returns per-chord (edge, pa, pb, type)."""
    k, L = dlinfo; v = g5.v
    X = L['X']; Y = L['Y']
    def oriented(loop, start_s):
        s0, s1, verts, edges = loop
        return verts if s0 == start_s else verts[::-1]
    xs = oriented(X, (k - 1) % 5); ys = oriented(Y, (k + 2) % 5)
    pos = {}; side = {}
    for i, x in enumerate(xs): pos[x] = i; side[x] = 'X'
    for i, y in enumerate(ys): pos[y] = len(xs) + 1 + i; side[y] = 'Y'
    vX = len(xs)  # v sits between X and Y on the circle (single point is enough for M-chord at v)
    chords = []
    for f in M:
        a, b = g5.E[f]
        if v in (a, b):
            w = b if a == v else a
            chords.append((f, min(vX, pos[w]), max(vX, pos[w]), 'v' + side[w]))
        else:
            t = ''.join(sorted(side[a] + side[b]))
            chords.append((f, min(pos[a], pos[b]), max(pos[a], pos[b]), t))
    return chords, len(xs), len(ys)


def fig8_axioms(g5, M, dlinfo):
    chords, nx_, ny_ = fig8_diagram(g5, M, dlinfo)
    xy = [c for c in chords if c[3] == 'XY']
    nxycross = sum(1 for a, b in itertools.combinations(xy, 2) if cross(a, b))
    # the v-chord must go into the X disk: it must lie on X side (type vX)
    vside = [c[3] for c in chords if c[3].startswith('v')][0]
    # full 3-region 2-SAT: XX chords in {Xin, out}, YY in {Yin, out}, XY in out, v-chord in Xin.
    # variable per XX/YY chord: 1=outer. crossing pairs on the circle cannot share a region.
    var = [c for c in chords if c[3] in ('XX', 'YY')]
    import itertools as it
    clauses = []  # 2-SAT over var indices; literal (i, val) means chord i outer==val
    forced = {}
    vi = {c[0]: i for i, c in enumerate(var)}
    ok = True
    for a, b in it.combinations(chords, 2):
        if not cross(a, b): continue
        ta, tb = a[3], b[3]
        def reg(t):
            return {'XY': {'O'}, 'vX': {'X'}, 'vY': {'Y'}, 'XX': {'X', 'O'}, 'YY': {'Y', 'O'}}[t]
        # forbid same region
        for r in reg(ta) & reg(tb):
            # clause: not(a in r and b in r)
            la = None if len(reg(ta)) == 1 else (vi[a[0]], r == 'O')
            lb = None if len(reg(tb)) == 1 else (vi[b[0]], r == 'O')
            if la is None and lb is None: ok = False
            elif la is None: forced.setdefault(lb[0], set()).add(not lb[1])
            elif lb is None: forced.setdefault(la[0], set()).add(not la[1])
            else: clauses.append(((la[0], not la[1]), (lb[0], not lb[1])))
    sat = ok and two_sat(len(var), clauses, forced)
    return {'xy_cross': nxycross, 'v_into_X': vside == 'vX', 'fig8_planar': sat}


def two_sat(nv, clauses, forced):
    g = nx.DiGraph(); lit = lambda i, val: 2 * i + (1 if val else 0)
    g.add_nodes_from(range(2 * nv))
    for (a, b) in clauses:  # a or b
        g.add_edge(lit(a[0], not a[1]), lit(*b)); g.add_edge(lit(b[0], not b[1]), lit(*a))
    for i, vals in forced.items():
        if len(vals) == 2: return False
        val = next(iter(vals)); g.add_edge(lit(i, not val), lit(i, val))
    comp = {}
    for ci, scc in enumerate(nx.strongly_connected_components(g)):
        for x in scc: comp[x] = ci
    return all(comp[2 * i] != comp[2 * i + 1] for i in range(nv))


def ball_planar_radius(g5):
    """largest r such that every induced ball B_r(u) is planar (u over all vertices)."""
    g = nx.Graph(); g.add_edges_from(g5.E)
    diam = nx.diameter(g)
    for r in range(1, diam + 1):
        for u in g:
            b = nx.ego_graph(g, u, radius=r)
            if not nx.check_planarity(b)[0]:
                return r - 1, diam
    return diam, diam


def orbit_axioms(g5, cyc):
    w = g5.word(cyc); L = len(cyc)
    res = {'L': L, 'word': ''.join(map(str, w)), 'law_viol': law_ok(w)}
    ham = []; f8 = []
    for t in range(L):
        P, M = cyc[t - 1], cyc[t]
        d = g5.dl(M)
        f8.append(fig8_axioms(g5, M, d))
        if w[t] == 1:
            chords, cons = ham_diagram(g5, P, M)
            nv, ed = signed_graph(chords, cons)
            nv0, ed0 = signed_graph(chords, [])
            ham.append({'bip_rot': parity_consistent(nv, ed), 'bip': parity_consistent(nv0, ed0),
                        'oddc_rot': shortest_odd_cycle(nv, ed), 'oddc': shortest_odd_cycle(nv0, ed0)})
    res['ham'] = ham; res['fig8'] = f8
    return res
