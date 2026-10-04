"""Generate docs/deadend/data.js: the dead-end region of order 17, graph 3.

Reuses trap_demo_data.py for per-root states, landscape data and the planar drawing.  Adds,
per root: the dead-end region (states with no strictly decreasing two-swap path to a target),
its one-swap neighbourhood with a deterministic spring layout for the network view, the WP7c
pattern of every region state, and replays of the math team's frozen breadcrumb policy
(breadcrumb-v1-global-min-depth3-canonical-lex) as event logs.  Every replay is asserted to
reproduce the warnings and target recorded in breadcrumb-warning-traces.json.
"""
import hashlib
import json
import math
import random
from pathlib import Path

from mass_core import FIXTURES, degree_five, parse_ascii
from trap_demo_data import relax, root_data, tutte
from wp7c_test import pattern

OUT = Path(__file__).resolve().parents[3] / "docs" / "deadend" / "data.js"
ORDER, GRAPH, FOCUS = 17, 3, 3


def two_ball(nxt, i):
    return set(nxt[i]) | {u for x in nxt[i] for u in nxt[x]}


def replay(states, start):
    """Frozen breadcrumb policy; returns the event log, warnings and target index."""
    R = [s["R"] for s in states]
    nxt = [s["next"] for s in states]
    warned, stack, events = [], [start], []
    while states[stack[-1]]["p"] == 1:
        c = stack[-1]
        cands = [j for j in two_ball(nxt, c) if R[j] < R[c] and j not in warned]
        if cands:
            j = min(cands, key=lambda j: (R[j], j))
            stack.append(j)
            events.append({"t": "move", "to": j})
            continue
        warned.append(c)
        events.append({"t": "warn", "at": c})
        if len(stack) > 1:
            stack.pop()
            events.append({"t": "back", "to": stack[-1]})
            continue
        ball, level = {c}, [c]
        for _ in range(3):
            level = [y for x in level for y in nxt[x] if y not in ball and not ball.add(y)]
        cands = [j for j in ball if R[j] < R[c] and j not in warned]
        j = min(cands, key=lambda j: (R[j], j))
        stack = [j]
        events.append({"t": "wave2", "to": j})
    return events, warned, stack[-1]


def spring(nodes, edges, seed=3):
    rng = random.Random(seed)
    pos = {v: [rng.uniform(-1, 1), rng.uniform(-1, 1)] for v in nodes}
    for it in range(900):
        step = 0.05 * (1 - it / 900) + 0.002
        force = {v: [0.0, 0.0] for v in nodes}
        for a in nodes:
            for b in nodes:
                if a < b:
                    dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
                    d2 = dx * dx + dy * dy + 1e-4
                    f = 0.03 / d2
                    force[a][0] += f * dx; force[a][1] += f * dy
                    force[b][0] -= f * dx; force[b][1] -= f * dy
        for a, b, w in edges:
            dx, dy = pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]
            d = math.hypot(dx, dy) + 1e-9
            f = w * (d - 0.35)
            force[a][0] += f * dx / d; force[a][1] += f * dy / d
            force[b][0] -= f * dx / d; force[b][1] -= f * dy / d
        for v in nodes:
            fx, fy = force[v]
            n = math.hypot(fx, fy) + 1e-9
            pos[v][0] += step * fx / n * min(1, n)
            pos[v][1] += step * fy / n * min(1, n)
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    sc = 2 / max(max(xs) - min(xs), max(ys) - min(ys), 1e-9)
    return {v: [round((p[0] - cx) * sc, 4), round((p[1] - cy) * sc, 4)] for v, p in pos.items()}


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    g = next(g for o in table["orders"] if o["order"] == ORDER for g in o["graphs_checked"] if g["graph_index"] == GRAPH)
    rot = parse_ascii(g["ascii"])
    pos, outer = tutte(rot, FOCUS)
    pos = relax(rot, pos, outer)
    traces_path = FIXTURES / "breadcrumb-warning-traces.json"
    traces = json.loads(traces_path.read_text())
    roots = {}
    for r in degree_five(rot):
        d = root_data(rot, r)
        st = d["states"]
        published = next(x for x in g["roots"] if x["root"] == r)
        assert d["pass"] == (published["outcome"] == "passes")
        region = [i for i, s in enumerate(st) if not s["descends"]]
        ring = sorted({j for i in region for j in st[i]["next"]} - set(region))
        d["region"] = region
        d["ring"] = ring
        if region:
            nodes = region + ring
            edges = [(a, b, 1.6 if (a in region and b in region) else 0.6)
                     for a in nodes for b in st[a]["next"] if b in nodes and a < b]
            d["net"] = {str(k): v for k, v in spring(nodes, edges).items()}
            index = {tuple(s["c"]): i for i, s in enumerate(st)}
            pats = {}
            for i in region:
                p = json.dumps(pattern(rot, r, d["V"], list(rot[r]), st[i]["c"]))
                pats.setdefault(p, []).append(i)
            d["patternGroups"] = sorted(pats.values())
            row = next(x for x in traces["rows"] if (x["order"], x["graph_index"], x["root"]) == (ORDER, GRAPH, r))
            runs = []
            for run in row["runs"]:
                if not run["warnings"]:
                    continue
                start = index[tuple(run["start"]["coloring"])]
                events, warned, end = replay(st, start)
                assert {tuple(st[i]["c"]) for i in warned} == {tuple(w["coloring"]) for w in run["warnings"]}
                assert tuple(st[end]["c"]) == tuple(run["target"]["coloring"])
                runs.append({"start": start, "events": events, "warnings": warned, "end": end})
            d["runs"] = runs
        roots[str(r)] = d
    data = {"ascii": g["ascii"], "order": ORDER, "graph_index": GRAPH, "rot": rot, "pos": pos, "outer": outer,
            "focus": FOCUS, "roots": roots,
            "inputs": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (FIXTURES / "mass-macro-results.json", traces_path)}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("// Generated by backgroundMaterial/planemap-structural/longtable/deadend_demo_data.py. Do not edit.\n"
                   "window.DEADEND_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n")
    print("wrote", OUT, OUT.stat().st_size, "bytes")
    for r, d in roots.items():
        if d["region"]:
            print(r, "region", d["region"], "ring", len(d["ring"]), "pattern groups", d["patternGroups"],
                  "replayed runs", len(d["runs"]), "warnings per run", sorted({len(x["warnings"]) for x in d["runs"]}))


if __name__ == "__main__":
    main()
