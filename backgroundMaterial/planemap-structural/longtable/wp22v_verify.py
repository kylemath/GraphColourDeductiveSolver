#!/usr/bin/env python3
"""WP22v: independent verifier for the S2 (Kempe radii) pre-registration.

Written from the specification only (WP22-S2-preregistration.md, WP22-interface.md,
a-structure.md section 1, MathConfinementAttack Step 1, l-attack.md section 1).
Standard library only.  Does not import or read any search code.

Commands
  cert FILE.json            check a certificate; exit 0 claim confirmed, 1 contradicted, 2 capped/invalid
  census A_r [--out F]      census of every doubly locked state of A_r (r = 3,4,5), all degree-5 holes
  census-check F.jsonl      recompute radii of records of a census file (--limit N, evenly spaced)
  planted                   planted-kill check (target = 'link uses <= 1 colour')

DEFINITIONS AS IMPLEMENTED
  State: plane triangulation (oriented faces), hole h of degree 5, proper 4-colouring of T-h,
    link of h with four colours.  Colours are stored per vertex index; the hole entry is HOLE.
  Canonical form: colours renumbered in order of first occurrence over vertices in increasing
    LABEL order, hole skipped.
  Kempe swap: pick an unordered colour pair {p,q} and one connected component of the subgraph of
    T-h induced by the vertices coloured p or q (single vertices are components); exchange p, q on
    it.  All (pair, component) choices are generated, including those whose canonical result is the
    same state.
  Filled: link of h uses <= 3 colours.  Radius: least number of swaps to a filled state.
  Doubly locked: link x0..x4 in rotation order (face orientation), repeated colour at x_j, x_{j+2};
    m = x_{j+1}, a = x_{j+3}, b = x_{j+4}; m,a in one component of the {col m, col a} subgraph of
    T-h and m,b in one component of the {col m, col b} subgraph.
  State cap (cert): DEFAULT_CAP = 300000 canonical states visited (memory about 60 MB).  A search
    that would exceed it reports CAPPED.
"""
import sys, json, hashlib
from collections import deque

HOLE = 255
DEFAULT_CAP = 300000


class Invalid(Exception):
    pass


# ----------------------------------------------------------------------------- graphs
class Tri:
    """A plane triangulation from oriented faces, validated."""

    def __init__(self, faces):
        self.faces = [tuple(int(x) for x in f) for f in faces]
        self._validate()

    def _validate(self):
        faces = self.faces
        if not faces:
            raise Invalid("NOT-TRIANGULATION: no faces")
        dir_count = {}
        for f in faces:
            if len(f) != 3 or len(set(f)) != 3:
                raise Invalid("NOT-TRIANGULATION: face %r is not three distinct vertices" % (f,))
            for i in range(3):
                e = (f[i], f[(i + 1) % 3])
                dir_count[e] = dir_count.get(e, 0) + 1
        for e, k in dir_count.items():
            if k != 1:
                raise Invalid("NOT-TRIANGULATION: directed edge %r lies in %d faces (need exactly 1)" % (e, k))
        for (a, b) in dir_count:
            if (b, a) not in dir_count:
                raise Invalid("NOT-TRIANGULATION: directed edge (%d,%d) has no reverse (%d,%d): not symmetric/oriented" % (a, b, b, a))
        if len({tuple(sorted(f)) for f in faces}) != len(faces):
            raise Invalid("NOT-TRIANGULATION: a triangle appears twice")
        self.labels = sorted({x for f in faces for x in f})
        self.n = len(self.labels)
        self.idx = {l: i for i, l in enumerate(self.labels)}
        edges = {frozenset(e) for e in dir_count}
        E, F, n = len(edges), len(faces), self.n
        if E != 3 * n - 6 or F != 2 * n - 4 or n - E + F != 2:
            raise Invalid("NOT-TRIANGULATION: Euler fails (n=%d E=%d F=%d; need E=3n-6=%d, F=2n-4=%d)" % (n, E, F, 3 * n - 6, 2 * n - 4))
        self.adj = [set() for _ in range(n)]
        for e in edges:
            a, b = tuple(e)
            self.adj[self.idx[a]].add(self.idx[b])
            self.adj[self.idx[b]].add(self.idx[a])
        # rotation at each vertex must be one cycle (rules out pinched surfaces)
        self.rot = []
        for vi in range(n):
            nxt = {}
            for f in faces:
                for i in range(3):
                    if self.idx[f[i]] == vi:
                        nxt[self.idx[f[(i + 1) % 3]]] = self.idx[f[(i + 2) % 3]]
            if len(nxt) != len(self.adj[vi]) or len(nxt) < 3:
                raise Invalid("NOT-TRIANGULATION: vertex %d has inconsistent rotation" % self.labels[vi])
            start = next(iter(nxt))
            cyc, x = [start], nxt[start]
            while x != start:
                cyc.append(x)
                x = nxt[x]
                if len(cyc) > len(nxt):
                    raise Invalid("NOT-TRIANGULATION: rotation at vertex %d is not a cycle" % self.labels[vi])
            if len(cyc) != len(nxt):
                raise Invalid("NOT-TRIANGULATION: link of vertex %d is not a single cycle" % self.labels[vi])
            self.rot.append(cyc)
        # connectivity
        seen, st = {0}, [0]
        while st:
            u = st.pop()
            for w in self.adj[u]:
                if w not in seen:
                    seen.add(w); st.append(w)
        if len(seen) != n:
            raise Invalid("NOT-TRIANGULATION: disconnected")

    def deg(self, label):
        return len(self.adj[self.idx[label]])


