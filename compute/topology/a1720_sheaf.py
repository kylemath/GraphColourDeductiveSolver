"""
a1720_sheaf.py -- Agent 1720, group S2 (M-Frontier, Track 6).

Proper 4-colourings of K4 are not a linear subspace, so no cellular sheaf of
vector spaces has H^0 equal to that set.  The linear stand-in computed here is
the constant cellular sheaf L with stalk F_2^2 and identity restrictions:

    (delta x)_{uv} = x_u + x_v    in F_2^2.

H^0 = ker delta (monochromatic assignments on a connected graph) and
H^1 = coker delta.  The same dimensions are recomputed over R with
numpy.linalg.matrix_rank on the signed coboundary (stalk R^2); the two
ranks agree because -1 = 1 in F_2.

Usage:
    /Users/fulkanjou/GraphColour/.venv/bin/python compute/topology/a1720_sheaf.py
"""

from __future__ import annotations

import json
import time
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "S2_results.json"

COLOURS: tuple[tuple[int, int], ...] = ((0, 0), (0, 1), (1, 0), (1, 1))


def edges(n: int) -> list[tuple[int, int]]:
    """Edges of K_n as pairs i < j."""
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def is_proper(n: int, colouring: tuple[tuple[int, int], ...]) -> bool:
    """True when adjacent vertices of K_n receive different colours in F_2^2."""
    return all(colouring[i] != colouring[j] for i, j in edges(n))


def count_proper(n: int) -> int:
    """Number of maps V(K_n) -> F_2^2 that are proper colourings."""
    return sum(1 for assign in product(COLOURS, repeat=n) if is_proper(n, assign))


def is_prime_power(n: int) -> bool:
    """True when n = p^k for a prime p and an integer k >= 1."""
    if n <= 1:
        return False
    p = 2
    m = n
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            return m == 1
        p += 1 if p == 2 else 2
    return True


def gf2_rank(matrix: np.ndarray) -> int:
    """Rank of a {0,1}-matrix over F_2, by Gaussian elimination on a numpy array."""
    reduced = np.array(matrix, dtype=np.uint8, copy=True) % np.uint8(2)
    rows, cols = reduced.shape
    rank = 0
    pivot_col = 0
    for row in range(rows):
        if pivot_col >= cols:
            break
        pivots = np.array([], dtype=int)
        while pivot_col < cols:
            pivots = np.flatnonzero(reduced[row:, pivot_col] == 1)
            if pivots.size:
                break
            pivot_col += 1
        if pivot_col >= cols:
            break
        pivot_row = row + int(pivots[0])
        if pivot_row != row:
            reduced[[row, pivot_row]] = reduced[[pivot_row, row]]
        for i in range(rows):
            if i != row and reduced[i, pivot_col] == 1:
                reduced[i, :] ^= reduced[row, :]
        rank += 1
        pivot_col += 1
    return rank


def coboundary_f2(n: int) -> np.ndarray:
    """Coboundary of the constant sheaf with stalk F_2^2, shape (2|E|, 2|V|).

    Column 2*v+k is vertex v, coordinate k.  Row 2*e+k is edge e, coordinate k.
    Over F_2 the signed formula x_head - x_tail is x_head + x_tail.
    """
    ed = edges(n)
    matrix = np.zeros((2 * len(ed), 2 * n), dtype=np.uint8)
    for ei, (i, j) in enumerate(ed):
        for k in range(2):
            matrix[2 * ei + k, 2 * i + k] = 1
            matrix[2 * ei + k, 2 * j + k] = 1
    return matrix


def coboundary_real(n: int) -> np.ndarray:
    """Signed coboundary of the constant sheaf with stalk R^2, for numpy.linalg."""
    ed = edges(n)
    matrix = np.zeros((2 * len(ed), 2 * n), dtype=float)
    for ei, (i, j) in enumerate(ed):
        for k in range(2):
            matrix[2 * ei + k, 2 * i + k] = -1.0
            matrix[2 * ei + k, 2 * j + k] = 1.0
    return matrix


def kernel_colourings(n: int) -> list[list[list[int]]]:
    """Global sections of L: assignments V -> F_2^2 with equal values on every edge."""
    sections: list[list[list[int]]] = []
    for assign in product(COLOURS, repeat=n):
        if all(assign[i] == assign[j] for i, j in edges(n)):
            sections.append([list(c) for c in assign])
    return sections


