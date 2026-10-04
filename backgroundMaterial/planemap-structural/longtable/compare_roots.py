"""Long Table: root 4 (fails) versus root 8 (passes) in order 17, graph 0.

Reproduces every number in LongTableReport3.md section 1: per-root counts, full-state target
distances (diagnostic only, never a rank), escape depth and the minimax barrier of each one-swap
stuck state, the boundary chain structure of the two-swap trap, and the size of its one- and
two-swap neighbourhoods with the variant ranks over them.  Facts only; no status claims.
"""
import hashlib
import heapq
import json
from collections import deque

from broaden_variants import ranks
from mass_core import FIXTURES, HERE, PAIRS, RootState, parse_ascii


def target_distances(s):
    dist = {i: 0 for i, inf in enumerate(s.info) if inf["p"] == 0}
    queue = deque(dist)
    while queue:
        x = queue.popleft()
        for _, _, y in s.info[x]["moves"]:
            if y not in dist:
                dist[y] = dist[x] + 1
                queue.append(y)
    return dist


def escape(s, i):
    """Fewest swaps to a strictly lower R, and least possible peak of R above start on the way."""
    R0 = s.info[i]["R"]
    seen, queue, depth = {i: 0}, deque([i]), None
    while queue:
        x = queue.popleft()
        if s.info[x]["R"] < R0:
            depth = seen[x]
            break
        for _, _, y in s.info[x]["moves"]:
            if y not in seen:
                seen[y] = seen[x] + 1
                queue.append(y)
    best, heap = {i: R0}, [(R0, i)]
    while heap:
        m, x = heapq.heappop(heap)
        if s.info[x]["R"] < R0:
            return depth, m - R0
        for _, _, y in s.info[x]["moves"]:
            mm = max(m, s.info[y]["R"])
            if mm < best.get(y, 1 << 60):
                best[y] = mm
                heapq.heappush(heap, (mm, y))
    return depth, None


def boundary_structure(s, i):
    c = s.C[i]
    col = dict(zip(s.V, c))
    rows = []
    for a, b in PAIRS:
        pending = {j for j, x in enumerate(c) if x in (a, b)}
        while pending:
            seed = min(pending)
            pending.discard(seed)
            comp, stack = {seed}, [seed]
            while stack:
                j = stack.pop()
                for k in s.adj[j]:
                    if k in pending:
                        pending.discard(k)
                        comp.add(k)
                        stack.append(k)
            hit = sorted(s.V[j] for j in comp if j in s.Bset)
            if hit:
                rows.append({"pair": [a, b], "meets_B": hit, "exterior_mass": len(comp) - len(hit),
                             "component": sorted(s.V[j] for j in comp)})
    return {"boundary_cyclic": s.rot[s.r], "boundary_colours": [col[v] for v in s.rot[s.r]], "chains": rows}


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    g = next(g for o in table["orders"] if o["order"] == 17 for g in o["graphs_checked"] if g["graph_index"] == 0)
    rot = parse_ascii(g["ascii"])
    out = {"scope": "Paired diagnostic at order 17 graph 0; target distance is reported, never used as a rank.",
           "inputs": {"mass-macro-results.json": hashlib.sha256((FIXTURES / "mass-macro-results.json").read_bytes()).hexdigest()},
           "roots": {}}
    for r in (4, 8):
        s = RootState(rot, r)
        dist = target_distances(s)
        stuck1 = [i for i, inf in enumerate(s.info) if inf["p"] == 1 and s.descent(i, 1)]
        rows = []
        for i in stuck1:
            depth, barrier = escape(s, i)
            rows.append({"state": i, "coloring": s.C[i], "rank": s.rank(i), "two_swap_stuck": s.descent(i, 2) is not None,
                         "target_distance": dist[i], "escape_depth": depth, "barrier_above_start": barrier})
        out["roots"][r] = {"neighbour_degrees": [len(rot[w]) for w in rot[r]], "orbits": len(s.C),
                           "non_target": sum(inf["p"] == 1 for inf in s.info),
                           "target_distance_histogram": {d: sum(1 for x in dist.values() if x == d) for d in range(max(dist.values()) + 1)},
                           "one_swap_stuck": rows}
        print(f"root {r}: " + "; ".join(f"depth {x['escape_depth']} barrier +{x['barrier_above_start']}"
                                       f"{' (two-swap stuck)' if x['two_swap_stuck'] else ''}" for x in rows))
    s = RootState(rot, 4)
    trap = next(x["state"] for x in out["roots"][4]["one_swap_stuck"] if x["two_swap_stuck"])
    n1 = {t for _, _, t in s.info[trap]["moves"]}
    n2 = {u for t in n1 for _, _, u in s.info[t]["moves"]} - n1 - {trap}
    rk = {i: ranks(s, i) for i in {trap} | n1 | n2}
    dist = target_distances(s)
    out["trap"] = {"state": trap, "structure": boundary_structure(s, trap),
                   "one_swap_states": len(n1), "two_swap_states": len(n2),
                   "target_distance": dist[trap],
                   "one_swap_target_distances": sorted(dist[t] for t in n1),
                   "two_swap_target_distances": sorted(dist[u] for u in n2),
                   "trap_is_minimum_over_two_ball": {v: rk[trap][v] <= min(rk[u][v] for u in n1 | n2)
                                                     for v in ("base", "lock", "lin", "Lallq", "linksq", "linksl")}}
    print("trap", trap, "target distance", dist[trap], "neighbourhood", len(n1), "+", len(n2),
          "minimum over 2-ball:", out["trap"]["trap_is_minimum_over_two_ball"])
    out["checkers"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (HERE / "compare_roots.py", HERE / "broaden_variants.py", HERE / "mass_core.py")}
    (HERE / "compare-roots.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
