#!/usr/bin/env python3
"""[exploratory] Local compute item 5 (run 3): glue radius-5 certificates and test whether radius 6 appears.

Gluing = connected sum along a vertex link: pick w in X (far from X's hole) and w' in Y with deg w = deg w' = k, delete both,
and identify the link cycle of w with the link cycle of w' (all k rotations, both orientations, i.e. 2k ways; one orientation
glues a mirror image of Y, which is still a plane triangulation). The result is a plane triangulation on |X| + |Y| - 2 - k
vertices. Core class is checked per graph: min degree >= 5 and #triangles = #faces = 2n - 4 (no separating triangle).
(By hand it is automatic: cycle vertices get degree d_X + d_Y - 4 >= 6, and neither side has a chord of the cycle.)
Pairs glued (X, Y): A = 91a307d1 (order 28, hole 22), B = 80b930d1 (order 32, hole 23), Errera (order 17, rho 3):
  A+B (both holes kept), A+Errera, B+Errera.  w must be at distance >= 2 from X's hole; w' at distance >= 2 from Y's
  certificate hole when Y is a certificate.
States tested: at X's hole, the certificate state of X (radius 5 in X) extended across the glued side by every proper
colouring of Y's side with the cycle colours fixed (up to EXT_CAP extensions per glued graph, DFS order); for A+B the same
at B's hole with B's certificate. Exact radius of each state by BFS in the glued graph (../common/rball, C++).
usage: python3 glue.py [--workers 6] [--ext-cap 24] > glue-results.jsonl ; summary line last.
       python3 glue.py --full-errera --workers 6 > glue-errera-full.jsonl   (exact rho over ALL states at the certificate
       hole of every certificate+Errera gluing, by ../common/krad; these graphs have 37-42 vertices)
       python3 glue.py --full-ab --workers 6 > glue-ab-full.jsonl   (exact rho over ALL states, A+B gluings, only the
       (graph, hole) pairs where an extension kept radius 5; needs glue-results.jsonl)"""
import json, os, sys, subprocess, tempfile, itertools, random
from collections import Counter, deque
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(H, "..", "..", "..")
CERT = os.path.join(ROOT, "studiointel", "run-C-2026-10-06", "cert")
RBALL = os.path.join(H, "..", "common", "rball")
EXT_CAP = int(sys.argv[sys.argv.index("--ext-cap") + 1]) if "--ext-cap" in sys.argv else 24


def rot_from_faces(F):
    nxt = {}
    for f in F:
        for i in range(3): nxt[(f[i], f[(i + 1) % 3])] = f[(i + 2) % 3]
    n = 1 + max(max(f) for f in F); rot = []
    for v in range(n):
        start = [b for (a, b) in nxt if a == v][0]; r = [start]
        while True:
            y = nxt[(v, r[-1])]
            if y == start: break
            r.append(y)
        rot.append(r)
    return rot


def load():
    out = {}
    for name, h in (("91a307d1852a1764", 22), ("80b930d1540e4ee3", 23)):
        F = json.load(open(os.path.join(CERT, name + ".graph.json")))["faces"]
        st = {int(k): v for k, v in json.load(open(os.path.join(CERT, name + ".hole%d.state.json" % h))).items()}
        out[name[:8]] = {"rot": rot_from_faces(F), "hole": h, "state": st}
    F = json.load(open(os.path.join(ROOT, "longtable", "studio-explore", "historical-traps", "Errera.json")))["faces_ccw"]
    out["Errera"] = {"rot": rot_from_faces(F), "hole": None, "state": None}
    return out


def bfs_dist(rot, s):
    d = {s: 0}; q = deque([s])
    while q:
        x = q.popleft()
        for y in rot[x]:
            if y not in d: d[y] = d[x] + 1; q.append(y)
    return d


def glue(X, w, Y, wp, shift, sign):
    """vertices: X's kept vertices keep labels; Y's interior vertices get new labels; cycle of w' identified to cycle of w."""
    Cx, Cy = X["rot"][w], Y["rot"][wp]; k = len(Cx)
    ymap = {Cy[(shift + sign * i) % k]: Cx[i] for i in range(k)}
    nX = len(X["rot"]); new = {}; nxt = nX
    for u in range(len(Y["rot"])):
        if u == wp: continue
        if u in ymap: new[u] = ymap[u]
        else: new[u] = nxt; nxt += 1
    # relabel compactly: X vertices except w, then Y interior
    E = set()
    for a in range(nX):
        if a == w: continue
        for b in X["rot"][a]:
            if b != w: E.add((min(a, b), max(a, b)))
    for a in range(len(Y["rot"])):
        if a == wp: continue
        for b in Y["rot"][a]:
            if b != wp: E.add((min(new[a], new[b]), max(new[a], new[b])))
    labels = sorted({x for e in E for x in e}); re = {x: i for i, x in enumerate(labels)}
    E = sorted((re[a], re[b]) for a, b in E)
    return len(labels), E, re, new


