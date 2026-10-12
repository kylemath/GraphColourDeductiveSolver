"""Independent review core (Track C review of Track H).  Written from scratch from the
definitions in QuarterFloor.lean / NoFrozen.lean / QuarterLockParity.lean /
VacancyShortFill.lean (Target, pairGraph, KempeStep) and TrackF/LockParity.md.
No TrackH / TrackF code is imported or copied.

Conventions
  adj : list of lists (vertex -> neighbours), h the hole, x[0..4] the link in cyclic order.
  A colouring is a tuple col with col[h] = -1 (the hole's colour is irrelevant).
  pairGraph(a,b): vertices v != h with col[v] in {a,b}; edges of G between them.
"""
from itertools import permutations

PERMS = list(permutations(range(4)))


def parse_line(line):
    """'name n a,b,c;d,e;...' -> (name, adj).  Extra tokens ignored."""
    parts = line.split()
    name, n, body = parts[0], int(parts[1]), parts[2]
    rows = body.split(';')
    assert len(rows) == n, (len(rows), n)
    adj = [[int(t) for t in r.split(',') if t != ''] for r in rows]
    return name, adj


def validate_simple(adj):
    n = len(adj)
    errs = []
    for v in range(n):
        if v in adj[v]:
            errs.append(('loop', v))
        if len(set(adj[v])) != len(adj[v]):
            errs.append(('multi', v))
        for w in adj[v]:
            if not (0 <= w < n) or v not in adj[w]:
                errs.append(('asym', v, w))
    return errs


def link_info(adj, h, x):
    """Check Pent: x are exactly the 5 neighbours of h, consecutive ones adjacent.
    Returns dict with chords (non-consecutive link pairs that are adjacent)."""
    S = [set(a) for a in adj]
    ok_nb = sorted(adj[h]) == sorted(x) and len(x) == 5 and len(set(x)) == 5
    cyc = all(x[(i + 1) % 5] in S[x[i]] for i in range(5))
    chords = [(i, (i + 2) % 5) for i in range(5) if x[(i + 2) % 5] in S[x[i]]]
    return dict(pent=ok_nb and cyc, chords=chords)


def colourings(adj, h, canonical=False):
    """All proper 4-colourings of G - h.  canonical=True: one per renaming orbit
    (first-occurrence normal form along the search order)."""
    n = len(adj)
    verts = [v for v in range(n) if v != h]
    # order: BFS-ish greedy max-constraint order for speed
    order = []
    placed = set()
    deg_in = {v: 0 for v in verts}
    while len(order) < len(verts):
        best = max((v for v in verts if v not in placed), key=lambda v: (deg_in[v], len(adj[v])))
        order.append(best)
        placed.add(best)
        for w in adj[best]:
            if w in deg_in:
                deg_in[w] += 1
    pos = {v: i for i, v in enumerate(order)}
    back = [[w for w in adj[v] if w != h and pos.get(w, 10**9) < pos[v]] for v in order]
    col = [-1] * n
    out = []

    def rec(i, maxc):
        if i == len(order):
            out.append(tuple(col))
            return
        v = order[i]
        used = 0
        for w in back[i]:
            used |= 1 << col[w]
        lim = min(3, maxc + 1) if canonical else 3
        for c in range(lim + 1):
            if not (used >> c) & 1:
                col[v] = c
                rec(i + 1, max(maxc, c))
        col[v] = -1

    rec(0, -1)
    if canonical:
        out = sorted({canon(c) for c in out})
    return out


def canon(col):
    """Renaming-orbit normal form: relabel colours by first occurrence in vertex order."""
    m = {}
    out = []
    for c in col:
        if c < 0:
            out.append(c)
            continue
        if c not in m:
            m[c] = len(m)
        out.append(m[c])
    return tuple(out)


def components(adj, h, col, a, b):
    """Components of pairGraph(a,b) restricted to active vertices: list of frozensets."""
    n = len(adj)
    seen = [False] * n
    comps = []
    for s in range(n):
        if s == h or seen[s] or col[s] not in (a, b):
            continue
        stack = [s]
        seen[s] = True
        comp = [s]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w != h and not seen[w] and col[w] in (a, b):
                    seen[w] = True
                    stack.append(w)
                    comp.append(w)
        comps.append(frozenset(comp))
    return comps


def comp_of(adj, h, col, a, b, v):
    if v == h or col[v] not in (a, b):
        return frozenset()
    seen = {v}
    stack = [v]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w != h and w not in seen and col[w] in (a, b):
                seen.add(w)
                stack.append(w)
    return frozenset(seen)


