"""Analysis of abstract windows / orbits in the chord normal form (frame-relative quantities)."""
import json


class Win:
    def __init__(self, d):
        self.n = n = d['n']
        self.E = [(i, (i + 1) % n) for i in range(n)] + [tuple(c) for c in d['chords']]
        self.fv = [tuple(e) for e in d['fv']]
        self.adj = [[] for _ in range(n)]
        for a, b in self.E:
            self.adj[a].append(b); self.adj[b].append(a)
        self.M = [set(tuple(sorted(e)) for e in Mt) for Mt in d['M']]
        self.W = len(self.M)
        self.fidx = {tuple(sorted(e)): s for s, e in enumerate(self.fv)}
        self.mate = []
        for Mt in self.M:
            m = {}
            for a, b in Mt: m[a] = b; m[b] = a
            self.mate.append(m)

    def key(self, a, b): return (a, b) if a < b else (b, a)

    def k(self, t):
        return self.fidx[self.key(0, self.mate[t][0])]

    def fend(self, s):
        a, b = self.fv[s]; return b if a == 0 else a

    def loops(self, t):
        """X_t, Y_t as ordered vertex lists (from v leaving via e1 / e4 resp.)"""
        k = self.k(t); Mt = self.mate[t]
        def walk(s0):
            x = self.fend(s0); prev = 0; out = []
            while x != 0:
                out.append(x)
                nb = [y for y in self.adj[x] if y != prev and Mt[x] != y]
                # x has 3 nbrs: one is M_t-mate, one is prev; but multi-adjacency impossible (simple)
                nxt = [y for y in self.adj[x] if y != Mt[x] and y != prev]
                assert len(nxt) == 1, (x, nxt)
                prev, x = x, nxt[0]
            return out
        X = walk((k - 1) % 5); Y = walk((k + 2) % 5)
        return X, Y

    def ham_positions(self, t):
        """H_t = M_{t-1} u M_t Hamiltonian; positions along H from v leaving via e2 (M_t edge)."""
        m1, m0 = self.mate[t], self.mate[t - 1]
        seq = []; x = m1[0]; use = 0  # next edge from x is M_{t-1}
        while x != 0:
            seq.append(x)
            x = m0[x] if use == 0 else m1[x]; use ^= 1
        assert len(seq) == self.n - 1
        pos = {x: i + 1 for i, x in enumerate(seq)}
        k = self.k(t)
        e = lambda i: self.fend((k - 2 + i) % 5)
        return seq, pos, {i: pos[e(i)] for i in (0, 1, 3)}

    def state(self, t):
        X, Y = self.loops(t)
        p = self.mate[t][0]
        return dict(k=self.k(t), X=len(X), Y=len(Y), a5v=p in set(X))


def load(path):
    out = []
    for l in open(path):
        l = l.strip()
        if l.startswith('{') and '"chords"' in l: out.append(Win(json.loads(l)))
    return out