def core_check(n, E):
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    tri = sum(1 for a, b in E for c in adj[a] & adj[b] if c > b)
    return len(E) == 3 * n - 6 and tri == 2 * n - 4 and min(len(x) for x in adj) >= 5, adj


def extensions(adj, fixed, free, cap, seed=0):
    rng = random.Random(seed)
    free = sorted(free, key=lambda u: -sum(1 for w in adj[u] if w in fixed)); out = []; col = dict(fixed)

    def rec(i):
        if len(out) >= cap: return
        if i == len(free): out.append(dict(col)); return
        u = free[i]; forb = {col[w] for w in adj[u] if w in col}
        cs = [0, 1, 2, 3]; rng.shuffle(cs)
        for c in cs:
            if c not in forb: col[u] = c; rec(i + 1); del col[u]
    # order free vertices so each is adjacent to already coloured ones where possible
    order, seen = [], set(fixed)
    pending = set(free)
    while pending:
        u = max(pending, key=lambda x: sum(1 for w in adj[x] if w in seen)); order.append(u); seen.add(u); pending.discard(u)
    free[:] = order
    rec(0)
    return out


def work(task):
    D = load_cache(); X, Y = D[task["X"]], D[task["Y"]]
    n, E, re, ymap = glue(X, task["w"], Y, task["wp"], task["shift"], task["sign"])
    ok, adj = core_check(n, E)
    res = {**task, "n": n, "core": ok, "tests": []}
    if not ok: return res
    jobs = []
    # hole of X with X's certificate state
    hx = re[X["hole"]]; fixed = {re[u]: c for u, c in X["state"].items() if u != task["w"]}
    free = [u for u in range(n) if u not in fixed and u != hx]
    for ext in extensions(adj, fixed, free, EXT_CAP, seed=hash((task["w"], task["wp"], task["shift"], task["sign"])) & 0xffff): jobs.append(("X", hx, ext))
    if Y["hole"] is not None:
        hy = re[ymap[Y["hole"]]]; fixed = {re[ymap[u]]: c for u, c in Y["state"].items() if u != task["wp"]}
        # cycle colours come from Y's state; extend into X's side
        free = [u for u in range(n) if u not in fixed and u != hy]
        for ext in extensions(adj, fixed, free, EXT_CAP, seed=1 + (hash((task["w"], task["wp"], task["shift"], task["sign"])) & 0xffff)): jobs.append(("Y", hy, ext))
    for side in ("X", "Y"):
        J = [j for j in jobs if j[0] == side]
        if not J: continue
        h = J[0][1]
        with tempfile.NamedTemporaryFile("w", suffix=".in", delete=False) as fh:
            fh.write("%d %d\n" % (n, len(E)) + "".join("%d %d\n" % e for e in E) + "%d %d\n" % (h, len(J)))
            for _, _, ext in J: fh.write(" ".join(str(ext.get(u, 0)) for u in range(n)) + "\n")
            p = fh.name
        out = subprocess.run(["nice", "-n", "10", RBALL, p, "9", "5000000"], capture_output=True, text=True).stdout.split("\n")
        os.unlink(p)
        rs = [int(l.split()[0]) for l in out if l.strip()]
        res["tests"].append({"side": side, "hole": h, "extensions": len(J), "radius_hist": dict(Counter(rs)), "max_r": max(rs)})
        if max(rs) >= 6:
            i = rs.index(max(rs)); res.setdefault("r_ge6_witness", []).append({"side": side, "hole": h, "E": E, "colouring": J[i][2]})
    return res


_C = None
def load_cache():
    global _C
    if _C is None: _C = load()
    return _C


def tasks():
    D = load_cache(); T = []
    for Xn, Yn in (("91a307d1", "80b930d1"), ("91a307d1", "Errera"), ("80b930d1", "Errera")):
        X, Y = D[Xn], D[Yn]
        dx = bfs_dist(X["rot"], X["hole"]); dy = bfs_dist(Y["rot"], Y["hole"]) if Y["hole"] is not None else None
        for w in range(len(X["rot"])):
            if dx[w] < 2: continue
            for wp in range(len(Y["rot"])):
                if dy is not None and dy[wp] < 2: continue
                k = len(X["rot"][w])
                if len(Y["rot"][wp]) != k: continue
                for shift in range(k):
                    for sign in (1, -1):
                        T.append({"X": Xn, "Y": Yn, "w": w, "wp": wp, "shift": shift, "sign": sign, "deg": k, "dist_w": dx[w]})
    return T


