"""Independent SAT encoder for R0 and variants (Long Table R0 attempt 1).  Not derived from sat_t1v.py.

Graph: Hamiltonian normal form, H = 0,1,...,n-1,0, v = 0, f0 = (0,n-1), f2 = (0,1); f1, f3, f4 are v-chords;
every other vertex carries exactly one chord.  Planarity: circle rule (PROOF-ATTEMPT-1 s1.3), optional.
Sequence N_0..N_{L-1} of perfect matchings, N_t & N_{t+1} = 0 (cyclic if closed), v-edge of N_t = f_{k_t},
k_t = k0 - 2t mod 5.
Modes:  r0     : N_0 = M0 = even H-edges (contains f2), N_1 = M1 = odd H-edges (contains f0)   [Conjecture R0]
        star   : N free (k0 = 2); the graph is only required to HAVE the Ham arc (M0 -> M1)   [R0*: D acyclic]
usage: r0sat.py mode n L [nonplanar] [open] [core]"""
import sys, time, itertools
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153, Glucose4


class R0Enc:
    def __init__(self, n, L, mode='r0', planar=True, closed=True, k0=2):
        self.n, self.L, self.mode, self.planar, self.closed = n, L, mode, planar, closed
        self.pool = IDPool(); self.groups = {}   # group name -> list of clauses
        P = self.pool
        V = range(1, n)
        # potential edges: ('h', i) H edge (i,i+1) i=1..n-2; 'f0', 'f2'; ('c', i, j) cubic chord; ('v', s, j)
        self.pe = []
        for i in range(1, n - 1): self.pe.append(('h', i, i + 1))
        self.adj = (mode == 'adj')
        self.hv = ('f0', 'f1') if self.adj else ('f0', 'f2')
        self.vc = (2, 3, 4) if self.adj else (1, 3, 4)
        self.pe += [(self.hv[0], 0, n - 1), (self.hv[1], 0, 1)]
        for i in range(1, n):
            for j in range(i + 2, n): self.pe.append(('c', i, j))
        for s in self.vc:
            for j in range(2, n - 1): self.pe.append(('v%d' % s, 0, j))
        self.pres = {}
        for e in self.pe:
            if e[0] in ('h',) + self.hv: self.pres[e] = None
            else: self.pres[e] = P.id(('x',) + e)
        inc = {x: [e for e in self.pe if x in (e[1], e[2])] for x in range(n)}
        self.inc = inc
        # graph structure
        for x in V:   # exactly one chord at x
            lits = [self.pres[e] for e in inc[x] if self.pres[e] is not None]
            self.card('graph', lits, 1)
        for s in self.vc:
            self.card('graph', [self.pres[e] for e in self.pe if e[0] == 'v%d' % s], 1)
        # matchings
        self.m = [{e: P.id(('m', t) + e) for e in self.pe} for t in range(L)]
        self.k = [(k0 - 2 * t) % 5 for t in range(L)]
        for t in range(L):
            g = 'pm%d' % t
            for e in self.pe:
                if self.pres[e] is not None: self.add(g, [-self.m[t][e], self.pres[e]])
            for x in V: self.card(g, [self.m[t][e] for e in inc[x]], 1)
            kt = self.k[t]; name = 'f%d' % kt if 'f%d' % kt in self.hv else 'v%d' % kt
            for e in inc[0]:
                if not (e[0] == name): self.add('frame%d' % t, [-self.m[t][e]])
            self.add('frame%d' % t, [self.m[t][e] for e in inc[0] if e[0] == name])
        for t in range(L if closed else L - 1):
            u = (t + 1) % L
            for e in self.pe: self.add('disj%d' % t, [-self.m[t][e], -self.m[u][e]])
        # Hamiltonian arc: M0 = {f2, (2,3), (4,5), ...}, M1 = {(1,2), (3,4), ..., f0}
        self.M0 = [('f2', 0, 1)] + [('h', i, i + 1) for i in range(2, n - 1, 2)]
        self.M1 = [('h', i, i + 1) for i in range(1, n - 1, 2)] + [('f0', 0, n - 1)]
        if mode == 'r0':
            for e in self.M0: self.add('ham', [self.m[0][e]])
            for e in self.M1: self.add('ham', [self.m[1][e]])
        if planar: self._planar()

    def add(self, g, c): self.groups.setdefault(g, []).append(c)

    def card(self, g, lits, k):
        for c in CardEnc.equals(lits=lits, bound=k, vpool=self.pool, encoding=EncType.pairwise if len(lits) <= 6 else EncType.seqcounter).clauses:
            self.add(g, c)

    def _planar(self):
        n, P = self.n, self.pool
        if self.adj:   # f2, f3, f4 on one side, f2 nearest vertex 1 (f1), f4 nearest n-1 (f0)
            VPOS = {4: n + .25, 3: n + .5, 2: n + .75}
            sl = {s: P.id(('vside', s)) for s in (2, 3, 4)}
            for a, b in ((2, 3), (3, 4)):
                self.add('vrot', [-sl[a], sl[b]]); self.add('vrot', [sl[a], -sl[b]])
        else:
            VPOS = {4: n + .25, 1: n + .5, 3: n + .75}
            sl = {s: P.id(('vside', s)) for s in (1, 3, 4)}
            self.add('vrot', [sl[1], sl[3]]); self.add('vrot', [-sl[1], -sl[3]])
            self.add('vrot', [-sl[3], sl[4]]); self.add('vrot', [sl[3], -sl[4]])
        items = []
        for e in self.pe:
            if e[0] == 'c': items.append(((e[1], e[2]), self.pres[e], P.id(('side',) + e)))
            elif e[0].startswith('v'):
                s = int(e[0][1]); items.append(((e[2], VPOS[s]), self.pres[e], sl[s]))
        def cross(c, d):
            a1, b1 = c; a2, b2 = d
            if len({a1, b1, a2, b2}) < 4: return False
            return (a1 < a2 < b1) != (a1 < b2 < b1)
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                (c1, p1, s1), (c2, p2, s2) = items[i], items[j]
                if not cross(c1, c2): continue
                if s1 == s2: self.add('planar', [-p1, -p2]); continue
                self.add('planar', [-p1, -p2, s1, s2]); self.add('planar', [-p1, -p2, -s1, -s2])

    def clauses(self, skip=()):
        return [c for g, cl in self.groups.items() if g not in skip for c in cl]

    def decode(self, model):
        S = set(x for x in model if x > 0)
        edges = [e for e in self.pe if self.pres[e] is None or self.pres[e] in S]
        N = [[e for e in self.pe if self.m[t][e] in S] for t in range(self.L)]
        return edges, N


