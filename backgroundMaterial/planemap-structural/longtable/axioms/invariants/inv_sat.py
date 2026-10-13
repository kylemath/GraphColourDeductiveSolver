"""Exact (SAT + lazy cuts, CEGAR) search for T1-v orbits.  Long Table, run 2, 13 Oct 2026.

Object: G simple, cubic except v (degree 5, cyclic order f0..f4 of its edges), a closed orbit
M_0 .. M_{L-1} of DL-good perfect matchings, M_{t+1} subset of E - M_t, f_{k_t - 2} in M_{t+1}
(frame advances -2 per step), word w[t] = #components(M_{t-1} u M_t).

Mode 'ham' (free graph).  Word 1212...: some state has M_{t-1} u M_t Hamiltonian.  WLOG (rotate t)
M_0 u M_1 = H is Hamiltonian, label vertices 0..n-1 along H, v = 0, M_0 = {(i,i+1): i even},
M_1 = {(i,i+1): i odd} (indices mod n), and (rotating the f labels) f_2 = (0,1) in M_0,
f_0 = (0,n-1) in M_1.  Then G = H + chord set C, C a matching on the cubic vertices plus 3 chords at v
labelled f_1, f_3, f_4 (free).  Every graph+orbit with word 1212... (L even, w[1] = 1 after a rotation)
has exactly this form, so the search over (C, labels, M_2..M_{L-1}) is exhaustive for given n, L.

Mode 'fixed' (given graph, for controls): x fixed, M_0 free, word condition replaced by the law (A2).

Eager clauses: graph degrees, perfect matchings, disjointness, v-edge frames.
Lazy cuts (all valid, i.e. they only exclude assignments that violate the definition):
  * a cycle of E - M_t avoiding v                   -> E - M_t disconnected
  * a v-loop of E - M_t with wrong pairing/parity    -> not DL
  * v's M_t-partner on the wrong loop                -> A5v (AXV=1) / anti-A5v (AXV=2) fails
  * too many / too few components of M_{t-1} u M_t  -> wrong word letter
"""
import sys, time, json, itertools
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153


