# Chordless hierarchy constructor (step (c) of Conjecture LML).
# A chordless disc = vertex set S spanning a near-triangulated disc whose boundary cycle is induced in G.
# Top-down: split a chordless disc U into two chordless discs A,B (sublevel sets of discrete harmonic functions,
# plus a small local repair), recurse until |U| <= L.  Root: split V(G) into two chordless discs.
import sys, random, collections, itertools, pickle, math, time
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla
import networkx as nx
sys.path.insert(0, '/mnt/project-files/multiscale'); sys.path.insert(0, '/mnt/project-files/multiscale/levelling')

class G:
    def __init__(self, adj):
        self.adj = [set(a) for a in adj]; n = self.n = len(adj)
        H = nx.Graph(); H.add_nodes_from(range(n))
        H.add_edges_from((u, w) for u in range(n) for w in adj[u] if u < w)
        ok, emb = nx.check_planarity(H); assert ok
        self.face = {}; self.faces = []; seen = set()
        for u, w in emb.edges():
            if (u, w) in seen: continue
            f = emb.traverse_face(u, w, mark_half_edges=seen); assert len(f) == 3
            fid = len(self.faces); self.faces.append(tuple(f))
            for i in range(3): self.face[(f[i], f[(i+1) % 3])] = fid
        assert len(self.faces) == 2*n-4
        self.vf = [[] for _ in range(n)]
        for i, f in enumerate(self.faces):
            for x in f: self.vf[x].append(i)
        self.deg = [len(a) for a in adj]
        self.fs = set(frozenset(f) for f in self.faces)

def check(g, S):
    """returns (status, walk, nchords). status: 'ok' chordless disc; 'chord' disc with chords (in G); 'nodisc'."""
    S = S if isinstance(S, set) else set(S)
    tris = set(i for v in S for i in g.vf[v] if all(x in S for x in g.faces[i]))
    if not tris: return 'nodisc', None, None
    V = set(x for i in tris for x in g.faces[i])
    if V != S: return 'nodisc', None, None
    nE = 0; bd = {}
    for i in tris:
        f = g.faces[i]
        for j in range(3):
            u, w = f[j], f[(j+1) % 3]
            other = g.face[(w, u)]
            if other not in tris:
                if u in bd: return 'nodisc', None, None
                bd[u] = w; nE += 2
            else: nE += 1
    nE //= 2
    if len(V)-nE+len(tris) != 1 or not bd: return 'nodisc', None, None
    start = next(iter(bd)); walk = [start]; x = bd[start]
    while x != start:
        walk.append(x); x = bd[x]
        if len(walk) > len(bd): return 'nodisc', None, None
    if len(walk) != len(bd): return 'nodisc', None, None
    bset = set(walk); nch = 0
    for b in walk: nch += len(g.adj[b] & bset) - 2
    nch //= 2
    return ('ok' if nch == 0 else 'chord'), walk, nch

def chord_list(g, walk):
    m = len(walk); pos = {v: i for i, v in enumerate(walk)}
    return [(u, w) for u in walk for w in g.adj[u] if w in pos and u < w and (pos[u]-pos[w]) % m not in (1, m-1)]

def harmonic(g, U, dir0, dir1, rng):
    """harmonic on U with f=0 on dir0, 1 on dir1 (Neumann elsewhere), plus tiny noise for tie breaking."""
    Ul = list(U); ix = {v: i for i, v in enumerate(Ul)}; n = len(Ul)
    fixed = {v: 0.0 for v in dir0}; fixed.update({v: 1.0 for v in dir1})
    free = [v for v in Ul if v not in fixed]; fi = {v: i for i, v in enumerate(free)}
    rows, cols, vals = [], [], []; b = np.zeros(len(free))
    for v in free:
        i = fi[v]; nb = [w for w in g.adj[v] if w in ix]
        rows.append(i); cols.append(i); vals.append(len(nb))
        for w in nb:
            if w in fi: rows.append(i); cols.append(fi[w]); vals.append(-1.0)
            else: b[i] += fixed[w]
    f = dict(fixed)
    if free:
        M = sp.csr_matrix((vals, (rows, cols)), shape=(len(free), len(free)))
        x = spla.spsolve(M.tocsc(), b)
        for v in free: f[v] = float(x[fi[v]])
    for v in f: f[v] += 1e-9*rng.random()
    return f

def score(st):
    s, w, nch = st
    return 0 if s == 'ok' else (nch if s == 'chord' else 1000)

