#!/usr/bin/env python3
"""wp22_radius.py -- S2 core: states at a degree-5 hole, doubly locked test, F, Kempe classes, radius (WP22).

Standard library only.  Written from WP22-interface.md and WP22-S2-preregistration.md (revision 2).  It imports
nothing from the project.  The existing prototypes were used as DATA/model only.

DEFINITIONS (same as WP22-interface.md)
  Hole(faces, v): faces = oriented triangles (a,b,c) of a plane triangulation T, v a vertex (degree 5 for states).
  A state is a proper 4-colouring of T-v, stored CANONICALLY as `bytes` of length n-1: the colour of every vertex except
  v, in increasing vertex-label order, colours renamed 0,1,2,.. in order of first occurrence over that order.
  filled(s)    : the link of v uses at most 3 colours.
  doubly locked: link x_0..x_4 (rotation order of the oriented faces) has 4 colours; the repeated colour sits at x_j and
                 x_{j+2}; m = x_{j+1}, a = x_{j+3}, b = x_{j+4}; m~a in one {col m, col a}-component of T-v and
                 m~b in one {col m, col b}-component.
  F(s)         : alpha = col x_j, c = col x_{j+3}; swap alpha<->c on the {alpha,c}-component of x_{j+2}.
  Kempe swap   : two colours and one whole component of the bichromatic subgraph of T-v, colours exchanged on it.
  Kempe class, radius, closed, capped: as in WP22-interface.md.

CAPS (documented choices; the pre-registration fixes only the first two)
  S2A_DEPTH = 6, S2A_CAP = 20000           breadth-first search per S2a evaluation (pre-registration)
  DEEP_CAP  = 100000                       S2a follow-up enumeration of an unresolved evaluation (<= 5 per tag)
  ENUM_CAP  = 1000000                      class enumeration for KILL-2 confirmation, S2b, S2c, tests.  A class that
                                           reaches the cap is reported 'capped' = inconclusive, never a kill or a pass.
                                           (1,000,000 canonical states of <= 40 vertices ~ 150 MB, ~15 CPU-minutes.)

BFS convention.  bfs(...) returns a dict with 'status':
  'found'   : a target state at distance r = 'radius'; 'ball' = number of states at distance < r (all untargeted)
  'closed'  : the whole class was enumerated (size 'explored'), no target in it (r = infinity)
  'depth'   : no target within max_depth swaps (r > max_depth), class not exhausted
  'capped'  : more than `cap` states met before an answer, or the CPU deadline passed (inconclusive)
The search stops as soon as a target state is GENERATED, so 'ball' counts levels 0..r-1 completely and is independent of
the order in which neighbours are generated.
"""
import hashlib
import json
import time

S2A_DEPTH = 6
S2A_CAP = 20000
DEEP_CAP = 100000
ENUM_CAP = 1000000


def canon(lst):
    """canonical renaming (first occurrence order) of a sequence of colours; returns bytes."""
    m = [-1, -1, -1, -1]
    k = 0
    out = bytearray(len(lst))
    for i, c in enumerate(lst):
        x = m[c]
        if x < 0:
            x = m[c] = k
            k += 1
        out[i] = x
    return bytes(out)


def norm_face(f):
    a, b, c = f
    return min((a, b, c), (b, c, a), (c, a, b))


def faces_key(faces):
    """canonical text of a face set: sorted, each face rotated to start at its least vertex."""
    return json.dumps(sorted(list(norm_face(f)) for f in faces), separators=(",", ":"))


def faces_sha256(faces):
    return hashlib.sha256(faces_key(faces).encode()).hexdigest()


