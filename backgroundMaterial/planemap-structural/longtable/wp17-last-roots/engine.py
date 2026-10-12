"""WP17 exploratory engine: per-root state graphs with extended feature vectors (cached)."""
import itertools, json, pickle, sys
from collections import deque
from pathlib import Path
HERE = Path(__file__).resolve().parent
LT = HERE.parent
sys.path.insert(0, str(LT))
from mass_core import RootState, parse_ascii, degree_five, FIXTURES
from wp11_cert import components, features as wp11_features, FEATURES

PAIRS = list(itertools.combinations(range(4), 2))
CACHE = HERE / "cache"


def corpus_graphs(orders=range(12, 21)):
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    for o in table["orders"]:
        if o["order"] in orders:
            for g in o["graphs_checked"]:
                yield o["order"], g["graph_index"], g["ascii"], parse_ascii(g["ascii"])


def bfs_dist(rot, r):
    """graph distances in T - r from the boundary set"""
    B = set(rot[r]); d = {v: 0 for v in B}; dq = deque(B)
    while dq:
        v = dq.popleft()
        for w in rot[v]:
            if w != r and w not in d:
                d[w] = d[v] + 1; dq.append(w)
    return d


def ext_features(rot, r, adj, B, col, dist):
    p, f = wp11_features(adj, B, col)
    f = dict(f)
    Bset = set(B)
    comps = components(adj, col)
    meets = [(pr, K) for pr, K in comps if K & Bset]
    cols = [col[v] for v in B]
    ext = [K - Bset for _, K in meets]
    f["maxK"] = max((len(e) for e in ext), default=0)
    f["touched"] = len(set().union(*ext)) if ext else 0
    f["nComp"] = len(meets)
    f["distSum"] = sum(dist[v] for e in ext for v in e)
    f["dist2"] = sum(dist[v] ** 2 for e in ext for v in e)
    f["allComps"] = len(comps)
    f["lin_int"] = sum(len(K) for _, K in comps if not (K & Bset))  # interior mass
    if p == 1:
        rho = next(x for x in set(cols) if cols.count(x) == 2)
        f["linRho"] = sum(len(K - Bset) for pr, K in meets if rho in pr)
        f["linNoRho"] = f["lin"] - f["linRho"]
        single = [v for v in B if cols.count(col[v]) == 1]
        # number of pairs of singleton boundary vertices joined by a 2-coloured chain
        where = {(pr, v): K for pr, K in comps for v in K}
        sl = 0
        for u, v in itertools.combinations(single, 2):
            pr = tuple(sorted((col[u], col[v])))
            if v in where[(pr, u)]:
                sl += 1
        f["singLinks"] = sl
        # rho-vertices: are the two rho vertices separated... chains from rho vertices to singles
        rv = [v for v in B if col[v] == rho]
        f["rhoLinks"] = sum(1 for a in rv for s in single
                            if s in where[(tuple(sorted((rho, col[s]))), a)])
        # boundary position: gap between the two rho vertices (1 or 2 in a 5-cycle: always 2 since nonadjacent)
    else:
        for k in ("linRho", "linNoRho", "singLinks", "rhoLinks"):
            f[k] = 0
    return p, f


def build_root(rot, r):
    s = RootState(rot, r)
    adj = {v: [w for w in rot[v] if w != r] for v in s.V}
    B = list(rot[r])
    dist = bfs_dist(rot, r)
    P, F, N = [], [], []
    for i, c in enumerate(s.C):
        col = dict(zip(s.V, c))
        p, f = ext_features(rot, r, adj, B, col, dist)
        P.append(p); F.append(f)
        N.append(sorted({t for _, _, t in s.info[i]["moves"] if t != i}))
    # Kempe distance to target (p=0) in the state graph
    kd = {i: 0 for i in range(len(P)) if P[i] == 0}
    dq = deque(kd)
    while dq:
        i = dq.popleft()
        for t in N[i]:
            if t not in kd:
                kd[t] = kd[i] + 1; dq.append(t)
    for i in range(len(P)):
        F[i]["kd"] = kd.get(i, 999)
    return {"V": s.V, "C": s.C, "B": B, "P": P, "F": F, "N": N, "moves": [s.info[i]["moves"] for i in range(len(P))]}


def load_all(orders=range(12, 21)):
    CACHE.mkdir(exist_ok=True)
    out = {}
    for order, gi, asc, rot in corpus_graphs(orders):
        fn = CACHE / f"{order}-{gi}.pkl"
        if fn.exists():
            out[(order, gi)] = pickle.loads(fn.read_bytes())
            continue
        roots = {r: build_root(rot, r) for r in degree_five(rot)}
        g = {"rot": rot, "ascii": asc, "roots": roots}
        fn.write_bytes(pickle.dumps(g))
        out[(order, gi)] = g
    return out


def stuck_states(R, rankf, macro=2):
    """indices of p=1 states with no <=macro endpoint of strictly lower rank"""
    P, F, N = R["P"], R["F"], R["N"]
    rk = [(P[i], rankf(F[i])) if P[i] else (0,) for i in range(len(P))]
    rk = [(P[i], rankf(F[i])) for i in range(len(P))]
    bad = []
    for i in range(len(P)):
        if P[i] != 1:
            continue
        r0 = rk[i]
        frontier, seen, ok = {i}, {i}, False
        for _ in range(macro):
            nxt = set()
            for a in frontier:
                for t in N[a]:
                    if rk[t] < r0:
                        ok = True; break
                    nxt.add(t)
                if ok: break
            if ok: break
            frontier = nxt
        if not ok:
            bad.append(i)
    return bad
