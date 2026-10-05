"""Independent check of pole-hole-noflorek.md on G_5 .. G_11 only (team rule: never n >= 14).

G_n: poles a, b; belt u_i, v_i (i mod n); edges a-u_i, b-v_i, u_i-u_{i+1},
v_i-v_{i+1}, u_i-v_i, u_i-v_{i-1}.  No a-b edge.  The hole is the pole a.

Moves (hole fixed at a): Kempe swaps of whole two-coloured components of G_n - a.
"Good" = the u-ring uses <= 3 colours (filled) or some colour occurs exactly once
on it (a singleton: one slide a -> u_i then gives a belt hole, belt-joined.md §3-§7).

For EVERY proper colouring of G_n - a (all labels, b of any colour) whose u-ring
has no singleton and all four colours, this script runs the strategy of
pole-hole-noflorek.md §4 and asserts, at every state:
  * the segment lemma (§2): between consecutive ring vertices of colour beta=c(b),
    the C-word v_{s-1} u_s v_s ... u_t v_t avoids beta and has period 3;
  * the junction lemma (§3): at a ring vertex u_i of colour beta with
    p=c(v_{i-1}), q=c(v_i), m = the fourth colour, c(u_{i-1}) in {q,m}, c(u_{i+1}) in {p,m};
  * every move is a swap of an exact Kempe component (recomputed independently)
    and leaves a proper colouring; the component sizes claimed in the text
    (single vertex for zeroing and toggles; exactly the segment for flips) hold;
  * the forced colours named in each row of the case table;
  * the degeneracy lemma: a degenerate R junction has every other junction of
    missing colour z_J;  with >= 3 junctions at most one R junction is degenerate;
  * exposure bound: sum_x E_x <= 2 n_0, so rule T1 applies whenever n_0 <= 2;
  * every round of rules F, K, S lowers n_0 by exactly 1 using <= 3 swaps;
  * the total number of swaps is <= 3(n_0 - 2) + n - 3 (n_0 at the start);
  * the run ends good.
It also recomputes, independently, which starts are fixed by ONE Kempe swap,
and reports how the strategy handles the remaining ones.
Imports no team code.
"""
from __future__ import annotations

import sys
from collections import Counter

A, B = 0, 1
STATS = Counter()  # how often each lemma was exercised


