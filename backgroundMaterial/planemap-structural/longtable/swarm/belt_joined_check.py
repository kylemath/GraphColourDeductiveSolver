"""Independent check of the joined belt argument (belt-joined.md) on G_5, G_8, G_11 only.

G_n: poles a, b; belt u_i, v_i (i mod n); edges a-u_i, b-v_i, u_i-u_{i+1},
v_i-v_{i+1}, u_i-v_i, u_i-v_{i-1}.  No a-b edge.

Moves on (hole h, proper colouring of G_n - h):
  slide: a neighbour x of h whose colour occurs once on N(h): h gets c(x), x becomes the hole;
  Kempe: swap the two colours on one bichromatic component of G_n - h (hole fixed).
Filled: N(hole) uses <= 3 colours.

What is checked (nothing here imports the team's earlier code):
 1. Edge count 6n = 3|V|-6, belt degrees 5, pole degrees n; the maps rotation r,
    ring swap s and reflection R are automorphisms (so hole u_0 represents every
    belt hole, and hole a represents both pole holes).
 2. Every proper colouring of G_n - u_0 (orbits under colour permutation):
    - equal poles: the one star swap of TwoPoleStarEscape.md fills;
    - unequal poles: the deterministic walk of belt-joined.md is executed: every
      start is classified into an opening row of the table, every later state
      into a row of the step table, every forced colour asserted, every slide
      checked to be legal, landing indices checked monotone in the linear range,
      and the walk must end filled.  Uncovered states raise.
    - independently, BFS by slides only (unequal) / slides+Kempe (equal).
 3. Every proper colouring of G_n - a: filled / singleton on the u-ring (then one
    slide to a belt hole, followed by the belt walk) / no singleton (BFS with
    slides and Kempe swaps; also: does one Kempe swap at the pole suffice?).
 4. Kempe connectivity of all colourings of G_n - a (Florek Thm 3.1 at these n).
Do not run with n >= 14 (team rule).
"""
from __future__ import annotations

import sys
from collections import deque

H = -1  # hole marker


class Belt:
    def __init__(self, n):
        assert 5 <= n <= 11, "team rule: n <= 11 only (residues 6,7,9,10 added 5 Oct); never n >= 14"
        self.n = n
        self.N = 2 * n + 2
        self.a, self.b = 0, 1
        self.adj = [set() for _ in range(self.N)]
        for i in range(n):
            self._e(self.a, self.U(i)); self._e(self.b, self.V(i))
            self._e(self.U(i), self.U(i + 1)); self._e(self.V(i), self.V(i + 1))
            self._e(self.U(i), self.V(i)); self._e(self.U(i), self.V(i - 1))
        self.adj = [sorted(s) for s in self.adj]
        self.edges = [(x, y) for x in range(self.N) for y in self.adj[x] if x < y]

    def _e(self, x, y):
        self.adj[x].add(y); self.adj[y].add(x)

    def U(self, i):
        return 2 + (i % self.n)

    def V(self, i):
        return 2 + self.n + (i % self.n)

    def name(self, x):
        if x == 0: return "a"
        if x == 1: return "b"
        if x < 2 + self.n: return f"u{x-2}"
        return f"v{x-2-self.n}"

    # automorphisms as vertex maps
    def rot(self):
        n = self.n
        m = [0, 1] + [self.U(i + 1) for i in range(n)] + [self.V(i + 1) for i in range(n)]
        return m

    def swap(self):
        n = self.n
        m = [1, 0] + [self.V(-i) for i in range(n)] + [self.U(-i) for i in range(n)]
        return m

    def refl(self):
        n = self.n
        m = [0, 1] + [self.U(-i) for i in range(n)] + [self.V(-1 - i) for i in range(n)]
        return m

    def is_aut(self, m):
        es = set(self.edges)
        return len(set(m)) == self.N and all(((min(m[x], m[y]), max(m[x], m[y])) in es) for x, y in self.edges)


# ---------------------------------------------------------------- basics
def proper(G, col):
    return all(col[x] == H or col[y] == H or col[x] != col[y] for x, y in G.edges)


