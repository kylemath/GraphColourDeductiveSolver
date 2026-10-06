#!/usr/bin/env python3
"""MathRadiusCensus / verify_census.py: independent verifier, written from the SPEC below only. It does not import or call
census.cpp, gen_tri.cpp or run_census.py and shares no code or data structure with them (states here are PARTITIONS of the
vertex set into colour classes, so no colour renaming is needed).

SPEC.
 Graph line:  G n hex nf a b c ...   (nf = 2n-4 triangular faces of a plane triangulation).
 Hole: a vertex v of degree 5. T-v = graph minus v. A state is a proper 4-colouring of T-v up to renaming of colours
   (= a partition of V(T-v) into at most 4 independent sets).
 Link x0..x4 = neighbours of v in cyclic order. Filled: the link meets <= 3 classes. Otherwise exactly one class holds two link
   vertices x_j, x_{j+2}; put beta=class(x_{j+1}), gamma=class(x_{j+3}), delta=class(x_{j+4}).
 Doubly locked (DL): unfilled, x_{j+1} and x_{j+3} are joined by a path in T-v inside the classes beta U gamma, AND x_{j+1}, x_{j+4}
   are joined by a path inside beta U delta.
 Kempe move: pick two classes A,B and a connected component K of the subgraph of T-v induced on A U B; exchange the two colours on K.
 Radius r(s): least number of Kempe moves from s to a filled state (None if no filled state is reachable).
 Per record (graph g, hole v) the program reports: ncol (#states), nfilled, ndl, hist_all[r] (#states of radius r),
   hist_dl[r] (# DL states of radius r), unreached (#states with no filled state in their class), unreached_dl, maxdl (max radius of a DL
   state, -1 if none), wit (a colouring of the whole vertex list, -1 at v, of a DL state of radius maxdl).
 Checks: record fields recomputed and compared; wit is a proper colouring, DL, radius == maxdl; the graph is a sphere triangulation
   with min degree 5 and sep == [has a triangle that is not a face]; --gen mode: graphs pairwise non-isomorphic (own canonical form),
   valid, and counted against the known list.
Usage: verify_census.py GRAPHS CENSUS.jsonl [more.jsonl ...] [--every K]    (verify every K-th record, default all)
       verify_census.py --gen GRAPHS [--known N]
"""
import sys, json, itertools
from collections import deque

def parse_graph(line):
    t = line.split(); assert t[0] == "G"; n = int(t[1]); hexs = t[2]; nf = int(t[3]); nums = list(map(int, t[4:]))
    assert len(nums) == 3 * nf
    return n, hexs, [tuple(nums[3*i:3*i+3]) for i in range(nf)]

def check_triangulation(n, faces):
    """returns (ok, msg, adjacency sets, sep flag)"""
    if len(faces) != 2 * n - 4: return False, "face count", None, None
    from collections import Counter
    ec = Counter()
    for f in faces:
        if len(set(f)) != 3: return False, "degenerate face", None, None
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])): ec[frozenset((a, b))] += 1
    if any(c != 2 for c in ec.values()): return False, "edge not in exactly 2 faces", None, None
    if len(ec) != 3 * n - 6: return False, "edge count", None, None
    adj = [set() for _ in range(n)]
    for e in ec:
        a, b = tuple(e); adj[a].add(b); adj[b].add(a)
    for v in range(n):
        # link of v must be a single cycle through all neighbours
        le = [tuple(x for x in f if x != v) for f in faces if v in f]
        if len(le) != len(adj[v]): return False, "link size", None, None
        g = {}
        for a, b in le: g.setdefault(a, []).append(b); g.setdefault(b, []).append(a)
        if any(len(x) != 2 for x in g.values()): return False, "link not 2-regular", None, None
        start = next(iter(g)); seen = {start}; st = [start]
        while st:
            u = st.pop()
            for w in g[u]:
                if w not in seen: seen.add(w); st.append(w)
        if len(seen) != len(g): return False, "link not connected", None, None
    tri = sum(1 for a in range(n) for b in adj[a] if b > a for c in adj[a] & adj[b] if c > b)
    return True, "ok", adj, tri != 2 * n - 4

def link_cycle(v, adj, faces):
    le = [tuple(x for x in f if x != v) for f in faces if v in f]
    g = {}
    for a, b in le: g.setdefault(a, []).append(b); g.setdefault(b, []).append(a)
    cyc = [le[0][0]]; prev = None
    while len(cyc) < len(g):
        nxt = [w for w in g[cyc[-1]] if w != prev][0] if prev is not None else g[cyc[-1]][0]
        prev = cyc[-1]; cyc.append(nxt)
    return cyc

