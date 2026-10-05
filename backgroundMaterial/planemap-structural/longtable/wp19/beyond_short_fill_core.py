"""Self-contained BFS for the mixed (slide + Kempe) and Kempe-only fill distances on an
arbitrary finite simple graph with palette {0..k-1}.  Written for beyond-short-fill.md;
independent of wp18_core / wp19_core.

Conventions (MathShortFillTheorem.md):
  state = (hole, colours) with colours a tuple over all vertices, colours[hole] = None.
  target: the hole's neighbour colours omit at least one palette colour.
  Kempe move: swap colours a,b on one whole connected component of the {a,b}-induced
    subgraph of G - hole (singleton components allowed).
  slide hole->u: legal when colours[u] occurs exactly once on N(hole); hole gets colours[u],
    u becomes the hole.
States are canonicalised by colour renaming (first occurrence in vertex order); every move
and the target predicate commute with renaming, so distances are unchanged.
"""
from collections import deque
from itertools import combinations


def canon(cols):
    seen = {}
    out = []
    for x in cols:
        if x is None:
            out.append(None)
        else:
            out.append(seen.setdefault(x, len(seen)))
    return tuple(out)


def is_proper(adj, cols):
    return all(cols[x] is None or cols[y] is None or cols[x] != cols[y]
               for x in range(len(adj)) for y in adj[x])


def is_target(adj, k, hole, cols):
    return len({cols[w] for w in adj[hole]}) < k


def kempe_moves(adj, k, hole, cols):
    """Yield (('K', a, b, frozenset(comp)), new_cols)."""
    n = len(adj)
    for a, b in combinations(range(k), 2):
        seen = set()
        for s in range(n):
            if s == hole or s in seen or cols[s] not in (a, b):
                continue
            comp = {s}
            st = [s]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y != hole and y not in comp and cols[y] in (a, b):
                        comp.add(y)
                        st.append(y)
            seen |= comp
            nxt = list(cols)
            for x in comp:
                nxt[x] = b if cols[x] == a else a
            yield ('K', a, b, frozenset(comp)), tuple(nxt)


def slide_moves(adj, hole, cols):
    lc = [cols[w] for w in adj[hole]]
    for u in adj[hole]:
        if lc.count(cols[u]) == 1:
            nxt = list(cols)
            nxt[hole] = cols[u]
            nxt[u] = None
            yield ('S', u), u, tuple(nxt)


def mixed_dist(adj, k, hole, cols, cap=None):
    """(ell, path) by BFS; ell None if no target within cap / at all."""
    start = (hole, canon(cols))
    prev = {start: None}
    q = deque([(start, 0)])
    while q:
        (h, c), d = q.popleft()
        if is_target(adj, k, h, c):
            path = []
            cur = (h, c)
            while prev[cur] is not None:
                p, mv = prev[cur]
                path.append(mv)
                cur = p
            return d, path[::-1]
        if cap is not None and d >= cap:
            continue
        for mv, nc in kempe_moves(adj, k, h, c):
            y = (h, canon(nc))
            if y not in prev:
                prev[y] = ((h, c), mv)
                q.append((y, d + 1))
        for mv, u, nc in slide_moves(adj, h, c):
            y = (u, canon(nc))
            if y not in prev:
                prev[y] = ((h, c), mv)
                q.append((y, d + 1))
    return None, None


def kempe_dist(adj, k, hole, cols, cap=None):
    """(kappa, path, class_size): Kempe-only BFS at the fixed hole, to exhaustion unless cap.
    kappa None means no target in the whole Kempe class ('nofill') when cap is None."""
    start = canon(cols)
    prev = {start: None}
    q = deque([(start, 0)])
    while q:
        c, d = q.popleft()
        if is_target(adj, k, hole, c):
            path = []
            cur = c
            while prev[cur] is not None:
                p, mv = prev[cur]
                path.append(mv)
                cur = p
            return d, path[::-1], len(prev)
        if cap is not None and d >= cap:
            continue
        for mv, nc in kempe_moves(adj, k, hole, c):
            y = canon(nc)
            if y not in prev:
                prev[y] = (c, mv)
                q.append((y, d + 1))
    return None, None, len(prev)


def fmt_move(mv):
    if mv[0] == 'S':
        return f"S->{mv[1]}"
    return f"K{{{mv[1]},{mv[2]}}}{sorted(mv[3])}"


def adj_from_edges(n, edges):
    adj = [set() for _ in range(n)]
    for x, y in edges:
        assert x != y
        adj[x].add(y)
        adj[y].add(x)
    return [sorted(a) for a in adj]


# ------------------------------------------------------------ whole-state-space BFS

def colourings_minus(adj, k, hole):
    """All proper k-colourings of G - hole, canonical (each renaming class once)."""
    n = len(adj)
    order = [v for v in range(n) if v != hole]
    cols = [None] * n
    out = []

    def rec(i, used):
        if i == len(order):
            out.append(tuple(cols))
            return
        v = order[i]
        for c in range(min(k, used + 1)):
            if all(cols[w] != c for w in adj[v]):
                cols[v] = c
                rec(i + 1, max(used, c + 1))
                cols[v] = None
    rec(0, 0)
    return out


