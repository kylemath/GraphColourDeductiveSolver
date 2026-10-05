"""EXPLORATORY (not a declared WP, not evidence). Long Table, 2026-10-05.

Plausibility reading for VH_C (face-avoiding hypothesis), page:
SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/interface/face-avoiding-reduction.md

Generates 4-connected spherical triangulations T with a face phi such that every
vertex off phi has degree >= 5 (the class C), by random edge flips with a simple
annealed score. No plantri. Orders kept small and outside the spent holdouts 19-24.

For each (T, phi):
  pure test : is there a degree-5 vertex v off phi and a legal fan tau such that every
              start (colouring of T-v proper on tau) lies in a Kempe class (hole fixed
              at v) that contains a filled state?  Pure fills never move the hole, so
              such a pair is phi-good.
  mixed test: only if the pure test fails; search the mixed move graph restricted to
              holes off V(phi) (BFS over states, uncapped up to a state budget).

Self-contained: imports no team code.
"""
from __future__ import annotations

import itertools
import json
import random
import sys
import time
from collections import deque

HOLE = 4
PAIRS = list(itertools.combinations(range(4), 2))


# ---------------------------------------------------------------- triangulations
def initial_faces(n, rng):
    """Stacked start: K4 then insert vertices into random faces (oriented ccw triples)."""
    faces = {(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 3, 2)}
    for v in range(4, n):
        f = rng.choice(sorted(faces))
        faces.remove(f)
        a, b, c = f
        faces |= {(a, b, v), (b, c, v), (c, a, v)}
    return faces


def norm(f):
    a, b, c = f
    m = min(f)
    while f[0] != m:
        f = (f[1], f[2], f[0])
    return f


def edge_face_map(faces):
    m = {}
    for f in faces:
        a, b, c = f
        m[(a, b)] = c
        m[(b, c)] = a
        m[(c, a)] = b
    return m


def adjacency(faces, n):
    adj = [set() for _ in range(n)]
    for a, b, c in faces:
        adj[a] |= {b, c}
        adj[b] |= {a, c}
        adj[c] |= {a, b}
    return adj


def rotation(faces, n):
    succ = [dict() for _ in range(n)]
    for a, b, c in faces:
        succ[a][b] = c
        succ[b][c] = a
        succ[c][a] = b
    rot = []
    for v in range(n):
        s = succ[v]
        start = min(s)
        cyc = [start]
        x = s[start]
        while x != start:
            cyc.append(x)
            x = s[x]
        assert len(cyc) == len(s)
        rot.append(cyc)
    return rot


def try_flip(faces, u, v, adj):
    em = edge_face_map(faces)
    if (u, v) not in em or (v, u) not in em:
        return False
    x = em[(u, v)]
    y = em[(v, u)]
    if x == y or y in adj[x] or len(adj[u]) <= 3 or len(adj[v]) <= 3:
        return False
    f1 = norm((u, v, x))
    f2 = norm((v, u, y))
    faces.discard(f1)
    faces.discard(f2)
    faces.add(norm((x, u, y)))
    faces.add(norm((y, v, x)))
    adj[u].discard(v)
    adj[v].discard(u)
    adj[x].add(y)
    adj[y].add(x)
    return True


def separating_triangles(faces, adj):
    fs = {frozenset(f) for f in faces}
    out = []
    n = len(adj)
    for u in range(n):
        for v in adj[u]:
            if v <= u:
                continue
            for w in adj[u] & adj[v]:
                if w <= v:
                    continue
                if frozenset((u, v, w)) not in fs:
                    out.append((u, v, w))
    return out


def best_face(faces, adj):
    low = {v for v in range(len(adj)) if len(adj[v]) < 5}
    best, bc = None, -1
    for f in faces:
        c = sum(1 for x in f if x in low)
        if c > bc:
            best, bc = f, c
    return best, len(low) - bc, low


