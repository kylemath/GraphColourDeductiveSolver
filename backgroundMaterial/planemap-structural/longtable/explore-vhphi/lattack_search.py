#!/usr/bin/env python3
"""lattack_search.py -- constructive hill-climb for long doubly-locked F-chains (team L-Attack).
Design = report section 5.  Standard library + lattack_verify.py.  Single process, CPU-capped.

State: (faces, v, col): oriented triangles (ccw) of a simple plane triangulation on <= NMAX vertices, v a degree-5
vertex (label kept), col a proper 4-colouring of T-v.   Objective S = k + 1/(1+d):
  k = chain length of the state (consecutive doubly locked F-iterates from s0);
  d = d1+d2 of the first failing iterate s_k = number of off-pair internal vertices on the cheapest m~a and m~b
      paths (0-1 BFS: vertices coloured in the lock pair cost 0, others 1); d = 1000 if its link lost 4 colours.
Moves: kempe swap | edge flip (v-free faces, colours of new diagonal differ) | stack a vertex in a face not
containing v | delete a degree-3 vertex not adjacent to v.  Accept if S' >= S (plateaus accepted).
Restart after STALL non-improving moves.  KILL: k >= 6, re-verified by lattack_verify.verify on the rotation system.
"""
import sys, time, random, json
from collections import deque
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
import lattack_verify as LV

NMAX = 30

def structure(faces, v):
    A = LV.adj_of(faces)
    nxt = {}
    for (a, b, c) in faces:
        for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
            if x == v: nxt[y] = z
    x0 = next(iter(nxt)); link = [x0]; x = nxt[x0]
    while x != x0: link.append(x); x = nxt[x]
    adj = {u: [w for w in A[u] if w != v] for u in A if u != v}
    return A, adj, link

def deficit(adj, col, s, t, pair):
    """min number of internal vertices outside colours `pair` on an s-t path in T-v (0-1 BFS)."""
    INF = 10 ** 6; dist = {s: 0}; dq = deque([s])
    while dq:
        u = dq.popleft(); du = dist[u]
        if u == t: return du
        for w in adj[u]:
            c = 0 if (col[w] in pair or w == t) else 1
            if du + c < dist.get(w, INF):
                dist[w] = du + c
                (dq.appendleft if c == 0 else dq.append)(w)
    return INF

def objective(adj, link, col):
    s = col; k = 0
    while k < 12 and LV.doubly_locked(adj, link, s):
        s = LV.F(adj, link, s); k += 1
    j = LV.repeat_index(link, s)
    if j is None: return k + 0.0, k
    m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
    d = deficit(adj, s, m, a, {s[m], s[a]}) + deficit(adj, s, m, b, {s[m], s[b]})
    return k + 1.0 / (1 + d), k

def init_state(rng, nlo=12, nhi=18):
    while True:
        n = rng.randint(nlo, nhi); faces = LV.random_triangulation(rng, n)
        A = LV.adj_of(faces); v5 = sorted(u for u in A if len(A[u]) == 5)
        if not v5: continue
        v = rng.choice(v5)
        for _ in range(30):
            col = LV.random_state(rng, faces, v, 60)
            if col is not None and len(set(col[x] for x in structure(faces, v)[2])) == 4:
                return faces, v, col

