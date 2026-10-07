#!/usr/bin/env python3
"""[exploratory] Run 26: engine + transport analysis for arbitrary plane triangulation T, degree-5 hole h, Kempe class given by a seed colouring.
Same pi / lambda / DL definitions as ../22-winding-escape/escape.py (re-implemented stand-alone, state = canonical tuple over BFS order of T-h
from link[0]; link order = rotation order at h), so it works for 37-vertex graphs where full enumeration is impossible."""
import sys, json, itertools, random
from collections import Counter
sys.path.insert(0, '../25-transport')
from scan import maxflow   # Ford-Fulkerson used in run 25

class Eng:
    def __init__(self, adj, hole, link):
        self.hole = hole; self.link = list(link)
        V = [u for u in adj if u != hole]
        order = [self.link[0]]; seen = {order[0]}
        for x in order:
            for y in sorted(adj[x]):
                if y != hole and y not in seen: seen.add(y); order.append(y)
        assert len(order) == len(V)
        self.order = order; idx = {u: i for i, u in enumerate(order)}; self.N = N = len(order)
        self.nbm = [0] * N
        for u in V:
            for w in adj[u]:
                if w != hole: self.nbm[idx[u]] |= 1 << idx[w]
        self.li = [idx[x] for x in self.link]
        self.linkmask = sum(1 << i for i in self.li)
        self._mv = {}
    @staticmethod
    def canon(c):
        mp = {}; return tuple(mp.setdefault(x, len(mp)) for x in c)
    def flood(self, start, M):
        comp = front = start; nbm = self.nbm
        while front:
            nb = 0; f = front
            while f:
                low = f & -f; nb |= nbm[low.bit_length() - 1]; f ^= low
            nb &= M & ~comp; comp |= nb; front = nb
        return comp
    @staticmethod
    def cm(s):
        c = [0, 0, 0, 0]
        for i, x in enumerate(s): c[x] |= 1 << i
        return c
    def comp(self, s, v, p, q):
        c = self.cm(s); return self.flood(1 << v, c[p] | c[q])
    def swap(self, s, K, p, q):
        d = list(s)
        for i in range(self.N):
            if K >> i & 1: d[i] = q if s[i] == p else p
        return self.canon(d)
    def moves(self, s):
        r = self._mv.get(s)
        if r is None:
            c = self.cm(s); r = []
            for p, q in itertools.combinations(range(4), 2):
                M = c[p] | c[q]
                while M:
                    K = self.flood(M & -M, c[p] | c[q]); M &= ~K
                    r.append((self.swap(s, K, p, q), p, q, K))
            self._mv[s] = r
        return r
    def pi_of(self, s):
        li = self.li; c = [s[li[t]] for t in range(5)]; cnt = Counter(c); comp = lambda v, p, q: self.comp(s, v, p, q); sw = lambda K, p, q: self.swap(s, K, p, q)
        if len(cnt) == 4:
            j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
            al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
            m, b = li[(j + 1) % 5], li[(j + 4) % 5]
            if comp(m, mu, B) >> b & 1: return sw(comp(li[(j + 2) % 5], al, A), al, A), 1
            return sw(comp(li[(j + 4) % 5], mu, B), mu, B), -1
        i = next(i for i in range(5) if cnt[c[i]] == 1)
        W, X, Y = c[i], c[(i + 1) % 5], c[(i + 2) % 5]; Z = ({0, 1, 2, 3} - {W, X, Y}).pop()
        K = comp(li[(i + 2) % 5], Y, Z)
        if not K >> li[(i + 4) % 5] & 1: return sw(K, Y, Z), -1
        return sw(comp(li[(i + 3) % 5], W, X), W, X), -3
    def dl_info(self, s):
        """None if not DL; else (alpha, lockmask = union of the two lock chains {mu,A}-comp of m and {mu,B}-comp of m)."""
        li = self.li; c = [s[li[t]] for t in range(5)]; cnt = Counter(c)
        if len(cnt) != 4: return None
        j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
        al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        m, a, b = li[(j + 1) % 5], li[(j + 3) % 5], li[(j + 4) % 5]
        K1 = self.comp(s, m, mu, A); K2 = self.comp(s, m, mu, B)
        if K1 >> a & 1 and K2 >> b & 1: return al, A, B, K1 | K2
        return None
    def is_filled(self, s): return len({s[i] for i in self.li}) == 3
    def bfs(self, s0):
        mem = [s0]; seen = {s0}
        for x in mem:
            for t, *_ in self.moves(x):
                if t not in seen: seen.add(t); mem.append(t)
        return mem
    def randcol(self, rng):
        N = self.N; prev = [[j for j in range(i) if self.nbm[i] >> j & 1] for i in range(N)]; col = [None] * N
        def rec(i):
            if i == N: return True
            cs = [0, 1, 2, 3]; rng.shuffle(cs)
            for c in cs:
                if all(col[j] != c for j in prev[i]):
                    col[i] = c
                    if rec(i + 1): return True
            return False
        rec(0); return self.canon(col)

def hall(pos, W, edges):
    """min over nonempty subsets S of positive cycles of cap(N(S))/supply(S); returns (ratio, S windings, cap, supply)."""
    best = None
    if len(pos) > 18: return None
    for r in range(1, len(pos) + 1):
        for S in itertools.combinations(pos, r):
            N = set().union(*[edges[z] for z in S]); c = sum(-W[n] for n in N); s = sum(W[z] for z in S)
            if best is None or c / s < best[0]: best = (c / s, sorted(W[z] for z in S), c, s)
    return best