def hole_of(col):
    return col.index(H)


def link_cols(G, col, h):
    return [col[x] for x in G.adj[h]]


def filled(G, col):
    h = hole_of(col)
    return len(set(link_cols(G, col, h))) <= 3


def normal(col):
    """first-occurrence normal form, hole kept as H"""
    mp, out = {}, []
    for c in col:
        if c == H:
            out.append(H)
            continue
        if c not in mp:
            mp[c] = len(mp)
        out.append(mp[c])
    return tuple(out)


def enumerate_deletion(G, h):
    """all proper colourings of G-h in first-occurrence normal form (vertex order 0..N-1)"""
    order = [x for x in range(G.N) if x != h]
    col = [None] * G.N
    col[h] = H
    res = []

    def rec(k, mx):
        if k == len(order):
            res.append(tuple(col)); return
        x = order[k]
        for c in range(min(mx + 2, 4)):
            if all(col[y] != c for y in G.adj[x] if col[y] is not None):
                col[x] = c
                rec(k + 1, max(mx, c))
                col[x] = None

    rec(0, -1)
    return res


def orbit_size(col):
    k = len(set(c for c in col if c != H))
    s = 1
    for j in range(k):
        s *= 4 - j
    return s


def slide_moves(G, col):
    h = hole_of(col)
    lk = link_cols(G, col, h)
    out = []
    for x in G.adj[h]:
        if lk.count(col[x]) == 1:
            c = list(col); c[h] = col[x]; c[x] = H
            out.append((x, tuple(c)))
    return out


def kempe_components(G, col):
    """list of (pair, component) for every bichromatic component"""
    out = []
    for p in range(4):
        for q in range(p + 1, 4):
            seen = set()
            for x in range(G.N):
                if col[x] in (p, q) and x not in seen:
                    comp, st = [], [x]
                    seen.add(x)
                    while st:
                        y = st.pop(); comp.append(y)
                        for z in G.adj[y]:
                            if z not in seen and col[z] in (p, q):
                                seen.add(z); st.append(z)
                    out.append(((p, q), comp))
    return out


def kempe_moves(G, col):
    out = []
    for (p, q), comp in kempe_components(G, col):
        c = list(col)
        for y in comp:
            c[y] = q if col[y] == p else p
        out.append(tuple(c))
    return out


def bfs_fill(G, start, kempe, cap=200000):
    """shortest number of moves to a filled state; None if not reached within cap"""
    s0 = normal(start)
    if filled(G, s0):
        return 0, 1
    dist = {s0: 0}
    dq = deque([s0])
    while dq:
        s = dq.popleft()
        nxt = [c for _, c in slide_moves(G, s)]
        if kempe:
            nxt += kempe_moves(G, s)
        for c in nxt:
            c = normal(c)
            if c in dist:
                continue
            dist[c] = dist[s] + 1
            if filled(G, c):
                return dist[c], len(dist)
            if len(dist) > cap:
                return None, len(dist)
            dq.append(c)
    return None, len(dist)


# ---------------------------------------------------------------- the hand walk
class Uncovered(Exception):
    pass


