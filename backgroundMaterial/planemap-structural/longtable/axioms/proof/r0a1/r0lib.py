"""R0 attempt 1 library (Long Table, 13 Oct 2026).  Self-contained (networkx only).

Objects.  G: n vertices, v = 0 of degree 5 with edges fv[0..4] in rotation order, all other vertices cubic.
Edges are (a, b) pairs; masks are int bitmasks over edge ids.

KEY REFORMULATION.  D = digraph on the perfect matchings of G with an arc M -> M' iff M & M' = 0 and
k(M') = k(M) - 2 (mod 5), k = index of the v-edge.  A closed R0 sequence of any length L is exactly a closed
walk in D (L = 0 mod 5 automatically), and R0 for G (all L at once) says:
    no "Hamiltonian arc" (M -> M' with M u M' a Hamiltonian cycle) lies in a strongly connected component of D.
"""
import itertools
import networkx as nx


class G5:
    def __init__(self, n, edges, fv):
        self.n, self.E, self.fv = n, list(edges), list(fv)
        self.m = len(self.E)
        self.inc = [[] for _ in range(n)]
        for i, (a, b) in enumerate(self.E):
            self.inc[a].append(i); self.inc[b].append(i)
        self.fidx = {e: s for s, e in enumerate(self.fv)}
        assert len(self.inc[0]) == 5 and all(len(self.inc[x]) == 3 for x in range(1, n)), 'degrees'

    def other(self, e, x):
        a, b = self.E[e]
        return b if a == x else a

    def pms(self):
        """all perfect matchings as bitmasks"""
        n, inc = self.n, self.inc
        out = []
        def rec(used, cur):
            # pick lowest unmatched vertex with fewest options
            best, bc = -1, 9
            for x in range(n):
                if not (used >> x) & 1:
                    c = 0
                    for e in inc[x]:
                        y = self.other(e, x)
                        if not (used >> y) & 1: c += 1
                    if c < bc: best, bc = x, c
                    if c == 0: return
            if best < 0:
                out.append(cur); return
            x = best
            for e in inc[x]:
                y = self.other(e, x)
                if not (used >> y) & 1:
                    rec(used | (1 << x) | (1 << y), cur | (1 << e))
        rec(0, 0)
        return out

    def k(self, M):
        for s, e in enumerate(self.fv):
            if (M >> e) & 1: return s
        raise ValueError

    def connected_spanning(self, S):
        """is the edge set S connected and spanning all vertices"""
        par = list(range(self.n))
        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        comps = self.n
        e = 0; s = S
        while s:
            if s & 1:
                a, b = self.E[e]; ra, rb = f(a), f(b)
                if ra != rb: par[ra] = rb; comps -= 1
            s >>= 1; e += 1
        return comps == 1

    def gadget(self):
        """v replaced by a 5-wheel (rim r_s attached to the far end of f_s): planar iff G planar with this
        rotation at v up to mirror; isomorphism of gadgets = isomorphism of (G, rotation up to dihedral)."""
        g = nx.Graph(); base = self.n
        for i, (a, b) in enumerate(self.E):
            if i in self.fidx:
                w = a if b == 0 else b
                g.add_edge(base + self.fidx[i], w)
            else:
                g.add_edge(a, b)
        hub = base + 5
        for s in range(5):
            g.add_edge(base + s, base + (s + 1) % 5); g.add_edge(hub, base + s)
        return g

    def planar_rot(self):
        return nx.check_planarity(self.gadget())[0]


def digraph(g, adv=-2):
    """PM digraph D.  returns (pms, ks, arcs list (i,j), ham set of arcs)"""
    P = g.pms()
    ks = [g.k(M) for M in P]
    byk = {s: [i for i in range(len(P)) if ks[i] == s] for s in range(5)}
    arcs, ham = [], set()
    for i, M in enumerate(P):
        for j in byk[(ks[i] + adv) % 5]:
            if M & P[j] == 0:
                arcs.append((i, j))
                if g.connected_spanning(M | P[j]): ham.add((i, j))
    return P, ks, arcs, ham


def analyse(g, adv=-2):
    P, ks, arcs, ham = digraph(g, adv)
    D = nx.DiGraph(); D.add_nodes_from(range(len(P))); D.add_edges_from(arcs)
    comp = {}
    sccs = [c for c in nx.strongly_connected_components(D)]
    for ci, c in enumerate(sccs):
        for x in c: comp[x] = ci
    cyc_sccs = [c for c in sccs if len(c) > 1]   # no loops (adv != 0)
    bad = [(i, j) for (i, j) in ham if comp[i] == comp[j]]
    return dict(P=P, ks=ks, arcs=arcs, ham=ham, D=D, sccs=sccs, comp=comp, cyc=cyc_sccs, bad=bad)


# ---------------- generators ----------------

def circle_planar(n, chords, vch):
    """circle rule of PROOF-ATTEMPT-1 s1.3: H = 0..n-1, v = 0, f0 = (0,n-1), f2 = (0,1);
    chords: list of (a,b) cubic chords; vch: {1: a1, 3: a3, 4: a4} far ends of f1, f3, f4.
    Planar with rotation f0..f4 at v (up to mirror) iff the crossing graph of the chords at positions
    1..n-1, f4 at n+.25, f1 at n+.5, f3 at n+.75 is 2-colourable with side(f1) != side(f3) = side(f4)."""
    VPOS = {4: n + .25, 1: n + .5, 3: n + .75}
    items = [tuple(sorted(c)) for c in chords] + [(vch[s], VPOS[s]) for s in (4, 1, 3)]
    names = list(range(len(chords))) + ['f4', 'f1', 'f3']
    def cross(c, d):
        a1, b1 = c; a2, b2 = d
        if len({a1, b1, a2, b2}) < 4: return False
        return (a1 < a2 < b1) != (a1 < b2 < b1)
    cg = nx.Graph(); cg.add_nodes_from(names)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if cross(items[i], items[j]): cg.add_edge(names[i], names[j])
    # constraint f1 != f3 == f4: add f1-f3 edge, and f3-f4 via a dummy path of length 2
    cg.add_edge('f1', 'f3'); cg.add_edge('f3', 'dummy'); cg.add_edge('dummy', 'f4')
    return nx.is_bipartite(cg)


