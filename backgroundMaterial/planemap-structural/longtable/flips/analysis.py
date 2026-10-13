#!/usr/bin/env python3
"""analysis.py -- exploratory tests of strengthened / inductive forms of the
polygon (two-triangulation) form of the Four Colour Theorem.

All colourings of the n-gon vertices 0..n-1 are normalised c0=0, c1=1.
G  = proper 4-colourings of the cycle C_n (normalised).
L(T) = colourings in G proper on the diagonals of triangulation T.
S(T1,T2) = L(T1) & L(T2) (4CT in this form <=> S nonempty).
Sets are Python-int bitmasks over the index of G.

Usage: analysis.py TEST n      TEST in {density, window, flips, kauffman, kempe, union}
"""
import sys, itertools, collections, json, time


def triangulations(n):
    """all triangulations of the convex n-gon as frozensets of diagonals (u,v), u<v"""
    memo = {}

    def rec(i, j):
        if j - i < 2:
            return [frozenset()]
        if (i, j) in memo:
            return memo[(i, j)]
        out = []
        for k in range(i + 1, j):
            for a in rec(i, k):
                for b in rec(k, j):
                    s = set(a) | set(b)
                    if k - i >= 2:
                        s.add((i, k))
                    if j - k >= 2:
                        s.add((k, j))
                    out.append(frozenset(s))
        memo[(i, j)] = out
        return out

    return rec(0, n - 1)


def ground(n):
    G = []
    for rest in itertools.product(range(4), repeat=n - 2):
        c = (0, 1) + rest
        if all(c[i] != c[(i + 1) % n] for i in range(n)):
            G.append(c)
    return G


def setup(n):
    Ts = triangulations(n)
    G = ground(n)
    # chord masks
    chord = {}
    for u in range(n):
        for v in range(u + 2, n):
            if u == 0 and v == n - 1:
                continue
            m = 0
            for idx, c in enumerate(G):
                if c[u] != c[v]:
                    m |= 1 << idx
            chord[(u, v)] = m
    full = (1 << len(G)) - 1
    Lm = []
    for T in Ts:
        m = full
        for d in T:
            m &= chord[d]
        Lm.append(m)
    return Ts, G, chord, Lm, full


def dihedral_images(T, n):
    out = []
    for r in range(n):
        for f in (0, 1):
            s = []
            for (u, v) in T:
                if f:
                    u, v = (-u) % n, (-v) % n
                u, v = (u + r) % n, (v + r) % n
                s.append((min(u, v), max(u, v)))
            out.append(frozenset(s))
    return out


def reps(Ts, n):
    seen = set()
    out = []
    for i, T in enumerate(Ts):
        if T in seen:
            continue
        out.append(i)
        for X in dihedral_images(T, n):
            seen.add(X)
    return out


def flip_neighbours(T, n):
    """yield (old diagonal, new diagonal, T') for every flip of T"""
    edges = set(T) | {(i, i + 1) for i in range(n - 1)} | {(0, n - 1)}
    adj = collections.defaultdict(set)
    for (u, v) in edges:
        adj[u].add(v)
        adj[v].add(u)
    for (a, c) in T:
        common = sorted(adj[a] & adj[c])
        assert len(common) == 2, (T, a, c, common)
        b, d = common
        new = (min(b, d), max(b, d))
        yield (a, c), new, frozenset((set(T) - {(a, c)}) | {new})


def popcount(x):
    return bin(x).count("1")


# ---------------------------------------------------------------- density
def test_density(n):
    """|L(T)|, |G|, |U| (union of all languages), and densities; also edge
    (Klein) picture: U computed directly."""
    Ts, G, chord, Lm, full = setup(n)
    sizes = set(popcount(m) for m in Lm)
    U = 0
    for m in Lm:
        U |= m
    # intersection statistics over all ordered pairs, T1 from dihedral reps
    R = reps(Ts, n)
    cnts = collections.Counter()
    tot = 0
    for i in R:
        for m2 in Lm:
            c = popcount(Lm[i] & m2)
            cnts[c] += 1
    L = sizes.pop() if len(sizes) == 1 else None
    nU = popcount(U)
    # random-model expectation of |S| if languages were independent random subsets of U
    exp_rand = L * L / nU
    mean = sum(k * v for k, v in cnts.items()) / sum(cnts.values())
    # pigeonhole needs L/|U| > 1/2
    res = dict(n=n, triangulations=len(Ts), G=len(G), L=L, U=nU, dens_G=L / len(G), dens_U=L / nU,
               min_S=min(cnts), mean_S=mean, rand_model_S=exp_rand,
               frac_pairs_S_eq_2=cnts[2] / sum(cnts.values()))
    print(json.dumps(res))


