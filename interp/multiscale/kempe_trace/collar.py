"""Collar normalisation SAT (CaDiCaL).  Disc S with ordered boundary bd (fixed colours), colouring col.
Collar of width w: free = vertices of S at distance 1..w-1 from bd (inside S); boundary and deeper vertices fixed.
Targets:  window(k): for every pair, every trace block lies in k cyclically consecutive boundary positions.
          exact(P):  the traces equal the given partitions P[pair] (list of blocks of boundary positions).
"""
import sys, itertools
from collections import deque
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace')
from kt import PAIRS, _find, traces, summary
from pysat.solvers import Cadical153

def depth_in(adj, S, bd):
    d = {v: 0 for v in bd}; q = deque(bd)
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y in S and y not in d: d[y] = d[x]+1; q.append(y)
    return d

class Collar:
    def __init__(self, adj, S, col, bd, w):
        self.adj, self.S, self.col, self.bd, self.w = adj, set(S), (dict(col) if isinstance(col, dict) else dict(enumerate(col))), list(bd), w
        d = depth_in(adj, self.S, bd)
        self.free = sorted(v for v in self.S if 1 <= d.get(v, 10**9) <= w-1)
        self.fs = set(self.free); self.pos = {v: i for i, v in enumerate(bd)}
        self.nv = 0; self.cls = []
        self.xv = {(v, c): self.new() for v in self.free for c in range(4)}
        for v in self.free:
            self.cls.append([self.xv[v, c] for c in range(4)])
            for c in range(4):
                for c2 in range(c+1, 4): self.cls.append([-self.xv[v, c], -self.xv[v, c2]])
            for u in adj[v]:
                if u in self.fs:
                    if u > v:
                        for c in range(4): self.cls.append([-self.xv[v, c], -self.xv[u, c]])
                elif u in self.S: self.cls.append([-self.xv[v, self.col[u]]])
        # contracted graphs per pair: nodes = free vertices (as ('f',v)) + fixed components (('s',id))
        self.G = {}
        for p in PAIRS:
            x, y = p
            fixed = [v for v in self.S if v not in self.fs and self.col[v] in p]
            par = {v: v for v in fixed}
            for v in fixed:
                for u in adj[v]:
                    if u in par and u > v:
                        a, b = _find(par, u), _find(par, v)
                        if a != b: par[a] = b
            sid = {}; sup_of = {}
            for v in fixed:
                r = _find(par, v); sid.setdefault(r, len(sid)); sup_of[v] = ('s', sid[r])
            nodes = [('f', v) for v in self.free] + [('s', i) for i in range(len(sid))]
            edges = set()
            for v in self.free:
                for u in adj[v]:
                    if u in self.fs:
                        if u > v: edges.add((('f', v), ('f', u)))
                    elif u in sup_of: edges.add((('f', v), sup_of[u]))
            bsup = {}   # boundary position -> super node (if its colour is in p)
            for i, v in enumerate(bd):
                if v in sup_of: bsup[i] = sup_of[v]
            self.G[p] = dict(nodes=nodes, edges=sorted(edges), bsup=bsup)
    def new(self): self.nv += 1; return self.nv
    def inpair(self, node, p):
        """literal list meaning 'node is in pair p' (free: disjunction of 2 colour vars; super: True)"""
        if node[0] == 's': return None
        return [self.xv[node[1], p[0]], self.xv[node[1], p[1]]]
    def add_labels(self, p, nlab):
        g = self.G[p]; lab = {(nd, l): self.new() for nd in g['nodes'] for l in range(nlab)}
        for nd in g['nodes']:
            for l in range(nlab):
                for l2 in range(l+1, nlab): self.cls.append([-lab[nd, l], -lab[nd, l2]])
        for a, b in g['edges']:
            ia, ib = self.inpair(a, p), self.inpair(b, p)
            # (a in pair) & (b in pair) & lab(a,l) -> lab(b,l), and symmetric.  'in pair' for a free vertex = x(a,x) or x(a,y)
            for l in range(nlab):
                for (s, t) in ((a, b), (b, a)):
                    ist = self.inpair(s, p); itt = self.inpair(t, p)
                    conds = []
                    for lits in (ist, itt):
                        if lits is not None: conds.append(lits)
                    # clause for each combination of which colour literal makes the vertex in-pair
                    for combo in itertools.product(*conds):
                        self.cls.append([-lab[s, l], lab[t, l]] + [-c for c in combo])
        return lab
    def target_window(self, k):
        L = len(self.bd)
        for p in PAIRS:
            lab = self.add_labels(p, L)
            for i, nd in self.G[p]['bsup'].items():
                self.cls.append([lab[nd, l] for l in range(L) if (i - l) % L < k])
    def target_exact(self, P, D=None):
        L = len(self.bd)
        for p in PAIRS:
            blocks = P[p]; g = self.G[p]; nb = len(blocks)
            lab = self.add_labels(p, nb)
            roots = set()
            for bi, blk in enumerate(blocks):
                for i in blk: self.cls.append([lab[g['bsup'][i], bi]])
                roots.add(g['bsup'][blk[0]])
            # reachability from roots within D steps on the contracted graph
            nbrs = {nd: [] for nd in g['nodes']}
            for a, b in g['edges']: nbrs[a].append(b); nbrs[b].append(a)
            DD = D or min(len(g['nodes']), 3*L)
            reach = {}
            for nd in g['nodes']:
                reach[nd, 0] = self.new()
                self.cls.append([reach[nd, 0]] if nd in roots else [-reach[nd, 0]])
            for k in range(1, DD+1):
                for nd in g['nodes']:
                    r = self.new(); reach[nd, k] = r
                    cl = [-r, reach[nd, k-1]]
                    for u in nbrs[nd]:
                        a = self.new(); cl.append(a)
                        self.cls.append([-a, reach[u, k-1]])
                        for lits in (self.inpair(u, p), self.inpair(nd, p)):
                            if lits is not None: self.cls.append([-a] + lits)
                    self.cls.append(cl)
            for blk in blocks:
                for i in blk[1:]: self.cls.append([reach[g['bsup'][i], DD]])
    def solve(self):
        s = Cadical153(bootstrap_with=self.cls); ok = s.solve()
        if not ok: s.delete(); return None
        mod = set(l for l in s.get_model() if l > 0); s.delete()
        col = dict(self.col)
        for v in self.free: col[v] = next(c for c in range(4) if self.xv[v, c] in mod)
        return col

def min_window(adj, S, col, bd, w, kmax=None):
    L = len(bd); kmax = kmax or L
    for k in range(1, kmax+1):
        C = Collar(adj, S, col, bd, w); C.target_window(k); r = C.solve()
        if r is not None:
            tr = traces(adj, S, r, bd); sm = summary(tr, L)
            assert sm['maxspan'] + 1 <= k, (sm, k)
            assert all(r[u] != r[v] for u in S for v in adj[u] if v in S)
            return k, r, sm
    return None, None, None

def exact(adj, S, col, bd, w, P):
    C = Collar(adj, S, col, bd, w); C.target_exact(P); r = C.solve()
    if r is None: return None
    tr = traces(adj, S, r, bd)
    assert all(sorted(tr[p]) == sorted(tuple(b) for b in P[p]) for p in PAIRS), 'exact target mismatch'
    assert all(r[u] != r[v] for u in S for v in adj[u] if v in S)
    return r
