"""Vacancy-D-reducibility checker (game value by retrograde min-max).

[computed, exploratory] Math worker, 2026-10-06. Model: see README.md section 1.

State of the abstract game:
  U-node  c            : colouring of K - v (canonical up to colour renaming), no outside knowledge
  K-node  (c, th, M)   : colouring plus the known outside matching M for split th
A split th is {0,th} | {the other two}; M is a non-crossing perfect matching of the
th-transitional ring edges (ring edges whose ends lie in different halves of th).
Player moves (cost 1 each): swap one th-component of K - v (components = inside same-half
edges + outside regions of M).  th-swaps preserve M; any other split's matching is chosen
afresh by the adversary.  Win = link of v uses <= 3 colours.

U(c)        = 0 if filled, else min_th max_M A(c,th,M)
A(c,th,M)   = 1 + min_C K(swap_C c, th, M)          (K = 0 for filled)
K(c,th,M)   = min(U(c), A(c,th,M))
Value iteration from +inf; round n gives exactly the states won within n swaps.
"""
import sys, time
from functools import lru_cache

INF = 10 ** 9


@lru_cache(None)
def nc_matchings(t):
    """All non-crossing perfect matchings of 0..t-1 on a circle, as partner tuples."""
    def rec(lo, hi):  # positions lo..hi-1
        if lo >= hi:
            return [dict()]
        out = []
        for j in range(lo + 1, hi, 2):
            for a in rec(lo + 1, j):
                for b in rec(j + 1, hi):
                    d = {lo: j, j: lo}
                    d.update(a); d.update(b)
                    out.append(d)
        return out
    if t % 2:
        return []
    return [tuple(d[i] for i in range(t)) for d in rec(0, t)]


def canon(c):
    """Relabel colours by first occurrence. Returns (canonical tuple, sigma dict)."""
    sig = {}
    out = []
    for x in c:
        if x not in sig:
            sig[x] = len(sig)
        out.append(sig[x])
    nxt = len(sig)
    for x in range(4):
        if x not in sig:
            sig[x] = nxt; nxt += 1
    return tuple(out), sig


def map_split(th, sig):
    h = {sig[0], sig[th]}
    if 0 in h:
        return (h - {0}).pop()
    return ({0, 1, 2, 3} - h - {0}).pop()


def swapcol(x, th):
    if x == 0: return th
    if x == th: return 0
    o = [y for y in (1, 2, 3) if y != th]
    return o[1] if x == o[0] else o[0]


class Config:
    def __init__(self, cfg):
        self.cfg = cfg
        link, ring = cfg['link'], cfg['ring']
        # vertex order: link, then BFS outwards (ring last is not needed)
        order = list(link)
        rest = [x for x in cfg['verts'] if x not in order]
        nb = {x: set() for x in cfg['verts']}
        for a, b in cfg['edges']:
            nb[a].add(b); nb[b].add(a)
        while rest:
            # pick a rest vertex with most coloured neighbours
            best = max(rest, key=lambda x: (len(nb[x] & set(order)), -x))
            order.append(best); rest.remove(best)
        self.order = order
        self.idx = {x: i for i, x in enumerate(order)}
        self.n = len(order)
        self.edges = [(self.idx[a], self.idx[b]) for a, b in cfg['edges']]
        self.nbr = [[] for _ in range(self.n)]
        for a, b in self.edges:
            self.nbr[a].append(b); self.nbr[b].append(a)
        self.link = [self.idx[x] for x in link]
        self.ring = [self.idx[x] for x in ring]
        self.m = len(self.ring)

    def filled(self, c):
        return len({c[i] for i in self.link}) <= 3

    def colourings(self):
        """All proper colourings of K - v, canonical (first-occurrence) in self.order."""
        n, nbr = self.n, self.nbr
        c = [-1] * n
        out = []
        def rec(i, mx):
            if i == n:
                out.append(tuple(c)); return
            used = {c[j] for j in nbr[i] if c[j] >= 0}
            for col in range(min(mx + 2, 4)):
                if col not in used:
                    c[i] = col
                    rec(i + 1, max(mx, col))
            c[i] = -1
        rec(0, -1)
        return out

    def trans(self, c, th):
        h = [(c[r] == 0 or c[r] == th) for r in self.ring]
        m = self.m
        return [i for i in range(m) if h[i] != h[(i + 1) % m]]

    def components(self, c, th, T, M):
        n = self.n
        par = list(range(n))
        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        h = [(x == 0 or x == th) for x in c]
        for a, b in self.edges:
            if h[a] == h[b]:
                par[f(a)] = f(b)
        t, m, ring = len(T), self.m, self.ring
        for k in range(t):
            p = M[(k + 1) % t]
            a = ring[(T[k] + 1) % m]
            b = ring[(T[p] + 1) % m]
            par[f(a)] = f(b)
        if t == 0:
            for r in ring:
                par[f(r)] = f(ring[0])
        groups = {}
        for x in range(n):
            groups.setdefault(f(x), []).append(x)
        return list(groups.values())