def score(faces, adj, target_low=None):
    d = [len(a) for a in adj]
    deficit = [max(0, 5 - x) for x in d]
    tot = sum(deficit)
    best_off = min(tot - sum(deficit[x] for x in f) for f in faces)
    deg3 = sum(max(0, 4 - x) for x in d)
    sep = len(separating_triangles(faces, adj))
    pen = 0 if target_low is None else abs(sum(1 for x in d if x < 5) - target_low)
    return 3 * best_off + 3 * deg3 + sep + 2 * pen


def generate(n, rng, steps=20000, target_low=None):
    faces = {norm(f) for f in initial_faces(n, rng)}
    adj = adjacency(faces, n)
    cur = score(faces, adj, target_low)
    temp = 2.0
    for it in range(steps):
        if cur == 0:
            return faces
        e = rng.choice(sorted(faces))
        i = rng.randrange(3)
        u, v = e[i], e[(i + 1) % 3]
        saved = (set(faces), [set(a) for a in adj])
        if not try_flip(faces, u, v, adj):
            continue
        new = score(faces, adj, target_low)
        if new <= cur or rng.random() < pow(2.718, (cur - new) / temp):
            cur = new
        else:
            faces, adj = saved
        temp = max(0.05, temp * 0.9997)
    return None


# ---------------------------------------------------------------- colourings, moves
def canon(state):
    seen = {}
    out = []
    for x in state:
        if x == HOLE:
            out.append(HOLE)
        else:
            out.append(seen.setdefault(x, len(seen)))
    return tuple(out)


def deletion_states(rot, v):
    n = len(rot)
    order = [u for u in range(n) if u != v]
    pos = {u: i for i, u in enumerate(order)}
    earlier = [[pos[w] for w in rot[u] if w != v and pos[w] < i] for i, u in enumerate(order)]
    cur = [0] * len(order)
    out = []

    def go(i, top):
        if i == len(order):
            st = [HOLE] * n
            for j, u in enumerate(order):
                st[u] = cur[j]
            out.append(tuple(st))
            return
        blocked = {cur[j] for j in earlier[i]}
        for a in range(min(3, top + 1) + 1):
            if a not in blocked:
                cur[i] = a
                go(i + 1, max(top, a))

    go(0, -1)
    return out


def filled(rot, st):
    h = st.index(HOLE)
    return len({st[w] for w in rot[h]}) <= 3


def kempe_moves(rot, st):
    for a, b in PAIRS:
        seen = set()
        for s, col in enumerate(st):
            if col not in (a, b) or s in seen:
                continue
            comp = {s}
            stack = [s]
            while stack:
                x = stack.pop()
                for y in rot[x]:
                    if y not in comp and st[y] in (a, b):
                        comp.add(y)
                        stack.append(y)
            seen |= comp
            nxt = list(st)
            for x in comp:
                nxt[x] = b if st[x] == a else a
            yield canon(nxt)


def slide_moves(rot, st, forbidden):
    h = st.index(HOLE)
    cols = [st[w] for w in rot[h]]
    for u in rot[h]:
        if u in forbidden:
            continue
        if cols.count(st[u]) == 1:
            nxt = list(st)
            nxt[h] = st[u]
            nxt[u] = HOLE
            yield canon(nxt)


def legal_fans(rot, v, adj):
    link = rot[v]
    fans = []
    for i in range(5):
        a, far, near = link[i], link[(i + 2) % 5], link[(i + 3) % 5]
        if far in adj[a] or near in adj[a]:
            continue
        fans.append((i, (a, far), (a, near)))
    return fans


def pure_good_fans(rot, adj, v):
    """Fans at v for which every start's Kempe class (hole v) contains a filled state."""
    states = deletion_states(rot, v)
    comp = {}
    good_comp = {}
    cid = 0
    for s in states:
        if s in comp:
            continue
        q = deque([s])
        comp[s] = cid
        has_fill = False
        while q:
            x = q.popleft()
            if not has_fill and filled(rot, x):
                has_fill = True
            for y in kempe_moves(rot, x):
                if y not in comp:
                    comp[y] = cid
                    q.append(y)
        good_comp[cid] = has_fill
        cid += 1
    out = []
    for fan in legal_fans(rot, v, adj):
        _, (a, b), (c, d) = fan
        ok = all(good_comp[comp[s]] for s in states if s[a] != s[b] and s[c] != s[d])
        if ok:
            out.append(fan[0])
    return out, len(states)


