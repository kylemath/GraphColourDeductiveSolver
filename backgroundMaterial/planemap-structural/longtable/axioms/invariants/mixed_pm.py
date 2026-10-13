"""Sub-conjecture beyond word 1212: closed orbits of ANY word (optionally with the chain-parity law) whose
A5v bits are not constant.  Free graph, normal form at a perfect matching: M_0 = {(2i, 2i+1)}, v = 0,
f_2 = (0, 1) in M_0 (any closed orbit has this form after relabelling).  Everything else free.
Mixed constraint: some a5[t] true and some a5[t] false (no WLOG shift needed: all t free).
Usage: mixed_pm.py n L mode(mixed|any|none) law(0|1) tlimit
"""
import sys, json, time
from pysat.formula import IDPool
from inv_sat import Enc, run


class EncPM(Enc):
    def __init__(self, n, L, law):
        self.closed = True; self.eager = 1; self.n, self.L, self.axv = n, L, 0
        self.mode, self.word, self.law = 'pm', None, law
        self.axvt = [0] * L
        self.pool = IDPool(); self.cl = []
        P = self.pool
        self.edges = []
        for i in range(n):
            for j in range(i + 1, n): self.edges.append((i, j))
        self.m = len(self.edges); self.eid = {}
        for i, (a, b) in enumerate(self.edges): self.eid[(a, b)] = i; self.eid[(b, a)] = i
        self.inc = [[] for _ in range(n)]
        for i, (a, b) in enumerate(self.edges): self.inc[a].append(i); self.inc[b].append(i)
        self.v = 0; self.vedges = self.inc[0]
        self.M0 = {self.eid[(2 * i, 2 * i + 1)] for i in range(n // 2)}
        self.H = self.M0
        self.X = {e: (None if e in self.M0 else P.id(('x', e))) for e in range(self.m)}
        self.lab = {s: {e: P.id(('lab', s, e)) for e in self.vedges} for s in range(5)}
        self.Y = {(t, e): P.id(('y', t, e)) for t in range(L) for e in range(self.m)}
        self.k = [(2 - 2 * t) % 5 for t in range(L)]
        # graph degrees
        for u in range(n):
            ch = [self.X[e] for e in self.inc[u] if self.X[e] is not None]
            self.card_eq(ch, 4 if u == 0 else 2)
        for e in range(self.m):
            if self.X[e] is not None:
                for t in range(L): self.add([-self.Y[t, e], self.X[e]])
        for s in range(5):
            self.card_eq([self.lab[s][e] for e in self.vedges], 1)
            for e in self.vedges:
                if self.X[e] is not None: self.add([-self.lab[s][e], self.X[e]])
        from pysat.card import CardEnc, EncType
        for e in self.vedges:
            ls = [self.lab[s][e] for s in range(5)]
            for c in CardEnc.atmost(lits=ls, bound=1, vpool=P, encoding=EncType.pairwise).clauses: self.add(c)
            self.add(([-self.X[e]] if self.X[e] is not None else []) + ls)
        self.add([self.lab[2][self.eid[(0, 1)]]])
        for t in range(L):
            for u in range(n): self.card_eq([self.Y[t, e] for e in self.inc[u]], 1)
            for e in range(self.m): self.add([-self.Y[t, e], -self.Y[(t + 1) % L, e]])
            for e in self.vedges:
                self.add([-self.lab[self.k[t]][e], self.Y[t, e]]); self.add([self.lab[self.k[t]][e], -self.Y[t, e]])
        for e in range(self.m): self.add([self.Y[0, e]] if e in self.M0 else [-self.Y[0, e]])
        # symmetry breaking is not needed for UNSAT answers; loops as in Enc
        self._eager_loops()


n, L, mode, law, tl = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
enc = EncPM(n, L, bool(law))
P = enc.pool; a5 = [P.id(('a5', t)) for t in range(L)]
for t in range(L):
    k = enc.k[t]
    for e in enc.vedges:
        a, b = enc.edges[e]; j = b if a == 0 else a
        z = P.id(('z', t, j))
        enc.add([-enc.lab[k][e], -z, a5[t]]); enc.add([-enc.lab[k][e], z, -a5[t]])
if mode in ('mixed', 'any'): enc.add(a5[:])
if mode == 'mixed': enc.add([-x for x in a5])
print(f'n={n} L={L} mode={mode} law={law} vars={enc.pool.top} clauses={len(enc.cl)}', flush=True)
st, sols, stats = run(enc, tl, verbose=False, max_sol=1)
print(json.dumps(dict(n=n, L=L, mode=mode, law=law, status=st, **stats)), flush=True)
for E, M, fv, info in sols:
    from ax_lib import G5
    idx = {e: i for i, e in enumerate(E)}
    g = G5(n, [enc.edges[e] for e in E], [idx[f] for f in fv])
    pat = []
    for t in range(L):
        Mt = frozenset(idx[e] for e in M[t]); d = g.dl(Mt); k, lp = d
        pat.append(1 if g.other(g.fv[k], g.v) in lp['X'][2] else 0)
    print('SOL edges', [enc.edges[e] for e in E], 'fv', [enc.edges[f] for f in fv], 'word', info['word'], 'A5v', pat, flush=True)