def orient_faces(faces):
    """Helper (not used by 'cert', which demands oriented input): orient an unoriented triangle
    list consistently by propagation; raises Invalid if impossible."""
    faces = [tuple(f) for f in faces]
    oriented = {0: faces[0]}
    by_edge = {}
    for k, f in enumerate(faces):
        for i in range(3):
            by_edge.setdefault(frozenset((f[i], f[(i + 1) % 3])), []).append(k)
    queue = deque([0])
    while queue:
        k = queue.popleft()
        f = oriented[k]
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            for k2 in by_edge[frozenset((a, b))]:
                if k2 == k or k2 in oriented:
                    continue
                g = faces[k2]
                # need directed edge (b,a) in oriented g
                for j in range(3):
                    if (g[j], g[(j + 1) % 3]) == (b, a):
                        oriented[k2] = g; break
                else:
                    oriented[k2] = (g[0], g[2], g[1])
                queue.append(k2)
    if len(oriented) != len(faces):
        raise Invalid("cannot orient: disconnected face set")
    return [list(oriented[k]) for k in range(len(faces))]


# ----------------------------------------------------------------------------- holes and states
class Hole:
    """Graph T with a distinguished vertex index h: adjacency in T-h, link in rotation order."""

    def __init__(self, T, h):
        self.T, self.h, self.n = T, h, T.n
        self.adj = [sorted(w for w in T.adj[u] if w != h) if u != h else [] for u in range(T.n)]
        self.link = list(T.rot[h])
        self.order = [u for u in range(T.n) if u != h]

    def canon(self, col):
        mp, out, k = {}, bytearray(self.n), 0
        for u in self.order:
            c = col[u]
            if c not in mp:
                mp[c] = k; k += 1
            out[u] = mp[c]
        out[self.h] = HOLE
        return bytes(out)

    def linkcolours(self, s):
        return len({s[x] for x in self.link})

    def filled(self, s):
        return self.linkcolours(s) <= 3

    def component(self, s, start, p, q):
        seen, st, adj = {start}, [start], self.adj
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen and (s[w] == p or s[w] == q):
                    seen.add(w); st.append(w)
        return seen

    def neighbours(self, s):
        """All canonical states one Kempe swap away (whole components, all pairs)."""
        res = set()
        adj, order = self.adj, self.order
        cols = sorted({s[u] for u in order})
        for ai in range(len(cols)):
            for bi in range(ai + 1, len(cols)):
                p, q = cols[ai], cols[bi]
                seen = set()
                for u in order:
                    if (s[u] == p or s[u] == q) and u not in seen:
                        comp = {u}; st = [u]
                        while st:
                            x = st.pop()
                            for w in adj[x]:
                                if w not in comp and (s[w] == p or s[w] == q):
                                    comp.add(w); st.append(w)
                        seen |= comp
                        t = bytearray(s)
                        for x in comp:
                            t[x] = q if s[x] == p else p
                        res.add(self.canon(t))
        return res

    def doubly_locked(self, s):
        lk = [s[x] for x in self.link]
        if len(self.link) != 5 or len(set(lk)) != 4:
            return False
        j = None
        for t in range(5):
            if lk[t] == lk[(t + 2) % 5]:
                j = t
        if j is None:
            return False
        m, a, b = self.link[(j + 1) % 5], self.link[(j + 3) % 5], self.link[(j + 4) % 5]
        return (a in self.component(s, m, s[m], s[a])) and (b in self.component(s, m, s[m], s[b]))

    def F(self, s):
        """Rotation F: swap col x_j and col x_{j+3} on the component of x_{j+2}; None if not 4-link."""
        lk = [s[x] for x in self.link]
        if len(set(lk)) != 4:
            return None
        j = [t for t in range(5) if lk[t] == lk[(t + 2) % 5]][0]
        x2, x3 = self.link[(j + 2) % 5], self.link[(j + 3) % 5]
        p, q = s[x2], s[x3]
        comp = self.component(s, x2, p, q)
        t = bytearray(s)
        for x in comp:
            t[x] = q if s[x] == p else p
        return self.canon(t)