class Walker:
    """Executes the deterministic walk of belt-joined.md on a colouring with hole u_0,
    c(a)=0, c(b)=1.  Asserts every forced colour stated in the table."""

    def __init__(self, G, col):
        self.G = G
        self.col = list(col)
        self.slides = 0
        self.trace = []
        self.phis = []

    def check_interval(self, kind, j):
        """the linear unprocessed interval carries input colours; record potential Phi"""
        G, n = self.G, self.G.n
        if kind == "Z":
            I = [G.V(k) for k in range(0, j)] + [G.U(k) for k in range(1, j + 1)]
        else:
            I = [G.V(k) for k in range(j, n)] + [G.U(k) for k in range(j + 1, n)]
        for x in I:
            self.need(self.col[x] == self.input[x], f"interval vertex {G.name(x)} changed")
        if self.phis:
            self.need(self.phis[-1] - len(I) in (4, 6), "potential did not drop by 4 or 6")
        self.phis.append(len(I))

    def c(self, x):
        return self.col[x]

    def need(self, cond, msg):
        if not cond:
            raise Uncovered(msg + " | " + self.show())

    def show(self):
        G = self.G
        return " ".join(f"{G.name(x)}={'H' if self.col[x]==H else self.col[x]}" for x in range(G.N))

    def slide(self, x):
        G, col = self.G, self.col
        h = hole_of(col)
        self.need(x in G.adj[h], f"slide target {G.name(x)} not adjacent to hole {G.name(h)}")
        lk = link_cols(G, col, h)
        self.need(lk.count(col[x]) == 1, f"illegal slide {G.name(h)}->{G.name(x)}")
        col[h] = col[x]; col[x] = H
        self.slides += 1
        self.need(proper(G, col), "improper after slide")

    def is_filled(self):
        return filled(self.G, self.col)

    # ---- downward Z-walk: hole v_i with c(v_{i+1}) = 0
    def zwalk(self, i, family):
        G, n = self.G, self.n
        U, V, c = G.U, G.V, self.c
        rho_family = None
        last = i
        while True:
            self.need(hole_of(self.col) == V(i), "hole is not v_i")
            self.need(c(V(i + 1)) == 0, "Z-state needs c(v_{i+1})=0")
            self.need(1 <= i <= n - 2, f"landing index {i} outside linear range [1,n-2]")
            self.check_interval("Z", i)
            if self.is_filled():
                self.trace.append(f"Z{i}:filled")
                return
            w, x, y = c(U(i + 1)), c(V(i - 1)), c(U(i))
            if w == 1:
                raise Uncovered("Q-state reached (not used by this proof's openings)")
            rho = w; tau = 5 - rho
            if family == "S":
                if rho_family is None:
                    rho_family = rho
                self.need(rho == rho_family, "S-family changed its trailing colour")
            if x == 0 and y == tau:
                self.need(family == "S0", "S0 row reached outside the S0 family")
                self.trace.append(f"S0@{i}")
                self.slide(U(i))                      # writes tau on v_i
                if c(U(i - 1)) == rho:
                    self.need(self.is_filled(), "S0: u_{i-1}=rho should fill"); self.trace.append("fill"); return
                self.need(c(U(i - 1)) == 1, "S0: u_{i-1} forced in {1,rho}")
                self.slide(U(i - 1))
                p, q = c(V(i - 2)), c(U(i - 2))
                self.need({p, q} == {2, 3}, "S0: v_{i-2},u_{i-2} forced {2,3}")
                self.slide(V(i - 2))
                self.need(c(V(i - 3)) == 0, "S0: v_{i-3} forced 0")
                nxt = i - 2
            elif x == tau and y == 1:
                self.need(family == "S", "S_tau1 outside S family")
                self.trace.append(f"Sτ1@{i}")
                self.need(c(U(i - 1)) == rho and c(V(i - 2)) == 0, "S_tau1 forced u_{i-1}=rho, v_{i-2}=0")
                self.slide(V(i - 1)); self.slide(V(i - 2))
                nxt = i - 2
            elif x == rho and y == tau:
                self.need(family == "S", "S_rhotau outside S family")
                self.need(c(U(i - 1)) == 1, "S_rhotau forced u_{i-1}=1")
                self.slide(U(i)); self.slide(U(i - 1))
                if c(V(i - 2)) == 0:
                    if c(U(i - 2)) == rho:
                        self.trace.append(f"Sρτ-A@{i}:fill")
                        self.need(self.is_filled(), "A_rho: u_{i-2}=rho should fill"); return
                    self.need(c(U(i - 2)) == tau, "A_rho: u_{i-2} forced in {rho,tau}")
                    self.trace.append(f"Sρτ-A@{i}")
                    self.slide(V(i - 1)); self.slide(V(i - 2))
                    self.need(c(V(i - 3)) == rho, "A_rho return: v_{i-3} forced rho")
                    nxt = i - 2
                else:
                    self.need(c(V(i - 2)) == tau, "S_rhotau: v_{i-2} forced in {0,tau}")
                    self.need(c(U(i - 2)) == rho and c(V(i - 3)) == 0, "B: forced u_{i-2}=rho, v_{i-3}=0")
                    self.trace.append(f"Sρτ-B@{i}")
                    self.slide(V(i - 2)); self.slide(V(i - 3))
                    nxt = i - 3
            else:
                raise Uncovered(f"Z-state not in table: w={w} x={x} y={y}")
            self.need(nxt < last, "landing index did not decrease")
            last = i = nxt

    # ---- upward D-walk (audit lemma): hole u_i, link (a,u_{i+1},v_i,v_{i-1},u_{i-1}) = (0,1,rho,tau,1)
    def dwalk(self, i):
        G, n = self.G, self.n
        U, V, c = G.U, G.V, self.c
        last = i - 1
        while True:
            self.need(hole_of(self.col) == U(i), "D: hole not u_i")
            self.need(0 <= i <= n - 2, f"D landing {i} outside linear range [0,n-2]")
            self.need(i > last, "D index did not increase")
            self.check_interval("D", i)
            rho, tau = c(V(i)), c(V(i - 1))
            self.need(c(U(i + 1)) == 1 and c(U(i - 1)) == 1 and {rho, tau} == {2, 3}, "D-state shape")
            self.trace.append(f"D@{i}")
            self.slide(V(i))
            if c(V(i + 1)) == tau:
                self.need(self.is_filled(), "D: x=tau should fill"); self.trace.append("fill"); return
            self.need(c(V(i + 1)) == 0, "D: x forced in {0,tau}")
            self.slide(V(i + 1))
            p = c(U(i + 2)); q = c(V(i + 2))
            self.need({p, q} == {2, 3} and c(U(i + 3)) == 1, "D: forced p,q,u_{i+3}=1")
            self.slide(U(i + 2))
            last, i = i, i + 2

    @property
    def n(self):
        return self.G.n

    def run(self):
        G, n = self.G, self.n
        U, V, c = G.U, G.V, self.c
        self.need(c(0) == 0 and c(1) == 1 and hole_of(self.col) == U(0), "walk precondition")
        if self.is_filled():
            return "F0"
        p, q, r, s = c(U(1)), c(V(0)), c(V(n - 1)), c(U(n - 1))
        refl = False
        if q == 0 or (q in (2, 3) and r in (2, 3) and p == r and s == 1):
            R = G.refl()
            self.col = [self.col[R[x]] for x in range(G.N)]   # c' = c o R
            refl = True
            p, q, r, s = c(U(1)), c(V(0)), c(V(n - 1)), c(U(n - 1))
        self.input = list(self.col)
        tag = "R" if refl else ""
        if q in (2, 3) and r in (2, 3):
            if p == 1 and s == q:
                case = "O1"
                self.slide(V(n - 1))
                self.need(c(V(n - 2)) == 0, "O1: v_{n-2} forced 0")
                self.slide(V(n - 2))
                self.zwalk(n - 2, "S")
            elif p == 1 and s == 1:
                case = "O2"
                self.dwalk(0)
            else:
                raise Uncovered("tight hole edge, pattern not in table")
        elif r == 0:
            sig, sigp = q, 5 - q
            if p == 1 and s == sigp:
                case = "O3a"
                self.slide(U(n - 1))
                self.need(c(V(n - 2)) == sig and c(U(n - 2)) == 1, "O3a forced v_{n-2}=sigma, u_{n-2}=1")
                self.slide(V(n - 2))
                self.zwalk(n - 2, "S")
            elif p == sigp and s == 1:
                case = "O3b"
                self.slide(U(n - 1))
                self.need({c(V(n - 2)), c(U(n - 2))} == {2, 3}, "O3b forced")
                self.slide(V(n - 2))
                self.need(c(V(n - 3)) == 0, "O3b forced v_{n-3}=0")
                self.zwalk(n - 2, "S0")
            else:
                raise Uncovered("r=0 pattern not in table")
        else:
            raise Uncovered("opening not in table")
        self.need(self.is_filled(), "walk ended unfilled")
        return case + tag


