# Geodesic top-down hierarchies (reviewer's suggestion) and seam/pocket statistics for any disc hierarchy.
# Root: shortest cycle separating two far-apart pole balls (cut-open along a shortest crossing path).
# Recursion: split disc U along a shortest path P in G[U] (or in an allowed set, mode 'deep') between boundary
# vertices x, y roughly opposite (mode 'refl': x, y reflex, d_U >= 5).  P goes to one side (both tried).
# Stats per split: G-chords of each child, their type (P-C, P-new, C-new, new-new) and distance to {x, y};
# per merge: j_A + j_B = number of pocket stretches the seam arcs cross (Lemma W), and pocket counts sA + sB.
import sys, random, collections, json, time
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy'); sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
sys.path.insert(0, '/mnt/project-files/multiscale')
import hier
from hier import G, check, chord_list, bfs_in

def rot_next(g, v, w):
    f = g.faces[g.face[(v, w)]]
    return [z for z in f if z != v and z != w][0]

def sides_of_path(g, Q, prev0, nextk):
    """for each Q[i]: set of neighbours on the 'L' side (rotation from next to prev)."""
    L = []
    for i, q in enumerate(Q):
        p = Q[i-1] if i > 0 else prev0; n = Q[i+1] if i+1 < len(Q) else nextk
        s = set(); z = rot_next(g, q, n)
        while z != p:
            s.add(z); z = rot_next(g, q, z)
        L.append(s)
    return L

def bfs_path(g, src, dst, allowed, rng):
    """shortest path in G[allowed], random tie breaking."""
    par = {src: None}; q = collections.deque([src])
    while q:
        x = q.popleft()
        if x == dst: break
        nb = [y for y in g.adj[x] if y in allowed and y not in par]; rng.shuffle(nb)
        for y in nb: par[y] = x; q.append(y)
    if dst not in par: return None
    P = [dst]
    while par[P[-1]] is not None: P.append(par[P[-1]])
    return P[::-1]

def shortest_sep_cycle(g, X, Y, rng):
    """shortest cycle of G - X - Y separating X from Y (X, Y connected)."""
    Vp = set(range(g.n)) - X - Y
    srcs = [v for v in Vp if g.adj[v] & X]
    d = bfs_in(g, srcs, Vp); ends = [v for v in Vp if v in d and g.adj[v] & Y]
    e = min(ends, key=lambda v: (d[v], rng.random()))
    Q = [e]
    while d[Q[-1]] > 0:
        Q.append(min((y for y in g.adj[Q[-1]] if y in d and d[y] == d[Q[-1]]-1), key=lambda y: rng.random()))
    Q = Q[::-1]
    prev0 = next(iter(g.adj[Q[0]] & X)); nextk = next(iter(g.adj[Q[-1]] & Y))
    Ls = sides_of_path(g, Q, prev0, nextk); qi = {q: i for i, q in enumerate(Q)}
    def nbrs(node):
        if isinstance(node, tuple):
            side, i = node; q = Q[i]; out = []
            for y in g.adj[q]:
                if y not in Vp: continue
                if y in qi:
                    if abs(qi[y]-i) == 1: out.append((side, qi[y]))
                elif (y in Ls[i]) == (side == 'L'): out.append(y)
            return out
        out = []
        for y in g.adj[node]:
            if y not in Vp: continue
            if y in qi:
                out.append(('L' if node in Ls[qi[y]] else 'R', qi[y]))
            else: out.append(y)
        return out
    best = None
    for i in range(len(Q)):
        s, t = ('L', i), ('R', i); par = {s: None}; dq = collections.deque([s])
        while dq:
            x = dq.popleft()
            if x == t: break
            for y in nbrs(x):
                if y not in par: par[y] = x; dq.append(y)
        if t not in par: continue
        P = [t]
        while par[P[-1]] is not None: P.append(par[P[-1]])
        cyc = [Q[x[1]] if isinstance(x, tuple) else x for x in P][:-1]
        if best is None or len(cyc) < len(best): best = cyc
    return best

def comps(g, S):
    S = set(S); seen = set(); out = []
    for v in S:
        if v in seen: continue
        c = {v}; q = [v]
        while q:
            z = q.pop()
            for t in g.adj[z]:
                if t in S and t not in c: c.add(t); q.append(t)
        seen |= c; out.append(c)
    return out

def chord_info(g, child_walk, P, C, dxy):
    """G-chords of a child boundary walk: type and distance (in U) of the nearer endpoint to {x, y}."""
    Ps, Cs = set(P), set(C); out = []
    for (u, w) in chord_list(g, child_walk):
        t = lambda v: 'P' if v in Ps else ('C' if v in Cs else 'N')
        out.append(dict(type=''.join(sorted(t(u)+t(w))), d=min(dxy.get(u, 99), dxy.get(w, 99))))
    return out