# ---------------------------------------------------------------- window
def canon(seq):
    m = {}
    out = []
    for x in seq:
        if x not in m:
            m[x] = len(m)
        out.append(m[x])
    return tuple(out)


def test_window(n, kmax=6):
    """Thomassen-style precolouring: for each pair and each k, every colouring of
    the boundary window 0..k-1 that is proper on the union graph induced on the
    window, does it extend?  (windows at all positions are covered because all
    ordered pairs are enumerated and the problem is rotation-invariant).
    Also: window = two non-consecutive vertices u,v (u!=v colours forced?)."""
    Ts, G, chord, Lm, full = setup(n)
    out = {}
    for k in range(3, min(kmax, n - 1) + 1):
        pats = collections.defaultdict(int)
        for idx, c in enumerate(G):
            pats[canon(c[:k])] |= 1 << idx
        bad = 0
        first = None
        npairs = 0
        worst_frac = 1.0
        for a, T1 in enumerate(Ts):
            for b, T2 in enumerate(Ts):
                if b < a:
                    continue
                npairs += 1
                S = Lm[a] & Lm[b]
                ch = [(u, v) for (u, v) in (T1 | T2) if v < k]
                allowed = [p for p in pats if all(p[u] != p[v] for (u, v) in ch)]
                ok = [p for p in allowed if S & pats[p]]
                if len(ok) < len(allowed):
                    bad += 1
                    worst_frac = min(worst_frac, len(ok) / len(allowed))
                    if first is None:
                        first = dict(T1=sorted(T1), T2=sorted(T2), missing=[p for p in allowed if not S & pats[p]])
        out[k] = dict(pairs=npairs, pairs_with_nonextendable_window=bad, worst_fraction_extendable=worst_frac, first=first)
        print(json.dumps(dict(n=n, k=k, **out[k])))
    # two arbitrary vertices: both "equal" and "different" realisable when non-adjacent?
    forced = 0
    first = None
    npairs = 0
    for a, T1 in enumerate(Ts):
        for b, T2 in enumerate(Ts):
            if b < a:
                continue
            npairs += 1
            S = Lm[a] & Lm[b]
            E = T1 | T2
            for u in range(n):
                for v in range(u + 2, n):
                    if (u, v) in E or (u == 0 and v == n - 1):
                        continue
                    if not (S & ~chord[(u, v)]) or not (S & chord[(u, v)]):
                        forced += 1
                        if first is None:
                            first = dict(T1=sorted(T1), T2=sorted(T2), u=u, v=v,
                                         always_equal=not (S & chord[(u, v)]))
    print(json.dumps(dict(n=n, test="nonadjacent pair both equal and different", pairs=npairs,
                          forced_vertex_pairs=forced, first=first)))


