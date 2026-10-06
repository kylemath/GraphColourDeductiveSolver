#!/usr/bin/env python3
"""wp22_search.py -- S2a: hill-climb on the Kempe radius of doubly locked states (WP22 pre-registration, rev. 2).

  wp22_search.py TAG [--cpu 120] [--max-steps N]        (prints the result JSON)

State (faces, v, col): oriented triangles of a plane triangulation with MINIMUM DEGREE >= 4 AT EVERY VISITED STATE, v a
vertex of degree 5, col a proper 4-colouring of T-v; every accepted state is doubly locked (r is only defined
for doubly locked states and the start state must be one).
Resolution of the pre-registration's ambiguity: S2a says "minimum degree at least 4" but names the prototype's moves
'stack' and 'delete a degree-3 vertex', which create degree-3 vertices.  Here the moves are exactly
  Kempe swap (probability 0.6): a uniformly chosen vertex u != v, a uniformly chosen other colour, the whole component;
  edge flip   (probability 0.4): a flip that keeps every degree >= 4 (both endpoints of the flipped edge had degree
                                 >= 5), does not touch v or an edge of the star of v, keeps the colouring proper
                                 (the two new-diagonal ends have different colours), keeps the graph simple.
Order is fixed per restart (uniform in 12..30).  Start graphs: random stacking from K4 to the order, then random flips
(the flip rule above, plus a descent on the number of degree<4 vertices), then REJECTION of any graph with a vertex of
degree < 4 (and of any graph with no degree-5 vertex or no doubly locked state found in 200 random Kempe swaps from
random colourings).
Objective (maximise, as a pair): (r, ball), r = Kempe radius of the current state from breadth-first search over Kempe
swaps of T-v to depth <= 6 and <= 20,000 canonical states; ball = number of states at distance < r from s0 (all
unfilled, = "number of unfilled states in the ball", tie-break).  If the search ends with depth > 6 or the cap, the
evaluation is "unresolved": r is set to 7 (meaning >= 7) with ball = states met, and (at most DEEP_MAX = 5 times per
tag) a follow-up enumeration up to DEEP_CAP = 100,000 states gives the exact radius, a closed class (KILL-2) or
'capped' (inconclusive).  A closed class with no filled state, from either search, is a KILL-2: a certificate in the
WP22-interface format is output and the tag stops.
Acceptance: S' >= S (plateaus accepted); `since` counts non-improving STEPS (a step is any attempted move, including an
illegal move or one that leaves the doubly locked states; the prototype did not count illegal moves) and a restart
happens at 400.  The depth-6 / 20,000-state search itself is never interrupted (so a replay is exact); only a deep follow-up
honours the CPU deadline.  Stop: CPU seconds (time.process_time) >= --cpu (reported "capped": the tag reached its cap, which is
inconclusive by the pre-registration) or --max-steps (testing).
Seed: random.Random("wp22|s2a|" + tag).  Determinism: the result is a function of (tag, number of steps done);
the CPU cap decides only where the run stops; the result records `steps` and a replay with --max-steps=<steps>
reproduces it byte for byte (timing is NOT in the result).
"""
import json
import random
import sys
import time

import wp22_radius as R

STALL = 400
P_KEMPE = 0.6
NLO, NHI = 12, 30
DEEP_MAX = 5
UNRESOLVED_R = 7


# ---------------------------------------------------------------------------------------- graph generation
def adj_of(faces):
    A = {}
    for t in faces:
        for x in t:
            A.setdefault(x, set()).update(y for y in t if y != x)
    return A


def other_face_vertex(faces, a, b):
    """the vertex d of the face containing the directed edge (b,a)  (the face on the other side of (a,b))."""
    for (x, y, z) in faces:
        if (x, y) == (b, a):
            return z
        if (y, z) == (b, a):
            return x
        if (z, x) == (b, a):
            return y
    return None


def flip_edge(faces, a, b, c, d):
    """faces contains (a,b,c) and a face (b,a,d) (cyclically); replace by (c,d,b),(d,c,a)."""
    return {f for f in faces if set(f) not in ({a, b, c}, {a, b, d})} | {(c, d, b), (d, c, a)}


def random_stacked(rng, n):
    faces = {(0, 1, 2), (0, 3, 1), (1, 3, 2), (2, 3, 0)}
    for w in range(4, n):
        f = rng.choice(sorted(faces))
        a, b, c = f
        faces.remove(f)
        faces |= {(a, b, w), (b, c, w), (c, a, w)}
    return faces