def swap(col, a, b, S):
    c = list(col)
    for v in S:
        c[v] = b if col[v] == a else a
    return tuple(c)


def kempe_neighbours(adj, h, col):
    """All KempeStep images (Lean KempeStep: a != b, a whole component with an active seed)."""
    res = []
    for a in range(4):
        for b in range(a + 1, 4):
            for K in components(adj, h, col, a, b):
                res.append(((a, b), K, swap(col, a, b, K)))
    return res


def filled(col, x):
    """Lean Target: some colour is missing on all neighbours of h."""
    return len({col[v] for v in x}) < 4


def repeat_j(col, x):
    """Unique j with RepeatAt (c x_j = c x_{j+2}, the other three distinct and distinct from it)."""
    js = []
    for j in range(5):
        a = col[x[j]]
        if a != col[x[(j + 2) % 5]]:
            continue
        m, A, B = col[x[(j + 1) % 5]], col[x[(j + 3) % 5]], col[x[(j + 4) % 5]]
        if len({a, m, A, B}) == 4:
            js.append(j)
    return js


def roles(col, x, j):
    X = [x[(j + k) % 5] for k in range(5)]
    al, mu, A, B = col[X[0]], col[X[1]], col[X[3]], col[X[4]]
    return X, al, mu, A, B


def boundary(adj, S):
    """|delta(S)| in G (edges to h count)."""
    return sum(1 for u in S for w in adj[u] if w not in S)


def oddcount(adj, S):
    return sum(1 for u in S if len(adj[u]) % 2 == 1)


def state_info(adj, h, x, col):
    """All hole-local quantities of an unfilled state (None if filled)."""
    js = repeat_j(col, x)
    if not js:
        return None
    assert len(js) == 1
    j = js[0]
    X, al, mu, A, B = roles(col, x, j)
    L1 = X[3] in comp_of(adj, h, col, mu, A, X[1])
    L2 = X[4] in comp_of(adj, h, col, mu, B, X[1])
    KaA = comp_of(adj, h, col, al, A, X[2])
    KaB = comp_of(adj, h, col, al, B, X[2])
    Kam = comp_of(adj, h, col, al, mu, X[2])
    inA = X[0] in KaA
    inB = X[0] in KaB
    bA, bB, bM = boundary(adj, KaA), boundary(adj, KaB), boundary(adj, Kam)
    oA, oB, oM = oddcount(adj, KaA), oddcount(adj, KaB), oddcount(adj, Kam)
    d = dict(j=j, roles=(al, mu, A, B), L1=L1, L2=L2, inA=inA, inB=inB,
             DL=L1 and L2,
             D1=(L1 == (not inB)), D2=(L2 == (not inA)),
             P1=((bA % 2 == 1) == (not inA)), P2=((bB % 2 == 1) == (not inB)), P3=(bM % 2 == 1),
             LP2=(L2 == (bA % 2 == 1)), LP1=(L1 == (bB % 2 == 1)),
             LP2odd=(L2 == (oA % 2 == 1)), LP1odd=(L1 == (oB % 2 == 1)),
             handshakeA=(bA % 2 == oA % 2), handshakeB=(bB % 2 == oB % 2), handshakeM=(bM % 2 == oM % 2),
             KaA=KaA, KaB=KaB)
    return d


def pi_map(adj, h, x, col, info=None):
    """pi = swap K_{alpha A}(x_{j+2}), defined iff x_j not in it.  Returns None if undefined."""
    if info is None:
        info = state_info(adj, h, x, col)
    if info is None or info['inA']:
        return None
    al, mu, A, B = info['roles']
    return swap(col, al, A, info['KaA'])


def pair_counts(adj, h, x, col, info):
    """(#alpha-mu, #AB, #alpha-A, #mu-B, #alpha-B, #mu-A) component counts (active vertices)."""
    al, mu, A, B = info['roles']
    pairs = [(al, mu), (A, B), (al, A), (mu, B), (al, B), (mu, A)]
    return tuple(len(components(adj, h, col, p, q)) for p, q in pairs)


RIGID = (1, 1, 2, 1, 2, 1)


def is_rigid(adj, h, x, col, info=None):
    if info is None:
        info = state_info(adj, h, x, col)
    if info is None or not info['DL'] or not info['D1'] or not info['D2']:
        return False
    return pair_counts(adj, h, x, col, info) == RIGID
