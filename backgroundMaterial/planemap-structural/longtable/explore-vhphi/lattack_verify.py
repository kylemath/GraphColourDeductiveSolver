#!/usr/bin/env python3
"""lattack_verify.py -- independent verifier for doubly locked F-chains (team L-Attack).
Standard library only. Written from the definitions in L-Attack's report, not from Math's scripts.

DEFINITIONS (all indices mod 5, link x0..x4 of v in rotation order):
  state s at hole v (deg v = 5): proper 4-colouring col of T-v whose link x0..x4 uses exactly 4 colours.
     Then exactly one colour repeats, at x_j and x_{j+2} (adjacent link vertices differ).  j = repeat index.
  middle single m = x_{j+1};  a = x_{j+3};  b = x_{j+4}.
  doubly locked: (L1) m and a lie in one component of the subgraph of T-v induced by colours {col m, col a},
                 (L2) m and b lie in one component of the subgraph induced by colours {col m, col b}.
     (j=0: colours (al,be,al,ga,de): be-ga path x1~x3 and be-de path x1~x4.)
  F(s): alpha = col x_j, c = col x_{j+3}; swap alpha<->c on the {alpha,c}-component of x_{j+2}.
  chain length of s = max k such that s, F(s), ..., F^{k-1}(s) are all doubly locked (0 if s is not).
  F is applied literally even if the next state fails to be a 4-colour-link state (then the chain stops).
Input format: rotation system rot = {u: [neighbours in counterclockwise order]}.
"""
import sys, random, itertools

def check_triangulation(rot):
    """Validate: simple, symmetric, every face (traced) a triangle, Euler V-E+F=2. Returns (ok,msg)."""
    for u, nb in rot.items():
        if len(set(nb)) != len(nb) or u in nb: return False, "not simple at %s" % u
        for w in nb:
            if u not in rot[w]: return False, "asymmetric"
    seen = set(); F = 0
    for u in rot:
        for w in rot[u]:
            if (u, w) in seen: continue
            F += 1; d = (u, w); L = 0
            while d not in seen:
                seen.add(d); a, b = d
                r = rot[b]; c = r[(r.index(a) - 1) % len(r)]
                d = (b, c); L += 1
            if L != 3: return False, "face of length %d" % L
    V = len(rot); E = sum(len(x) for x in rot.values()) // 2
    if V - E + F != 2: return False, "Euler fails %d-%d+%d" % (V, E, F)
    return True, "ok"

def proper(rot, v, col):
    return all(col[u] != col[w] for u in rot if u != v for w in rot[u] if w != v)

def comp(adj, col, start, pair):
    """component of start in the subgraph induced by colours in pair (adj excludes v)."""
    S = {start}; st = [start]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in S and col[w] in pair:
                S.add(w); st.append(w)
    return S

def repeat_index(link, col):
    cs = [col[x] for x in link]
    if len(set(cs)) != 4: return None
    js = [j for j in range(5) if cs[j] == cs[(j + 2) % 5]]
    return js[0] if len(js) == 1 else None

def doubly_locked(adj, link, col):
    j = repeat_index(link, col)
    if j is None: return False
    m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
    return (a in comp(adj, col, m, {col[m], col[a]})) and (b in comp(adj, col, m, {col[m], col[b]}))

def F(adj, link, col):
    j = repeat_index(link, col)
    if j is None: return None
    al, c = col[link[j]], col[link[(j + 3) % 5]]
    K = comp(adj, col, link[(j + 2) % 5], {al, c})
    new = dict(col)
    for u in K: new[u] = c if col[u] == al else al
    return new

def chain(adj, link, col, cap=40):
    k = 0; s = col; trace = []
    while k < cap and doubly_locked(adj, link, s):
        trace.append((repeat_index(link, s), tuple(s[x] for x in link)))
        k += 1; s = F(adj, link, s)
    return k, trace

def verify(rot, v, col, require_triangulation=True):
    """Full from-scratch verification. Returns dict with chain length and trace."""
    if require_triangulation:
        ok, msg = check_triangulation(rot)
        if not ok: return {"ok": False, "why": msg}
    if len(rot[v]) != 5: return {"ok": False, "why": "deg v != 5"}
    if not proper(rot, v, col): return {"ok": False, "why": "colouring not proper on T-v"}
    link = list(rot[v])
    adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}
    for i in range(5):
        if link[(i + 1) % 5] not in rot[link[i]]: return {"ok": False, "why": "link not a cycle"}
    k, tr = chain(adj, link, {u: col[u] for u in adj})
    return {"ok": True, "chain": k, "trace": tr}