def move(rng, faces, v, col):
    """returns new (faces, col) or None if the sampled move is illegal."""
    r = rng.random()
    A = LV.adj_of(faces); verts = [u for u in A if u != v]
    if r < 0.5:   # kempe
        u = rng.choice(verts); c1 = col[u]; c2 = rng.choice([c for c in range(4) if c != c1])
        adj = {x: [w for w in A[x] if w != v] for x in verts}
        K = LV.comp(adj, col, u, {c1, c2}); new = dict(col)
        for w in K: new[w] = c2 if col[w] == c1 else c1
        return faces, new
    if r < 0.8:   # flip
        t = rng.choice(sorted(faces)); a, b, c = t
        if rng.random() < 0.5: a, b, c = b, c, a
        d = None
        for (x, y, z) in faces:
            if (x, y) == (b, a): d = z
            elif (y, z) == (b, a): d = x
            elif (z, x) == (b, a): d = y
        if v in (a, b, c, d) or d in A[c] or col[c] == col[d] or len(A[a]) < 4 or len(A[b]) < 4: return None
        nf = {f for f in faces if set(f) not in ({a, b, c}, {a, b, d})} | {(c, d, b), (d, c, a)}
        return nf, col
    if r < 0.9:   # stack
        if len(A) >= NMAX: return None
        f = rng.choice(sorted(faces))
        if v in f: return None
        free = [c for c in range(4) if c not in {col[x] for x in f}]
        if len(free) != 1: return None
        w = max(A) + 1; a, b, c = f
        nf = (set(faces) - {f}) | {(a, b, w), (b, c, w), (c, a, w)}
        new = dict(col); new[w] = free[0]
        return nf, new
    # delete degree-3 vertex
    cand = [u for u in verts if len(A[u]) == 3 and v not in A[u]]
    if not cand or len(A) <= 8: return None
    w = rng.choice(cand); fs = [f for f in faces if w in f]
    nb = [x for f in fs for x in f if x != w]
    if len(set(nb)) != 3: return None
    # remaining face: the three neighbours with orientation taken from a face (a,b,w) -> (a,b,c) cyclic
    (a, b, _) = next(( (x, y, z) if z == w else (y, z, x) if x == w else (z, x, y)) for (x, y, z) in fs[:1])
    c = next(u for u in set(nb) if u not in (a, b))
    # fs[0] after rotation is (a,b,w) ccw? we need cyclic orientation (a,b,c) consistent with outer side
    nf = (set(faces) - set(fs)) | {(a, b, c)}
    new = dict(col); del new[w]
    return nf, new

def hillclimb(tag, cpu_budget, stall=400, nlo=12, nhi=18):
    rng = random.Random("lattack|hc|" + tag); t0 = time.process_time()
    best = (-1, None); runs = []; evals = 0; restart = 0
    while time.process_time() - t0 < cpu_budget:
        faces, v, col = init_state(rng, nlo, nhi); rot = None
        _, adj, link = structure(faces, v); S, k = objective(adj, link, col); since = 0; runbest = k
        while since < stall and time.process_time() - t0 < cpu_budget:
            mv = move(rng, faces, v, col)
            if mv is None: continue
            nf, nc = mv
            try: _, adj2, link2 = structure(nf, v)
            except Exception: continue
            if len(link2) != 5: continue
            S2, k2 = objective(adj2, link2, nc); evals += 1
            if S2 >= S:
                since = 0 if S2 > S else since + 1
                faces, col, S, k, adj, link = nf, nc, S2, k2, adj2, link2
                if k > runbest: runbest = k
                if k > best[0]: best = (k, (faces, v, dict(col)))
                if k >= 6: break
            else: since += 1
        runs.append(runbest); restart += 1
        if best[0] >= 6: break
    return {"best": best[0], "runs": runs, "evals": evals, "cpu": time.process_time() - t0,
            "state": best[1]}

def baseline(tag, cpu_budget, nlo=12, nhi=18, per=20):
    rng = random.Random("lattack|rs|" + tag); t0 = time.process_time(); hist = {}; evals = 0; best = 0
    while time.process_time() - t0 < cpu_budget:
        n = rng.randint(nlo, nhi); faces = LV.random_triangulation(rng, n)
        A = LV.adj_of(faces); v5 = sorted(u for u in A if len(A[u]) == 5)
        if not v5: continue
        v = rng.choice(v5); _, adj, link = structure(faces, v)
        for _ in range(per):
            col = LV.random_state(rng, faces, v, 60)
            if col is None: continue
            k, _t = LV.chain(adj, link, col); evals += 1
            hist[k] = hist.get(k, 0) + 1; best = max(best, k)
    return {"best": best, "hist": hist, "evals": evals, "cpu": time.process_time() - t0}

def confirm(state):
    faces, v, col = state; rot = LV.faces_to_rot(faces)
    return LV.verify(rot, v, col)

if __name__ == "__main__":
    mode = sys.argv[1]; tag = sys.argv[2]; budget = float(sys.argv[3])
    if mode == "hc":
        r = hillclimb(tag, budget); st = r.pop("state")
        r["confirm"] = confirm(st)["chain"] if st else None
        if st and r["confirm"] and r["confirm"] >= 6:
            r["witness"] = {"faces": sorted(st[0]), "v": st[1], "col": sorted(st[2].items())}
        print(json.dumps(r))
    else:
        print(json.dumps(baseline(tag, budget)))
