"""Spot-check the degeneracy product bound on one stored chromatic polynomial.

Reads T_6_1 (and the equality-case record T_6_0) from the A1 database.
Does not recompute a chromatic polynomial: values come from stored coefficients.

Usage:
    /Users/fulkanjou/GraphColour/.venv/bin/python compute/chromatic/a1720_a2_degeneracy_check.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRI = ROOT / "compute" / "data" / "triangulations_n4_11.json"
POLY = ROOT / "compute" / "data" / "chromatic_polys_n4_11.json"


def elimination(n: int, edges: list[list[int]]) -> list[int]:
    """Back-degrees in a greedy order: repeatedly delete a minimum-degree vertex."""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    alive = set(range(n))
    removed: list[int] = []
    while alive:
        v = min(alive, key=lambda x: (len(adj[x] & alive), x))
        removed.append(len(adj[v] & alive))
        for u in adj[v] & alive:
            adj[u].discard(v)
        alive.remove(v)
    removed.reverse()
    return removed


def eval_asc(coeffs: list[int], k: int) -> int:
    total = 0
    power = 1
    for c in coeffs:
        total += c * power
        power *= k
    return total


def worst_case(n: int, d: int, k: int) -> int:
    value = 1
    for i in range(1, n + 1):
        value *= k - min(d, i - 1)
    return value


def main() -> None:
    t0 = time.perf_counter()
    tri = json.loads(TRI.read_text())
    poly = json.loads(POLY.read_text())
    edges = tri["graphs"]["6"][1]
    rec = poly["graphs"]["6"][1]
    back = elimination(6, edges)
    deg = max(back)
    print(f"record {rec['name']} degeneracy {deg} back {back}")
    for k in (4, 5, 6):
        p_val = eval_asc(rec["coeffs"], k)
        actual = 1
        for d_i in back:
            actual *= k - d_i
        worst = worst_case(6, deg, k)
        print(
            f"k={k} P={p_val} product={actual} worst={worst} "
            f"P>=product {p_val >= actual} product>=worst {actual >= worst}"
        )
    # Equality case for the 3-tree formula, stored coefficients only.
    closed_forms = {
        ("4", 0): [0, -6, 11, -6, 1],  # k(k-1)(k-2)(k-3)
        ("5", 0): [0, 18, -39, 29, -9, 1],  # k(k-1)(k-2)(k-3)^2
        ("6", 0): [0, -54, 135, -126, 56, -12, 1],  # k(k-1)(k-2)(k-3)^3
    }
    for (n, i), closed in closed_forms.items():
        rec_i = poly["graphs"][n][i]
        print(
            f"record {rec_i['name']} P4={rec_i['P4']} "
            f"coeffs_match_3tree {rec_i['coeffs'] == closed}"
        )
    print(f"elapsed_seconds {time.perf_counter() - t0:.4f}")


if __name__ == "__main__":
    main()
