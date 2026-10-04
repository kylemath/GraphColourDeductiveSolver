"""Generate docs/trap/data.js for the interactive trap demo (order 17, graph 0).

Everything shown on the page comes from mass_core.py, the implementation that reproduced the
published corpus results.  Per root: every deletion colouring (canonical form), p, q, R, linear
mass, full-state target distance (diagnostic only), Kempe move adjacency, one- and two-swap
stuck flags for the published rank and the lin variant, and whether the state can descend
to a target along a strictly decreasing two-swap path (the input-avoidance check).  Also a
straight-line Tutte drawing of the triangulation and the minimal-barrier escape from each
two-swap trap.
"""
import heapq
import json
import math
from collections import deque
from pathlib import Path

from broaden_variants import components
from mass_core import FIXTURES, RootState, degree_five, parse_ascii

OUT = Path(__file__).resolve().parents[3] / "docs" / "trap" / "data.js"


def faces(rot):
    seen, out = set(), []
    for v, ns in enumerate(rot):
        for w in ns:
            if (v, w) in seen:
                continue
            f, d = [], (v, w)
            while d not in seen:
                seen.add(d)
                f.append(d[0])
                a, b = d
                d = (b, rot[b][(rot[b].index(a) + 1) % len(rot[b])])
            out.append(f)
    return out