# ---------- generation helpers (used only by the self-test and the search) ----------
def faces_to_rot(faces):
    nxt = {}
    for (a, b, c) in faces:
        nxt.setdefault(a, {})[b] = c; nxt.setdefault(b, {})[c] = a; nxt.setdefault(c, {})[a] = b
    rot = {}
    for u, m in nxt.items():
        x0 = next(iter(m)); L = [x0]; x = m[x0]
        while x != x0: L.append(x); x = m[x]
        rot[u] = L
    return rot

def random_triangulation(rng, n, nflips=None):
    faces = {(0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0)}   # K4, outward orientation consistent
    # K4 faces oriented ccw as seen from outside: check via Euler later
    for w in range(4, n):
        f = rng.choice(sorted(faces)); a, b, c = f
        faces.remove(f); faces |= {(a, b, w), (b, c, w), (c, a, w)}
    faces = flip_random(rng, faces, nflips if nflips is not None else 8 * n)
    return faces

def adj_of(faces):
    A = {}
    for t in faces:
        for x in t:
            A.setdefault(x, set()).update(y for y in t if y != x)
    return A

def flip_random(rng, faces, nflips, forbid=frozenset()):
    faces = set(faces)
    for _ in range(nflips):
        A = adj_of(faces)
        t = rng.choice(sorted(faces)); a, b, c = t
        if rng.random() < 0.5: a, b, c = b, c, a
        # edge (a,b) with third c; find the face on the other side, (b,a,d) up to rotation
        d = None
        for (x, y, z) in faces:
            if (x, y) == (b, a): d = z
            elif (y, z) == (b, a): d = x
            elif (z, x) == (b, a): d = y
        if d is None or d == c or d in A[c] or len(A[a]) < 4 or len(A[b]) < 4: continue
        if a in forbid or b in forbid or c in forbid or d in forbid: continue
        for f in list(faces):
            if set(f) in ({a, b, c}, {a, b, d}): faces.discard(f)
        faces |= {(c, d, b), (d, c, a)}
    return faces

def random_state(rng, faces, v, mix=60):
    """random proper 4-colouring of T-v (DFS random order) then Kempe mixing; returns col or None."""
    A = adj_of(faces); verts = [u for u in A if u != v]
    col = {}
    order = verts[:]; rng.shuffle(order)
    def dfs(i):
        if i == len(order): return True
        u = order[i]; cs = [c for c in range(4) if all(col.get(w) != c for w in A[u] if w != v)]
        rng.shuffle(cs)
        for c in cs:
            col[u] = c
            if dfs(i + 1): return True
            del col[u]
        return False
    sys.setrecursionlimit(10000)
    if not dfs(0): return None
    adj = {u: [w for w in A[u] if w != v] for u in verts}
    for _ in range(mix):
        u = rng.choice(verts); c1 = col[u]; c2 = rng.choice([c for c in range(4) if c != c1])
        K = comp(adj, col, u, {c1, c2})
        for w in K: col[w] = c2 if col[w] == c1 else c1
    return col

def selftest(seed_tag="lattack-selftest", ntri=400, per_tri=40, nlo=12, nhi=20):
    from collections import Counter
    rng = random.Random(seed_tag); cnt = Counter(); nlocked = 0; best = None
    for t in range(ntri):
        n = rng.randint(nlo, nhi); faces = random_triangulation(rng, n)
        rot = faces_to_rot(faces)
        ok, msg = check_triangulation(rot); assert ok, msg
        v5 = [u for u in rot if len(rot[u]) == 5]
        if not v5: continue
        v = rng.choice(v5)
        for _ in range(per_tri):
            col = random_state(rng, faces, v)
            if col is None: continue
            r = verify(rot, v, col); assert r["ok"], r
            if r["chain"] >= 1:
                nlocked += 1; cnt[r["chain"]] += 1
                if best is None or r["chain"] > best[0]: best = (r["chain"], n, v, dict(col), faces)
    return cnt, nlocked, best

if __name__ == "__main__":
    ntri = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    cnt, nl, best = selftest(ntri=ntri)
    print("doubly locked states:", nl)
    for k in sorted(cnt): print("chain", k, cnt[k], "%.2f%%" % (100.0 * cnt[k] / nl))
    print("max chain", best[0] if best else None)
