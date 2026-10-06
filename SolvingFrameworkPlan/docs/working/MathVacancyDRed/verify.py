"""Independent brute-force verifier for the vacancy-D-reducibility abstraction.

[computed, exploratory] Math worker, 2026-10-06.

For explicit triangulations T containing the disc K (the original graph and random
completions obtained by edge flips strictly outside K):
  1. enumerate all proper 4-colourings of T - v (up to colour renaming);
  2. build the real Kempe graph (whole-component swaps, all six colour pairs, in T - v) and
     compute the real Kempe radius (swap distance to a filled state) of every state;
  3. CONSERVATIVITY A: for every state and every split th, the real partition of K - v into
     th-components of T - v must equal the abstract partition for SOME non-crossing matching M;
  4. CONSERVATIVITY B: real radius(s) <= abstract game value U(s|K) for every state s.
"""
import random, sys, time
from collections import defaultdict, deque
import graphs, vdred


def colourings_minus_v(F, v):
    adj = graphs.adjacency(F)
    # order: BFS from v's link
    order, seen = [], {v}
    dq = deque(sorted(adj[v]))
    seen |= set(adj[v])
    while dq:
        x = dq.popleft(); order.append(x)
        for y in sorted(adj[x]):
            if y not in seen:
                seen.add(y); dq.append(y)
    idx = {x: i for i, x in enumerate(order)}
    nbr = [[idx[y] for y in adj[x] if y != v] for x in order]
    n = len(order)
    c = [-1] * n
    out = []
    def rec(i, mx):
        if i == n:
            out.append(tuple(c)); return
        used = {c[j] for j in nbr[i] if c[j] >= 0}
        for col in range(min(mx + 2, 4)):
            if col not in used:
                c[i] = col; rec(i + 1, max(mx, col))
        c[i] = -1
    rec(0, -1)
    return order, idx, nbr, out


def comps(c, nbr, half):
    """components of the subgraph induced by vertices whose colour lies in `half`."""
    n = len(c)
    lab = [-1] * n
    res = []
    for s in range(n):
        if lab[s] >= 0 or c[s] not in half:
            continue
        lab[s] = len(res); comp = [s]; st = [s]
        while st:
            x = st.pop()
            for y in nbr[x]:
                if lab[y] < 0 and c[y] in half:
                    lab[y] = lab[s]; comp.append(y); st.append(y)
        res.append(comp)
    return res


def real_radius(F, v):
    order, idx, nbr, cols = colourings_minus_v(F, v)
    link = [idx[x] for x in graphs.adjacency(F)[v]]
    sid = {c: i for i, c in enumerate(cols)}
    filled = [len({c[i] for i in link}) <= 3 for c in cols]
    pairs = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    G = [set() for _ in cols]
    for i, c in enumerate(cols):
        for (a, b) in pairs:
            for comp in comps(c, nbr, (a, b)):
                c2 = list(c)
                for x in comp:
                    c2[x] = b if c2[x] == a else a
                cc, _ = vdred.canon(c2)
                j = sid[cc]
                if j != i:
                    G[i].add(j)
    dist = [None] * len(cols)
    dq = deque()
    for i in range(len(cols)):
        if filled[i]:
            dist[i] = 0; dq.append(i)
    while dq:
        i = dq.popleft()
        for j in G[i]:
            if dist[j] is None:
                dist[j] = dist[i] + 1; dq.append(j)
    return order, idx, nbr, cols, dist


def check(F, v, cfg, res, label):
    t0 = time.process_time()
    C = res['_C']; U = res['_U']
    order, idx, nbr, cols, dist = real_radius(F, v)
    kpos = [idx[x] for x in C.order]          # position in T-v colouring of K-v vertex i
    viol_A = viol_B = 0
    worst_gap = None
    nstates = len(cols)
    for s, c in enumerate(cols):
        ck = tuple(c[p] for p in kpos)
        if C.filled(ck):
            continue
        # A: partition inclusion, raw colours
        for th in (1, 2, 3):
            halfA = (0, th); halfB = tuple(x for x in range(4) if x not in halfA)
            real = set()
            for half in (halfA, halfB):
                for comp in comps(c, nbr, half):
                    cs = set(comp)
                    kk = frozenset(i for i, p in enumerate(kpos) if p in cs)
                    if kk:
                        real.add(kk)
            T = C.trans(ck, th)
            ok = any({frozenset(g) for g in C.components(ck, th, T, M)} == real
                     for M in vdred.nc_matchings(len(T)))
            if not ok:
                viol_A += 1
        # B: radius bound
        cc, _ = vdred.canon(ck)
        u = U[cc]
        r = dist[s]
        if u < vdred.INF and (r is None or r > u):
            viol_B += 1
        if u < vdred.INF and r is not None:
            worst_gap = max(worst_gap or 0, u - r)
    hist = defaultdict(int)
    for d in dist:
        hist[d] += 1
    return dict(label=label, n=len(order) + 1, states=nstates, radius_hist=dict(sorted(hist.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))),
                viol_A=viol_A, viol_B=viol_B, max_abstract_minus_real=worst_gap,
                cpu=round(time.process_time() - t0, 2))


def outside_flips(F, cfg, k, rng):
    """k random edge flips of edges both of whose faces lie outside the disc K."""
    Kverts = set(cfg['verts']) | {cfg['v']}
    adj0 = graphs.adjacency(F)
    # inside faces of the disc: same rule as ball_config
    v, r = cfg['v'], cfg['r']
    dist = {v: 0}; fr = [v]
    while fr:
        nf = []
        for x in fr:
            for y in adj0[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1; nf.append(y)
        fr = nf
    inside = {frozenset(f) for f in F if all(dist[x] <= r for x in f) and min(dist[x] for x in f) < r}
    faces = [frozenset(f) for f in F]
    done = 0; tries = 0
    while done < k and tries < 2000:
        tries += 1
        adj = graphs.adjacency([tuple(f) for f in faces])
        out = [f for f in faces if f not in inside]
        f = rng.choice(out)
        a, b = rng.sample(sorted(f), 2)
        g = [h for h in faces if a in h and b in h and h != f]
        if len(g) != 1 or g[0] in inside:
            continue
        g = g[0]
        c = next(iter(f - {a, b})); d = next(iter(g - {a, b}))
        if d in adj[c] or len(adj[a]) <= 3 or len(adj[b]) <= 3:
            continue
        faces.remove(f); faces.remove(g)
        faces += [frozenset((a, c, d)), frozenset((b, c, d))]
        done += 1
    F2 = [tuple(sorted(f)) for f in faces]
    graphs.check_triangulation(F2)
    return F2


if __name__ == '__main__':
    nvar = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    rng = random.Random(20261006)
    cases = [('T4', graphs.T4(), 4), ('A3', graphs.A(3), 0), ('A4', graphs.A(4), 0), ('pentakis', graphs.pentakis(), 0)]
    for name, F, v in cases:
        cfg = graphs.ball_config(F, v, 2)
        res = vdred.solve(cfg, verbose=False)
        print(name, 'abstract: reducible', res['reducible'], 'depth', res['depth'], res['hist'], flush=True)
        print('  ', check(F, v, cfg, res, name + ' original'), flush=True)
        nv = nvar if name != 'pentakis' else max(1, nvar // 5)
        for k in range(nv):
            F2 = outside_flips(F, cfg, rng.randint(1, 8), rng)
            print('  ', check(F2, v, cfg, res, f'{name} flipped#{k}'), flush=True)