def all_distances(adj, k, holes_kappa=None):
    """Return (ell, kappa): ell[(hole, cols)] mixed distance (missing = no target reachable);
    kappa[h][cols] Kempe-only distance at hole h for h in holes_kappa (missing = nofill).
    Both by multi-source BFS from targets; all moves are reversible."""
    n = len(adj)
    states = {h: colourings_minus(adj, k, h) for h in range(n)}
    ell = {}
    frontier = []
    for h in range(n):
        for c in states[h]:
            if is_target(adj, k, h, c):
                ell[(h, c)] = 0
                frontier.append((h, c))
    d = 0
    while frontier:
        d += 1
        nxt = []
        for h, c in frontier:
            for _, nc in kempe_moves(adj, k, h, c):
                y = (h, canon(nc))
                if y not in ell:
                    ell[y] = d
                    nxt.append(y)
            for _, u, nc in slide_moves(adj, h, c):
                y = (u, canon(nc))
                if y not in ell:
                    ell[y] = d
                    nxt.append(y)
        frontier = nxt
    kappa = {}
    for h in (holes_kappa if holes_kappa is not None else range(n)):
        kd = {}
        frontier = [c for c in states[h] if is_target(adj, k, h, c)]
        for c in frontier:
            kd[c] = 0
        d = 0
        while frontier:
            d += 1
            nxt = []
            for c in frontier:
                for _, nc in kempe_moves(adj, k, h, c):
                    y = canon(nc)
                    if y not in kd:
                        kd[y] = d
                        nxt.append(y)
            frontier = nxt
        kappa[h] = kd
    return states, ell, kappa


def replay(adj, k, hole, cols, path):
    """Replay a canonical-label path on actual colours.  Returns list of (move_text, hole,
    cols) in actual colours, and asserts each move is legal and the end is a target."""
    h = hole
    cur = tuple(cols)
    out = []
    for mv in path:
        if mv[0] == 'S':
            u = mv[1]
            lc = [cur[w] for w in adj[h]]
            assert u in adj[h] and lc.count(cur[u]) == 1, "illegal slide"
            nxt = list(cur)
            nxt[h] = cur[u]
            nxt[u] = None
            out.append((f"slide {h}->{u} carrying {cur[u]}", u, tuple(nxt)))
            h, cur = u, tuple(nxt)
        else:
            comp = mv[3]
            # find actual pair: canonical labels of cur
            cmap = {}
            for x in cur:
                if x is not None and x not in cmap:
                    cmap[x] = len(cmap)
            inv = {v: c for c, v in cmap.items()}
            a, b = inv.get(mv[1], None), inv.get(mv[2], None)
            # a label may be unused in cur; pick an unused actual colour
            unused = [c for c in range(k) if c not in cmap]
            if a is None:
                a = unused.pop(0)
            if b is None:
                b = unused.pop(0)
            # check comp is a whole {a,b} component of G - h
            assert h not in comp
            assert all(cur[x] in (a, b) for x in comp)
            for x in comp:
                for y in adj[x]:
                    if y != h and cur[y] in (a, b):
                        assert y in comp, "not a whole component"
            st = [min(comp)]
            seen = {min(comp)}
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y in comp and y not in seen:
                        seen.add(y)
                        st.append(y)
            assert seen == set(comp), "component not connected"
            nxt = list(cur)
            for x in comp:
                nxt[x] = b if cur[x] == a else a
            out.append((f"swap {{{a},{b}}} on {sorted(comp)}", h, tuple(nxt)))
            cur = tuple(nxt)
    assert is_target(adj, k, h, cur), "replay does not end at a target"
    assert is_proper(adj, cur)
    return out


# ------------------------------------------------------------ path anatomy (Lemma L3+)

def component(adj, hole, cols, start, pair):
    a, b = pair
    comp = {start}
    st = [start]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y != hole and y not in comp and cols[y] in (a, b):
                comp.add(y)
                st.append(y)
    return comp


def anatomy(adj, k, h, s, ell, kap_h=None):
    """For a start s (canonical, hole h) with ell(s) == 3, list every slide h->u with
    ell(t) == 2 and every two-swap Kempe fill K1 K2 of t at u, with the L3/L3+ flags."""
    out = []
    for mv, u, t in slide_moves(adj, h, s):
        tc = canon(t)
        if ell.get((u, tc)) != 2:
            continue
        sigma = t[h]
        for mv1, t1 in kempe_moves(adj, k, u, t):
            if is_target(adj, k, u, t1):
                continue
            fills2 = [mv2 for mv2, t2 in kempe_moves(adj, k, u, t1) if is_target(adj, k, u, t2)]
            if not fills2:
                continue
            _, a, b, K1 = mv1
            rho = b if a == sigma else a if b == sigma else None
            rec = {"u": u, "sigma": sigma, "pair": (a, b), "K1": sorted(K1),
                   "sigma_in_pair": rho is not None, "h_in_K1": h in K1,
                   "n_K2": len(fills2)}
            if rho is not None:
                rnu = [y for y in adj[u] if y != h and s[y] == rho]
                Ht = component(adj, u, t, h, (sigma, rho))
                J = component(adj, h, s, u, (sigma, rho))
                rec.update({
                    "rho": rho,
                    "rho_nbrs_u": rnu,
                    "rho_nbrs_u_in_K1": [y for y in rnu if y in K1],
                    "rho_nbrs_u_in_Ht": [y for y in rnu if y in Ht],
                    "K1_meets_Nh": sorted(set(K1) & set(adj[h]) - {u}),
                    "J_has_rho_nbr_h": any(y in J for y in adj[h] if s[y] == rho),
                    "common_rho_nbr_hu": [y for y in adj[h] if y in adj[u] and s[y] == rho],
                })
            out.append(rec)
    return out
