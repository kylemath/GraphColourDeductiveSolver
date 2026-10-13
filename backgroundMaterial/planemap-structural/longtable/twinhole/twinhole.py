"""Twin-hole mirror sums: glue a map G (triangulation with hole h) to a copy G' along a face triangle D = (x, y, z)
that avoids the hole. Both copies keep their hole. A joint state is a proper 4-colouring of the glued graph minus
both holes, up to renaming; we fix the renaming by colouring D as (0, 1, 2), so a joint state is a pair (i, j) of
G-colourings (of G - h) that both colour D as (0, 1, 2).

Kempe moves of the glued graph, in this representation:
  * an (a,b)-component of side i that avoids D is a whole component of the glued graph: (i, j) -> (swap_i, j)
    (and symmetrically on side j). It is never the only (a,b)-component (D always holds a or b), so never a renaming.
  * every colour pair (a,b) meets D (D uses 3 of the 4 colours); the D vertices coloured a or b are adjacent, so they
    lie in ONE component K = C_i u C_j. Swapping K then renaming a<->b to put D back to (0,1,2) gives
    (T_i[ab], T_j[ab]) with T_i[ab] = (a b) o swap_{C_i}(i).
Filled: the rim of each hole uses <= 3 colours. We BFS from the jointly filled set and report exact depths.
Single-hole baseline dG on G alone uses the same moves on one side (interior moves and i -> T_i[ab]).
"""
import json, sys, collections, itertools, time

PAIRS = [(a, b) for a in range(4) for b in range(a + 1, 4)]


def load(path):
    d = json.load(open(path))
    rot = json.loads(d['rot']) if isinstance(d['rot'], str) else d['rot']
    return d['name'], rot, d['hole']


def faces(rot):
    pos = [{w: k for k, w in enumerate(r)} for r in rot]
    seen, out = set(), []
    for u in range(len(rot)):
        for v in rot[u]:
            if (u, v) in seen: continue
            f, a, b = [], u, v
            while (a, b) not in seen:
                seen.add((a, b)); f.append(a)
                r = rot[b]; c = r[(pos[b][a] - 1) % len(r)]   # next edge of the face (orientation-consistent)
                a, b = b, c
            out.append(tuple(f))
    return out


def colourings(adj, hole, D):
    """all proper 4-colourings of G - hole with D coloured (0,1,2), as tuples (hole gets -1)"""
    n = len(adj)
    order = list(D) + [u for u in range(n) if u != hole and u not in D]
    # BFS-ish order from D for better pruning
    seen = set(D); order = list(D); q = collections.deque(D)
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w != hole and w not in seen: seen.add(w); order.append(w); q.append(w)
    order += [u for u in range(n) if u != hole and u not in seen]
    c = [-1] * n
    for k, u in enumerate(D): c[u] = k
    out = []

    def rec(t):
        if t == len(order): out.append(tuple(c)); return
        u = order[t]
        if c[u] >= 0: rec(t + 1); return
        bad = {c[w] for w in adj[u]}
        for col in range(4):
            if col not in bad:
                c[u] = col; rec(t + 1)
        c[u] = -1

    rec(0)
    return out


def side_tables(adj, hole, D, link, cols):
    idx = {c: k for k, c in enumerate(cols)}
    Dset = set(D)
    inner, T, filled = [], [], []
    n = len(adj)
    for c in cols:
        filled.append(len({c[u] for u in link}) <= 3)
        mv, tt = [], {}
        for (a, b) in PAIRS:
            comp = [-1] * n; nc = 0
            for s in range(n):
                if s == hole or comp[s] >= 0 or c[s] not in (a, b): continue
                stack = [s]; comp[s] = nc; members = []
                while stack:
                    u = stack.pop(); members.append(u)
                    for w in adj[u]:
                        if w != hole and comp[w] < 0 and c[w] in (a, b): comp[w] = nc; stack.append(w)
                nc += 1
                sw = list(c)
                for u in members: sw[u] = b if c[u] == a else a
                if Dset & set(members):
                    sw = [(b if x == a else a if x == b else x) if x >= 0 else -1 for x in sw]   # rename a<->b
                    tt[(a, b)] = idx[tuple(sw)]
                else:
                    mv.append(idx[tuple(sw)])
        inner.append(mv); T.append([tt[p] for p in PAIRS])
    return inner, T, filled


def bfs(N, nbrs, sources):
    dist = [-1] * N; q = collections.deque()
    for s in sources: dist[s] = 0; q.append(s)
    while q:
        u = q.popleft()
        for w in nbrs(u):
            if dist[w] < 0: dist[w] = dist[u] + 1; q.append(w)
    return dist


def run(path, max_states=4_000_000, face_pick='far'):
    name, rot, hole = load(path)
    n = len(rot); adj = [set(r) for r in rot]; link = rot[hole]
    # hop distance from the hole, to pick the glued face
    hd = [-1] * n; hd[hole] = 0; q = collections.deque([hole])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if hd[w] < 0: hd[w] = hd[u] + 1; q.append(w)
    fs = [f for f in faces(rot) if len(f) == 3 and hole not in f]
    far = max(fs, key=lambda f: (min(hd[u] for u in f), sum(hd[u] for u in f)))
    near = min(fs, key=lambda f: (sum(hd[u] for u in f), f))
    res = []
    for tag, D in (('far', far), ('near', near)):
        cols = colourings(adj, hole, D); S = len(cols)
        if S * S > max_states:
            res.append(dict(map=name, n=n, face=tag, D=D, S=S, skipped='S^2 = %d too big' % (S * S))); continue
        t0 = time.time()
        inner, T, filled = side_tables(adj, hole, D, link, cols)
        # single hole on G
        dG = bfs(S, lambda i: inner[i] + T[i], [i for i in range(S) if filled[i]])
        # twin holes
        N = S * S
        def nb(u):
            i, j = divmod(u, S)
            out = [a * S + j for a in inner[i]] + [i * S + b for b in inner[j]]
            out += [T[i][p] * S + T[j][p] for p in range(6)]
            return out
        dJ = bfs(N, nb, [i * S + j for i in range(S) if filled[i] for j in range(S) if filled[j]])
        sym = [dJ[i * S + i] for i in range(S)]
        hist = collections.Counter(dJ)
        excess = collections.Counter()
        for i in range(S):
            for j in range(S):
                d = dJ[i * S + j]
                if d >= 0: excess[d - max(dG[i], dG[j])] += 1
        res.append(dict(map=name, n=n, face=tag, D=D, S=S, joint=N, secs=round(time.time() - t0, 1),
                        maxG=max(dG), unfillG=dG.count(-1), maxJ=max(dJ), unfillJ=dJ.count(-1),
                        histJ=dict(sorted(hist.items())), sym_equals_dG=all(sym[i] == dG[i] for i in range(S)),
                        excess_over_maxside=dict(sorted(excess.items()))))
    return res


if __name__ == '__main__':
    for p in sys.argv[1:]:
        for r in run(p):
            print(json.dumps(r)); sys.stdout.flush()