def filled_pred(H, s):
    return H.linkcolours(s) <= 3


def planted_pred(H, s):
    return H.linkcolours(s) <= 1


def kempe_search(H, s0, target=filled_pred, cap=DEFAULT_CAP):
    """Layered BFS over the Kempe class of canonical state s0.
    Returns ('RADIUS', r, visited) | ('CLOSED', class_size, class_size) | ('CAPPED', None, visited)."""
    s0 = H.canon(s0)
    seen = {s0}
    layer, d = [s0], 0
    while layer:
        for s in layer:
            if target(H, s):
                return ("RADIUS", d, len(seen))
        nxt = []
        for s in layer:
            for t in H.neighbours(s):
                if t not in seen:
                    seen.add(t); nxt.append(t)
                    if len(seen) > cap:
                        return ("CAPPED", None, len(seen))
        layer, d = nxt, d + 1
    return ("CLOSED", len(seen), len(seen))


# ----------------------------------------------------------------------------- certificate
def load_cert(path):
    try:
        with open(path) as fh:
            c = json.load(fh)
    except Exception as e:
        raise Invalid("cannot read certificate: %s" % e)
    for k in ("faces", "v", "colouring"):
        if k not in c:
            raise Invalid("certificate lacks field '%s'" % k)
    return c


def build_state(c):
    T = Tri(c["faces"])
    v = int(c["v"])
    if v not in T.idx:
        raise Invalid("hole v=%r is not a vertex" % v)
    if T.deg(v) != 5:
        raise Invalid("hole v=%d has degree %d, need 5" % (v, T.deg(v)))
    H = Hole(T, T.idx[v])
    col = {}
    for k, x in c["colouring"].items():
        col[int(k)] = x
    for l in T.labels:
        if l == v:
            if l in col:
                raise Invalid("colouring assigns a colour to the hole v=%d" % v)
            continue
        if l not in col:
            raise Invalid("colouring misses vertex %d" % l)
        if not isinstance(col[l], int) or not 0 <= col[l] <= 3:
            raise Invalid("colour of vertex %d is %r, need 0..3" % (l, col[l]))
    extra = set(col) - set(T.labels)
    if extra:
        raise Invalid("colouring mentions non-vertices %s" % sorted(extra))
    s = bytearray(T.n)
    for l in T.labels:
        s[T.idx[l]] = HOLE if l == v else col[l]
    for u in range(T.n):
        if u == H.h:
            continue
        for w in H.adj[u]:
            if w > u and s[u] == s[w]:
                raise Invalid("improper colouring: edge (%d,%d) is monochromatic (colour %d)" % (T.labels[u], T.labels[w], s[u]))
    if len({s[x] for x in H.link}) != 4:
        raise Invalid("link of v uses %d colours, need 4" % len({s[x] for x in H.link}))
    return T, H, H.canon(s)