def verify(enc, edges, N):
    """independent check with r0lib: graph degrees, PMs, disjointness, frames, Ham arc (r0), planar_rot"""
    from r0lib import G5
    n = enc.n
    idx = {}; E = []
    for e in edges: idx[e] = len(E); E.append((e[1], e[2]))
    def fid(s):
        return idx[next(e for e in edges if e[0] in ('f%d' % s, 'v%d' % s))]
    fv = [fid(s) for s in range(5)]
    g = G5(n, E, fv)
    Ms = [sum(1 << idx[e] for e in Nt) for Nt in N]
    pm = all(sorted(x for e in Nt for x in (e[1], e[2])) == list(range(n)) for Nt in N)
    L = len(N)
    dis = all(Ms[t] & Ms[(t + 1) % L] == 0 for t in range(L if enc.closed else L - 1))
    fr = [g.k(M) for M in Ms]
    ham = [g.connected_spanning(Ms[t] | Ms[(t + 1) % L]) for t in range(L)]
    return dict(pm=pm, disjoint=dis, frames=fr, ham_arcs=[t for t in range(L) if ham[t]], planar_rot=g.planar_rot()), g


if __name__ == '__main__':
    mode, n, L = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    planar = 'nonplanar' not in sys.argv; closed = 'open' not in sys.argv
    t0 = time.time()
    enc = R0Enc(n, L, mode, planar, closed)
    import threading
    tl = float(next((a[2:] for a in sys.argv if a.startswith('t=')), 550))
    s = Glucose4(bootstrap_with=enc.clauses())
    tm = threading.Timer(tl, s.interrupt); tm.start()
    r = s.solve_limited(expect_interrupt=True); tm.cancel()
    if r is None: print(f'mode={mode} n={n} L={L} -> TIMEOUT ({time.time()-t0:.1f}s)'); sys.exit()
    print(f'mode={mode} n={n} L={L} planar={planar} closed={closed} -> {"SAT" if r else "UNSAT"} '
          f'({time.time()-t0:.1f}s, {enc.pool.top} vars)', flush=True)
    if r:
        edges, N = enc.decode(s.get_model())
        info, g = verify(enc, edges, N)
        print('verify:', info)
        print('chords:', [(e[1], e[2]) if e[0] == 'c' else (e[0], e[2]) for e in edges if e[0] in ('c',) or e[0].startswith('v')])