def random_flips(rng, faces, nflips, descend=False):
    """random edge flips.  Every flip leaves all of its endpoints a,b with degree >= 4; with descend, a flip is made
    only if the number of vertices of degree < 4 does not increase."""
    faces = set(faces)
    A = adj_of(faces)
    for _ in range(nflips):
        t = rng.choice(sorted(faces))
        a, b, c = t
        if rng.random() < 0.5:
            a, b, c = b, c, a
        d = other_face_vertex(faces, a, b)
        if d is None or d == c or d in A[c]:
            continue
        if len(A[a]) < 4 or len(A[b]) < 4:
            continue
        if descend:
            before = sum(1 for x in (a, b, c, d) if len(A[x]) < 4)
            after = sum(1 for x, dg in ((a, len(A[a]) - 1), (b, len(A[b]) - 1), (c, len(A[c]) + 1),
                                        (d, len(A[d]) + 1)) if dg < 4)
            if after > before:
                continue
        else:
            if len(A[a]) < 5 or len(A[b]) < 5:
                continue
        faces = flip_edge(faces, a, b, c, d)
        A[a].discard(b)
        A[b].discard(a)
        A[c].add(d)
        A[d].add(c)
    return faces


def random_colouring(rng, faces, v):
    """random proper 4-colouring of T-v by randomised DFS (None if the search fails)."""
    A = adj_of(faces)
    verts = [u for u in sorted(A) if u != v]
    order = verts[:]
    rng.shuffle(order)
    col = {}
    budget = [20000]

    def dfs(i):
        if i == len(order):
            return True
        budget[0] -= 1
        if budget[0] < 0:
            return False
        u = order[i]
        cs = [c for c in range(4) if all(col.get(w) != c for w in A[u] if w != v)]
        rng.shuffle(cs)
        for c in cs:
            col[u] = c
            if dfs(i + 1):
                return True
            del col[u]
        return False

    return dict(col) if dfs(0) else None


def kempe_random(rng, H, st, k):
    """k random Kempe swaps; yields every intermediate colouring list."""
    col = list(st)
    for _ in range(k):
        u = rng.randrange(H.N)
        c1 = col[u]
        c2 = rng.choice([c for c in range(4) if c != c1])
        K = H.comp(col, u, c1, c2)
        for w in K:
            col[w] = c2 if col[w] == c1 else c1
        yield col


def init_state(rng, nlo=NLO, nhi=NHI):
    """start state: min degree >= 4, v of degree 5, doubly locked.  Returns (faces, v, colouring dict)."""
    while True:
        n = rng.randint(nlo, nhi)
        faces = random_stacked(rng, n)
        faces = random_flips(rng, faces, 60 * n, descend=True)
        faces = random_flips(rng, faces, 8 * n)
        A = adj_of(faces)
        if min(len(x) for x in A.values()) < 4:
            continue
        v5 = sorted(u for u in A if len(A[u]) == 5)
        if not v5:
            continue
        v = rng.choice(v5)
        col = random_colouring(rng, faces, v)
        if col is None:
            continue
        H = R.Hole(faces, v)
        base = [col[u] for u in H.labels]
        if H.is_dl(base):
            return faces, v, col
        for cur in kempe_random(rng, H, base, 200):
            if H.is_dl(cur):
                return faces, v, {u: cur[i] for i, u in enumerate(H.labels)}


# ---------------------------------------------------------------------------------------- moves
def move(rng, faces, v, col):
    """one move; returns (faces, col) or None when the sampled move is illegal."""
    if rng.random() < P_KEMPE:
        A = adj_of(faces)
        adj = {x: [w for w in A[x] if w != v] for x in A if x != v}
        u = rng.choice(sorted(adj))
        c1 = col[u]
        c2 = rng.choice([c for c in range(4) if c != c1])
        seen = {u}
        stack = [u]
        while stack:
            x = stack.pop()
            for w in adj[x]:
                if w not in seen and col[w] in (c1, c2):
                    seen.add(w)
                    stack.append(w)
        new = dict(col)
        for w in seen:
            new[w] = c2 if col[w] == c1 else c1
        return faces, new
    A = adj_of(faces)
    t = rng.choice(sorted(faces))
    a, b, c = t
    if rng.random() < 0.5:
        a, b, c = b, c, a
    d = other_face_vertex(faces, a, b)
    if d is None or d == c or v in (a, b, c, d) or d in A[c] or col[c] == col[d]:
        return None
    if len(A[a]) < 5 or len(A[b]) < 5:
        return None
    return flip_edge(faces, a, b, c, d), col


# ---------------------------------------------------------------------------------------- objective
class Evaluator:
    def __init__(self, deadline, target=None):
        self.deadline = deadline
        self.target = target          # planted-fault tests only: a callable H -> predicate on canonical states replacing 'filled'
        self.deep_used = 0
        self.unresolved = 0
        self.deep_log = []

    def evaluate(self, faces, v, col):
        """returns (score (r, ball) or None if not doubly locked, info dict)."""
        H = R.Hole(faces, v)
        base = [col[u] for u in H.labels]
        if len(H.link) != 5 or not H.is_dl(base):
            return None, None
        s0 = R.canon(base)
        info = H.bfs(s0, target=(self.target(H) if self.target else None), max_depth=R.S2A_DEPTH, cap=R.S2A_CAP)
        st = info["status"]
        if st == "found":
            return (info["radius"], info["ball"]), info
        if st == "closed":
            return (10 ** 6, info["ball"]), info          # targetless, exhaustively enumerated: KILL-2
        self.unresolved += 1
        score = (UNRESOLVED_R, info["ball"])
        if self.deep_used < DEEP_MAX and (self.deadline is None or time.process_time() < self.deadline):
            self.deep_used += 1
            deep = H.bfs(s0, target=(self.target(H) if self.target else None), cap=R.DEEP_CAP, deadline=self.deadline)
            self.deep_log.append({"deep_status": deep["status"], "radius": deep.get("radius"),
                                  "explored": deep["explored"]})
            if deep["status"] == "found":
                score = (deep["radius"], deep["ball"])
                info = dict(deep)
            elif deep["status"] == "closed":
                return (10 ** 6, deep["ball"]), deep
            else:
                info = dict(info, deep_status=deep["status"])
        return score, info