def try_split(g, U, walk, x, y, allowed, rng):
    """returns list of candidate (A, B, info) for path P from x to y; P assigned to either side."""
    P = bfs_path(g, x, y, allowed, rng)
    if P is None: return []
    m = len(walk); pos = {v: i for i, v in enumerate(walk)}; ix, iy = pos[x], pos[y]
    arc1 = set(walk[(ix+k) % m] for k in range(1, (iy-ix) % m)); arc2 = set(walk) - arc1 - {x, y}
    Ps = set(P); s1, s2 = set(), set(); stray = 0
    for c in comps(g, U - Ps):
        if c & arc1 and not c & arc2: s1 |= c
        elif c & arc2 and not c & arc1: s2 |= c
        else: stray += 1; s1 |= c   # cannot happen for a disc; recorded
    dxy = bfs_in(g, [x, y], U); out = []
    for A, B in ((s1 | Ps, s2), (s1, s2 | Ps)):
        if not A or not B: continue
        sa, sb = check(g, A), check(g, B)
        info = dict(x=x, y=y, lenP=len(P), stray=stray, stA=sa[0], stB=sb[0], chA=sa[2], chB=sb[2],
                    Pside='A' if Ps <= A else 'B',
                    chinfo=(chord_info(g, sa[1], P, walk, dxy) if sa[0] == 'chord' else []) + (chord_info(g, sb[1], P, walk, dxy) if sb[0] == 'chord' else []),
                    Pmin_dC=None)
        out.append((A, B, sa, sb, info, P))
    return out

def geo_split(g, U, walk, rng, mode='plain', e=2, npairs=8, minfrac=0.2):
    """mode: plain | refl (x, y reflex) | deep (P interior at d_C >= dmin except end vertices whose only C-neighbour
       is x or y) | refldeep | refldeep3 (dmin = 3)."""
    m = len(walk); du = {v: len(g.adj[v] & U) for v in walk}; Cs = set(walk)
    refl = [i for i in range(m) if du[walk[i]] >= 5]
    dC = bfs_in(g, walk, U); dmin = 3 if mode.endswith('3') else 2
    deep = 'deep' in mode
    def pairs(starts, frac):
        out = []
        for ix in rng.sample(starts, min(npairs, len(starts))):
            ys = [j for j in starts if frac*m <= (j-ix) % m <= (1-frac)*m]
            if ys: out.append((ix, ys))
        return out
    used_refl = False; pl = []
    if mode.startswith('refl') and len(refl) >= 2:
        pl = pairs(refl, 1/3) or pairs(refl, 1/4) or pairs(refl, 1/6); used_refl = bool(pl)
    if not pl: pl = pairs(list(range(m)), 1/3)
    cands = []
    for ix, ys in pl:
        x = walk[ix]; dx = bfs_in(g, [x], U)
        jy = max(ys, key=lambda j: (dx.get(walk[j], -1), rng.random())); y = walk[jy]
        if deep:
            dy = bfs_in(g, [y], U)
            allowed = set(v for v in U if v in (x, y) or dC[v] >= dmin or
                          ((dx.get(v, 99) <= e or dy.get(v, 99) <= e) and (g.adj[v] & Cs) <= {x, y}))
        else: allowed = U
        for (A, B, sa, sb, info, P) in try_split(g, U, walk, x, y, allowed, rng):
            info['Pmid_mindC'] = min([dC[v] for v in P[e+1:len(P)-e-1]], default=None)
            bal = min(len(A), len(B))/len(U)
            pen = (1000 if 'nodisc' in (sa[0], sb[0]) else 0) + (100 if bal < minfrac else 0)
            cands.append((pen + (sa[2] or 0) + (sb[2] or 0), -bal, rng.random(), A, B, sa, sb, info))
        if deep and not any(c[7]['x'] == x for c in cands):   # no deep path: plain path for this pair
            for (A, B, sa, sb, info, P) in try_split(g, U, walk, x, y, U, rng):
                info['Pmid_mindC'] = None; info['deep_fallback'] = True
                bal = min(len(A), len(B))/len(U)
                pen = (1000 if 'nodisc' in (sa[0], sb[0]) else 0) + (100 if bal < minfrac else 0)
                cands.append((pen + (sa[2] or 0) + (sb[2] or 0), -bal, rng.random(), A, B, sa, sb, info))
    if not cands: return None
    cands.sort(key=lambda t: t[:3]); c = cands[0]
    c[7]['used_refl'] = used_refl; c[7]['nrefl'] = len(refl); c[7]['bal'] = round(-c[1], 3)
    c[7]['any_chordless'] = any(t[5][0] == 'ok' and t[6][0] == 'ok' for t in cands)
    return c[3:]

