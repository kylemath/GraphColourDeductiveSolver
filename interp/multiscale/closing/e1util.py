from cl import *
_G = {}
def base(mapname):
    if mapname not in _G:
        if mapname.startswith('ico'): _G[mapname] = icosphere(int(mapname[3:]))
        else: _G[mapname] = load_map(mapname)
    return [set(a) for a in _G[mapname]]
def make_case(mapname, kind, rng):
    """kinds: bal (ball half), wig (random-frontier half), lop (B = small ball r 2-4), lopA (A tiny),
       dsx (defects flipped within distance 2 of the seam on both sides), dsA (defects only on A side),
       third (A ~ n/3 wiggly)"""
    adj = base(mapname); n = len(adj)
    for attempt in range(30):
        T = Tri(adj) if attempt == 0 or kind.startswith('ds') else T
        seedv = rng.randrange(n)
        if kind in ('bal', 'dsx', 'dsA'): A0 = grow(T, seedv, n//2, rng, wiggle=0.0)
        elif kind == 'wig': A0 = grow(T, seedv, n//2, rng, wiggle=1.0)
        elif kind == 'third': A0 = grow(T, seedv, n//3, rng, wiggle=0.7)
        elif kind == 'lop': A0 = set(range(n)) - set(bfs(T.adj, seedv, rng.choice([2, 3, 4])))
        elif kind == 'lopA': A0 = set(bfs(T.adj, seedv, rng.choice([1, 2, 3])))
        A, r = smooth(T, A0, rng)
        if A is None: continue
        meta = {}
        if kind.startswith('ds'):
            seam = set(x for e in seam_edges(T, A) for x in e)
            if kind == 'dsA':
                dA = multi_bfs(T.adj, [v for v in seam if v in A], A)
                cen = [v for v, d in dA.items() if d in (1, 2)]
            else: cen = list(seam)
            adj2 = flip_defects_near(T.adj, cen, 0, len(seam)//3, rng)
            if kind == 'dsA':  # keep flips with all four vertices inside A: redo restricted
                adj2 = flip_restricted(T.adj, set(cen), A, len(seam)//3, rng)
            T = Tri(adj2)
            A2, r = smooth(T, A, rng)
            if A2 is None: T = Tri(adj); continue
            A = A2; meta['flipped'] = True
        cA, cB = r
        meta['degs'] = dict(collections.Counter(T.deg))
        return T, A, cA, cB, meta
    return None, None, None, None, None
def flip_restricted(adj, region, A, nflips, rng, mindeg=5, maxdeg=9):
    adj = [set(a) for a in adj]; reg = sorted(region); done = 0; tries = 0
    while done < nflips and tries < nflips*300:
        tries += 1; a = rng.choice(reg); b = rng.choice(sorted(adj[a])); cn = adj[a] & adj[b]
        if len(cn) != 2 or b not in A: continue
        c, d = cn
        if c not in A or d not in A or d in adj[c]: continue
        if len(adj[a])-1 < mindeg or len(adj[b])-1 < mindeg or len(adj[c])+1 > maxdeg or len(adj[d])+1 > maxdeg: continue
        adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c); done += 1
    return adj
