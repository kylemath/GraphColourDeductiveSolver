"""Failing-root vacancy-slide subsystem on the published mass-macro table.

Vertices are the two-swap-stuck canonical orbits at published failing roots.
A vacancy slide moves the deleted vertex from the current root to a boundary
vertex of unique colour. Passing roots are forbidden destinations: a slide
that lands on one is recorded and then ignored. Roots outside the six
published mass-failure graphs are never coloured.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from inquiry_slide import colour_view, slide_returns
from mass_core import FIXTURES, RootState, canon, parse_ascii

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "failing-subsystem.json"


def labels_of(state: RootState) -> dict[int, str]:
    """target if p = 0; stuck if no two-swap descent; otherwise descends."""
    labels = {}
    for i, info in enumerate(state.info):
        if info["p"] == 0:
            labels[i] = "target"
        elif state.descent(i, 2) is not None:
            labels[i] = "stuck"
        else:
            labels[i] = "descends"
    return labels


def proper_on_deletion(rot, deleted: int, col: dict[int, int]) -> bool:
    for v, ns in enumerate(rot):
        if v == deleted:
            continue
        for w in ns:
            if w == deleted or w < v:
                continue
            if col[v] == col[w]:
                return False
    return True


def landing_record(rot, failing: set[int], states, labels, deleted: int, col: dict[int, int]) -> dict:
    degree = len(rot[deleted])
    base = {"vertex": deleted, "degree": degree}
    if degree != 5:
        return {**base, "kind": "not_a_root"}
    if deleted not in failing:
        return {**base, "kind": "passing"}
    state = states[deleted]
    colouring = canon(tuple(col[v] for v in state.V))
    if colouring not in state.index:
        raise AssertionError(f"slide to failing root {deleted} is not a canonical orbit")
    idx = state.index[colouring]
    info = state.info[idx]
    return {
        **base,
        "kind": labels[deleted][idx],
        "orbit": idx,
        "p": info["p"],
        "q": info["q"],
        "R": info["R"],
        "coloring": list(colouring),
    }


def apply_slide(col: dict[int, int], deleted: int, x: int) -> dict[int, int]:
    new = dict(col)
    new[deleted] = col[x]
    del new[x]
    return new


def slide_map(rot, state: RootState, i: int, failing, states, labels) -> dict:
    """One-step slides, and two-step slides whose intermediate vertex is not degree 5."""
    col, _boundary, singletons, gap, _d5, locked = colour_view(rot, state, i)
    one = []
    two = []
    for x in singletons:
        back, onward = slide_returns(rot, state.r, col, x)
        new = apply_slide(col, state.r, x)
        if not proper_on_deletion(rot, x, new):
            raise AssertionError(f"improper slide {state.r} -> {x}")
        rec = landing_record(rot, failing, states, labels, x, new)
        rec.update({"from_root": state.r, "via": None, "back": back, "gap": gap, "locked": locked})
        one.append(rec)
        if len(rot[x]) == 5:
            continue
        counts: dict[int, int] = {}
        for vertex in rot[x]:
            counts[new[vertex]] = counts.get(new[vertex], 0) + 1
        onward_seen = []
        for y in rot[x]:
            if len(rot[y]) != 5 or counts[new[y]] != 1:
                continue
            if y != state.r:
                onward_seen.append(y)
            new2 = apply_slide(new, x, y)
            if not proper_on_deletion(rot, y, new2):
                raise AssertionError(f"improper two-step {state.r} -> {x} -> {y}")
            rec2 = landing_record(rot, failing, states, labels, y, new2)
            cancels = y == state.r and canon(tuple(new2[v] for v in state.V)) == state.C[i]
            rec2.update({
                "from_root": state.r,
                "via": x,
                "via_degree": len(rot[x]),
                "returns_to_start": y == state.r,
                "cancels_to_same_orbit": cancels,
            })
            two.append(rec2)
        if sorted(onward_seen) != sorted(onward):
            raise AssertionError(f"onward mismatch at root {state.r}: {onward_seen} vs {onward}")
    return {"one": one, "two": two}


def kempe_maps(rot, state: RootState, i: int, failing, states, labels) -> list[dict]:
    """One Kempe swap at the same root, then the same slide relations."""
    out = []
    seen = set()
    for pair, comp, t in state.info[i]["moves"]:
        key = (pair, comp, t)
        if key in seen:
            continue
        seen.add(key)
        moved = slide_map(rot, state, t, failing, states, labels)
        out.append({
            "pair": list(pair),
            "component": list(comp),
            "neighbor_orbit": t,
            "neighbor_kind": labels[state.r][t],
            "neighbor_p": state.info[t]["p"],
            "neighbor_q": state.info[t]["q"],
            "neighbor_R": state.info[t]["R"],
            "slides": moved,
        })
    return out


def keep_slide(rec: dict, nontrivial_two: bool = False) -> bool:
    if rec["kind"] in ("not_a_root", "passing"):
        return False
    if nontrivial_two and rec.get("cancels_to_same_orbit"):
        return False
    return rec["kind"] in ("stuck", "descends", "target")


def node_key(root: int, orbit: int) -> str:
    return f"{root}:{orbit}"


def condense(nodes: list[str], edges: list[tuple[str, str]]):
    index = {n: i for i, n in enumerate(nodes)}
    adj = [[] for _ in nodes]
    for a, b in edges:
        if a in index and b in index:
            adj[index[a]].append(index[b])
    rev = [[] for _ in nodes]
    for i, ns in enumerate(adj):
        for j in ns:
            rev[j].append(i)
    seen = [False] * len(nodes)
    order = []

    def walk(i):
        seen[i] = True
        for j in adj[i]:
            if not seen[j]:
                walk(j)
        order.append(i)

    for i in range(len(nodes)):
        if not seen[i]:
            walk(i)
    comp = [-1] * len(nodes)
    members: list[list[str]] = []

    def assign(i, k):
        comp[i] = k
        members[k].append(nodes[i])
        for j in rev[i]:
            if comp[j] < 0:
                assign(j, k)

    for i in reversed(order):
        if comp[i] < 0:
            members.append([])
            assign(i, len(members) - 1)
    outgoing = []
    for k in range(len(members)):
        leave = set()
        for n in members[k]:
            for j in adj[index[n]]:
                if comp[j] != k:
                    leave.add(nodes[j])
        outgoing.append(sorted(leave))
    return members, outgoing


def reachable(start: str, adj: dict[str, set[str]]) -> set[str]:
    seen = set()
    stack = [start]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj.get(n, ()))
    return seen


def analyze_graph(order: int, graph_index: int, ascii_line: str, failing: list[int], published: dict) -> dict:
    rot = parse_ascii(ascii_line)
    failing_set = set(failing)
    states = {}
    labels = {}
    for root in failing:
        state = RootState(rot, root)
        state.check_closure()
        states[root] = state
        labels[root] = labels_of(state)
        got = sum(1 for lab in labels[root].values() if lab == "stuck")
        expect = published[root]["two_swap_stuck_orbits"]
        if got != expect:
            raise AssertionError(f"{order}:{graph_index} root {root} stuck {got} != published {expect}")
        witness = tuple(published[root]["failure_witness"]["coloring"])
        if witness not in state.index or labels[root][state.index[witness]] != "stuck":
            raise AssertionError(f"published failure witness at {order}:{graph_index} root {root} is not stuck")

    orbits = []
    for root in failing:
        state = states[root]
        for i, lab in labels[root].items():
            if lab != "stuck":
                continue
            slides = slide_map(rot, state, i, failing_set, states, labels)
            kempe = kempe_maps(rot, state, i, failing_set, states, labels)
            info = state.info[i]
            orbits.append({
                "root": root,
                "orbit": i,
                "p": info["p"],
                "q": info["q"],
                "R": info["R"],
                "vertex_order": list(state.V),
                "coloring": list(state.C[i]),
                "boundary": list(rot[root]),
                "slides": slides,
                "kempe": summarize_kempe(root, i, kempe),
            })

    nodes = [node_key(o["root"], o["orbit"]) for o in orbits]
    by_node = {node_key(o["root"], o["orbit"]): o for o in orbits}

    def destinations(orbit, which: str):
        rows = []
        for rec in orbit["slides"][which]:
            if which == "two" and rec.get("cancels_to_same_orbit"):
                rows.append({"class": "cancel", **{k: rec[k] for k in ("vertex", "via", "kind")}})
                continue
            rows.append({
                "class": rec["kind"],
                "vertex": rec["vertex"],
                "degree": rec["degree"],
                "orbit": rec.get("orbit"),
                "p": rec.get("p"),
                "q": rec.get("q"),
                "via": rec.get("via"),
                "returns_to_start": rec.get("returns_to_start", False),
            })
        return rows

    slide_edges = []
    escape = defaultdict(list)
    passing = defaultdict(list)
    for orbit in orbits:
        src = node_key(orbit["root"], orbit["orbit"])
        for which in ("one", "two"):
            for rec in orbit["slides"][which]:
                if rec["kind"] == "passing":
                    passing[src].append({"length": 1 if which == "one" else 2, "to": rec["vertex"], "via": rec.get("via")})
                elif rec["kind"] == "not_a_root":
                    continue
                elif which == "two" and rec.get("cancels_to_same_orbit"):
                    continue
                elif rec["kind"] == "stuck":
                    dst = node_key(rec["vertex"], rec["orbit"])
                    slide_edges.append((src, dst, which, rec.get("via")))
                elif rec["kind"] in ("descends", "target"):
                    escape[src].append({
                        "length": 1 if which == "one" else 2,
                        "to_root": rec["vertex"],
                        "orbit": rec["orbit"],
                        "kind": rec["kind"],
                        "p": rec["p"],
                        "q": rec["q"],
                        "via": rec.get("via"),
                    })

    simple_edges = []
    seen_e = set()
    for src, dst, which, via in slide_edges:
        key = (src, dst)
        if key not in seen_e:
            seen_e.add(key)
            simple_edges.append(key)

    members, outgoing = condense(nodes, simple_edges)
    adj = defaultdict(set)
    for src, dst in simple_edges:
        adj[src].add(dst)
    success = set()
    for src, rows in escape.items():
        if rows:
            success.add(src)
    # An orbit reaches a descending or target orbit if some stuck orbit reachable
    # from it, including itself, has an escape slide.
    reaches = {}
    for n in nodes:
        blob = reachable(n, adj)
        hits = sorted(blob & success)
        reaches[n] = {
            "stuck_reachable": sorted(blob),
            "escape_from": hits,
            "reaches_descending_or_target": bool(hits),
        }

    kempe_edges = []
    kempe_escape = defaultdict(list)
    kempe_passing = defaultdict(int)
    neighbor_kind_counts = {}
    for orbit in orbits:
        src = node_key(orbit["root"], orbit["orbit"])
        neighbor_kind_counts[src] = orbit["kempe"]["neighbor_kinds"]
        kempe_passing[src] = orbit["kempe"]["passing_landings"]
        for rec in orbit["kempe"]["failing_landings"]:
            if rec["kind"] == "stuck":
                kempe_edges.append((src, node_key(rec["vertex"], rec["orbit"])))
            elif rec["kind"] in ("descends", "target"):
                kempe_escape[src].append(rec)
    kempe_simple = sorted(set(kempe_edges))
    kempe_adj = defaultdict(set)
    for src, dst in kempe_simple:
        kempe_adj[src].add(dst)
    kempe_success = {src for src, rows in kempe_escape.items() if rows}
    kempe_reaches = {}
    for n in nodes:
        blob = reachable(n, kempe_adj)
        hits = sorted(v for v in blob if v in kempe_success)
        # escapes are not nodes; a node reaches one if it or a Kempe-slide descendant has one
        direct = n in kempe_success or any(v in kempe_success for v in blob)
        kempe_reaches[n] = {
            "stuck_reachable": sorted(blob),
            "reaches_descending_or_target": direct,
        }

    # Targets reachable by slides that stay on failing roots, allowing a walk
    # through descending orbits as well as stuck ones. Used only for the OPEN test.
    open_adj = defaultdict(set)
    target_nodes = set()
    for orbit in orbits:
        src = node_key(orbit["root"], orbit["orbit"])
        for which in ("one", "two"):
            for rec in orbit["slides"][which]:
                if rec.get("cancels_to_same_orbit"):
                    continue
                if rec["kind"] == "stuck":
                    open_adj[src].add(node_key(rec["vertex"], rec["orbit"]))
                elif rec["kind"] == "target":
                    target_nodes.add(src)
                elif rec["kind"] == "descends":
                    # continuing from a descending orbit is a different question;
                    # record the landing so OPEN can follow slides from it below.
                    open_adj[src].add(f"descend:{rec['vertex']}:{rec['orbit']}")

    # Slides out of every descending orbit at a failing root, still forbidding passing roots.
    descend_ids = []
    for root in failing:
        state = states[root]
        for i, lab in labels[root].items():
            if lab != "descends":
                continue
            did = f"descend:{root}:{i}"
            descend_ids.append(did)
            slides = slide_map(rot, state, i, failing_set, states, labels)
            for which in ("one", "two"):
                for rec in slides[which]:
                    if rec.get("cancels_to_same_orbit"):
                        continue
                    if rec["kind"] == "stuck":
                        open_adj[did].add(node_key(rec["vertex"], rec["orbit"]))
                    elif rec["kind"] == "descends":
                        open_adj[did].add(f"descend:{rec['vertex']}:{rec['orbit']}")
                    elif rec["kind"] == "target":
                        open_adj[did].add(f"target:{rec['vertex']}:{rec['orbit']}")
                        target_nodes.add(f"target:{rec['vertex']}:{rec['orbit']}")
            if state.info[i]["p"] == 0:
                target_nodes.add(did)

    def reaches_target(start: str) -> bool:
        seen = set()
        stack = [start]
        while stack:
            n = stack.pop()
            if n in seen:
                continue
            seen.add(n)
            if n in target_nodes or n.startswith("target:"):
                return True
            stack.extend(open_adj.get(n, ()))
        return False

    orbit_views = []
    for orbit in orbits:
        src = node_key(orbit["root"], orbit["orbit"])
        orbit_views.append({
            "id": src,
            "root": orbit["root"],
            "orbit": orbit["orbit"],
            "p": orbit["p"],
            "q": orbit["q"],
            "R": orbit["R"],
            "vertex_order": orbit["vertex_order"],
            "coloring": orbit["coloring"],
            "boundary": orbit["boundary"],
            "one_step": destinations(orbit, "one"),
            "two_step": destinations(orbit, "two"),
            "passing": passing[src],
            "escape": escape[src],
            "reaches": reaches[src],
            "reaches_target_on_failing_roots": reaches_target(src),
            "kempe_neighbor_kinds": neighbor_kind_counts[src],
            "kempe_passing_landings": kempe_passing[src],
            "kempe_failing_landings": orbit["kempe"]["failing_landings"],
            "kempe_reaches": kempe_reaches[src],
            "kempe_examples": orbit["kempe"]["examples"],
        })

    terminal = []
    for k, group in enumerate(members):
        group_set = set(group)
        escapes = []
        for n in group:
            escapes.extend(escape[n])
        external_stuck = [n for n in outgoing[k] if n not in group_set]
        terminal.append({
            "members": sorted(group),
            "stuck_edges_leaving": external_stuck,
            "escapes_to_descending_or_target": escapes,
            "dead_end": not external_stuck and not escapes,
        })

    return {
        "order": order,
        "graph_index": graph_index,
        "ascii_sha256": published_sha(published),
        "failing_roots": failing,
        "passing_roots": published["__passing__"],
        "stuck_orbit_count": len(nodes),
        "orbits": orbit_views,
        "stuck_edges": [{"src": a, "dst": b, "how": how, "via": via} for a, b, how, via in slide_edges],
        "terminal_components": terminal,
        "kempe_stuck_edges": [{"src": a, "dst": b} for a, b in kempe_simple],
        "acyclic_ignoring_nothing": not any(a == b or (b, a) in seen_e for a, b in seen_e) and not _has_longer_cycle(nodes, simple_edges),
    }


def _has_longer_cycle(nodes, edges) -> bool:
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
    colour = {n: 0 for n in nodes}

    def dfs(n):
        colour[n] = 1
        for m in adj[n]:
            if colour[m] == 1 or (colour[m] == 0 and dfs(m)):
                return True
        colour[n] = 2
        return False

    return any(colour[n] == 0 and dfs(n) for n in nodes)


def published_sha(published) -> str:
    return published.get("__sha__", "")


def summarize_kempe(root: int, orbit: int, kempe: list[dict]) -> dict:
    kinds = {"stuck": 0, "descends": 0, "target": 0}
    failing = []
    passing = 0
    seen_fail = set()
    examples = []
    for move in kempe:
        kinds[move["neighbor_kind"]] = kinds.get(move["neighbor_kind"], 0) + 1
        for which, length in (("one", 1), ("two", 2)):
            for rec in move["slides"][which]:
                if rec["kind"] == "passing":
                    passing += 1
                    continue
                if rec["kind"] not in ("stuck", "descends", "target"):
                    continue
                if rec.get("cancels_to_same_orbit"):
                    continue
                key = (length, rec["vertex"], rec.get("orbit"), rec["kind"], move["neighbor_orbit"], tuple(move["pair"]))
                if key in seen_fail:
                    continue
                seen_fail.add(key)
                row = {
                    "length": length,
                    "kind": rec["kind"],
                    "vertex": rec["vertex"],
                    "orbit": rec.get("orbit"),
                    "p": rec.get("p"),
                    "q": rec.get("q"),
                    "via": rec.get("via"),
                    "kempe_pair": move["pair"],
                    "kempe_component": move["component"],
                    "neighbor_orbit": move["neighbor_orbit"],
                    "neighbor_kind": move["neighbor_kind"],
                    "neighbor_q": move["neighbor_q"],
                }
                failing.append(row)
                if len(examples) < 8 and rec["kind"] in ("descends", "target", "stuck"):
                    examples.append(row)
    # Prefer escape examples, otherwise stuck-to-stuck examples.
    escapes = [row for row in failing if row["kind"] in ("descends", "target")]
    stuck_hits = [row for row in failing if row["kind"] == "stuck" and not (row["vertex"] == root and row["orbit"] == orbit)]
    chosen = (escapes or stuck_hits or failing)[:6]
    return {
        "neighbor_kinds": kinds,
        "passing_landings": passing,
        "failing_landings": failing,
        "examples": chosen,
    }


def load_published():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    graphs = []
    for order in table["orders"]:
        for graph in order["graphs_checked"]:
            if not graph["failing_roots"]:
                continue
            roots = {}
            for root in graph["roots"]:
                if root["root"] in graph["failing_roots"]:
                    roots[root["root"]] = root
            roots["__passing__"] = graph["passing_roots"]
            roots["__sha__"] = graph["ascii_sha256"]
            graphs.append((order["order"], graph["graph_index"], graph["ascii"], list(graph["failing_roots"]), roots))
    return graphs


def main():
    graphs = load_published()
    reports = []
    for order, index, ascii_line, failing, published in graphs:
        print(f"graph {order}:{index} failing {failing}", flush=True)
        reports.append(analyze_graph(order, index, ascii_line, failing, published))
        rep = reports[-1]
        dead = [c for c in rep["terminal_components"] if c["dead_end"]]
        print(
            f"  stuck {rep['stuck_orbit_count']} dead-end components {len(dead)}"
            f" edges {len(rep['stuck_edges'])} kempe-edges {len(rep['kempe_stuck_edges'])}",
            flush=True,
        )
    payload = {"graphs": reports}
    OUT_JSON.write_text(json.dumps(payload, indent=1) + "\n")
    print("wrote", OUT_JSON, flush=True)


if __name__ == "__main__":
    main()
