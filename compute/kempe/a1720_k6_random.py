"""
a1720_k6_random.py -- K6: KC5 on random planar triangulations beyond n = 11.

Random triangulations: random stacked triangulation (face splits) on n
vertices, then many random edge flips (face-set representation; a flip of uv
with opposite vertices a, b is allowed iff a != b, ab is not an edge and
deg u, deg v >= 4, which keeps the triangulation simple).  Optionally the
walk is biased to minimum degree 5 (the relevant case for a minimal
counterexample).  At each degree-5 vertex the full Kempe-class structure of
G - v is computed with a1720_k6_kc5.analyse_vertex.

Not uniform sampling and not exhaustive: evidence only.
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path
from typing import FrozenSet, List, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a1720_k6_kc5 import ROOT, adjacency, analyse_vertex, degree5_vertices  # noqa: E402

Face = FrozenSet[int]


def random_triangulation(n: int, rng: random.Random, flips: int = 2000,
                         min_deg5: bool = False) -> List[Tuple[int, int]]:
    """Edge list of a random simple triangulation of the sphere on n >= 4 vertices."""
    faces: Set[Face] = {frozenset(s) for s in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]}
    for x in range(4, n):
        f = rng.choice(sorted(faces, key=sorted))
        faces.remove(f)
        a, b, c = sorted(f)
        faces |= {frozenset((a, b, x)), frozenset((a, c, x)), frozenset((b, c, x))}

    def edges_of(fs: Set[Face]) -> Set[FrozenSet[int]]:
        return {frozenset(e) for f in fs for e in [tuple(sorted(f))[:2], tuple(sorted(f))[1:],
                                                     (min(f), max(f))]}

    E = edges_of(faces)
    deg = [0] * n
    for e in E:
        for u in e:
            deg[u] += 1
    edge_faces = {}
    for f in faces:
        for e in edges_of({f}):
            edge_faces.setdefault(e, []).append(f)
    steps = 0
    while steps < flips or (min_deg5 and min(deg) < 5 and steps < 50 * flips):
        steps += 1
        e = rng.choice(list(E))
        u, v = tuple(e)
        f1, f2 = edge_faces[e]
        (a,) = f1 - e
        (b,) = f2 - e
        if a == b or frozenset((a, b)) in E or deg[u] < 4 or deg[v] < 4:
            continue
        if min_deg5 and min(deg) >= 5 and (deg[u] == 5 or deg[v] == 5):
            continue
        g1, g2 = frozenset((a, b, u)), frozenset((a, b, v))
        for f in (f1, f2):
            faces.remove(f)
            for ee in edges_of({f}):
                edge_faces[ee].remove(f)
        E.remove(e)
        del edge_faces[e]
        ab = frozenset((a, b))
        E.add(ab)
        edge_faces[ab] = []
        for g in (g1, g2):
            faces.add(g)
            for ee in edges_of({g}):
                edge_faces[ee].append(g)
        deg[u] -= 1
        deg[v] -= 1
        deg[a] += 1
        deg[b] += 1
    assert len(E) == 3 * n - 6 and len(faces) == 2 * n - 4
    return sorted(tuple(sorted(e)) for e in E)


def main(ns: List[int], per_n: int, budget_s: float, seed: int = 1720) -> None:
    rng = random.Random(seed)
    out = {"seed": seed, "per_n": per_n, "budget_seconds_per_n": budget_s, "runs": []}
    for n in ns:
        t0 = time.time()
        rec = {"n": n, "graphs": 0, "pairs": 0, "classes": 0, "bad_classes": 0,
               "multi_class_pairs": 0, "max_classes": 0, "max_dist": 0,
               "min_deg5_graphs": 0, "bad": []}
        while rec["graphs"] < per_n and time.time() - t0 < budget_s:
            want5 = rec["graphs"] % 2 == 1
            E = random_triangulation(n, rng, flips=20 * n, min_deg5=want5)
            adj = adjacency(n, E)
            rec["graphs"] += 1
            rec["min_deg5_graphs"] += min(len(a) for a in adj) >= 5
            for v in degree5_vertices(adj):
                r = analyse_vertex(adj, v)
                rec["pairs"] += 1
                rec["classes"] += r["n_classes"]
                rec["bad_classes"] += r["n_bad_classes"]
                rec["multi_class_pairs"] += r["n_classes"] > 1
                rec["max_classes"] = max(rec["max_classes"], r["n_classes"])
                rec["max_dist"] = max(rec["max_dist"], r["max_kempe_distance_to_fix"])
                if r["n_bad_classes"]:
                    rec["bad"].append({"edges": E, **r})
                    print("BAD", n, v, E, flush=True)
        rec["elapsed_seconds"] = round(time.time() - t0, 1)
        print(json.dumps({k: v for k, v in rec.items() if k != "bad"}), flush=True)
        out["runs"].append(rec)
    p = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "K6_random.json"
    p.write_text(json.dumps(out, indent=1))
    print("wrote", p)


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [12, 14, 16, 18, 20]
    per_n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    budget = float(sys.argv[3]) if len(sys.argv) > 3 else 120.0
    main(ns, per_n, budget)