def block_colouring(G, word):
    """explicit 4-colouring of G_n from a word of blocks 'A' (length 2) and 'B' (length 3);
    a=0, b=1, rho=2, tau=3.  A at base k: v_k=0, v_{k+1}=tau, u_{k+1}=1, u_{k+2}=rho.
    B at base k: v_k=0, v_{k+1}=rho, v_{k+2}=tau, u_{k+1}=tau, u_{k+2}=1, u_{k+3}=rho."""
    col = [None] * G.N
    col[0], col[1] = 0, 1
    k = 0
    for w in word:
        if w == "A":
            col[G.V(k)], col[G.V(k + 1)], col[G.U(k + 1)], col[G.U(k + 2)] = 0, 3, 1, 2
            k += 2
        else:
            col[G.V(k)], col[G.V(k + 1)], col[G.V(k + 2)] = 0, 2, 3
            col[G.U(k + 1)], col[G.U(k + 2)], col[G.U(k + 3)] = 3, 1, 2
            k += 3
    assert k == G.n and None not in col
    return col


def to_unequal_frame(col):
    """permute colours so that c(a)=0, c(b)=1"""
    ca, cb = col[0], col[1]
    rest = [k for k in range(4) if k not in (ca, cb)]
    mp = {ca: 0, cb: 1, rest[0]: 2, rest[1]: 3}
    return [H if x == H else mp[x] for x in col]