def verify_claim(res, claim, dl):
    kind, val, vis = res
    if kind == "CAPPED":
        return 2, "CAPPED: state cap reached after %d states, inconclusive" % vis
    if claim is None:
        return 0, "no claim given; result reported only"
    if kind == "RADIUS":
        if claim.get("radius") is None:
            return 1, "CONTRADICTED: claim is a targetless class but a filled state exists at distance %d" % val
        if claim["radius"] != val:
            return 1, "CONTRADICTED: claimed radius %r, recomputed radius %d" % (claim["radius"], val)
        return 0, "CONFIRMED: radius %d" % val
    # CLOSED
    if claim.get("radius") is not None:
        return 1, "CONTRADICTED: claimed radius %r but the class (size %d) is closed with no filled state" % (claim["radius"], val)
    if not claim.get("class_closed_no_filled"):
        return 1, "CONTRADICTED: claim has radius null but lacks class_closed_no_filled"
    if "class_size" in claim and claim["class_size"] != val:
        return 1, "CONTRADICTED: claimed class size %r, recomputed %d" % (claim["class_size"], val)
    return 0, "CONFIRMED: closed class of size %d with no filled state" % val


def cmd_cert(path, cap=DEFAULT_CAP, orient=False):
    try:
        c = load_cert(path)
        if orient:
            c["faces"] = orient_faces(c["faces"])
        T, H, s0 = build_state(c)
    except Invalid as e:
        print("INVALID:", e)
        return 2
    dl = H.doubly_locked(s0)
    res = kempe_search(H, s0, filled_pred, cap)
    if res[0] == "RADIUS":
        print("RADIUS %d" % res[1])
    elif res[0] == "CLOSED":
        print("CLOSED-NO-FILLED class size %d" % res[1])
    else:
        print("CAPPED after %d states (cap %d)" % (res[2], cap))
    print("start doubly locked: %s" % dl)
    code, msg = verify_claim(res, c.get("claim"), dl)
    print(msg)
    return code


# ----------------------------------------------------------------------------- the family A_r
def build_A(r):
    """A_r (a-structure.md section 1): v=0, ring vertex (i,t) = 1+5i+t, cap c = 5r+1.
    Edges: v~(0,t); (i,t)~(i,t+1); (i+1,t)~(i,t),(i,t+1); c~(r-1,t).
    Triangles: (v,(0,t),(0,t+1)); ((i,t),(i,t+1),(i+1,t)); ((i,t+1),(i+1,t+1),(i+1,t)); (c,(r-1,t+1),(r-1,t))."""
    def V(i, t):
        return 1 + 5 * i + (t % 5)
    cap = 5 * r + 1
    faces = []
    for t in range(5):
        faces.append((0, V(0, t), V(0, t + 1)))
        faces.append((cap, V(r - 1, t + 1), V(r - 1, t)))
        for i in range(r - 1):
            faces.append((V(i, t), V(i, t + 1), V(i + 1, t)))
            faces.append((V(i, t + 1), V(i + 1, t + 1), V(i + 1, t)))
    return orient_faces(faces)


def faces_hash(faces):
    """Defined here (spec leaves it open): sha256 of repr of sorted faces, each rotated so its smallest label is first."""
    norm = []
    for f in faces:
        k = f.index(min(f))
        norm.append(tuple(f[k:] + f[:k]))
    return hashlib.sha256(repr(sorted(norm)).encode()).hexdigest()


def enumerate_states(H):
    """All proper 4-colourings of T-h in canonical form (DFS in label order with first-occurrence symmetry breaking)."""
    order, adj = H.order, H.adj
    col = [HOLE] * H.n
    out = []

    def rec(k, used):
        if k == len(order):
            out.append(bytes(col)); return
        u = order[k]
        forb = {col[w] for w in adj[u] if col[w] != HOLE}
        for c in range(min(used + 1, 4)):
            if c not in forb:
                col[u] = c
                rec(k + 1, max(used, c + 1))
        col[u] = HOLE

    rec(0, 0)
    return out