def subspace_witness() -> dict[str, object]:
    """Two proper F_2^2-colourings of K4 whose sum is not proper."""
    c1 = ((0, 0), (0, 1), (1, 0), (1, 1))
    c2 = ((0, 0), (1, 0), (0, 1), (1, 1))
    total = tuple(
        ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2) for a, b in zip(c1, c2)
    )
    zero = tuple((0, 0) for _ in range(4))
    n_proper = count_proper(4)
    return {
        "graph": "K4",
        "vertices": [0, 1, 2, 3],
        "ambient": "(F_2^2)^4",
        "c1": [list(c) for c in c1],
        "c2": [list(c) for c in c2],
        "sum": [list(c) for c in total],
        "c1_proper": is_proper(4, c1),
        "c2_proper": is_proper(4, c2),
        "sum_proper": is_proper(4, total),
        "zero_proper": is_proper(4, zero),
        "n_proper_4_colourings": n_proper,
        "cardinality_is_prime_power": is_prime_power(n_proper),
        "closed_under_addition": False,
        "contains_zero": False,
    }


def graph_cohomology(n: int) -> dict[str, object]:
    """Dimensions of H^0 and H^1 for the constant sheaf L on K_n."""
    ed = edges(n)
    over_f2 = coboundary_f2(n)
    over_r = coboundary_real(n)
    rank_f2 = gf2_rank(over_f2)
    rank_r = int(np.linalg.matrix_rank(over_r, tol=1e-8))
    dim_c0 = 2 * n
    dim_c1 = 2 * len(ed)
    sections = kernel_colourings(n)
    proper_sections = [
        s for s in sections if is_proper(n, tuple(tuple(c) for c in s))
    ]
    return {
        "graph": f"K{n}",
        "n": n,
        "m": len(ed),
        "planar": n <= 4,
        "four_colourable": n <= 4,
        "n_proper_colourings": count_proper(n),
        "dim_C0": dim_c0,
        "dim_C1": dim_c1,
        "rank_delta_F2": rank_f2,
        "rank_delta_R": rank_r,
        "ranks_agree": rank_f2 == rank_r,
        "dim_H0": dim_c0 - rank_f2,
        "dim_H1": dim_c1 - rank_f2,
        "H1_vanishes": dim_c1 - rank_f2 == 0,
        "n_global_sections": len(sections),
        "n_proper_global_sections": len(proper_sections),
        "global_sections": sections,
    }


def main() -> None:
    started = time.perf_counter()
    witness = subspace_witness()
    k4 = graph_cohomology(4)
    k5 = graph_cohomology(5)
    elapsed = time.perf_counter() - started

    if not (
        witness["c1_proper"]
        and witness["c2_proper"]
        and not witness["sum_proper"]
        and not witness["zero_proper"]
        and witness["n_proper_4_colourings"] == 24
        and witness["cardinality_is_prime_power"] is False
    ):
        raise SystemExit("subspace witness failed")
    for graph, n in ((k4, 4), (k5, 5)):
        expect_rank = 2 * (n - 1)
        if graph["rank_delta_F2"] != expect_rank or not graph["ranks_agree"]:
            raise SystemExit(f"unexpected rank on K{n}: {graph}")
        if graph["dim_H0"] != 2 or graph["n_global_sections"] != 4:
            raise SystemExit(f"unexpected H^0 on K{n}: {graph}")
        if graph["n_proper_global_sections"] != 0:
            raise SystemExit(f"a global section was proper on K{n}")
    if k4["dim_H1"] != 6 or k5["dim_H1"] != 12:
        raise SystemExit("unexpected H^1 dimensions")
    if k4["n_proper_colourings"] != 24 or k5["n_proper_colourings"] != 0:
        raise SystemExit("unexpected proper-colouring counts")

    out = {
        "group": "S2",
        "manager": "M-Frontier",
        "verdict": "killed",
        "stand_in": {
            "name": "constant cellular sheaf",
            "stalk": "F_2^2",
            "restrictions": "identity",
            "coboundary": "(delta x)_uv = x_u + x_v over F_2",
            "relation": (
                "A 0-cochain is a proper 4-colouring iff (delta x)_e != 0 "
                "for every edge. H^0 is the kernel, not that set."
            ),
        },
        "witness": witness,
        "K4": k4,
        "K5": k5,
        "kill_test_met": True,
        "elapsed_seconds": elapsed,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(
        json.dumps(
            {
                "verdict": out["verdict"],
                "K4_dim_H0": k4["dim_H0"],
                "K4_dim_H1": k4["dim_H1"],
                "K5_dim_H0": k5["dim_H0"],
                "K5_dim_H1": k5["dim_H1"],
                "elapsed_seconds": elapsed,
                "out": str(OUT),
            }
        )
    )


if __name__ == "__main__":
    main()