# ---------------------------------------------------------------- flips
def test_flips(n):
    """(1) |L(T) & L(T')| / |L(T)| for every flip.
    (2) for each colouring c in U: is the flip graph restricted to
        {T : c in L(T)} connected?
    (3) Geodesic strengthening: for T1,T2 with S nonempty, does some
        flip-geodesic (shortest path in the full flip graph) keep a fixed
        colouring proper throughout?
    (4) halving bound |S(T1,T2)| >= |L| / 2^d(T1,T2)?"""
    Ts, G, chord, Lm, full = setup(n)
    index = {T: i for i, T in enumerate(Ts)}
    nbr = [[(old, new, index[T2]) for (old, new, T2) in flip_neighbours(T, n)] for T in Ts]
    ratios = collections.Counter()
    for i, T in enumerate(Ts):
        for (_, _, j) in nbr[i]:
            ratios[popcount(Lm[i] & Lm[j]) / popcount(Lm[i])] += 1
    print(json.dumps(dict(n=n, test="per-flip retained fraction", hist={str(k): v for k, v in ratios.items()})))
    # (2) connectivity of c-proper flip graphs
    U = 0
    for m in Lm:
        U |= m
    disconnected = 0
    ncol = 0
    first = None
    comps_hist = collections.Counter()
    for idx in range(len(G)):
        if not (U >> idx) & 1:
            continue
        ncol += 1
        nodes = [i for i in range(len(Ts)) if (Lm[i] >> idx) & 1]
        ns = set(nodes)
        seen = set()
        comps = 0
        for s in nodes:
            if s in seen:
                continue
            comps += 1
            st = [s]
            seen.add(s)
            while st:
                x = st.pop()
                for (_, _, y) in nbr[x]:
                    if y in ns and y not in seen:
                        seen.add(y)
                        st.append(y)
        comps_hist[comps] += 1
        if comps > 1:
            disconnected += 1
            if first is None:
                first = dict(c=G[idx], proper_triangulations=len(nodes), components=comps)
    print(json.dumps(dict(n=n, test="c-proper flip graph connected", colourings=ncol, disconnected=disconnected,
                          components_hist=dict(comps_hist), first=first)))
    # (3)+(4) geodesics, T1 over dihedral reps
    R = reps(Ts, n)
    geo_fail = 0
    geo_first = None
    halving_fail = 0
    halving_first = None
    npairs = 0
    min_ratio = 1e9
    extra_hist = collections.Counter()
    t0 = time.time()
    for a in R:
        # BFS distances
        dist = {a: 0}
        order = [a]
        for x in order:
            for (_, _, y) in nbr[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    order.append(y)
        # alive[x] = colours (bitmask) surviving along some geodesic from a to x
        alive = {a: Lm[a]}
        for x in order[1:]:
            m = 0
            for (_, _, y) in nbr[x]:
                if dist.get(y, 1e9) == dist[x] - 1:
                    m |= alive[y]
            alive[x] = m & Lm[x]
        # c-proper distance minimum (for how much longer than geodesic we need)
        for b in range(len(Ts)):
            npairs += 1
            S = Lm[a] & Lm[b]
            d = dist[b]
            if not alive[b]:
                geo_fail += 1
                if geo_first is None:
                    geo_first = dict(T1=sorted(Ts[a]), T2=sorted(Ts[b]), d=d, S=popcount(S))
            L = popcount(Lm[a])
            r = popcount(S) * (2 ** d) / L
            min_ratio = min(min_ratio, r)
            if r < 1:
                halving_fail += 1
                if halving_first is None:
                    halving_first = dict(T1=sorted(Ts[a]), T2=sorted(Ts[b]), d=d, S=popcount(S), L=L)
    print(json.dumps(dict(n=n, test="geodesic keeps a colouring", pairs=npairs, fails=geo_fail, first=geo_first)))
    print(json.dumps(dict(n=n, test="|S| >= |L|/2^d", pairs=npairs, fails=halving_fail, min_ratio=min_ratio,
                          first=halving_first)))
    # (5) for c-preserving paths: excess length over geodesic (n small only)
    if n <= 9:
        excess = collections.Counter()
        for a in R:
            dist = {a: 0}
            order = [a]
            for x in order:
                for (_, _, y) in nbr[x]:
                    if y not in dist:
                        dist[y] = dist[x] + 1
                        order.append(y)
            best = {}
            Lb = Lm[a]
            idxs = [i for i in range(len(G)) if (Lb >> i) & 1]
            for idx in idxs:
                dc = {a: 0}
                q = [a]
                for x in q:
                    for (_, _, y) in nbr[x]:
                        if y not in dc and (Lm[y] >> idx) & 1:
                            dc[y] = dc[x] + 1
                            q.append(y)
                for y, dd in dc.items():
                    if y not in best or dd < best[y]:
                        best[y] = dd
            for b in range(len(Ts)):
                excess[best[b] - dist[b]] += 1
        print(json.dumps(dict(n=n, test="min over common c of c-preserving distance minus flip distance",
                              hist=dict(excess))))


# ---------------------------------------------------------------- kauffman
UNIT_MUL = {}
for u in (1, 2, 3):
    for v in (1, 2, 3):
        if u == v:
            continue
        UNIT_MUL[(u, v)] = (1 if (u, v) in ((1, 2), (2, 3), (3, 1)) else -1, u ^ v)


def bracket_value(T, c, n):
    """signed cross-product value of the bracketing T (root side (0,n-1)) under
    leaf values x_i = c_i xor c_{i+1} (i=0..n-2), units 1=i,2=j,3=k."""
    E = set(T) | {(i, i + 1) for i in range(n - 1)}
    memo = {}

    def val(i, j):
        if j == i + 1:
            return (1, c[i] ^ c[i + 1])
        if (i, j) in memo:
            return memo[(i, j)]
        for k in range(i + 1, j):
            if ((i, k) in E) and ((k, j) in E):
                s1, u1 = val(i, k)
                s2, u2 = val(k, j)
                if u1 == 0 or u2 == 0 or u1 == u2:
                    r = (0, 0)
                else:
                    s, u = UNIT_MUL[(u1, u2)]
                    r = (s * s1 * s2, u)
                memo[(i, j)] = r
                return r
        raise RuntimeError

    return val(0, n - 1)


def test_kauffman(n):
    """Does every pair admit a common colouring whose two bracketings are equal
    *with sign* (not just up to sign)?"""
    Ts, G, chord, Lm, full = setup(n)
    sign = []
    for T, m in zip(Ts, Lm):
        sm = 0
        x = m
        while x:
            low = x & -x
            idx = low.bit_length() - 1
            s, u = bracket_value(T, G[idx], n)
            assert u != 0
            if s > 0:
                sm |= low
            x ^= low
        sign.append(sm)
    fails = 0
    first = None
    npairs = 0
    for a in range(len(Ts)):
        for b in range(a, len(Ts)):
            npairs += 1
            S = Lm[a] & Lm[b]
            eq = S & ~(sign[a] ^ sign[b])
            if not eq:
                fails += 1
                if first is None:
                    first = dict(T1=sorted(Ts[a]), T2=sorted(Ts[b]), S=popcount(S))
    # also: within L(T) is the + sign exactly half?
    halves = collections.Counter(popcount(s) / popcount(m) for s, m in zip(sign, Lm))
    print(json.dumps(dict(n=n, test="Kauffman equal-with-sign", pairs=npairs, fails=fails, first=first,
                          plus_fraction_hist={str(k): v for k, v in halves.items()})))


# ---------------------------------------------------------------- kempe
def test_kempe(n):
    """number of Kempe classes of the 4-colourings of the union graph (colourings
    modulo colour permutation), T1 over dihedral reps, all T2."""
    Ts, G, chord, Lm, full = setup(n)
    R = reps(Ts, n)
    hist = collections.Counter()
    first = None
    for a in R:
        for b in range(len(Ts)):
            S = Lm[a] & Lm[b]
            E = set(Ts[a]) | set(Ts[b]) | {(i, (i + 1) % n) for i in range(n)}
            adj = collections.defaultdict(list)
            for (u, v) in E:
                adj[u].append(v)
                adj[v].append(u)
            cols = set()
            x = S
            while x:
                low = x & -x
                cols.add(canon(G[low.bit_length() - 1]))
                x ^= low
            seen = set()
            classes = 0
            for c0 in cols:
                if c0 in seen:
                    continue
                classes += 1
                seen.add(c0)
                st = [c0]
                while st:
                    c = st.pop()
                    for p, q in itertools.combinations(range(4), 2):
                        done = set()
                        for s in range(n):
                            if c[s] not in (p, q) or s in done:
                                continue
                            comp = {s}
                            st2 = [s]
                            while st2:
                                y = st2.pop()
                                for z in adj[y]:
                                    if z not in comp and c[z] in (p, q):
                                        comp.add(z)
                                        st2.append(z)
                            done |= comp
                            d = list(c)
                            for y in comp:
                                d[y] = q if c[y] == p else p
                            d = canon(d)
                            if d not in seen:
                                seen.add(d)
                                st.append(d)
            hist[classes] += 1
            if classes > 1 and first is None:
                first = dict(T1=sorted(Ts[a]), T2=sorted(Ts[b]), colourings=len(cols), classes=classes)
    print(json.dumps(dict(n=n, test="Kempe classes of union graph", hist=dict(hist), first=first)))




# ---------------------------------------------------------------- halving
def crosses(e, f):
    (a, b), (c, d) = e, f
    if len({a, b, c, d}) < 4:
        return False
    return (a < c < b) != (a < d < b)


def test_halving(n):
    """(A) aggregated bound |S(T1,T2)| >= 2^(n-2-m), m = |T2 \\ T1|, all pairs.
    (B) per-step bound: for every T1, every dissection D (non-crossing chords,
        thought of as drawn outside) and every chord e not in T1|D that does not
        cross D: #col(T1+D+e) >= #col(T1+D)/2.
    (C) ordered version: for every pair there is an order of adding T2\\T1 in
        which every step keeps >= 1/2 (only checked where (B) fails)."""
    Ts, G, chord, Lm, full = setup(n)
    R = reps(Ts, n)
    failA = 0
    firstA = None
    minratio = 1e9
    for a in R:
        for b in range(len(Ts)):
            m = len(Ts[b] - Ts[a])
            s = popcount(Lm[a] & Lm[b])
            r = s / 2 ** (n - 2 - m)
            minratio = min(minratio, r)
            if r < 1:
                failA += 1
                if firstA is None:
                    firstA = dict(T1=sorted(Ts[a]), T2=sorted(Ts[b]), m=m, S=s)
    print(json.dumps(dict(n=n, test="aggregated |S| >= 2^(n-2-m)", pairs_T1reps=len(R) * len(Ts), fails=failA,
                          min_ratio=minratio, first=firstA)))
    # dissections
    diss = set()
    for T in Ts:
        T = sorted(T)
        for r in range(len(T) + 1):
            for sub in itertools.combinations(T, r):
                diss.add(frozenset(sub))
    chords = list(chord)
    failB = 0
    firstB = None
    worst = 1.0
    checks = 0
    for a in R:
        for D in diss:
            m = Lm[a]
            for d in D:
                m &= chord[d]
            tot = popcount(m)
            for e in chords:
                if e in Ts[a] or e in D or any(crosses(e, f) for f in D):
                    continue
                checks += 1
                keep = popcount(m & chord[e])
                if 2 * keep < tot:
                    failB += 1
                    if keep / tot < worst:
                        worst = keep / tot
                    if firstB is None or len(D) < len(firstB["D"]):
                        firstB = dict(T1=sorted(Ts[a]), D=sorted(D), e=e, before=tot, after=keep)
    print(json.dumps(dict(n=n, test="per-step chord keeps >= 1/2", dissections=len(diss), checks=checks,
                          fails=failB, worst_fraction=worst, smallest_D_fail=firstB)))
    # (C) ordered version
    failC = 0
    firstC = None
    for a in R:
        for b in range(len(Ts)):
            new = sorted(Ts[b] - Ts[a])
            # DP over subsets: reachable sets where every step kept >= 1/2
            start = Lm[a]
            reach = {0: start}
            frontier = [0]
            ok = False
            seen = {0}
            while frontier:
                nf = []
                for msk in frontier:
                    m = reach[msk]
                    if msk == (1 << len(new)) - 1:
                        ok = True
                        break
                    for i, e in enumerate(new):
                        if msk >> i & 1:
                            continue
                        m2 = m & chord[e]
                        if 2 * popcount(m2) >= popcount(m):
                            nm = msk | 1 << i
                            if nm not in seen:
                                seen.add(nm)
                                reach[nm] = m2
                                nf.append(nm)
                if ok:
                    break
                frontier = nf
            if not ok:
                failC += 1
                if firstC is None:
                    firstC = dict(T1=sorted(Ts[a]), T2=sorted(Ts[b]), S=popcount(Lm[a] & Lm[b]))
    print(json.dumps(dict(n=n, test="some order of adding T2-diagonals keeps >= 1/2 each step", fails=failC,
                          first=firstC)))


# ---------------------------------------------------------------- dissection bound
def test_dissect(n):
    """A': for every triangulation T1 (dihedral reps) and every dissection D
    (non-crossing chord set; drawn outside), #col(T1 + D) >= 2^(n-2-|D \\ T1|).
    Reports min ratio and the distribution of the slack exponent."""
    Ts, G, chord, Lm, full = setup(n)
    R = reps(Ts, n)
    diss = set()
    for T in Ts:
        T = sorted(T)
        for r in range(len(T) + 1):
            for sub in itertools.combinations(T, r):
                diss.add(frozenset(sub))
    fails = 0
    first = None
    minratio = 1e9
    tight = collections.Counter()
    checks = 0
    for a in R:
        for D in diss:
            m = Lm[a]
            for d in D:
                m &= chord[d]
            k = len(D - Ts[a])
            c = popcount(m)
            checks += 1
            r = c / 2 ** (n - 2 - k)
            minratio = min(minratio, r)
            if r == 1:
                tight[k] += 1
            if r < 1:
                fails += 1
                if first is None:
                    first = dict(T1=sorted(Ts[a]), D=sorted(D), k=k, col=c)
    print(json.dumps(dict(n=n, test="dissection bound #col(T1+D) >= 2^(n-2-|D-T1|)", dissections=len(diss),
                          checks=checks, fails=fails, min_ratio=minratio, tight_by_m=dict(tight), first=first)))


if __name__ == "__main__":
    test, n = sys.argv[1], int(sys.argv[2])
    globals()["test_" + test](n)