def cert_of(faces, v, col, claim):
    H = R.Hole(faces, v)
    return R.make_cert(H, R.canon([col[u] for u in H.labels]), claim)


# ---------------------------------------------------------------------------------------- the search
def search_tag(tag, cpu_cap=120.0, max_steps=None, stall=STALL, nlo=NLO, nhi=NHI, target_factory=None):
    """S2a for one tag.  Returns the deterministic result dict (no timing); the CPU seconds are in 'cpu' only if
    the caller asks (see run_tag)."""
    rng = random.Random("wp22|s2a|" + tag)
    t0 = time.process_time()
    deadline = t0 + cpu_cap if cpu_cap is not None else None
    ev = Evaluator(deadline)
    if target_factory is not None:
        ev.target = target_factory
    steps = 0
    evals = 0
    restarts = 0
    best = None                       # (score, faces, v, col, info)
    per_restart = []
    hist = {}
    kills = []
    stop = None

    def out_of_budget():
        if max_steps is not None and steps >= max_steps:
            return "max_steps"
        if deadline is not None and time.process_time() >= deadline:
            return "cpu_cap"
        return None

    while stop is None and not kills:
        faces, v, col = init_state(rng, nlo, nhi)
        score, info = ev.evaluate(faces, v, col)
        order = len(adj_of(faces))
        evals += 1
        since = 0
        rbest = score
        restarts += 1
        if score[0] >= 10 ** 6:
            kills.append(cert_of(faces, v, col, {"radius": None, "class_closed_no_filled": True,
                                                  "class_size": info["ball"]}))
            break
        hist[str(score[0])] = hist.get(str(score[0]), 0) + 1
        if best is None or score > best[0]:
            best = (score, faces, v, dict(col), info)
        while since < stall:
            stop = out_of_budget()
            if stop:
                break
            steps += 1
            mv = move(rng, faces, v, col)
            if mv is None:
                since += 1
                continue
            nf, nc = mv
            sc2, info2 = ev.evaluate(nf, v, nc)
            if sc2 is None:
                since += 1
                continue
            evals += 1
            hist[str(sc2[0])] = hist.get(str(sc2[0]), 0) + 1
            if sc2[0] >= 10 ** 6:
                kills.append(cert_of(nf, v, nc, {"radius": None, "class_closed_no_filled": True,
                                                  "class_size": info2["ball"]}))
                break
            if sc2 >= score:
                since = 0 if sc2 > score else since + 1
                faces, col, score, info = nf, nc, sc2, info2
                if score > rbest:
                    rbest = score
                if best is None or score > best[0]:
                    best = (score, faces, v, dict(col), info)
            else:
                since += 1
        per_restart.append([rbest[0], rbest[1], order])
    res = {"tag": tag, "seed": "wp22|s2a|" + tag, "steps": steps, "evals": evals, "restarts": restarts,
           "stopped": "kill" if kills else stop, "capped": (stop == "cpu_cap"),
           "unresolved_evals": ev.unresolved, "deep_followups": ev.deep_log,
           "r_hist": dict(sorted(hist.items(), key=lambda kv: int(kv[0]))),
           "per_restart_best": per_restart, "kill2": kills}
    if best is not None:
        sc, faces, v, col, info = best
        res["best"] = {"r": sc[0], "ball": sc[1], "order": len(adj_of(faces)), "status": info["status"],
                       "cert": cert_of(faces, v, col, {"radius": sc[0] if info["status"] == "found" else None,
                                                       "at_least": sc[0], "status": info["status"]})}
    return res


def run_tag(tag, cpu_cap=120.0, max_steps=None):
    """returns (result, cpu seconds)."""
    t = time.process_time()
    res = search_tag(tag, cpu_cap, max_steps)
    return res, time.process_time() - t


def dumps(res):
    return json.dumps(res, sort_keys=True, separators=(",", ":"))


def tags():
    return ["t%03d" % i for i in range(1, 41)]


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("tag")
    ap.add_argument("--cpu", type=float, default=120.0)
    ap.add_argument("--max-steps", type=int, default=None)
    a = ap.parse_args()
    r, cpu = run_tag(a.tag, a.cpu, a.max_steps)
    print(dumps(r))
    print("cpu %.1f" % cpu, file=sys.stderr)