class G:
    def __init__(self, n):
        assert 5 <= n <= 11, "team rule: this checker runs n = 5..11 only; never n >= 14"
        self.n = n
        self.N = 2 * n + 2
        adj = [set() for _ in range(self.N)]

        def e(x, y):
            adj[x].add(y); adj[y].add(x)
        for i in range(n):
            e(A, self.U(i)); e(B, self.V(i))
            e(self.U(i), self.U(i + 1)); e(self.V(i), self.V(i + 1))
            e(self.U(i), self.V(i)); e(self.U(i), self.V(i - 1))
        self.adj = [sorted(s) for s in adj]
        # belt = square of the 2n-cycle C: u_0 v_0 u_1 v_1 ...
        C = [self.U(k // 2) if k % 2 == 0 else self.V(k // 2) for k in range(2 * n)]
        sq = set()
        for k in range(2 * n):
            for d in (1, 2):
                sq.add(frozenset((C[k], C[(k + d) % (2 * n)])))
        belt = {frozenset((x, y)) for x in range(2, self.N) for y in self.adj[x] if y >= 2}
        assert belt == sq, "belt is not C_{2n}^2"
        self.C = C

    def U(self, i):
        return 2 + (i % self.n)

    def V(self, i):
        return 2 + self.n + (i % self.n)


def proper(g, col):
    for x in range(1, g.N):
        for y in g.adj[x]:
            if y != A and col[x] == col[y]:
                return False
    return col[A] is None


def enumerate_colourings(g):
    order = [B] + [g.U(i) for i in range(g.n)] + [g.V(i) for i in range(g.n)]
    col = [None] * g.N
    out = []

    def rec(k):
        if k == len(order):
            out.append(tuple(col)); return
        x = order[k]
        for c in range(4):
            if all(col[y] != c for y in g.adj[x] if y != A):
                col[x] = c; rec(k + 1); col[x] = None
    rec(0)
    return out


def ring(g, col):
    return [col[g.U(i)] for i in range(g.n)]


def good(g, col):
    cnt = Counter(ring(g, col))
    return len(cnt) <= 3 or 1 in cnt.values()


def component(g, col, s, x, y):
    assert col[s] in (x, y)
    seen = {s}; st = [s]
    while st:
        w = st.pop()
        for z in g.adj[w]:
            if z != A and z not in seen and col[z] in (x, y):
                seen.add(z); st.append(z)
    return seen


def kempe(g, col, s, x, y):
    K = component(g, col, s, x, y)
    new = list(col)
    for w in K:
        new[w] = y if col[w] == x else x
    assert proper(g, new)
    return new, K


def fourth(*cs):
    r = {0, 1, 2, 3} - set(cs)
    assert len(r) == 1
    return r.pop()


class Run:
    def __init__(self, g, col):
        self.g, self.col, self.n = g, list(col), g.n
        self.beta = col[B]
        self.moves = 0
        self.steps = []

    def u(self, i): return self.col[self.g.U(i)]
    def v(self, i): return self.col[self.g.V(i)]

    def junctions(self):
        return [i for i in range(self.n) if self.u(i) == self.beta]

    def jinfo(self, i):
        """Junction lemma (§3): returns type, p, q, m with forced-colour asserts."""
        be = self.beta
        p, q = self.v(i - 1), self.v(i)
        assert p != q and be not in (p, q)
        m = fourth(be, p, q)
        al, ga = self.u(i - 1), self.u(i + 1)
        assert al in (q, m), "junction lemma: u_{i-1} in {q,m}"
        assert ga in (p, m), "junction lemma: u_{i+1} in {p,m}"
        t = {(q, p): 'F', (m, p): 'R1', (q, m): 'R2', (m, m): 'X'}[(al, ga)]
        return t, p, q, m

    def check_segments(self):
        J = self.junctions()
        if not J:
            return
        g, n, be = self.g, self.n, self.beta
        for a_, b_ in zip(J, J[1:] + [J[0] + n]):
            word = []
            for k in range(a_, b_):
                word.append(self.v(k))
                if k + 1 < b_:
                    word.append(self.u(k + 1))
            assert len(word) % 2 == 1 and len(word) >= 3
            assert be not in word, "segment lemma: no beta in a segment"
            for k in range(len(word) - 3 + 1):
                assert len(set(word[k:k + 3])) == 3
            for k in range(len(word) - 3):
                assert word[k] == word[k + 3], "segment lemma: period 3"

    def exposures(self):
        E = Counter()
        for i in range(self.n):
            x = self.u(i)
            if x != self.beta and self.beta in (self.u(i - 1), self.u(i + 1)):
                E[x] += 1
        return E

    def swap(self, s, x, y, expect=None):
        new, K = kempe(self.g, self.col, s, x, y)
        if expect is not None:
            assert K == expect, "component differs from the one claimed"
        self.col = new
        self.moves += 1
        return K

    def degenerate(self, i):
        """R-kill is blocked: the swapped component would contain the far ring neighbour."""
        t, p, q, m = self.jinfo(i)
        g = self.g
        if t == 'R1':
            K = component(g, self.col, g.V(i), q, m)
            dg = g.U(i - 1) in K; z = p
        else:
            K = component(g, self.col, g.V(i - 1), p, m)
            dg = g.U(i + 1) in K; z = q
        STATS['R junction tested'] += 1
        if dg:  # degeneracy lemma (§4): every other junction has missing colour z
            STATS['degenerate R junction (lemma asserted)'] += 1
            for j in self.junctions():
                if j != i:
                    assert self.jinfo(j)[3] == z, "degeneracy lemma"
        return dg

    def kill(self, i):
        """Rule K (§4): one swap makes junction i free, one toggle removes it."""
        g = self.g
        t, p, q, m = self.jinfo(i)
        if t == 'R1':
            assert self.u(i - 1) == m and self.u(i + 1) == p   # forced
            self.swap(g.V(i), q, m)
            assert self.v(i) == m and self.v(i - 1) == p and self.u(i - 1) == m and self.u(i + 1) == p
            t2, _, _, m2 = self.jinfo(i); assert t2 == 'F' and m2 == q
        else:
            assert self.u(i + 1) == m and self.u(i - 1) == q   # forced
            self.swap(g.V(i - 1), p, m)
            assert self.v(i - 1) == m and self.v(i) == q and self.u(i + 1) == m and self.u(i - 1) == q
            t2, _, _, m2 = self.jinfo(i); assert t2 == 'F' and m2 == p
        if good(g, self.col):
            return
        self.toggle(i)

    def toggle(self, i):
        """Rule F: a free junction is a one-vertex (beta, m) component; recolour it m."""
        t, p, q, m = self.jinfo(i)
        assert t == 'F' and self.u(i - 1) == q and self.u(i + 1) == p
        self.swap(self.g.U(i), self.beta, m, expect={self.g.U(i)})
        assert self.u(i) == m

    def run(self):
        g, n, be = self.g, self.n, self.beta
        n0_start = len(self.junctions())
        bound = 3 * (n0_start - 2) + n - 3
        while True:
            self.check_segments()
            if good(g, self.col):
                break
            J = self.junctions()
            n0 = len(J)
            assert n0 >= 2
            E = self.exposures()
            assert sum(E.values()) <= 2 * n0
            info = {i: self.jinfo(i) for i in J}
            xs = [x for x in range(4) if x != be and E[x] <= 1]
            if n0 <= 2:
                assert xs, "T1 must apply when n0 <= 2"
            if xs:                                    # rule T1
                x = xs[0]
                for i in range(n):
                    if good(g, self.col):
                        break
                    if self.u(i) == x and be not in (self.u(i - 1), self.u(i + 1)):
                        self.swap(g.U(i), be, x, expect={g.U(i)})
                        assert self.u(i) == be
                assert good(g, self.col)
                cnt = Counter(ring(g, self.col))
                assert cnt[x] <= 1
                self.steps.append('T1')
                break
            assert n0 >= 3
            before = self.moves
            F = [i for i in J if info[i][0] == 'F']
            Rs = [i for i in J if info[i][0] in ('R1', 'R2')]
            if F:                                     # rule F
                self.toggle(F[0]); self.steps.append('F')
            else:
                nd = [i for i in Rs if not self.degenerate(i)]
                if nd:                                # rule K
                    self.kill(nd[0]); self.steps.append('K')
                else:
                    assert len(Rs) <= 1, "at most one degenerate R with n0 >= 3"
                    assert not Rs, "one degenerate R and no F: T1 should have applied"
                    # rule S: all junctions X; flip the segment between two consecutive ones
                    assert all(info[i][0] == 'X' for i in J)
                    i, j = J[0], J[1]
                    m1, m2 = info[i][3], info[j][3]
                    z = min({0, 1, 2, 3} - {be, m1, m2})
                    x, y = sorted({0, 1, 2, 3} - {be, z})
                    seg = {g.V(k) for k in range(i, j)} | {g.U(k) for k in range(i + 1, j)}
                    S = {w for w in seg if self.col[w] in (x, y)}
                    self.swap(next(iter(S)), x, y, expect=S)
                    ti, tj = self.jinfo(i)[0], self.jinfo(j)[0]
                    assert ti in ('R1', 'R2') and tj in ('R1', 'R2')
                    self.steps.append('S')
                    if not good(g, self.col):
                        di, dj = self.degenerate(i), self.degenerate(j)
                        assert not (di and dj), "S: one of the two new R junctions is non-degenerate"
                        self.kill(j if di else i)
                        self.steps.append('K')
            if not good(g, self.col):
                assert len(self.junctions()) == n0 - 1, "a round lowers n0 by exactly 1"
            assert self.moves - before <= 3
        assert good(g, self.col)
        assert self.moves <= bound, (self.moves, bound)
        # the good state: filled, or a legal slide a -> singleton
        cnt = Counter(ring(g, self.col))
        if len(cnt) == 4:
            single = [i for i in range(n) if cnt[self.u(i)] == 1]
            assert single
        return self.moves


def main():
    out = []
    totals = {}
    for n in range(5, 12):
        g = G(n)
        cols = enumerate_colourings(g)
        assert len(cols) % 24 == 0
        starts = []
        for c in cols:
            assert proper(g, c)
            cnt = Counter(ring(g, c))
            if len(cnt) == 4 and min(cnt.values()) >= 2:
                starts.append(c)
        mv = Counter(); pat = Counter(); one_fail = []; hard_pat = Counter(); hard_mv = Counter()
        for c in starts:
            r = Run(g, c)
            k = r.run()
            mv[k] += 1; pat['+'.join(r.steps)] += 1
            # independent: does a single Kempe swap reach a good state?
            one = False
            for x in range(4):
                for y in range(x + 1, 4):
                    seen = set()
                    for s in range(1, g.N):
                        if s in seen or c[s] not in (x, y):
                            continue
                        new, K = kempe(g, c, s, x, y); seen |= K
                        if good(g, new):
                            one = True; break
                    if one: break
                if one: break
            if not one:
                one_fail.append(c); hard_pat['+'.join(r.steps)] += 1; hard_mv[k] += 1
        L = len(starts)
        assert L % 24 == 0 and len(one_fail) % 24 == 0
        out.append(f"===== G_{n}: proper colourings of G_n - a: {len(cols)} labelled ({len(cols)//24} up to colour permutation)")
        out.append(f"  no-singleton pole starts: {L} labelled = {L//24} orbits under colour permutation")
        if L:
            out.append(f"  strategy (T1/F/K/S) ends good in every start; all lemmas and forced colours asserted")
            out.append(f"  swaps used: {dict(sorted(mv.items()))} (max {max(mv)}; hand bound 3(n0-2)+n-3)")
            out.append(f"  rule sequences: {dict(sorted(pat.items(), key=lambda t: -t[1]))}")
            out.append(f"  starts not fixed by one Kempe swap: {len(one_fail)} labelled = {len(one_fail)//24} orbits")
            if one_fail:
                out.append(f"    their rule sequences: {dict(hard_pat)}; swaps used: {dict(sorted(hard_mv.items()))}")
                c = min(one_fail, key=lambda c: (c[B], ring(g, c)))
                out.append(f"    example (b={c[B]}): u = {''.join(map(str, ring(g, c)))}, v = {''.join(str(c[g.V(i)]) for i in range(n))}")
        totals[n] = L // 24
        if STATS:
            out.append(f"  lemma use: {dict(STATS)}")
        STATS.clear()
    out.append(f"summary: no-singleton orbits by n: {totals}; every one handled by the case table; nothing run for n >= 12")
    text = "\n".join(out)
    print(text)


if __name__ == "__main__":
    main()