def census_graph(r):
    faces = build_A(r)
    T = Tri(faces)
    degs = sorted(len(a) for a in T.adj)
    return faces, T, degs


def cmd_census(name, outpath=None):
    r = int(name.split("_")[1])
    faces, T, degs = census_graph(r)
    expect_n = 5 * r + 2
    assert T.n == expect_n, (T.n, expect_n)
    assert set(degs) <= {5, 6}
    print("%s: order %d (expected %d), degrees %s, faces_sha256 %s" % (name, T.n, expect_n, {d: degs.count(d) for d in (5, 6)}, faces_hash(faces)[:16]))
    fh = open(outpath, "w") if outpath else None
    sha = faces_hash(faces)
    # rotation automorphisms sigma_k: (i,t)->(i,t+k) fix v, cap; used only to group holes into classes
    def sigma(lab, k):
        if lab == 0 or lab == 5 * r + 1:
            return lab
        i, t = divmod(lab - 1, 5)
        return 1 + 5 * i + (t + k) % 5
    edges = {frozenset((T.labels[u], T.labels[w])) for u in range(T.n) for w in T.adj[u]}
    for k in range(1, 5):
        assert {frozenset(sigma(x, k) for x in e) for e in edges} == edges, "sigma not an automorphism"
    holes = [T.labels[u] for u in range(T.n) if len(T.adj[u]) == 5]
    classes = {}
    for h in holes:
        classes.setdefault(frozenset(sigma(h, k) for k in range(5)), []).append(h)
    total_hist, per_hole = {}, {}
    for h in holes:
        H = Hole(T, T.idx[h])
        states = enumerate_states(H)
        sset = set(states)
        # multi-source BFS from filled states (swaps are involutions, so the graph is undirected)
        dist = {s: 0 for s in states if H.filled(s)}
        frontier = list(dist)
        d = 0
        while frontier:
            d += 1
            nxt = []
            for s in frontier:
                for t in H.neighbours(s):
                    if t not in sset:
                        raise AssertionError("swap left the enumerated space")
                    if t not in dist:
                        dist[t] = d; nxt.append(t)
            frontier = nxt
        hist, nonDL = {}, 0
        ndl = 0
        for s in states:
            if H.linkcolours(s) == 4 and H.doubly_locked(s):
                ndl += 1
                rr = dist.get(s)
                key = "inf" if rr is None else rr
                hist[key] = hist.get(key, 0) + 1
                if fh:
                    rec = {"graph": name, "v": h, "faces_sha256": sha,
                           "state": [-1 if u == H.h else s[u] for u in range(T.n)],
                           "doubly_locked": True, "radius": rr}
                    fh.write(json.dumps(rec) + "\n")
        per_hole[h] = hist
        print("  hole %2d: %6d canonical states, %5d with 4-link, %4d doubly locked, radius histogram %s" % (
            h, len(states), sum(1 for s in states if H.linkcolours(s) == 4), ndl, dict(sorted(hist.items(), key=lambda kv: (kv[0] == 'inf', kv[0] if kv[0] != 'inf' else 0)))))
        for key, val in hist.items():
            total_hist[key] = total_hist.get(key, 0) + val
    print("  per hole class (orbits under the 5-fold rotation, tested as automorphism; equality of histograms inside a class is CHECKED):")
    for cl, hs in classes.items():
        ref = per_hole[hs[0]]
        same = all(per_hole[h] == ref for h in hs)
        print("    class %s: histogram %s  symmetric-consistent=%s" % (sorted(hs), dict(ref), same))
    print("  total over all %d holes: %s" % (len(holes), dict(total_hist)))
    if fh:
        fh.close()