class Hole:
    """a triangulation with a distinguished vertex v; all state operations live here."""

    def __init__(self, faces, v):
        faces = [tuple(f) for f in faces]
        succ = {}
        for a, b, c in faces:
            for u, p, q in ((a, b, c), (b, c, a), (c, a, b)):
                d = succ.setdefault(u, {})
                if p in d:
                    raise ValueError("inconsistent orientation at %s" % u)
                d[p] = q
        rot = {}
        for u, m in succ.items():
            start = next(iter(m))
            cyc = [start]
            x = m[start]
            while x != start:
                cyc.append(x)
                x = m[x]
                if len(cyc) > len(m):
                    raise ValueError("link of %s is not one cycle" % u)
            if len(cyc) != len(m):
                raise ValueError("link of %s is not one cycle" % u)
            rot[u] = cyc
        if v not in rot:
            raise ValueError("hole not a vertex")
        self.faces = faces
        self.rot = rot
        self.v = v
        self.n = len(rot)
        self.labels = sorted(u for u in rot if u != v)
        self.idx = {u: i for i, u in enumerate(self.labels)}
        self.N = len(self.labels)
        self.adj = [[self.idx[w] for w in rot[u] if w != v] for u in self.labels]
        self.link_labels = list(rot[v])
        self.link = [self.idx[x] for x in self.link_labels]
        self.degree = {u: len(r) for u, r in rot.items()}

    # ------------------------------------------------------------------ validity
    def check(self):
        """simple graph, symmetric, Euler V-E+F=2, every face a triangle (faces given), return message or None."""
        for u, r in self.rot.items():
            if len(set(r)) != len(r) or u in r:
                return "not simple at %s" % u
            for w in r:
                if u not in self.rot[w]:
                    return "asymmetric"
        E = sum(len(r) for r in self.rot.values()) // 2
        if self.n - E + len(self.faces) != 2 or 3 * len(self.faces) != 2 * E:
            return "Euler fails"
        return None

    def proper(self, col):
        return all(col[i] != col[j] for i in range(self.N) for j in self.adj[i])

    # ------------------------------------------------------------------ state <-> labelled colouring
    def state_of(self, colouring):
        """colouring: dict label -> colour (v absent or ignored) -> canonical state."""
        return canon([colouring[u] for u in self.labels])

    def colouring_of(self, st):
        return {u: st[i] for i, u in enumerate(self.labels)}

    # ------------------------------------------------------------------ predicates
    def filled(self, st):
        c = [st[i] for i in self.link]
        return len(set(c)) < 4

    def comp(self, col, start, c1, c2):
        seen = {start}
        stack = [start]
        adj = self.adj
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in seen and (col[w] == c1 or col[w] == c2):
                    seen.add(w)
                    stack.append(w)
        return seen

    def repeat_index(self, col):
        cs = [col[x] for x in self.link]
        if len(set(cs)) != 4:
            return None
        js = [j for j in range(5) if cs[j] == cs[(j + 2) % 5]]
        return js[0] if len(js) == 1 else None

    def is_dl(self, col):
        j = self.repeat_index(col)
        if j is None:
            return False
        L = self.link
        m, a, b = L[(j + 1) % 5], L[(j + 3) % 5], L[(j + 4) % 5]
        return (a in self.comp(col, m, col[m], col[a])) and (b in self.comp(col, m, col[m], col[b]))

    def F(self, col):
        j = self.repeat_index(col)
        if j is None:
            return None
        L = self.link
        al, c = col[L[j]], col[L[(j + 3) % 5]]
        K = self.comp(col, L[(j + 2) % 5], al, c)
        new = list(col)
        for u in K:
            new[u] = c if col[u] == al else al
        return new

    def chain_len(self, col, cap=40):
        """consecutive doubly locked F-iterates from col (0 if not doubly locked), at most cap."""
        k = 0
        s = list(col)
        while k < cap and s is not None and self.is_dl(s):
            k += 1
            s = self.F(s)
        return k

    # ------------------------------------------------------------------ Kempe neighbours
    def neighbours(self, st):
        """canonical states reachable from st by one Kempe swap (st itself excluded), unique."""
        adj = self.adj
        N = self.N
        out = set()
        for c1 in range(3):
            for c2 in range(c1 + 1, 4):
                seen = bytearray(N)
                for u in range(N):
                    cu = st[u]
                    if seen[u] or (cu != c1 and cu != c2):
                        continue
                    seen[u] = 1
                    members = [u]
                    stack = [u]
                    while stack:
                        x = stack.pop()
                        for w in adj[x]:
                            if not seen[w]:
                                cw = st[w]
                                if cw == c1 or cw == c2:
                                    seen[w] = 1
                                    members.append(w)
                                    stack.append(w)
                    new = list(st)
                    for x in members:
                        new[x] = c2 if st[x] == c1 else c1
                    t = canon(new)
                    if t != st:
                        out.add(t)
        return out

    # ------------------------------------------------------------------ breadth-first search
    def bfs(self, s0, target=None, max_depth=None, cap=None, deadline=None):
        """level-by-level search from canonical state s0 for the nearest state with target(st) true
        (default: filled).  See the module docstring for the result."""
        if target is None:
            target = self.filled
        if target(s0):
            return {"status": "found", "radius": 0, "ball": 0, "explored": 1}
        seen = {s0}
        frontier = [s0]
        d = 0
        tick = 0
        while frontier:
            if max_depth is not None and d >= max_depth:
                return {"status": "depth", "radius": None, "ball": len(seen), "explored": len(seen),
                        "depth_reached": d}
            before = len(seen)
            nxt = []
            for st in frontier:
                tick += 1
                if deadline is not None and (tick & 63) == 0 and time.process_time() > deadline:
                    return {"status": "capped", "radius": None, "ball": len(seen), "explored": len(seen),
                            "why": "deadline"}
                for t in self.neighbours(st):
                    if t in seen:
                        continue
                    if target(t):
                        return {"status": "found", "radius": d + 1, "ball": before, "explored": len(seen) + 1}
                    seen.add(t)
                    nxt.append(t)
                if cap is not None and len(seen) > cap:
                    return {"status": "capped", "radius": None, "ball": len(seen), "explored": len(seen),
                            "why": "cap"}
            frontier = nxt
            d += 1
        return {"status": "closed", "radius": None, "ball": len(seen), "explored": len(seen),
                "class_size": len(seen)}

    def enumerate_class(self, s0, cap=ENUM_CAP, deadline=None):
        """the whole Kempe class of s0 (set of canonical states), or None if capped."""
        seen = {s0}
        stack = [s0]
        tick = 0
        while stack:
            st = stack.pop()
            tick += 1
            if deadline is not None and (tick & 63) == 0 and time.process_time() > deadline:
                return None
            for t in self.neighbours(st):
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
            if len(seen) > cap:
                return None
        return seen

    def class_radii(self, s0, cap=ENUM_CAP, deadline=None, target=None):
        """multi-source radius: enumerate the class of s0 and return (dist, class_size) where dist maps every state of
        the class to its distance to the nearest target state (absent if unreached); (None, None) if capped."""
        if target is None:
            target = self.filled
        cls = self.enumerate_class(s0, cap, deadline)
        if cls is None:
            return None, None
        dist = {}
        fr = []
        for t in cls:
            if target(t):
                dist[t] = 0
                fr.append(t)
        d = 0
        while fr:
            d += 1
            nxt = []
            for st in fr:
                for t in self.neighbours(st):
                    if t not in dist:
                        dist[t] = d
                        nxt.append(t)
            fr = nxt
        return dist, len(cls)