def star_swap(G, col):
    """TwoPoleStarEscape: hole u_0, c(a)=c(b)=A. Returns filled colouring or raises."""
    n, U, V = G.n, G.U, G.V
    A = col[0]
    assert col[1] == A
    lk = link_cols(G, col, U(0))
    if len(set(lk)) <= 3:
        return "filled-already"
    for z in (V(n - 1), V(0)):
        B = col[z]
        if lk.count(B) == 1:
            comp = None
            for (p, q), cp in kempe_components(G, col):
                if {p, q} == {A, B} and 1 in cp:
                    comp = cp
            expect = {1} | {V(i) for i in range(n) if col[V(i)] == B}
            if set(comp) != expect:
                raise Uncovered("star component not as stated")
            c = list(col)
            for y in comp:
                c[y] = B if col[y] == A else A
            if not (proper(G, c) and filled(G, c)):
                raise Uncovered("star swap did not fill")
            return f"star size {len(comp)}"
    raise Uncovered("no singleton on other ring")


# ---------------------------------------------------------------- Florek check
def kempe_connected(G, cols):
    idx = {c: k for k, c in enumerate(cols)}
    par = list(range(len(cols)))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x

    for c in cols:
        for d in kempe_moves(G, c):
            d = normal(d)
            ra, rb = find(idx[c]), find(idx[d])
            if ra != rb:
                par[ra] = rb
    return len({find(k) for k in range(len(cols))})