def repair(g, U, A, maxit, minfrac):
    """greedy local search: moves are (vertices to A, vertices to B). Candidate moves come from chords
       (endpoints, small pockets, pocket + / neighbours across the seam) and non-disc defects."""
    A = set(A); B = U - A
    def ev(A, B):
        sa, sb = check(g, A), check(g, B); return score(sa)+score(sb), sa, sb
    cur, sa, sb = ev(A, B); tabu = set()
    for it in range(maxit):
        if cur == 0: return A, B
        cands = []
        for side, (X, Y, st) in enumerate(((A, B, sa), (B, A, sb))):
            def mv(toY, toX=frozenset()):
                toY = frozenset(toY); toX = frozenset(toX)
                cands.append((toX, toY) if side == 0 else (toY, toX))
            if st[0] == 'chord':
                for (x, y) in chord_list(g, st[1])[:4]:
                    mv({x}); mv({y})
                    rest = X-{x, y}; comps = []; seen = set()
                    for v in rest:
                        if v in seen: continue
                        c = {v}; q = [v]
                        while q:
                            z = q.pop()
                            for t in g.adj[z]:
                                if t in rest and t not in c: c.add(t); q.append(t)
                        seen |= c; comps.append(c)
                    comps.sort(key=len)
                    for c in comps[:-1]:
                        if len(c) < 0.2*len(U):
                            mv(c)
                            nb = set(w for v in c for w in g.adj[v] if w in Y)
                            if len(nb) < 12:
                                mv((), nb)
                                for w in nb: mv((), {w}); mv(c | {x}, ()); mv(c | {y}, ())
            elif st[0] == 'nodisc':
                bad = [v for v in X if not any(all(t in X for t in g.faces[i]) for i in g.vf[v])]
                for v in bad[:6]: mv({v})
                if not bad:
                    for v in list(X):
                        nd = 0
                        for i in g.vf[v]:
                            if all(t in X for t in g.faces[i]):
                                f = g.faces[i]; j = f.index(v); w = f[(j+1) % 3]
                                if not all(t in X for t in g.faces[g.face[(w, v)]]): nd += 1
                        if nd > 1:
                            mv({v})
                            for w in g.adj[v]:
                                if w in Y: mv((), {w})
                        if len(cands) > 30: break
        best = None
        for (toA, toB) in set(cands):
            key = (toA, toB)
            if key in tabu: continue
            A2 = (A - toB) | toA; B2 = U - A2
            if min(len(A2), len(B2)) < minfrac*len(U): continue
            r = ev(A2, B2)
            if best is None or r[0] < best[0][0]: best = (r, A2, B2, key)
        if best is None: break
        tabu.add((best[3][1], best[3][0]))   # forbid immediate undo
        (cur, sa, sb), A, B, _ = best
    return (A, B) if cur == 0 else None

def bfs_in(g, srcs, U):
    d = {s: 0 for s in srcs}; q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in g.adj[x]:
            if y in U and y not in d: d[y] = d[x]+1; q.append(y)
    return d

def reflex(g, X, walk):
    return sum(1 for v in walk if len(g.adj[v] & X) >= 5)