def mixed_good_fans(rot, adj, v, forbidden, budget=400000):
    states = deletion_states(rot, v)
    reach = {}
    out = []
    for fan in legal_fans(rot, v, adj):
        _, (a, b), (c, d) = fan
        ok = True
        for s in states:
            if not (s[a] != s[b] and s[c] != s[d]):
                continue
            if s in reach:
                if not reach[s]:
                    ok = False
                    break
                continue
            seen = {s}
            q = deque([s])
            found = False
            while q and len(seen) < budget:
                x = q.popleft()
                if filled(rot, x):
                    found = True
                    break
                for y in itertools.chain(kempe_moves(rot, x), slide_moves(rot, x, forbidden)):
                    if y not in seen:
                        seen.add(y)
                        q.append(y)
            if not found and len(seen) >= budget:
                found = None  # inconclusive
            for x in seen:
                if found:
                    reach[x] = True
            reach[s] = found
            if not found:
                ok = False if found is False else None
                break
        out.append((fan[0], ok))
    return out


def invariant(adj):
    degs = [len(a) for a in adj]
    return tuple(sorted((degs[v], tuple(sorted(degs[w] for w in adj[v]))) for v in range(len(adj))))


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    orders = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [10, 11, 12, 13, 14]
    tries = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    rng = random.Random(seed)
    results = []
    seen_inv = set()
    t0 = time.time()
    for n in orders:
        for t in range(tries):
            for target in (3, 2, 1, 0):
                faces = generate(n, rng, target_low=target)
                if faces is None:
                    continue
                adj = adjacency(faces, n)
                inv = invariant(adj)
                if (inv, target) in seen_inv:
                    continue
                seen_inv.add((inv, target))
                rot = rotation(faces, n)
                low = sorted(v for v in range(n) if len(adj[v]) < 5)
                phis = [f for f in sorted(faces) if set(low) <= set(f)]
                deg5 = [v for v in range(n) if len(adj[v]) == 5]
                pure = {}
                for v in deg5:
                    pure[v], _ = pure_good_fans(rot, adj, v)
                pure_vertices = {v for v in deg5 if pure[v]}
                for phi in phis:
                    off = pure_vertices - set(phi)
                    rec = {
                        "n": n, "low": low, "degs": [len(a) for a in adj],
                        "phi": list(phi), "pure_good_off_phi": sorted(off),
                        "deg5_off_phi": sorted(set(deg5) - set(phi)),
                        "faces": [list(f) for f in sorted(faces)],
                    }
                    if not off:
                        mixed = {}
                        for v in sorted(set(deg5) - set(phi)):
                            mixed[v] = mixed_good_fans(rot, adj, v, set(phi))
                        rec["mixed"] = {str(k): v for k, v in mixed.items()}
                        rec["verdict"] = (
                            "mixed-pass" if any(ok for fans in mixed.values() for _, ok in fans if ok)
                            else "FAIL-or-inconclusive")
                    else:
                        rec["verdict"] = "pure-pass"
                    results.append(rec)
                print(n, target, len(low), "phis", len(phis), "pure-good deg5", len(pure_vertices),
                      "of", len(deg5), [r["verdict"] for r in results[-len(phis):]] if phis else "-",
                      f"{time.time()-t0:.0f}s", flush=True)
    json.dump(results, open(f"vhphi-explore-seed{seed}.json", "w"))
    v = [r["verdict"] for r in results]
    print("SUMMARY", {k: v.count(k) for k in set(v)})


if __name__ == "__main__":
    main()