# ---------------------------------------------------------------- main
def main(ns):
    for n in ns:
        G = Belt(n)
        print(f"===== G_{n}: |V|={G.N}, |E|={len(G.edges)} (3|V|-6={3*G.N-6})")
        degs = sorted({len(G.adj[x]) for x in range(2, G.N)})
        print(f"belt degrees {degs}, pole degrees {len(G.adj[0])},{len(G.adj[1])}")
        print(f"automorphisms: rotation {G.is_aut(G.rot())}, ring swap {G.is_aut(G.swap())}, reflection {G.is_aut(G.refl())}")

        word = {5: "AB", 6: "AAA", 7: "AAB", 8: "AAAA", 9: "AAAB", 10: "AAAAA", 11: "AAAAB"}[n]
        full = block_colouring(G, word)
        t = list(full); t[0] = H
        print(f"explicit block colouring {word}: proper {proper(G, full)}; restricted to G-a, u-ring colours "
              f"{sorted(set(full[G.U(i)] for i in range(n)))} (filled target: {filled(G, t)})")

        # ---------- belt hole u_0
        cols = enumerate_deletion(G, G.U(0))
        lab = sum(orbit_size(c) for c in cols)
        eq = [c for c in cols if c[0] == c[1]]
        un = [c for c in cols if c[0] != c[1]]
        print(f"[belt hole u0] orbits {len(cols)} (labelled {lab}); equal-pole {len(eq)}, unequal {len(un)}")
        for c in eq:
            print(f"  equal-pole orbit: {star_swap(G, list(c))}; slides+Kempe BFS distance {bfs_fill(G, c, True)[0]}")
        cases, maxslides, maxbfs, worst = {}, 0, 0, None
        maxphi_steps = 0
        steps = {}
        for c in un:
            w = Walker(G, to_unequal_frame(list(c)))
            case = w.run()
            cases[case] = cases.get(case, 0) + 1
            for t in w.trace:
                key = t.split("@")[0] + ("" if "@" not in t else ("" if ":" not in t else ":" + t.split(":")[1]))
                steps[key] = steps.get(key, 0) + 1
            maxphi_steps = max(maxphi_steps, len(w.phis))
            if w.slides > maxslides:
                maxslides, worst = w.slides, (case, w.trace)
            d, _ = bfs_fill(G, c, False)
            assert d is not None, "slides-only BFS failed"
            maxbfs = max(maxbfs, d)
        print(f"  unequal: every start classified and filled by the table walk; opening cases {dict(sorted(cases.items()))}")
        print(f"  linear-interval invariant and potential drop (4 or 6) checked at every landing; most landings in one walk {maxphi_steps}")
        print(f"  step rows used: {dict(sorted(steps.items()))}")
        print(f"  longest table walk {maxslides} slides ({worst[0]}: {' '.join(worst[1])}); "
              f"slides-only BFS shortest-walk maximum {maxbfs}")

        # ---------- pole hole a
        pc = enumerate_deletion(G, 0)
        plab = sum(orbit_size(c) for c in pc)
        nf = ns_ = nn = 0
        nosing = []
        for c in pc:
            if filled(G, c):
                nf += 1; continue
            ring = [c[G.U(i)] for i in range(n)]
            sing = [i for i in range(n) if ring.count(ring[i]) == 1]
            if sing:
                ns_ += 1
                i = sing[0]
                d = list(c); d[0] = d[G.U(i)]; d[G.U(i)] = H
                # rotate so the hole is u_0: c'(x) = d(rot^i(x))
                r = list(range(G.N))
                rot = G.rot()
                for _ in range(i):
                    r = [rot[x] for x in r]
                d = [d[r[x]] for x in range(G.N)]
                assert d[G.U(0)] == H and proper(G, d)
                if d[0] == d[1]:
                    star_swap(G, d)
                else:
                    Walker(G, to_unequal_frame(d)).run()
            else:
                nn += 1
                nosing.append(c)
        one = 0
        maxd = 0
        for c in nosing:
            ok = any(filled(G, k) or any(
                [k[G.U(j)] for j in range(n)].count(k[G.U(i)]) == 1 for i in range(n))
                for k in kempe_moves(G, c))
            one += ok
            d, _ = bfs_fill(G, c, True)
            assert d is not None
            maxd = max(maxd, d)
        print(f"[pole hole a] orbits {len(pc)} (labelled {plab}); filled {nf}; singleton on u-ring {ns_} "
              f"(slide to a belt hole, then table walk / star: all filled); no singleton {nn}")
        if nn:
            print(f"  no-singleton starts: one Kempe swap at the pole gives a fill or a u-ring singleton in {one}/{nn}; "
                  f"slides+Kempe BFS max distance {maxd}")
        comps = kempe_connected(G, pc)
        print(f"[Florek 3.1 check] Kempe classes among colourings of G_{n}-a (orbits): {comps}")
        sys.stdout.flush()


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or [5, 8, 11]
    main(ns)