def solve(cfg, verbose=True, max_nodes=None):
    t0 = time.process_time()
    C = Config(cfg)
    cols = C.colourings()
    unf = [c for c in cols if not C.filled(c)]
    uid = {c: i for i, c in enumerate(unf)}
    # K-nodes
    knodes = []          # (u index, th, M)
    kid = {}
    for c in unf:
        for th in (1, 2, 3):
            T = C.trans(c, th)
            for M in nc_matchings(len(T)):
                kid[(c, th, M)] = len(knodes)
                knodes.append((uid[c], th, M))
    if verbose:
        print(f"  K - v: {C.n} vertices, ring {C.m}; colourings {len(cols)}, unfilled {len(unf)}, "
              f"K-nodes {len(knodes)}", flush=True)
    if max_nodes and len(knodes) > max_nodes:
        return dict(aborted=True, colourings=len(cols), unfilled=len(unf), knodes=len(knodes))
    # successors: for each K-node, list of successor K-node ids (-1 = filled)
    succ = []
    for (u, th, M) in knodes:
        c = unf[u]
        T = C.trans(c, th)
        s = set()
        for comp in C.components(c, th, T, M):
            c2 = list(c)
            for x in comp:
                c2[x] = swapcol(c2[x], th)
            cc, sig = canon(c2)
            if C.filled(cc):
                s.add(-1)
            else:
                s.add(kid[(cc, map_split(th, sig), M)])
        succ.append(tuple(s))
    # group K-nodes by (u, th)
    byu = [[[] for _ in range(4)] for _ in unf]
    for i, (u, th, M) in enumerate(knodes):
        byu[u][th].append(i)
    t1 = time.process_time()
    K = [INF] * len(knodes)
    U = [INF] * len(unf)
    rounds = 0
    while True:
        rounds += 1
        A = [1 + min((0 if j < 0 else K[j]) for j in s) for s in succ]
        Un = []
        for u in range(len(unf)):
            best = INF
            for th in (1, 2, 3):
                ids = byu[u][th]
                val = max(A[i] for i in ids) if ids else INF
                best = min(best, val)
            Un.append(min(best, INF))
        Kn = [min(Un[knodes[i][0]], A[i], INF) for i in range(len(knodes))]
        Kn = [x if x < INF else INF for x in Kn]
        Un = [x if x < INF else INF for x in Un]
        if Kn == K and Un == U:
            break
        K, U = Kn, Un
    t2 = time.process_time()
    hist = {}
    for x in U:
        hist[x] = hist.get(x, 0) + 1
    res = dict(colourings=len(cols), unfilled=len(unf), knodes=len(knodes),
               reducible=all(x < INF for x in U), depth=max(U) if all(x < INF for x in U) else None,
               hist={('inf' if k >= INF else k): v for k, v in sorted(hist.items())},
               cpu_build=round(t1 - t0, 2), cpu_solve=round(t2 - t1, 2), rounds=rounds)
    res['_U'] = {c: U[i] for i, c in enumerate(unf)}
    res['_C'] = C
    return res


if __name__ == '__main__':
    import graphs
    which = sys.argv[1:] or ['T4', 'A3', 'pentakis']
    for w in which:
        w, _, rr = w.partition(':')
        rr = int(rr or 2)
        if w == 'T4':
            F, v = graphs.T4(), 4
        elif w.startswith('A'):
            F, v = graphs.A(int(w[1:])), 0
        elif w == 'pentakis':
            F, v = graphs.pentakis(), 0
        graphs.check_triangulation(F)
        cfg = graphs.ball_config(F, v, rr)
        print(w, 'r =', rr, 'v =', v, 'link', cfg['link'], 'ring', cfg['ring'], flush=True)
        r = solve(cfg)
        print('  ', {k: x for k, x in r.items() if not k.startswith('_')}, flush=True)