def radius(H, s0, cap=ENUM_CAP, deadline=None, max_depth=None, target=None):
    """exact radius by breadth-first search.  Returns (r, info): r an int, float('inf') for a closed targetless
    class, None if capped / depth-limited (inconclusive)."""
    info = H.bfs(s0, target=target, max_depth=max_depth, cap=cap, deadline=deadline)
    if info["status"] == "found":
        return info["radius"], info
    if info["status"] == "closed":
        return float("inf"), info
    return None, info


# ---------------------------------------------------------------------------------------- certificates
def make_cert(H, st, claim):
    return {"faces": [list(f) for f in sorted(H.faces)], "v": H.v,
            "colouring": {str(u): int(st[i]) for i, u in enumerate(H.labels)}, "claim": claim}


def check_cert(cert, cap=ENUM_CAP):
    """re-check a certificate of this module (own code; the independent verifier is a separate team's job).
    Returns (ok, message)."""
    H = Hole([tuple(f) for f in cert["faces"]], cert["v"])
    msg = H.check()
    if msg:
        return False, msg
    if H.degree[H.v] != 5:
        return False, "v is not of degree 5"
    col = [cert["colouring"][str(u)] for u in H.labels]
    if not H.proper(col):
        return False, "colouring not proper"
    s0 = canon(col)
    if not H.is_dl(list(s0)) and cert["claim"].get("require_dl", True):
        return False, "state is not doubly locked"
    r, info = radius(H, s0, cap=cap)
    cl = cert["claim"]
    if cl.get("radius") is not None:
        return (r == cl["radius"]), "recomputed radius %r" % (r,)
    if cl.get("class_closed_no_filled"):
        ok = r == float("inf") and info["class_size"] == cl.get("class_size", info["class_size"])
        return ok, "recomputed %s, class size %s" % (info["status"], info.get("class_size"))
    return False, "unknown claim"


# ---------------------------------------------------------------------------------------- enumeration of states
def all_states(H, need_four_link=True, max_states=None):
    """every proper 4-colouring of T-v up to colour renaming (canonical states).  With need_four_link only those whose
    link uses 4 colours.  DFS in a BFS order from the link (link vertices first), colours introduced in order."""
    order = list(H.link)
    inset = set(order)
    i = 0
    while i < len(order):
        for w in H.adj[order[i]]:
            if w not in inset:
                inset.add(w)
                order.append(w)
        i += 1
    for u in range(H.N):          # disconnected pieces (cannot happen for triangulations, kept for safety)
        if u not in inset:
            inset.add(u)
            order.append(u)
    pos = {u: k for k, u in enumerate(order)}
    prior = [[w for w in H.adj[u] if pos[w] < pos[u]] for u in order]
    col = [-1] * H.N
    out = []
    linkset = set(H.link)
    last_link_pos = max(pos[x] for x in H.link)

    def rec(k, used):
        if k == H.N:
            st = canon(col)
            if need_four_link and len({st[x] for x in H.link}) < 4:
                return
            out.append(st)
            return
        u = order[k]
        banned = {col[w] for w in prior[k]}
        for c in range(min(used + 1, 4)):
            if c in banned:
                continue
            col[u] = c
            if need_four_link and k == last_link_pos:
                if len({col[x] for x in H.link}) < 4:
                    col[u] = -1
                    continue
            rec(k + 1, max(used, c + 1))
        col[u] = -1

    import sys
    sys.setrecursionlimit(max(10000, sys.getrecursionlimit()))
    rec(0, 0)
    return out
