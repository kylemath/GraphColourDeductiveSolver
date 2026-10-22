"""Kempe traces of a coloured disc (or annulus with one distinguished boundary cycle).

trace(adj, S, col, bd, pair) -> list of blocks; each block = sorted tuple of boundary POSITIONS (indices into bd)
   of the boundary vertices coloured in `pair` that lie in one connected component of G[S][{x,y}].
traces(adj, S, col, bd) -> dict {(x,y): blocks} for the 6 pairs.
noncrossing(blocks) -> bool  (cyclic non-crossing of the position sets)
signature(blocks, L) -> dict(nblocks, nsingle, depth, maxspan)
   depth   = cyclic nesting depth (min over cut points of the linear nesting depth; 1 = no nesting)
   maxspan = largest cyclic span of a block (0 for singletons); a block fits in a window of width maxspan+1.
"""
import itertools
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

def _find(par, x):
    while par[x] != x:
        par[x] = par[par[x]]; x = par[x]
    return x

def trace(adj, S, col, bd, pair):
    x, y = pair
    V = [v for v in S if col[v] in (x, y)]
    par = {v: v for v in V}
    for v in V:
        for u in adj[v]:
            if u in par and u > v:
                a, b = _find(par, u), _find(par, v)
                if a != b: par[a] = b
    comp = {}
    for pos, v in enumerate(bd):
        if v in par: comp.setdefault(_find(par, v), []).append(pos)
    return sorted(tuple(b) for b in comp.values())

def traces(adj, S, col, bd):
    S = set(S)
    return {p: trace(adj, S, col, bd, p) for p in PAIRS}

def noncrossing(blocks):
    for P, Q in itertools.combinations(blocks, 2):
        # crossing iff exists a<b<c<d (linear order of positions) with a,c in P, b,d in Q or vice versa
        pts = sorted([(p, 0) for p in P] + [(q, 1) for q in Q])
        # count alternations around the cycle
        lab = [t for _, t in pts]
        alt = sum(1 for i in range(len(lab)) if lab[i] != lab[i-1])
        if alt >= 4: return False
    return True

def span(block, L):
    if len(block) == 1: return 0
    b = sorted(block); gaps = [(b[(i+1) % len(b)] - b[i]) % L for i in range(len(b))]
    return L - max(gaps)

def _linear_depth(blocks):
    iv = sorted(((min(b), -max(b)) for b in blocks))
    stack = []; best = 0
    for lo, nhi in iv:
        hi = -nhi
        while stack and stack[-1] < lo: stack.pop()
        stack.append(hi); best = max(best, len(stack))
    return best

def depth(blocks, L):
    if not blocks: return 0
    best = None
    for cut in range(L):
        rb = [tuple(sorted(((p - cut) % L) for p in b)) for b in blocks]
        d = _linear_depth(rb)
        if best is None or d < best: best = d
    return best

def signature(blocks, L):
    return dict(nblocks=len(blocks), nsingle=sum(1 for b in blocks if len(b) == 1),
                depth=depth(blocks, L), maxspan=max((span(b, L) for b in blocks), default=0))

def summary(tr, L):
    """aggregate over the 6 pairs"""
    sig = {p: signature(b, L) for p, b in tr.items()}
    return dict(nblocks=sum(s['nblocks'] for s in sig.values()), nsingle=sum(s['nsingle'] for s in sig.values()),
                depth=max(s['depth'] for s in sig.values()), maxspan=max(s['maxspan'] for s in sig.values()),
                noncrossing=all(noncrossing(b) for b in tr.values()), per_pair=sig)

def boundary_cycle(adj, S):
    """ordered boundary cycle of a disc S (vertices of S with a neighbour outside), assuming it is an induced cycle."""
    S = set(S); bd = [v for v in S if any(u not in S for u in adj[v])]
    bs = set(bd)
    nb = {v: [u for u in adj[v] if u in bs] for v in bd}
    if any(len(nb[v]) != 2 for v in bd): return None
    cyc = [bd[0]]; prev = None
    while True:
        cur = cyc[-1]; nxt = nb[cur][0] if nb[cur][0] != prev else nb[cur][1]
        if nxt == cyc[0]: break
        cyc.append(nxt); prev = cur
    return cyc if len(cyc) == len(bd) else None
