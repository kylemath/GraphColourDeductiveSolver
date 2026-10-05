"""EXPLORATORY (not a declared WP, not evidence). Long Table, 2026-10-05.

Quadrilateral-face game for VH^4 (page: interface/four-cycle-reduction.md).
Members: take a generated class-C triangulation, delete an edge st so that its two faces
merge into a 4-face phi containing every vertex of degree < 5 (degrees read after deletion).

Pure game at a fixed hole v (deg 5, off phi, legal fan): the player picks a Kempe swap of a
component K of (G-v)[a,b]. If K meets phi and a second {a,b}-component K' meets phi, the
adversary chooses whether K' is swapped as well. The player wins on a state whose link uses
<= 3 colours. Attractor computed on the closure of the starts under all outcomes.
A pair passes if every start (colouring of G-v proper on the fan chords) is winning.
"""
from __future__ import annotations

import itertools
import json
import random
import sys
import time

import vhphi_explore as E

PAIRS = E.PAIRS


def outcomes(adj, st, phi):
    """Yield, per player move, the list of possible successor states."""
    n = len(st)
    for a, b in PAIRS:
        seen = set()
        comps = []
        for s in range(n):
            if st[s] not in (a, b) or s in seen:
                continue
            comp = {s}
            stack = [s]
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if y not in comp and st[y] in (a, b):
                        comp.add(y)
                        stack.append(y)
            seen |= comp
            comps.append(comp)
        meeting = [c for c in comps if c & phi]
        for comp in comps:
            sets = [comp]
            if comp & phi and len(meeting) == 2:
                other = meeting[0] if meeting[1] is comp else meeting[1]
                sets.append(comp | other)
            res = []
            for S in sets:
                nxt = list(st)
                for x in S:
                    nxt[x] = b if st[x] == a else a
                res.append(E.canon(nxt))
            yield res


def filled_adj(adj, st, v):
    return len({st[w] for w in adj[v]}) <= 3


def pure_game(adj, v, fans, phi):
    n = len(adj)
    # colourings of G - v
    rotlike = [sorted(a) for a in adj]
    states = [E.canon(s) for s in E.deletion_states(rotlike, v)]
    states = list(dict.fromkeys(states))
    succ = {}
    for s in states:
        succ[s] = list(outcomes(adj, s, phi))
    win = {s for s in states if filled_adj(adj, s, v)}
    changed = True
    while changed:
        changed = False
        for s in states:
            if s in win:
                continue
            for res in succ[s]:
                if all(r in win for r in res):
                    win.add(s)
                    changed = True
                    break
    out = []
    for i, (p, q), (r, t) in fans:
        ok = all(s in win for s in states if s[p] != s[q] and s[r] != s[t])
        out.append((i, ok))
    return out, len(states)


def legal_fans_adj(rot, v, adj):
    link = rot[v]
    fans = []
    for i in range(5):
        a, far, near = link[i], link[(i + 2) % 5], link[(i + 3) % 5]
        if far in adj[a] or near in adj[a]:
            continue
        fans.append((i, (a, far), (a, near)))
    return fans


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    orders = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [13, 14, 15]
    tries = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    rng = random.Random(seed)
    results = []
    t0 = time.time()
    seen = set()
    for n in orders:
        for t in range(tries):
            for target in (2, 1, 0):
                faces = E.generate(n, rng, target_low=target)
                if faces is None:
                    continue
                adjT = E.adjacency(faces, n)
                inv = E.invariant(adjT)
                if inv in seen:
                    continue
                seen.add(inv)
                rot = E.rotation(faces, n)
                em = E.edge_face_map(faces)
                done = 0
                for s in range(n):
                    for tt in sorted(adjT[s]):
                        if tt <= s or done >= 4:
                            continue
                        x, y = em[(s, tt)], em[(tt, s)]
                        phi = {s, tt, x, y}
                        adj = [set(a) for a in adjT]
                        adj[s].discard(tt)
                        adj[tt].discard(s)
                        if any(len(adj[w]) < 5 for w in range(n) if w not in phi):
                            continue
                        if x in adjT[y]:
                            continue  # chord xy: phi not induced
                        deg5 = [w for w in range(n) if w not in phi and len(adj[w]) == 5]
                        passing = []
                        adv_hurts = []
                        for w in deg5:
                            fans = legal_fans_adj(rot, w, adj)
                            res, _ = pure_game(adj, w, fans, phi)
                            res0, _ = pure_game(adj, w, fans, set())
                            if any(ok for _, ok in res):
                                passing.append(w)
                            for (i, ok), (_, ok0) in zip(res, res0):
                                if ok0 and not ok:
                                    adv_hurts.append([w, i])
                        rec = {"n": n, "phi": sorted(phi), "deleted": [s, tt],
                               "degs": [len(a) for a in adj], "deg5_off": deg5,
                               "pure_game_good": passing, "adversary_hurts": adv_hurts,
                               "verdict": "pass" if passing else "FAIL-pure",
                               "faces": [list(f) for f in sorted(faces)]}
                        results.append(rec)
                        done += 1
                        print(n, target, "phi", sorted(phi), "good", len(passing), "of", len(deg5), "adv-hurts", len(adv_hurts),
                              rec["verdict"], f"{time.time()-t0:.0f}s", flush=True)
    json.dump(results, open(f"vhphi-quad-explore-seed{seed}.json", "w"))
    v = [r["verdict"] for r in results]
    print("SUMMARY", {k: v.count(k) for k in set(v)})


if __name__ == "__main__":
    main()