class Enc:
    def __init__(self, n, L, axv, mode='ham', fixed=None, word='1212', law=False, eager=True, closed=True):
        self.closed = closed
        assert L % 5 == 0 or not closed
        self.eager = eager
        self.n, self.L, self.axv, self.mode, self.word, self.law = n, L, axv, mode, word, law
        # per-state axiom: 0 none, 1 A5v, 2 anti-A5v (axv may be an int or a length-L list)
        self.axvt = list(axv) if isinstance(axv, (list, tuple)) else [axv] * L
        self.pool = IDPool(); self.cl = []
        P = self.pool
        if mode == 'ham':
            self.edges = [(i, (i + 1) % n) for i in range(n)]  # H edges h_i
            self.H = set(range(n))
            for i in range(n):
                for j in range(i + 2, n):
                    if i == 0 and j == n - 1: continue
                    self.edges.append((i, j))
        else:
            gn, gE, gfv = fixed
            self.edges = [tuple(e) for e in gE]; self.H = set()
            self.gfv = gfv
        self.m = len(self.edges)
        self.eid = {}
        for i, (a, b) in enumerate(self.edges):
            self.eid[(a, b)] = i; self.eid[(b, a)] = i
        self.inc = [[] for _ in range(n)]
        for i, (a, b) in enumerate(self.edges):
            self.inc[a].append(i); self.inc[b].append(i)
        self.v = 0 if mode == 'ham' else self._fixed_v()
        self.vedges = self.inc[self.v]
        # edge presence
        self.X = {e: (None if (e in self.H or mode == 'fixed') else P.id(('x', e))) for e in range(self.m)}
        # labels: lab[s][e] for v-edge e
        self.lab = {s: {e: P.id(('lab', s, e)) for e in self.vedges} for s in range(5)}
        # matchings
        self.Y = {}
        for t in range(L):
            for e in range(self.m):
                self.Y[t, e] = P.id(('y', t, e))
        self.k = [(2 - 2 * t) % 5 for t in range(L)]
        self._eager()

    def _fixed_v(self):
        a, b = self.edges[self.gfv[0]]; c, d = self.edges[self.gfv[1]]
        return a if a in (c, d) else b

    def add(self, c): self.cl.append(c)

    def card_eq(self, lits, k):
        if not lits:
            if k: self.add([])
            return
        r = CardEnc.equals(lits=lits, bound=k, vpool=self.pool, encoding=EncType.seqcounter)
        for c in r.clauses: self.add(c)

    def xlit(self, e):  # literal "edge present", None if always present
        return self.X[e]

    def _eager(self):
        n, L, v = self.n, self.L, self.v
        # graph
        if self.mode == 'ham':
            for u in range(n):
                ch = [self.X[e] for e in self.inc[u] if self.X[e] is not None]
                self.card_eq(ch, 3 if u == v else 1)
            for e in range(self.m):
                if self.X[e] is not None:
                    for t in range(L): self.add([-self.Y[t, e], self.X[e]])
        # labels: each s exactly one present v-edge, each present v-edge exactly one label
        for s in range(5):
            self.card_eq([self.lab[s][e] for e in self.vedges], 1)
            for e in self.vedges:
                if self.X[e] is not None: self.add([-self.lab[s][e], self.X[e]])
        for e in self.vedges:
            ls = [self.lab[s][e] for s in range(5)]
            r = CardEnc.atmost(lits=ls, bound=1, vpool=self.pool, encoding=EncType.pairwise)
            for c in r.clauses: self.add(c)
            if self.X[e] is not None: self.add([-self.X[e]] + ls)
            else: self.add(ls)
        if self.mode == 'ham':
            h0, hl = self.eid[(0, 1)], self.eid[(n - 1, 0)]
            self.add([self.lab[2][h0]]); self.add([self.lab[0][hl]])
        else:
            for s, e in enumerate(self.gfv): self.add([self.lab[s][e]])
        # matchings
        for t in range(L):
            for u in range(n):
                self.card_eq([self.Y[t, e] for e in self.inc[u]], 1)
            for e in range(self.m):
                if self.closed or t + 1 < L:
                    self.add([-self.Y[t, e], -self.Y[(t + 1) % L, e]])
            for e in self.vedges:  # v-edge of M_t is f_{k_t}
                self.add([-self.lab[self.k[t]][e], self.Y[t, e]])
                self.add([self.lab[self.k[t]][e], -self.Y[t, e]])
        if self.mode == 'ham':
            for t in (0, 1):
                for e in range(self.m):
                    if e in self.H and e % 2 == t: self.add([self.Y[t, e]])
                    else: self.add([-self.Y[t, e]])
        if self.eager: self._eager_loops()

    def _eager_loops(self):
        """z[t,u] = 1 iff cubic vertex u lies on the X loop of E - M_t.  Propagation along E - M_t,
        v-edge ends forced by the frame (=> loop pairing is eager), |X| even (XOR chain),
        A5v / anti-A5v as a unit implication.  Sound: in a valid DL state z = loop membership
        satisfies all of these.  Complete only together with the lazy connectivity cuts."""
        n, L, v, P = self.n, self.L, self.v, self.pool
        for t in range(L):
            z = {u: P.id(('z', t, u)) for u in range(n) if u != v}
            k = self.k[t]
            for e, (a, b) in enumerate(self.edges):
                if v in (a, b):
                    j = b if a == v else a
                    for s in range(5):
                        d = (s - k) % 5
                        if d in (1, 4):
                            self.add([-self.lab[s][e], self.Y[t, e], z[j]])
                        elif d in (2, 3):
                            self.add([-self.lab[s][e], self.Y[t, e], -z[j]])
                        elif d == 0 and self.axvt[t]:
                            self.add([-self.lab[s][e], z[j] if self.axvt[t] == 1 else -z[j]])
                    continue
                pre = [] if self.X[e] is None else [-self.X[e]]
                self.add(pre + [self.Y[t, e], -z[a], z[b]])
                self.add(pre + [self.Y[t, e], z[a], -z[b]])
            us = [u for u in range(n) if u != v]
            p = z[us[0]]
            for u in us[1:]:
                q = P.id(('par', t, u))
                a, b = p, z[u]
                self.add([-q, a, b]); self.add([-q, -a, -b]); self.add([q, -a, b]); self.add([q, a, -b])
                p = q
            self.add([-p])  # |X| even
        # connectivity by ranks (optional, eager=2): every non-root vertex has a neighbour (in the
        # subgraph) of strictly smaller rank => every vertex reaches a root.  Slower than lazy cuts.
        # eager=2: Q and U; 3: U at odd t only; 4: Q only
        for t in (range(L) if self.eager >= 2 else []):
            # Q_t = E - M_t connected (root v)
            if self.eager in (2, 4):
                self._ranked(('Q', t), lambda e, t=t: (-self.Y[t, e],), roots1=True)
            if self.word == '1212' and (self.closed or t > 0) and (self.eager == 2 or (self.eager == 3 and t % 2 == 1)):
                # U_t = M_{t-1} u M_t: 1 component (t odd), <= 2 components (t even)
                tp = (t - 1) % L
                self._ranked(('U', t), lambda e, t=t, tp=tp: (self.Y[t, e], self.Y[tp, e]),
                             roots1=(t % 2 == 1), inU=True)

    def _ranked(self, tag, edge_in, roots1=True, inU=False):
        """edge_in(e): for Q, (-y,) meaning edge in iff present and not y; for U, (y_t, y_tp) meaning
        in iff one of them true.  roots1: only v is a root; else one extra free root."""
        n, v, P = self.n, self.v, self.pool
        R = n  # ranks 0..n-1, order encoding o(u,i) = rank_u >= i, i = 1..n-1
        o = lambda u, i: P.id(('o',) + tag + (u, i))
        for u in range(n):
            for i in range(1, R - 1): self.add([-o(u, i + 1), o(u, i)])
        self.add([-o(v, 1)])
        rho = None
        if not roots1:
            rho = {u: P.id(('rho',) + tag + (u,)) for u in range(n) if u != v}
            r = CardEnc.atmost(lits=list(rho.values()), bound=1, vpool=P, encoding=EncType.seqcounter)
            for c in r.clauses: self.add(c)
        for u in range(n):
            if u == v: continue
            ps = []
            for e in self.inc[u]:
                w = self.other(e, u)
                p = P.id(('p',) + tag + (u, e)); ps.append(p)
                if inU:
                    a, b = edge_in(e); self.add([-p, a, b])
                else:
                    (ny,) = edge_in(e); self.add([-p, ny])
                    if self.X[e] is not None: self.add([-p, self.X[e]])
                self.add([-p, o(u, 1)])
                for i in range(1, R - 1):
                    self.add([-p, -o(w, i), o(u, i + 1)])
                self.add([-p, -o(w, R - 1)])
            self.add(ps + ([rho[u]] if rho else []))

    # ------------- decode and check -------------
    def decode(self, model):
        S = set(l for l in model if l > 0)
        E = [e for e in range(self.m) if self.X[e] is None or self.X[e] in S]
        M = [frozenset(e for e in E if self.Y[t, e] in S) for t in range(self.L)]
        fv = [None] * 5
        for s in range(5):
            for e in self.vedges:
                if self.lab[s][e] in S: fv[s] = e
        return E, M, fv

    def other(self, e, x):
        a, b = self.edges[e]; return b if a == x else a

    def cut_present(self, t, edges, inM):
        """literals whose disjunction says: NOT(all `edges` present and (not) in M_t)."""
        c = []
        for e in edges:
            if self.X[e] is not None: c.append(-self.X[e])
            c.append(-self.Y[t, e] if inM else self.Y[t, e])
        return c

    def check(self, E, M, fv):
        """returns (list of cuts, info). empty cuts => valid orbit."""
        n, v, L = self.n, self.v, self.L
        Es = set(E); cuts = []; info = {}
        fidx = {e: s for s, e in enumerate(fv)}
        adjE = [[] for _ in range(n)]
        for e in E:
            a, b = self.edges[e]; adjE[a].append(e); adjE[b].append(e)
        words = []
        for t in range(L):
            Q = Es - M[t]
            # components of Q through cubic vertices: trace cycles not through v
            seen = set(); bad = False
            # loops from v
            loops = []
            for e0 in adjE[v]:
                if e0 in M[t] or e0 in seen: continue
                path = [e0]; seen.add(e0); x = self.other(e0, v); e = e0; verts = []
                while x != v:
                    verts.append(x)
                    e = [g for g in adjE[x] if g in Q and g != e][0]
                    path.append(e); seen.add(e); x = self.other(e, x)
                loops.append((fidx[e0], fidx[e], verts, path))
            onloop = set(x for lp in loops for x in lp[2]) | {v}
            for x0 in range(n):
                if x0 in onloop: continue
                # cycle through x0
                cyc = []; x = x0; e = None; vs = []
                while True:
                    vs.append(x)
                    e = [g for g in adjE[x] if g in Q and g != e][0]
                    cyc.append(e); x = self.other(e, x)
                    if x == x0: break
                onloop |= set(vs)
                cuts.append(self.cut_present(t, cyc, False)); bad = True
            k = self.k[t]
            if not bad:
                want = {frozenset({(k - 1) % 5, (k + 1) % 5}): 'X', frozenset({(k + 2) % 5, (k - 2) % 5}): 'Y'}
                cls = {}
                for (s0, s1, verts, path) in loops:
                    c = want.get(frozenset({s0, s1}))
                    par_ok = c is not None and (len(verts) % 2 == (0 if c == 'X' else 1))
                    if not par_ok:
                        cl = self.cut_present(t, path, False)
                        cl += [-self.lab[s0][path[0]], -self.lab[s1][path[-1]]]
                        cuts.append(cl); bad = True
                    else:
                        cls[c] = (s0, s1, verts, path)
                if not bad and self.axvt[t]:
                    fk = fv[k]; a = self.other(fk, v)
                    wrong = 'Y' if self.axvt[t] == 1 else 'X'
                    s0, s1, verts, path = cls[wrong]
                    if a in verts:
                        cl = self.cut_present(t, path, False)
                        cl += [-self.lab[s0][path[0]], -self.lab[s1][path[-1]], -self.Y[t, fk]]
                        cuts.append(cl); bad = True
            # word letter
            if not self.closed and t == 0:
                words.append(0); continue
            U = M[t - 1] | M[t]
            comps = []; done = set()
            for x0 in range(n):
                if x0 in done: continue
                cyc = []; x = x0; e = None
                while True:
                    done.add(x)
                    e = [g for g in adjE[x] if g in U and g != e][0]
                    cyc.append(e); x = self.other(e, x)
                    if x == x0: break
                comps.append(cyc)
            words.append(len(comps))
            if self.word == '1212':
                wt = 1 if t % 2 == 1 else 2
                if len(comps) > wt:
                    comps.sort(key=len)
                    cl = []
                    for cyc in comps[:wt + 1]:
                        for e in cyc:
                            cl.append(-self.Y[(t - 1) % L, e] if e in M[t - 1] else -self.Y[t, e])
                    cuts.append(cl)
                elif len(comps) < wt:
                    cl = []
                    for e in comps[0]:
                        cl.append(-self.Y[(t - 1) % L, e] if e in M[t - 1] else -self.Y[t, e])
                    cuts.append(cl)
        info['word'] = ''.join(map(str, words))
        if not cuts and self.law:
            viol = sum(1 for t in range(L) if (words[t] - words[t - 1]) % 2 == 0)
            if viol:
                # block this whole orbit (fixed-graph mode only)
                cuts.append([-self.Y[t, e] for t in range(L) for e in M[t]])
                info['lawviol'] = viol
        return cuts, info