def main():
    wk = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 6
    T = tasks(); hist = Counter(); maxr = 0; ncore = 0; ntests = 0; wit = None; by_pair = {}
    with Pool(wk) as pool:
        for r in pool.imap_unordered(work, T, chunksize=4):
            ncore += r["core"]
            for t in r["tests"]:
                key = "%s+%s:%s" % (r["X"], r["Y"], t["side"]); bp = by_pair.setdefault(key, Counter())
                for rr, m in t["radius_hist"].items(): hist[rr] += m; bp[rr] += m; ntests += m
                maxr = max(maxr, t["max_r"])
            if r.get("r_ge6_witness") and wit is None: wit = r
            r.pop("r_ge6_witness", None); print(json.dumps(r), flush=True)
    print(json.dumps({"summary": True, "glued_graphs": len(T), "core_class": ncore, "states_tested": ntests,
                      "radius_hist": dict(sorted(hist.items())), "by_pair_side": {k: dict(sorted(v.items())) for k, v in by_pair.items()},
                      "max_radius": maxr, "ext_cap": EXT_CAP, "first_r_ge6": wit}), flush=True)


if __name__ == "__main__" and "--full-errera" not in sys.argv and "--full-ab" not in sys.argv:
    main()


# ---- full-enumeration mode for the smaller (certificate + Errera) gluings: exact rho over ALL states at the hole ----
KRAD = os.path.join(H, "..", "common", "krad")


def work_full(task):
    D = load_cache(); X, Y = D[task["X"]], D[task["Y"]]
    n, E, re, ymap = glue(X, task["w"], Y, task["wp"], task["shift"], task["sign"])
    ok, adj = core_check(n, E)
    res = {**task, "n": n, "core": ok}
    if not ok: return res
    with tempfile.NamedTemporaryFile("w", suffix=".el", delete=False) as fh:
        fh.write("%d %d\n" % (n, len(E)) + "".join("%d %d\n" % e for e in E)); p = fh.name
    o = json.loads(subprocess.run(["nice", "-n", "10", KRAD, p, str(re[X["hole"]])], capture_output=True, text=True).stdout)
    os.unlink(p)
    res.update({"hole": re[X["hole"]], "states": o["n_states"], "kappa": o["n_classes"], "targetless": o["targetless_classes"], "rho": o["rho"]})
    return res


def main_full():
    wk = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 6
    T = [t for t in tasks() if t["Y"] == "Errera"]; hist = Counter(); tl = 0; kap = Counter()
    with Pool(wk) as pool:
        for r in pool.imap_unordered(work_full, T, chunksize=4):
            print(json.dumps(r), flush=True)
            if r["core"]: hist["%s+Errera rho=%d" % (r["X"], r["rho"])] += 1; tl += r["targetless"] > 0; kap[r["kappa"]] += 1
    print(json.dumps({"summary": True, "mode": "full", "glued_graphs": len(T), "rho_hist": dict(sorted(hist.items())),
                      "graphs_with_targetless": tl, "kappa_hist": dict(sorted(kap.items()))}), flush=True)


if __name__ == "__main__" and "--full-errera" in sys.argv:
    main_full()


# ---- full-enumeration mode for A+B gluings (52-53 vertices, ~0.7-1.2M states each): only the (graph, hole) pairs where
# some extension of the certificate state kept radius 5 in the extension test (read from glue-results.jsonl) ----
def work_full_ab(item):
    task, side = item
    D = load_cache(); X, Y = D[task["X"]], D[task["Y"]]
    n, E, re, ymap = glue(X, task["w"], Y, task["wp"], task["shift"], task["sign"])
    h = re[X["hole"]] if side == "X" else re[ymap[Y["hole"]]]
    with tempfile.NamedTemporaryFile("w", suffix=".el", delete=False) as fh:
        fh.write("%d %d\n" % (n, len(E)) + "".join("%d %d\n" % e for e in E)); p = fh.name
    o = json.loads(subprocess.run(["nice", "-n", "10", KRAD, p, str(h)], capture_output=True, text=True).stdout)
    os.unlink(p)
    return {**task, "side": side, "n": n, "hole": h, "states": o["n_states"], "kappa": o["n_classes"], "targetless": o["targetless_classes"], "rho": o["rho"]}


def main_full_ab():
    wk = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 6
    items = []
    for l in open(os.path.join(H, "glue-results.jsonl")):
        r = json.loads(l)
        if r.get("summary") or r["Y"] != "80b930d1": continue
        for t in r["tests"]:
            if t["max_r"] >= 5: items.append(({k: r[k] for k in ("X", "Y", "w", "wp", "shift", "sign", "deg", "dist_w")}, t["side"]))
    hist = Counter(); tl = 0; mx = 0
    with Pool(wk) as pool:
        for r in pool.imap_unordered(work_full_ab, items, chunksize=2):
            print(json.dumps(r), flush=True); hist["side %s rho=%d" % (r["side"], r["rho"])] += 1; tl += r["targetless"] > 0; mx = max(mx, r["states"])
    print(json.dumps({"summary": True, "mode": "full-ab", "graph_hole_pairs": len(items), "rho_hist": dict(sorted(hist.items())),
                      "with_targetless": tl, "max_states": mx}), flush=True)


if __name__ == "__main__" and "--full-ab" in sys.argv:
    main_full_ab()