def perfect_matchings_of(vs):
    if not vs:
        yield []; return
    a = vs[0]
    for i in range(1, len(vs)):
        rest = vs[1:i] + vs[i + 1:]
        for pm in perfect_matchings_of(rest):
            yield [(a, vs[i])] + pm


def normal_form_graphs(n, planar=True):
    """all chord diagrams in the Hamiltonian normal form (G simple).  yields (G5, chords, vch).
    Every (G, rot, Ham arc) with the Ham cycle through two non-adjacent v-edges appears (relabelled)."""
    H = [(i, i + 1) for i in range(n - 1)] + [(n - 1, 0)]
    cand = list(range(2, n - 1))
    for a1, a3, a4 in itertools.permutations(cand, 3):
        rest = [x for x in range(1, n) if x not in (a1, a3, a4)]
        for pm in perfect_matchings_of(rest):
            if any(abs(a - b) == 1 for a, b in pm): continue   # parallel to H edge
            vch = {1: a1, 3: a3, 4: a4}
            if planar and not circle_planar(n, pm, vch): continue
            # edges: H path edges (1..n-2), then f0=(n-1,0), f2=(0,1), chords
            edges = [(i, i + 1) for i in range(1, n - 1)]
            f0 = len(edges); edges.append((0, n - 1))
            f2 = len(edges); edges.append((0, 1))
            fe = {}
            for s in (1, 3, 4):
                fe[s] = len(edges); edges.append((0, vch[s]))
            edges += pm
            fv = [f0, fe[1], f2, fe[3], fe[4]]
            yield G5(n, edges, fv), pm, vch


def canon_key(g):
    gg = g.gadget()
    return nx.weisfeiler_lehman_graph_hash(gg, iterations=4), gg


class IsoBucket:
    def __init__(self):
        self.b = {}

    def add(self, g):
        """returns (is_new, representative index)"""
        h, gg = canon_key(g)
        lst = self.b.setdefault(h, [])
        for idx, (gg2, rep) in enumerate(lst):
            if nx.is_isomorphic(gg, gg2):
                return False, rep
        lst.append((gg, g))
        return True, g

    def reps(self):
        return [rep for lst in self.b.values() for gg, rep in lst]


def planar_normal_forms(n):
    """fast generator of the planar chord diagrams of the normal form (same output set as
    normal_form_graphs(n, planar=True)): chords are added one at a time and the side 2-colouring is
    maintained by an incremental bipartiteness check."""
    VPOS = {4: n + .25, 1: n + .5, 3: n + .75}
    def cross(c, d):
        a1, b1 = c; a2, b2 = d
        if len({a1, b1, a2, b2}) < 4: return False
        return (a1 < a2 < b1) != (a1 < b2 < b1)
    def bip(items, extra):
        # items: list of intervals; extra: list of (i, j, same?) constraints
        m = len(items)
        adj = [[] for _ in range(m)]
        for i in range(m):
            for j in range(i + 1, m):
                if cross(items[i], items[j]):
                    adj[i].append((j, 1)); adj[j].append((i, 1))
        for i, j, d in extra:
            adj[i].append((j, d)); adj[j].append((i, d))
        col = [-1] * m
        for s in range(m):
            if col[s] >= 0: continue
            col[s] = 0; st = [s]
            while st:
                x = st.pop()
                for y, d in adj[x]:
                    want = col[x] ^ d
                    if col[y] < 0: col[y] = want; st.append(y)
                    elif col[y] != want: return False
        return True
    cand = list(range(2, n - 1))
    for a1, a3, a4 in itertools.permutations(cand, 3):
        vch = {1: a1, 3: a3, 4: a4}
        base = [(a4, VPOS[4]), (a1, VPOS[1]), (a3, VPOS[3])]
        extra = [(1, 2, 1), (2, 0, 0)]   # f1 != f3, f3 == f4
        if not bip(base, extra): continue
        rest0 = [x for x in range(1, n) if x not in (a1, a3, a4)]
        def rec(rest, chords):
            if not rest:
                yield list(chords); return
            a = rest[0]
            for i in range(1, len(rest)):
                b = rest[i]
                if abs(a - b) == 1: continue
                c = (min(a, b), max(a, b))
                items = base + chords + [c]
                if not bip(items, extra): continue
                chords.append(c)
                yield from rec(rest[1:i] + rest[i + 1:], chords)
                chords.pop()
        for pm in rec(rest0, []):
            edges = [(i, i + 1) for i in range(1, n - 1)]
            f0 = len(edges); edges.append((0, n - 1))
            f2 = len(edges); edges.append((0, 1))
            fe = {}
            for s in (1, 3, 4):
                fe[s] = len(edges); edges.append((0, vch[s]))
            edges += pm
            yield G5(n, edges, [f0, fe[1], f2, fe[3], fe[4]]), pm, vch