def run(enc, tlimit=600, verbose=True, max_sol=1, symcheck=None):
    s = Cadical153(bootstrap_with=enc.cl)
    t0 = time.time(); it = 0; ncuts = 0; sols = []
    while True:
        if time.time() - t0 > tlimit:
            s.delete(); return 'TIMEOUT', sols, dict(iters=it, cuts=ncuts, sec=time.time() - t0)
        if not s.solve():
            s.delete(); return 'UNSAT', sols, dict(iters=it, cuts=ncuts, sec=time.time() - t0)
        it += 1
        E, M, fv = enc.decode(s.get_model())
        cuts, info = enc.check(E, M, fv)
        if cuts:
            for c in cuts: s.add_clause(c)
            ncuts += len(cuts)
            if verbose and it % 2000 == 0:
                print(f'  it={it} cuts={ncuts} t={time.time()-t0:.0f}s', flush=True)
            continue
        sols.append((E, M, fv, info))
        if len(sols) >= max_sol:
            s.delete(); return 'SAT', sols, dict(iters=it, cuts=ncuts, sec=time.time() - t0)
        # block this exact orbit and go on
        s.add_clause([-enc.Y[t, e] for t in range(enc.L) for e in M[t]])


def to_line(enc, E, fv):
    """TrackU graph line: n m edges... f0..f4 (edge ids in the emitted list)."""
    idx = {e: i for i, e in enumerate(E)}
    toks = [enc.n, len(E)]
    for e in E: toks += list(enc.edges[e])
    toks += [idx[f] for f in fv]
    return ' '.join(map(str, toks))


if __name__ == '__main__':
    n, L, axv = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 600
    eager = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    enc = Enc(n, L, axv, eager=eager)
    print(f'n={n} L={L} axv={axv} eager={eager} vars={enc.pool.top} clauses={len(enc.cl)}', flush=True)
    st, sols, stats = run(enc, tl)
    print(json.dumps(dict(n=n, L=L, axv=axv, eager=eager, status=st, **stats)))
    for E, M, fv, info in sols:
        print('SOL', to_line(enc, E, fv), info)
