#!/usr/bin/env python3
"""studiointel radius.py -- PRODUCER. Exact Kempe radius at a degree-5 hole of a spherical triangulation. stdlib only.

Definitions (MathConjectureR sec.1; Tait-lock page pd2_lock_proof.md "Definition matched"):
 state = proper 4-colouring of T-v, canonical by first occurrence along a fixed BFS order of T-v.
 filled = link of v uses <=3 colours. unfilled: link uses 4 colours, exactly one repeat c(x_j)=c(x_{j+2}); m=x_{j+1}, a=x_{j+3}, b=x_{j+4}.
 lock1: a is in the {c(m),c(a)}-component of m in T-v.  lock2: b is in the {c(m),c(b)}-component of m.  DL = both.
 NL = filled or unfilled-not-DL.  move = whole-component Kempe swap (singletons allowed) in T-v.
 radius r(s) = 1 + d(s,NL) for DL s (d in moves); 1 for unfilled non-DL; 0 for filled. rho(v) = max r (None = infinite, i.e. a targetless class exists).
"""
import sys, json, itertools, hashlib, time
from collections import deque, Counter

def prepare(faces, hole):
    succ = {}
    for f in faces:
        if hole in f:
            i = f.index(hole); x, y = f[(i + 1) % 3], f[(i + 2) % 3]; succ[x] = y
    x0 = next(iter(succ)); link = [x0]
    while len(link) < len(succ): link.append(succ[link[-1]])
    adj = {}
    for f in faces:
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            if hole in (a, b): continue
            adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    # BFS order from link[0]
    order = [link[0]]; seen = {link[0]}; q = deque([link[0]])
    while q:
        u = q.popleft()
        for w in sorted(adj[u]):
            if w not in seen: seen.add(w); order.append(w); q.append(w)
    assert len(order) == len(adj)
    idx = {u: i for i, u in enumerate(order)}
    nb = [sorted(idx[w] for w in adj[u]) for u in order]
    return order, idx, nb, [idx[x] for x in link]

def canon(col):
    mp = {}; out = []
    for c in col:
        if c not in mp: mp[c] = len(mp)
        out.append(mp[c])
    return tuple(out)

def enumerate_states(nb, cap):
    n = len(nb); res = []; col = [-1] * n
    def rec(i, used):
        if i == n:
            res.append(tuple(col)); return
        if len(res) > cap: return
        forb = {col[w] for w in nb[i] if w < i}
        for c in range(min(used + 1, 4)):
            if c not in forb:
                col[i] = c; rec(i + 1, max(used, c + 1))
        col[i] = -1
    col[0] = 0; rec(1, 1)
    return res

def comp(nb, col, start, p, q):
    seen = {start}; st = [start]
    while st:
        u = st.pop()
        for w in nb[u]:
            if w not in seen and (col[w] == p or col[w] == q): seen.add(w); st.append(w)
    return seen

def classify(nb, link, col):
    """0 filled, 1 unfilled non-DL, 2 DL; also returns None"""
    lc = [col[x] for x in link]
    if len(set(lc)) <= 3: return 0
    for j in range(5):
        if lc[j] == lc[(j + 2) % 5]: break
    m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
    mu = col[m]
    if a not in comp(nb, col, m, mu, col[a]): return 1
    if b not in comp(nb, col, m, mu, col[b]): return 1
    return 2

def swaps(nb, col):
    n = len(col)
    for p, q in itertools.combinations(range(4), 2):
        seen = set()
        for u in range(n):
            if col[u] not in (p, q) or u in seen: continue
            K = comp(nb, col, u, p, q); seen |= K
            new = list(col)
            for w in K: new[w] = q if col[w] == p else p
            yield canon(new)

def analyse(faces, hole, cap=2000000):
    order, idx, nb, link = prepare(faces, hole)
    states = enumerate_states(nb, cap)
    if len(states) > cap: return {'hole': hole, 'inconclusive': 'more than %d states' % cap}
    # canonical-by-first-occurrence along BFS order already holds for DFS output with used-bound
    cls = {s: classify(nb, link, s) for s in states}
    cnt = Counter(cls.values())
    DL = [s for s in states if cls[s] == 2]
    dist = {}; frontier = []
    nbrs = {}
    for s in DL:
        nl = []; ndl = []
        for t in swaps(nb, s):
            (ndl if cls[t] == 2 else nl).append(t)
        nbrs[s] = ndl
        if nl: dist[s] = 1; frontier.append(s)
    # BFS inside DL graph (swap graph symmetric)
    q = deque(frontier)
    while q:
        s = q.popleft()
        for t in nbrs[s]:
            if t not in dist: dist[t] = dist[s] + 1; q.append(t)
    unreached = [s for s in DL if s not in dist]
    hist = Counter(1 + dist[s] for s in DL if s in dist)
    out = {'hole': hole, 'n_states': len(states), 'n_filled': cnt[0], 'n_unfilled_nonDL': cnt[1], 'n_DL': cnt[2],
           'DL_radius_hist': {str(k): hist[k] for k in sorted(hist)}, 'unreached_DL': len(unreached)}
    if unreached:
        out['rho'] = None; w = unreached[0]
    elif DL:
        w = max(DL, key=lambda s: dist[s]); out['rho'] = 1 + dist[w]
    elif cnt[1]: out['rho'] = 1; w = None
    else: out['rho'] = 0; w = None
    if unreached: out['targetless'] = [[int(x) for x in t] for t in unreached]   # union of all-DL Kempe classes; certificate input for check.py tl
    if w is not None: out['witness'] = {'state': [int(x) for x in w], 'order': [int(u) for u in order]}
    return out

def graph_hash(faces): return hashlib.sha256(json.dumps(sorted(map(list, faces))).encode()).hexdigest()

if __name__ == '__main__':
    import graphs
    spec = sys.argv[1]; holes = sys.argv[2] if len(sys.argv) > 2 else 'five'
    from builders import build
    faces = build(spec)
    dg = graphs.degrees(faces)
    hs = [v for v in sorted(dg) if dg[v] == 5] if holes == 'five' else [int(x) for x in holes.split(',')]
    t = time.time()
    for h in hs:
        r = analyse(faces, h); r.pop('targetless', None); r['graph'] = spec; r['graph_sha256'] = graph_hash(faces); r['secs'] = round(time.time() - t, 1)
        print(json.dumps(r), flush=True)