def split(g, U, walk, rng, tries=8, minfrac=0.2, nth=12, rep=8, L=12, want=4):
    """split chordless disc U (boundary walk; None for the whole sphere) into two chordless discs.
       Transitions are placed at reflex boundary vertices (U-degree >= 5, see Lemma 1); the apex is forced
       to the other side.  Several valid splits are collected; the one whose large children have the most
       reflex boundary vertices (then the most balanced) is returned.  None if no attempt was evaluable,
       (None, best_invalid, info) if no valid split was found."""
    Ul = list(U); best = None; att = 0; found = []; pairs = []
    n = len(Ul)
    if walk is not None:
        m = len(walk); pos = {v: i for i, v in enumerate(walk)}
        R = [i for i in range(m) if len(g.adj[walk[i]] & U) >= 5]
        apex = {}
        for i in range(m):
            a, b = walk[i], walk[(i+1) % m]
            z = [x for x in g.adj[a] & g.adj[b] & U if (frozenset((a, b, x)) in g.fs)]
            apex[i] = z[0] if z else None
    def q(X, st):
        return 99 if len(X) <= L else min(reflex(g, X, st[1]), want)
    for t in range(tries):
        if walk is None:
            s = rng.choice(Ul); d = bfs_in(g, [s], U); far = max(d, key=d.get)
            d2 = bfs_in(g, [far], U); s2 = max(d2, key=d2.get)
            dir0, dir1 = ([far], [s2]) if t % 2 == 0 else ([s], [far])
            if dir0 == dir1: continue
        else:
            # pick two transition edges, each with a reflex endpoint
            du = [len(g.adj[v] & U) for v in walk]
            T = [(i, 0) for i in R if du[(i+1) % m] >= 4] + [((i-1) % m, 1) for i in R if du[(i-1) % m] >= 4]   # (edge index, reflex endpoint: 0 = walk[i])
            if len(T) < 2 or t >= tries-1:
                # fallback: arbitrary arcs
                i = rng.randrange(m); a = rng.randint(max(1, m//3), max(1, (2*m)//3))
                dir0 = [walk[(i+k) % m] for k in range(a)]; dir1 = [walk[(i+k) % m] for k in range(a, m)]
            else:
                if t == 0 or not pairs:
                    pairs = []
                    for (e1, r1) in rng.sample(T, min(8, len(T))):
                        d = bfs_in(g, [walk[e1]], U)
                        for (e2, r2) in T:
                            ml = min((e2-e1) % m, (e1-e2) % m)
                            if ml >= max(2, m//6):
                                pairs.append(((d.get(walk[e2], 99)+1)/ml + 0.05*rng.random(), e1, r1, e2, r2))
                    pairs.sort(); pairs = pairs[:tries]
                    if not pairs: continue
                _, e1, r1, e2, r2 = pairs.pop(0)
                # A = arc walk[e1+1 .. e2]  (edge e1 = (walk[e1], walk[e1+1]) is a transition, likewise e2)
                arcA = [walk[(e1+1+k) % m] for k in range((e2-e1) % m)]
                arcB = [walk[(e2+1+k) % m] for k in range((e1-e2) % m)]
                if not arcA or not arcB: continue
                dir0, dir1 = set(arcA), set(arcB)
                for (e, r, side) in ((e1, r1, 'start'), (e2, r2, 'end')):
                    z = apex[e]
                    if z is None or z in dir0 or z in dir1: continue
                    a, b = walk[e], walk[(e+1) % m]
                    refl = a if r == 0 else b
                    # put apex on the side opposite the reflex endpoint
                    (dir1 if refl in dir0 else dir0).add(z)
                dir0, dir1 = list(dir0), list(dir1)
        f = harmonic(g, U, dir0, dir1, rng)
        sig = [0.0, 0.03, 0.08][t % 3]
        if sig:
            for v in f:
                if v not in dir0 and v not in dir1: f[v] += sig*rng.random()
        order = sorted(Ul, key=f.get)
        lo = max(1, int(minfrac*n)); ks = sorted(range(lo, n-lo+1), key=lambda k: abs(k-n/2))
        if len(ks) > nth: ks = ks[:: max(1, len(ks)//nth)][:nth]
        loc_best = None
        for k in ks:
            att += 1
            A = set(order[:k]); B = U - A
            if (walk is not None) and (not set(dir0) <= A or set(dir1) & A): continue
            sa, sb = check(g, A), check(g, B)
            if sa[0] == 'ok' and sb[0] == 'ok':
                found.append((min(q(A, sa), q(B, sb)), min(len(A), len(B)), A, B)); break
            sc = score(sa)+score(sb)
            if loc_best is None or sc < loc_best[0]: loc_best = (sc, A, B)
        else:
            if loc_best is not None and rep:
                r = repair(g, U, loc_best[1], rep, minfrac*0.5)
                if r:
                    A, B = r; found.append((min(q(A, check(g, A)), q(B, check(g, B))), min(len(A), len(B)), A, B))
            if loc_best is not None and (best is None or loc_best[0] < best[0]): best = loc_best
        if found and (max(x[0] for x in found) >= want or len(found) >= 4): break
    if found:
        x = max(found, key=lambda x: (x[0], x[1]))
        return x[2], x[3], dict(att=att, q=x[0])
    return None if best is None else (None, best, dict(att=att))

def exhaustive_split(g, U):
    """all partitions of a small U into two chordless discs; returns one (most balanced) or None."""
    Ul = sorted(U); n = len(Ul); best = None
    for mask in range(1, 2**(n-1)):
        A = set(Ul[i] for i in range(n) if mask >> i & 1); B = U - A
        if len(A) < 3 or len(B) < 3: continue
        if check(g, A)[0] == 'ok' and check(g, B)[0] == 'ok':
            bal = min(len(A), len(B))
            if best is None or bal > best[0]: best = (bal, A, B)
    return best and (best[1], best[2])

def build(g, L=12, seed=0, exh=0, tries=8):
    """top-down hierarchy. returns stats dict. bad nodes are split with the min-violation split."""
    rng = random.Random(seed); stats = dict(nodes=0, bad=[], leaves=[], unsplit=[], balance=[], depth=0, rep=0)
    stack = [(set(range(g.n)), None, 0)]
    while stack:
        U, walk, dep = stack.pop(); stats['depth'] = max(stats['depth'], dep)
        if walk is not None and len(U) <= L:
            stats['leaves'].append(len(U)); continue
        r = split(g, U, walk, rng, tries=(tries if len(U) > 300 else 3*tries), L=L)
        if (r is None or r[0] is None) and walk is not None and len(U) <= exh:
            e = exhaustive_split(g, U)
            if e: r = (e[0], e[1], dict(att=-1, rep=False))
            else:
                stats['unsplit'].append(len(U)); stats['leaves'].append(len(U)); continue
        if r is None: raise RuntimeError('nothing')
        if r[0] is None:
            sc, A, B = r[1]
            sa, sb = check(g, A), check(g, B)
            stats['bad'].append(dict(n=len(U), m=len(walk) if walk else 0, refl=reflex(g, U, walk) if walk else -1, chordlessU=(walk is None or check(g, U)[0] == 'ok'), dep=dep, chA=sa[2], chB=sb[2], stA=sa[0], stB=sb[0]))
            if sa[0] == 'nodisc' or sb[0] == 'nodisc':
                stats['leaves'].append(len(U)); stats['unsplit'].append(len(U)); continue
        else:
            A, B, info = r; stats.setdefault('q', []).append(info.get('q'))
            sa, sb = check(g, A), check(g, B)
        stats['nodes'] += 1; stats['balance'].append(min(len(A), len(B))/len(U))
        stack.append((A, sa[1], dep+1)); stack.append((B, sb[1], dep+1))
    return stats

# ---------------- generators ----------------
def icosphere(f):
    import ms_tilt
    return [set(s) for s in ms_tilt.icosphere(f)]

def flips(adj, nflips, rng, mindeg=5, maxdeg=9):
    adj = [set(a) for a in adj]; n = len(adj); done = 0; tries = 0
    while done < nflips and tries < nflips*100:
        tries += 1; a = rng.randrange(n); b = rng.choice(sorted(adj[a])); cn = adj[a] & adj[b]
        if len(cn) != 2: continue
        c, d = cn
        if d in adj[c]: continue
        if len(adj[a])-1 < mindeg or len(adj[b])-1 < mindeg or len(adj[c])+1 > maxdeg or len(adj[d])+1 > maxdeg: continue
        adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c); done += 1
    return adj

def drum(d, k):
    """two hubs of degree d, k antiprism rings of length d between them (min degree 5 if k>=2)."""
    adj = [set() for _ in range(2+d*k)]; N, S = 0, 1
    r = lambda i, j: 2+i*d+(j % d)
    def e(a, b): adj[a].add(b); adj[b].add(a)
    for i in range(k):
        for j in range(d):
            e(r(i, j), r(i, j+1))
            if i+1 < k: e(r(i, j), r(i+1, j)); e(r(i, j), r(i+1, j+1))
    for j in range(d): e(N, r(0, j)); e(S, r(k-1, j))
    return adj

def glue_faces(adjs, rng):
    """connected sum along faces: nested separating triangles. glue each next map into a random face of the result."""
    adj = [set(a) for a in adjs[0]]
    for a2 in adjs[1:]:
        g = G(adj); f = rng.choice(g.faces); g2 = G(a2); f2 = g2.faces[0]
        off = len(adj); mp = {}
        for v in range(len(a2)):
            if v in f2: mp[v] = f[f2.index(v)]
            else: mp[v] = off; off += 1
        adj += [set() for _ in range(off-len(adj))]
        for v in range(len(a2)):
            for w in a2[v]: adj[mp[v]].add(mp[w])
        # remove face triangle duplicates are fine (sets); the shared face is no longer a face: ok (separating triangle)
    return adj

def sep_short_cycles(g, maxlen=5, limit=None):
    """count separating triangles, induced 4-cycles, induced 5-cycles that are not vertex links."""
    adj = g.adj; facesets = set(frozenset(f) for f in g.faces); c3 = 0
    for u in range(g.n):
        for v in adj[u]:
            if v > u:
                for w in adj[u] & adj[v]:
                    if w > v and frozenset((u, v, w)) not in facesets: c3 += 1
    c4 = 0
    for u in range(g.n):          # induced 4-cycles u a v b, u smallest, u-v nonadjacent
        for v in set().union(*[adj[a] for a in adj[u]]) - adj[u] - {u}:
            if v < u: continue
            cn = [a for a in adj[u] & adj[v] if a > u]
            for a, b in itertools.combinations(cn, 2):
                if b not in adj[a]: c4 += 1
    c4 //= 1
    return dict(sep3=c3, ind4=c4)