def all_partitions(verts, nbr):
    """all proper colourings with <=4 classes as partitions (tuples of sorted bitmasks), by incremental class assignment"""
    order = list(verts); res = []
    def rec(i, classes):
        if i == len(order): res.append(tuple(sorted(classes))); return
        u = order[i]; mu = 1 << u
        for k in range(len(classes)):
            if classes[k] & nbr[u]: continue
            classes[k] |= mu; rec(i + 1, classes); classes[k] &= ~mu
        if len(classes) < 4:
            classes.append(mu); rec(i + 1, classes); classes.pop()
    rec(0, [])
    return res

def comp_in(mask, nbr, s):
    seen = 1 << s; st = [s]
    while st:
        u = st.pop(); x = nbr[u] & mask & ~seen
        while x:
            w = (x & -x).bit_length() - 1; x &= x - 1; seen |= 1 << w; st.append(w)
    return seen

def cls_of(p, u):
    for c in p:
        if (c >> u) & 1: return c
    raise ValueError

def analyse(n, faces, adj, v):
    nbr = [0] * n
    for a in range(n):
        for b in adj[a]:
            if a != v and b != v: nbr[a] |= 1 << b
    lk = link_cycle(v, adj, faces); verts = [u for u in range(n) if u != v]
    parts = all_partitions(verts, nbr)
    index = {p: i for i, p in enumerate(parts)}
    def is_filled(p): return len({cls_of(p, x) for x in lk}) <= 3
    def dl(p):
        if is_filled(p): return False
        cs = [cls_of(p, x) for x in lk]
        j = [t for t in range(5) if cs[t] == cs[(t + 2) % 5]]; assert len(j) == 1; j = j[0]
        x1, x3, x4 = lk[(j + 1) % 5], lk[(j + 3) % 5], lk[(j + 4) % 5]
        b, g, d = cls_of(p, x1), cls_of(p, x3), cls_of(p, x4)
        return bool((comp_in(b | g, nbr, x1) >> x3) & 1) and bool((comp_in(b | d, nbr, x1) >> x4) & 1)
    def moves(p):
        out = []
        for A, B in itertools.combinations(p, 2):
            U = A | B; done = 0
            for s in range(n):
                if (U >> s) & 1 and not (done >> s) & 1:
                    K = comp_in(U, nbr, s); done |= K
                    A2 = (A & ~K) | (B & K); B2 = (B & ~K) | (A & K)
                    q = tuple(sorted([c for c in p if c != A and c != B] + [c for c in (A2, B2) if c]))
                    out.append(q)
        return out
    # BFS on the reverse of an undirected graph: moves are involutions, so distances from the filled set are symmetric
    dist = {}; dq = deque()
    for p in parts:
        if is_filled(p): dist[p] = 0; dq.append(p)
    while dq:
        p = dq.popleft()
        for q in moves(p):
            if q not in dist: dist[q] = dist[p] + 1; dq.append(q)
    return parts, dist, dl, is_filled, lk, nbr

def verify_record(r, graphs):
    n, hexs, faces = graphs[r["g"]]
    errs = []
    if hexs != r["hex"] or n != r["n"]: return ["graph/hex mismatch"]
    ok, msg, adj, sep = check_triangulation(n, faces)
    if not ok: return ["invalid triangulation: " + msg]
    if min(len(a) for a in adj) < 5: errs.append("min degree < 5")
    if int(sep) != r["sep"]: errs.append("sep flag")
    v = r["v"]
    if len(adj[v]) != 5: return errs + ["hole degree != 5"]
    parts, dist, dl, is_filled, lk, nbr = analyse(n, faces, adj, v)
    exp = {"ncol": len(parts), "nfilled": sum(is_filled(p) for p in parts), "ndl": sum(dl(p) for p in parts)}
    unr = [p for p in parts if p not in dist]
    ha = {}; hd = {}; md = -1
    for p in parts:
        if p in dist:
            ha[dist[p]] = ha.get(dist[p], 0) + 1
            if dl(p): hd[dist[p]] = hd.get(dist[p], 0) + 1; md = max(md, dist[p])
    exp["unreached"] = len(unr); exp["unreached_dl"] = sum(dl(p) for p in unr); exp["maxdl"] = md
    for k, x in exp.items():
        if r[k] != x: errs.append(f"{k}: file {r[k]} verifier {x}")
    def hl(h): top = max(h) if h else 0; return [h.get(i, 0) for i in range(top + 1)]
    for k, h in (("hist_all", ha), ("hist_dl", hd)):
        f = list(r[k])
        while len(f) > 1 and f[-1] == 0: f.pop()
        e = hl(h)
        while len(e) > 1 and e[-1] == 0: e.pop()
        if f != e: errs.append(f"{k}: file {f} verifier {e}")
    if "wit" in r:
        w = r["wit"]; classes = {}
        for u in range(n):
            if u != v: classes[w[u]] = classes.get(w[u], 0) | (1 << u)
        p = tuple(sorted(classes.values()))
        if w[v] != -1 or any(nbr[a] & m and True for m in p for a in range(n) if (m >> a) & 1 and nbr[a] & m): errs.append("wit not proper")
        elif p not in dist or not dl(p) or dist[p] != md: errs.append("wit is not a DL state of radius maxdl")
    elif md >= 0: errs.append("missing wit")
    return errs

