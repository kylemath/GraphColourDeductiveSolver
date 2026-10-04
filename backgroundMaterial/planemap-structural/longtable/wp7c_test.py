"""WP7c: injective charging of warnings to locked boundary patterns (see WP7c-declaration.md).

Consumes breadcrumb-warning-traces.json (hash-checked); regenerates no colourings.
Facts only; no status claims.
"""
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from mass_core import FIXTURES, HERE, parse_ascii

PAIRS = list(combinations(range(4), 2))


def manifest_ok():
    root = FIXTURES.parents[1]
    for line in (FIXTURES / "breadcrumb-warning-SHA256SUMS").read_text().splitlines():
        digest, _, rel = line.partition("  ")
        assert hashlib.sha256((root / rel).read_bytes()).hexdigest() == digest, rel


def partition(vertices, adj, active):
    """Blocks of `vertices` under connectivity in the subgraph induced on `active`."""
    comp = {}
    for v in vertices:
        if v in comp:
            continue
        seen, stack = {v}, [v]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w in active and w not in seen:
                    seen.add(w)
                    stack.append(w)
        for u in seen:
            comp[u] = frozenset(seen)
    return comp


def pattern(rot, r, V, B, colouring):
    col = dict(zip(V, colouring))
    names = {}
    for b in B:
        names.setdefault(col[b], len(names))
    assert len(names) == 4
    norm = {v: names[x] for v, x in col.items()}
    adj = {v: [w for w in rot[v] if w != r] for v in V}
    Bset = set(B)
    out = [tuple(norm[b] for b in B)]
    for x, y in PAIRS:
        active = {v for v in V if norm[v] in (x, y)}
        pos = [k for k, b in enumerate(B) if norm[b] in (x, y)]
        full = partition([B[k] for k in pos], adj, active)
        local = partition([B[k] for k in pos], adj, active & Bset)
        F = tuple(sorted({tuple(sorted(k for k in pos if B[k] in full[B[j]])) for j in pos}))
        L = tuple(sorted({tuple(sorted(k for k in pos if B[k] in local[B[j]])) for j in pos}))
        E = tuple(any(u not in Bset for u in full[B[blk[0]]]) for blk in F)
        out.append((F, L, E))
    return tuple(out)


def main():
    manifest_ok()
    path = FIXTURES / "breadcrumb-warning-traces.json"
    data = json.loads(path.read_text())
    collisions, per_root, runs_checked = [], [], 0
    for row in data["rows"]:
        rot = parse_ascii(row["ascii"])
        r, V, B = row["root"], row["vertex_order"], row["boundary_cyclic_order"]
        assert sorted(B) == sorted(rot[r])
        by_pattern = defaultdict(set)
        for run_index, run in enumerate(row["runs"]):
            warned = {tuple(w["coloring"]) for w in run["warnings"]}
            if not warned:
                continue
            runs_checked += 1
            pats = {}
            for c in warned:
                p = pattern(rot, r, V, B, c)
                by_pattern[p].add(c)
                if p in pats:
                    collisions.append({"order": row["order"], "graph_index": row["graph_index"], "root": r,
                                       "run": run_index, "colorings": [list(pats[p]), list(c)]})
                pats[p] = c
        warned_all = set().union(*by_pattern.values()) if by_pattern else set()
        per_root.append({"order": row["order"], "graph_index": row["graph_index"], "root": r,
                         "distinct_warned": len(warned_all), "distinct_patterns": len(by_pattern),
                         "max_colorings_per_pattern": max((len(v) for v in by_pattern.values()), default=0)})
    out = {"scope": "WP7c test of injective charging within runs, on the supplied breadcrumb warning traces; "
                    "finite evidence, no status claims.",
           "runs_with_warnings_checked": runs_checked, "collisions": collisions,
           "c7c_survives": not collisions, "per_root": per_root,
           "inputs": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()},
           "checkers": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (HERE / "wp7c_test.py", HERE / "WP7c-declaration.md")}}
    (HERE / "wp7c-results.json").write_text(json.dumps(out, indent=1) + "\n")
    print("runs with warnings checked:", runs_checked, "| collisions within a run:", len(collisions))
    for x in per_root:
        print(f"  order {x['order']} graph {x['graph_index']} root {x['root']}: distinct warned {x['distinct_warned']},"
              f" distinct patterns {x['distinct_patterns']}, max per pattern {x['max_colorings_per_pattern']}")


if __name__ == "__main__":
    main()