def build_geo(g, L=40, seed=0, mode='plain', e=2, root_k=3):
    rng = random.Random(seed)
    s = rng.randrange(g.n); d = bfs_in(g, [s], set(range(g.n))); t = max(d, key=d.get)
    dt = bfs_in(g, [t], set(range(g.n))); s = max(dt, key=dt.get); ds = bfs_in(g, [s], set(range(g.n)))
    f = {v: ds[v]-dt[v] for v in range(g.n)}
    X = set(v for v in range(g.n) if f[v] < -root_k); Y = set(v for v in range(g.n) if f[v] > root_k)
    C = shortest_sep_cycle(g, X, Y, rng); Cs = set(C)
    sx = [c for c in comps(g, set(range(g.n)) - Cs)]
    sideX = set().union(*[c for c in sx if c & X]); sideY = set(range(g.n)) - Cs - sideX
    best = None
    for A, B in ((sideX | Cs, sideY), (sideX, sideY | Cs)):
        sa, sb = check(g, A), check(g, B); sc = (1000 if 'nodisc' in (sa[0], sb[0]) else 0) + (sa[2] or 0) + (sb[2] or 0)
        if best is None or sc < best[0]: best = (sc, A, B, sa, sb)
    _, A, B, sa, sb = best
    nodes = [dict(S=set(range(g.n)), kids=[], dep=0, info=dict(root=True, lenC=len(C), chA=sa[2], chB=sb[2], stA=sa[0], stB=sb[0], sizes=[len(A), len(B)]))]
    stack = [(A, sa, 1, 0), (B, sb, 1, 0)]
    while stack:
        U, st, dep, par = stack.pop()
        nid = len(nodes); nodes.append(dict(S=U, kids=[], dep=dep, info=None, chordless=(st[0] == 'ok'), nch=st[2]))
        nodes[par]['kids'].append(nid)
        if len(U) <= L or st[0] == 'nodisc': continue
        r = geo_split(g, U, st[1], rng, mode, e)
        if r is None or 'nodisc' in (r[2][0], r[3][0]):      # retry: more pairs, then deep routing
            for mo2 in (mode, 'deep' if 'deep' not in mode else 'plain'):
                r2 = geo_split(g, U, st[1], rng, mo2, e, npairs=24)
                if r2 is not None and 'nodisc' not in (r2[2][0], r2[3][0]): r = r2; r[4]['retry'] = mo2; break
        if r is None: nodes[nid]['info'] = dict(fail=True); continue
        A, B, sa, sb, info = r; nodes[nid]['info'] = info
        if 'nodisc' in (sa[0], sb[0]): info['leaf_nodisc'] = True; continue
        stack.append((A, sa, dep+1, nid)); stack.append((B, sb, dep+1, nid))
    return nodes

# ---------- seam statistics (any hierarchy) ----------
def disc_tris(g, S):
    return set(i for v in S for i in g.vf[v] if all(x in S for x in g.faces[i]))

def pocket_labels(g, S, tris):
    """triangle -> pocket id (cut along internal chords) and the boundary dict u -> w."""
    bd = {}; edges = set()
    for i in tris:
        f = g.faces[i]
        for j in range(3):
            u, w = f[j], f[(j+1) % 3]; edges.add(frozenset((u, w)))
            if g.face[(w, u)] not in tris: bd[u] = w
    bE = set(frozenset((u, w)) for u, w in bd.items())
    ch = set(e for e in edges if all(v in bd for v in e) and e not in bE)
    par = {i: i for i in tris}
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i in tris:
        f = g.faces[i]
        for j in range(3):
            u, w = f[j], f[(j+1) % 3]; o = g.face[(w, u)]
            if o in tris and frozenset((u, w)) not in ch: par[find(i)] = find(o)
    return {i: find(i) for i in tris}, bd, len(ch)

def seam_stats(g, U, A, B):
    """j_X = number of maximal stretches of X's seam arc lying in one pocket of X (pocket changes along the arc + 1
       per arc segment); s_X = number of pockets of X touching the seam arc."""
    tU = disc_tris(g, U); res = {}
    for nm, X in (('A', A), ('B', B)):
        tX = disc_tris(g, X); lab, bd, nch = pocket_labels(g, X, tX)
        if not bd: res[nm] = dict(j=0, s=0, ch=0); continue
        start = next(iter(bd)); walk = [start]
        while bd[walk[-1]] != start: walk.append(bd[walk[-1]])
        m = len(walk)
        seq = []   # per boundary edge: pocket id if seam edge else None
        for i in range(m):
            u, w = walk[i], walk[(i+1) % m]; o = g.face[(w, u)]
            seq.append(lab[g.face[(u, w)]] if o in tU else None)
        j = 0; pk = set(x for x in seq if x is not None)
        for i in range(m):
            if seq[i] is not None and (seq[i-1] is None or seq[i-1] != seq[i]): j += 1
        if all(x is not None for x in seq) and len(set(seq)) == 1: j = 1
        res[nm] = dict(j=j, s=len(pk), ch=nch)
    return dict(j=res['A']['j']+res['B']['j'], s=res['A']['s']+res['B']['s'], chA=res['A']['ch'], chB=res['B']['ch'], nU=len(U))

def tree_seams(g, nodes):
    out = []
    for i, nd in enumerate(nodes):
        if len(nd['kids']) == 2:
            a, b = nd['kids']; st = seam_stats(g, nd['S'], nodes[a]['S'], nodes[b]['S']); st['root'] = (i == 0); out.append(st)
    return out