# ----------------------------------------------------------------------------- census-check
def cmd_census_check(path, limit=2000, cap=DEFAULT_CAP):
    recs = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    n = len(recs)
    step = max(1, n // limit) if limit else 1
    chosen = recs[::step][:limit] if limit else recs
    cache, bad, skipped, hash_diff = {}, 0, 0, 0
    for rec in chosen:
        g = rec["graph"]
        if not g.startswith("A_"):
            skipped += 1; continue
        if g not in cache:
            faces = build_A(int(g[2:]))
            cache[g] = (Tri(faces), faces_hash(faces))
        T, sha = cache[g]
        if rec.get("faces_sha256") != sha:
            hash_diff += 1
        if rec["v"] not in T.idx:
            print("MISMATCH: hole %r not a vertex of %s" % (rec["v"], g)); bad += 1; continue
        H = Hole(T, T.idx[rec["v"]])
        s = bytearray(T.n)
        for u in range(T.n):
            s[u] = HOLE if u == H.h else rec["state"][u]
        problems = []
        if rec["state"][H.h] != -1:
            problems.append("hole entry not -1")
        for u in range(T.n):
            if u != H.h:
                for w in H.adj[u]:
                    if w > u and s[u] == s[w]:
                        problems.append("improper at edge (%d,%d)" % (u, w)); break
        s = H.canon(s)
        if [(-1 if u == H.h else s[u]) for u in range(T.n)] != rec["state"]:
            problems.append("state not in canonical form")
        dl = H.linkcolours(s) == 4 and H.doubly_locked(s)
        if dl != rec["doubly_locked"]:
            problems.append("doubly_locked recomputed %s, record %s" % (dl, rec["doubly_locked"]))
        res = kempe_search(H, s, filled_pred, cap)
        got = res[1] if res[0] == "RADIUS" else (None if res[0] == "CLOSED" else "capped")
        claim = rec["radius"]
        if claim in ("inf", -1):
            claim = None
        if got == "capped":
            problems.append("capped, inconclusive")
        elif got != claim:
            problems.append("radius recomputed %r, record %r" % (got, rec["radius"]))
        if problems:
            bad += 1
            print("MISMATCH %s v=%s: %s" % (g, rec["v"], "; ".join(problems)))
    print("census-check: %d records in file, %d examined (every %d-th), %d skipped (not A_r), %d mismatches, faces_sha256 differs from my own definition in %d (informational: hash definition is unspecified)" % (
        n, len(chosen), step, skipped, bad, hash_diff))
    return 1 if bad else 0


# ----------------------------------------------------------------------------- planted
def cmd_planted():
    faces = build_A(3)
    T = Tri(faces)
    H = Hole(T, T.idx[0])
    sts = [s for s in enumerate_states(H) if H.linkcolours(s) == 4 and H.doubly_locked(s)]
    s0 = sts[0]
    true_res = kempe_search(H, s0, filled_pred)
    plant_res = kempe_search(H, s0, planted_pred)
    print("A_3 centre, first doubly locked state: true predicate -> %s; planted predicate (link <= 1 colour) -> %s" % (true_res[:2], plant_res[:2]))
    ok = true_res[0] == "RADIUS" and plant_res[0] == "CLOSED" and plant_res[1] > 1
    # class size must agree with an independent flood fill of the class
    seen, st = {s0}, [s0]
    while st:
        x = st.pop()
        for y in H.neighbours(x):
            if y not in seen:
                seen.add(y); st.append(y)
    ok = ok and len(seen) == plant_res[1]
    print("class size by flood fill %d, by planted BFS %d; planted kill logic %s" % (len(seen), plant_res[1], "WORKS" if ok else "FAILS"))
    return 0 if ok else 1


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    cmd = argv[1]
    cap = DEFAULT_CAP
    if "--cap" in argv:
        cap = int(argv[argv.index("--cap") + 1])
    if cmd == "cert":
        return cmd_cert(argv[2], cap, orient="--orient" in argv)
    if cmd == "census":
        out = argv[argv.index("--out") + 1] if "--out" in argv else None
        names = [argv[2]] if argv[2] != "all" else ["A_3", "A_4", "A_5"]
        for nm in names:
            cmd_census(nm, out if len(names) == 1 else None)
        return 0
    if cmd == "census-check":
        lim = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else 2000
        return cmd_census_check(argv[2], lim, cap)
    if cmd == "planted":
        return cmd_planted()
    print("unknown command", cmd); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