def tutte(rot, focus):
    """Barycentric drawing with the outer face chosen as far as possible from `focus`."""
    dist = {focus: 0}
    q = deque([focus])
    while q:
        v = q.popleft()
        for w in rot[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                q.append(w)
    outer = max(faces(rot), key=lambda f: (sum(dist[v] for v in f), -min(f)))
    pos = {v: [0.0, 0.0] for v in range(len(rot))}
    for k, v in enumerate(outer):
        a = math.pi / 2 + 2 * math.pi * k / 3
        pos[v] = [math.cos(a), -math.sin(a)]
    for _ in range(4000):
        for v in range(len(rot)):
            if v in outer:
                continue
            pos[v] = [sum(pos[w][0] for w in rot[v]) / len(rot[v]), sum(pos[w][1] for w in rot[v]) / len(rot[v])]
    return [[round(x, 4) for x in pos[v]] for v in range(len(rot))], outer


def _cross(p1, p2, p3, p4):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = orient(p3, p4, p1), orient(p3, p4, p2)
    d3, d4 = orient(p1, p2, p3), orient(p1, p2, p4)
    return d1 * d2 < 0 and d3 * d4 < 0


def relax(rot, pos, outer, rounds=600):
    """Spring relaxation that only accepts moves keeping the straight-line drawing planar."""
    import random
    rng = random.Random(17)
    edges = [(v, w) for v in range(len(rot)) for w in rot[v] if v < w]
    P = [list(p) for p in pos]

    def ok(v):
        for (a, b) in edges:
            if v not in (a, b):
                continue
            for (c, d) in edges:
                if len({a, b, c, d}) == 4 and _cross(P[a], P[b], P[c], P[d]):
                    return False
        return True

    for it in range(rounds):
        step = 0.06 * (1 - it / rounds) + 0.004
        for v in rng.sample(range(len(rot)), len(rot)):
            if v in outer:
                continue
            fx = fy = 0.0
            for w in range(len(rot)):
                if w == v:
                    continue
                dx, dy = P[v][0] - P[w][0], P[v][1] - P[w][1]
                d2 = dx * dx + dy * dy + 1e-6
                fx += 0.02 * dx / d2
                fy += 0.02 * dy / d2
            for w in rot[v]:
                dx, dy = P[w][0] - P[v][0], P[w][1] - P[v][1]
                d = math.hypot(dx, dy) + 1e-9
                fx += (d - 0.55) * dx / d
                fy += (d - 0.55) * dy / d
            norm = math.hypot(fx, fy) + 1e-9
            old = P[v][:]
            P[v] = [old[0] + step * fx / norm, old[1] + step * fy / norm]
            if math.hypot(*P[v]) > 0.97 or not ok(v):
                P[v] = old
    return [[round(x, 4) for x in p] for p in P]


def root_data(rot, r):
    s = RootState(rot, r)
    n = len(s.C)
    nxt = [sorted({t for _, _, t in s.info[i]["moves"]} - {i}) for i in range(n)]
    dist = {i: 0 for i in range(n) if s.info[i]["p"] == 0}
    q = deque(dist)
    while q:
        x = q.popleft()
        for y in nxt[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    R = [s.info[i]["R"] for i in range(n)]
    lin = []
    for i in range(n):
        comps = components(s, s.C[i])
        lin.append((s.info[i]["p"], sum(len(K - s.Bset) for _, K in comps if K & s.Bset)))

    def stuck(rank, i):
        if rank[i][0] != 1:
            return False
        two = set(nxt[i]) | {u for t in nxt[i] for u in nxt[t]}
        return not any(rank[j] < rank[i] for j in two)

    good = {}
    for i in sorted(range(n), key=lambda i: R[i]):
        if s.info[i]["p"] == 0:
            good[i] = True
            continue
        two = set(nxt[i]) | {u for t in nxt[i] for u in nxt[t]}
        good[i] = any(R[j] < R[i] and good[j] for j in two)
    states = []
    for i in range(n):
        states.append({"c": list(s.C[i]), "p": s.info[i]["p"], "q": s.info[i]["q"], "R": R[i], "lin": lin[i][1],
                       "d": dist[i], "next": nxt[i],
                       "stuck1": s.info[i]["p"] == 1 and s.descent(i, 1) is not None,
                       "stuck2": s.info[i]["p"] == 1 and s.descent(i, 2) is not None,
                       "stuck2lin": s.info[i]["p"] == 1 and stuck(lin, i),
                       "descends": good[i]})
    traps = [i for i, st in enumerate(states) if st["stuck2"]]
    escapes = {}
    for t in traps:
        best, heap, prev, end = {t: (R[t], 0)}, [(R[t], 0, t)], {}, None
        while heap:
            m, d, x = heapq.heappop(heap)
            if R[x] < R[t]:
                end = x
                break
            for y in nxt[x]:
                key = (max(m, R[y]), d + 1)
                if key < best.get(y, (1 << 60, 0)):
                    best[y] = key
                    prev[y] = x
                    heapq.heappush(heap, (*key, y))
        path, x = [end], end
        while x != t:
            x = prev[x]
            path.append(x)
        path.reverse()
        # continue greedily (strict two-swap descent) from the landing state to a target
        # then descend: prefer a single downhill swap, else a two-swap macro, always into states that descend
        x = end
        while states[x]["p"] == 1:
            one = [(R[y], y) for y in nxt[x] if R[y] < R[x] and good[y]]
            if one:
                path.append(min(one)[1])
            else:
                _, y, j = min((R[j], y, j) for y in nxt[x] for j in nxt[y] if R[j] < R[x] and good[j])
                path += [y, j]
            x = path[-1]
        escapes[t] = {"path": path, "barrier": best[end][0] - R[t]}
    return {"root": r, "V": s.V, "B": list(rot[r]), "states": states, "traps": traps,
            "escapes": {str(k): v for k, v in escapes.items()},
            "maxd": max(dist.values()), "pass": not traps, "passLin": not any(st["stuck2lin"] for st in states),
            "scale": s.scale}


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    g = next(g for o in table["orders"] if o["order"] == 17 for g in o["graphs_checked"] if g["graph_index"] == 0)
    rot = parse_ascii(g["ascii"])
    pos, outer = tutte(rot, 4)
    pos = relax(rot, pos, outer)
    roots = {}
    for r in degree_five(rot):
        roots[str(r)] = root_data(rot, r)
        published = next(x for x in g["roots"] if x["root"] == r)
        assert roots[str(r)]["pass"] == (published["outcome"] == "passes")
        assert len(roots[str(r)]["states"]) == published["coloring_orbits"]
    data = {"ascii": g["ascii"], "order": 17, "graph_index": 0, "rot": rot, "pos": pos, "outer": outer,
            "roots": roots,
            "linkReward": "Rewarding boundary-linking chains (q - k*links, k = 5..80) left the stuck counts at roots 4, 6, 9, 14 unchanged."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("// Generated by backgroundMaterial/planemap-structural/longtable/trap_demo_data.py. Do not edit.\n"
                   "window.TRAP_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n")
    print("wrote", OUT, OUT.stat().st_size, "bytes")
    for r, d in roots.items():
        print(r, "pass" if d["pass"] else "FAIL", "lin pass" if d["passLin"] else "lin FAIL", "maxd", d["maxd"],
              "traps", d["traps"], {k: (v["path"], v["barrier"]) for k, v in d["escapes"].items()})


if __name__ == "__main__":
    main()