def canon_code(n, faces):
    """own canonical form: unoriented triangulation -> rotation systems by face walking (both mirror images), minimum BFS code over roots."""
    adj = [set() for _ in range(n)]
    for f in faces:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2])): adj[a].add(b); adj[b].add(a)
    # cyclic order of neighbours around each vertex via the link
    rot = []
    for v in range(n):
        rot.append(link_cycle(v, adj, faces))
    # make orientations consistent: choose orientation of each vertex so that adjacent vertices agree, by BFS over faces.
    # Simple method: a vertex's rotation as list r; orientation sign s[v]; for edge (a,b) with face (a,b,c): in a positive rotation
    # at a, c follows b iff the face is oriented a->b->c.  Resolve by propagation over vertices using shared face (a,b,c).
    sign = [None] * n; sign[0] = 1; dq = deque([0])
    def follows(v, b, c, s):  # does c directly follow b in rotation of v with sign s
        r = rot[v]; i = r.index(b); return r[(i + s) % len(r)] == c
    while dq:
        a = dq.popleft()
        for b in adj[a]:
            for f in faces:
                if a in f and b in f:
                    c = [x for x in f if x != a and x != b][0]
                    # face oriented a,b,c (positive at a if c follows b). Orientation at a with sign[a]: positive iff follows(a,b,c,sign[a])
                    pos = follows(a, b, c, sign[a])
                    # same face seen from b: oriented b,c,a: positive at b iff a follows c
                    for s in (1, -1):
                        if follows(b, c, a, s) == pos:
                            if sign[b] is None: sign[b] = s; dq.append(b)
                            break
    best = None
    for mirror in (1, -1):
        R = []
        for v in range(n):
            r = rot[v] if sign[v] * mirror == 1 else rot[v][::-1]
            R.append(r)
        for x in range(n):
            for y in adj[x]:
                lab = {x: 0}; order = [x]; code = []; ref = {x: y}
                qi = 0
                while qi < len(order):
                    w = order[qi]; qi += 1
                    r = R[w]; i = r.index(ref[w]); lw = len(r)
                    for t in range(lw):
                        u = r[(i + t) % lw]
                        if u not in lab: lab[u] = len(order); order.append(u); ref[u] = w
                        code.append(lab[u])
                    code.append(-1)
                code = tuple(code)
                if best is None or code < best: best = code
    return best

KNOWN = {12:1, 13:0, 14:1, 15:1, 16:3, 17:4, 18:12, 19:23, 20:73, 21:192, 22:651}

def gen_mode(path, known=True):
    gs = [parse_graph(l) for l in open(path) if l.startswith("G")]
    codes = set(); bad = 0
    for n, h, f in gs:
        ok, msg, adj, sep = check_triangulation(n, f)
        if not ok or min(len(a) for a in adj) < 5: print("INVALID graph", h[:16], msg); bad += 1; continue
        codes.add(canon_code(n, f))
    ns = {g[0] for g in gs}
    print(f"graphs={len(gs)} distinct(own canonical form)={len(codes)} invalid={bad} orders={sorted(ns)}")
    if len(codes) != len(gs): print("DUPLICATES present"); return 1
    if len(ns) == 1 and known:
        n = ns.pop()
        if n in KNOWN: print(f"known count at n={n}: {KNOWN[n]} ->", "MATCH" if KNOWN[n] == len(gs) else "MISMATCH"); return 0 if KNOWN[n] == len(gs) and not bad else 1
    return 1 if bad else 0

def main():
    a = sys.argv[1:]
    if a and a[0] == "--gen": sys.exit(gen_mode(a[1]))
    every = 1
    if "--every" in a: i = a.index("--every"); every = int(a[i + 1]); del a[i:i + 2]
    graphs = {}
    for i, l in enumerate(x for x in open(a[0]) if x.startswith("G")): graphs[i] = parse_graph(l)
    nbad = ntot = 0
    for path in a[1:]:
        for k, line in enumerate(open(path)):
            if k % every: continue
            r = json.loads(line)
            if r.get('capped'): print('skipped capped record', r['g'], r['v']); continue
            ntot += 1; e = verify_record(r, graphs)
            if e: nbad += 1; print("MISMATCH", path, "g", r["g"], "v", r["v"], e)
    print(f"verified {ntot} records, {nbad} mismatches"); sys.exit(1 if nbad else 0)
if __name__ == "__main__": main()