def flow_report(pos, W, edges):
    sup = {z: W[z] for z in pos}; nb = set().union(*[edges[z] for z in pos]) if pos else set()
    snk = {n: -W[n] for n in nb}
    f = maxflow(sup, snk, edges); tot = sum(sup.values()); h = hall(pos, W, edges)
    return dict(ok=f == tot, flow=f, supply=tot, capreach=sum(snk.values()), nneg_reach=len(nb),
                hall_ratio=None if h is None else round(h[0], 3), hall_set=None if h is None else dict(W=h[1], cap=h[2], supply=h[3]))

def analyse_class(E, mem, tag):
    """mem: list of states of one Kempe class. Returns record or None if no positive pi-cycle."""
    pi = {}; lam = {}
    for x in mem: pi[x], lam[x] = E.pi_of(x)
    cyc = {}; cycles = []
    for x in mem:
        if x in cyc: continue
        z = []; y = x
        while y not in cyc: cyc[y] = len(cycles); z.append(y); y = pi[y]
        assert y == x
        sl = sum(lam[y] for y in z); assert sl % 5 == 0
        cycles.append((z, sl // 5))
    U = sum(1 for x in mem if not E.is_filled(x)); F = len(mem) - U
    assert 3 * F - U == -5 * sum(w for _, w in cycles), 'Theorem W'
    W = {i: w for i, (z, w) in enumerate(cycles)}
    pos = [i for i in W if W[i] > 0]
    if not pos: return None
    dl = {}
    def DL(x):
        if x not in dl: dl[x] = E.dl_info(x)
        return dl[x]
    ex = {}
    def exits(ci):
        """{target cycle: counters} over link-free swaps from states of cycle ci; keys: dlany, dlother, dlalpha, dllb, dlnonlb, any."""
        if ci in ex: return ex[ci]
        d = {}
        for x in cycles[ci][0]:
            info = DL(x)
            for t, p, q, K in E.moves(x):
                if t == x or K & E.linkmask: continue
                cj = cyc[t]
                if cj == ci: continue
                c = d.setdefault(cj, Counter()); c['any'] += 1
                if info:
                    al, A, B, lock = info
                    c['dl'] += 1
                    if frozenset((p, q)) in (frozenset((al, A)), frozenset((al, B))): c['alphaAB'] += 1
                    else: c['other'] += 1
                    if K & lock: c['lb'] += 1
                    else: c['nonlb'] += 1
                    if frozenset((p, q)) not in (frozenset((al, A)), frozenset((al, B))) and K & lock: c['other_lb'] += 1
        ex[ci] = d; return d
    neg = [i for i in W if W[i] < 0]
    ea = {z: {c for c, k in exits(z).items() if k['dl'] and W[c] < 0} for z in pos}
    eb = {z: {c for c, k in exits(z).items() if k['other'] and W[c] < 0} for z in pos}
    e_any = {z: {c for c, k in exits(z).items() if k['any'] and W[c] < 0} for z in pos}
    ed = {z: {c for c, k in exits(z).items() if k['lb'] and W[c] < 0} for z in pos}
    ee = {z: {c for c, k in exits(z).items() if k['other_lb'] and W[c] < 0} for z in pos}
    rep = dict(a_DL_allpairs=flow_report(pos, W, ea), b_DL_otherpair=flow_report(pos, W, eb), c_anystate=flow_report(pos, W, e_any),
               d_DL_lockbreaking=flow_report(pos, W, ed), e_DL_otherpair_lockbreaking=flow_report(pos, W, ee))
    # zero-winding relay need: only if (a) fails, else record 0 needed
    relay = None
    if not rep['a_DL_allpairs']['ok']:
        er = {}
        for z in pos:
            s = set(ea[z])
            for m, k in exits(z).items():
                if k['dl'] and W[m] == 0:
                    s |= {c for c, k2 in exits(m).items() if k2['any'] and W[c] < 0}
            er[z] = s
        relay = flow_report(pos, W, er)
    # lock-breaking statistics over exits from DL states of positive cycles
    lb = []
    for z in pos:
        tot = lbn = tn = lbneg = 0
        for c, k in exits(z).items():
            tot += k['dl']; lbn += k['lb']
            if W[c] < 0: tn += k['dl']; lbneg += k['lb']
        lb.append(dict(w=W[z], L=len(cycles[z][0]), nDL=sum(1 for x in cycles[z][0] if DL(x)), exits_DL=tot, exits_lockbreaking=lbn,
                       exits_to_neg=tn, exits_to_neg_lockbreaking=lbneg, exits_to_neg_nonlb=tn - lbneg))
    hist = Counter((w, len(z)) for z, w in cycles)
    # positive cycles: are all DL? (Gamma-cycles)
    return dict(tag=tag, states=len(mem), F=F, ncyc=len(cycles), sumw=sum(W.values()), minw=min(W.values()), npos=len(pos), nzero=sum(1 for i in W if W[i] == 0), nneg=len(neg),
                posW=sorted((W[z] for z in pos), reverse=True), supply=sum(W[z] for z in pos), zero_relay_needed=relay is not None,
                relay=relay, transport=rep, lockbreak=lb,
                every_pos_has_lb_exit_to_neg=all(r['exits_to_neg_lockbreaking'] > 0 for r in lb),
                all_neg_exits_lockbreaking=all(r['exits_to_neg_nonlb'] == 0 for r in lb),
                all_exits_lockbreaking=all(r['exits_DL'] == r['exits_lockbreaking'] for r in lb),
                hist=sorted([[w, L, n] for (w, L), n in hist.items()], reverse=True))
