"""Numerical Colin de Verdière certificate: mu(G) >= 3 for K4 and the octahedron.

A witness is a real symmetric matrix M with the Colin de Verdière sign pattern,
exactly one negative eigenvalue (multiplicity one), and corank 3. The Strong
Arnold Property is tested, not assumed: the only symmetric matrix X supported
on the non-edges with MX = 0 is X = 0. Equivalently, if the rows u_i of a
kernel basis are taken in R^3, the linear conditions u_i^T S u_j = 0 for every
diagonal index and every edge force the symmetric 3x3 matrix S to be zero.

Definitions follow van der Holst, Lovász, and Schrijver, "The Colin de Verdière
graph parameter", Bolyai Soc. Math. Stud. 7 (1999), conditions (M1)--(M3).
"""

from __future__ import annotations

import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import numpy as np

TOL = 1e-8
OUT = Path(
    "/Users/fulkanjou/GraphColour/backgroundMaterial/agent1720/groups/S1_results.json"
)

# Exact kernel bases whose columns span ker(M). Rows are the vectors u_i.
K4_KERNEL = (
    (1, 1, 1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
)
OCT_KERNEL = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


def k4_matrix() -> list[list[int]]:
    """All-ones matrix with a minus sign: off-diagonal entries are -1."""
    return [[-1, -1, -1, -1] for _ in range(4)]


def octahedron_nonedges() -> list[tuple[int, int]]:
    """Three opposite pairs. The complement is a perfect matching."""
    return [(0, 1), (2, 3), (4, 5)]


def octahedron_matrix() -> list[list[int]]:
    """Negative adjacency matrix of the octahedral graph.

    Vertices 0..5. Non-edges are the opposite pairs (0,1), (2,3), (4,5).
    Every other off-diagonal entry is -1.
    """
    non = set(octahedron_nonedges())
    matrix = [[0] * 6 for _ in range(6)]
    for i in range(6):
        for j in range(i + 1, 6):
            if (i, j) not in non:
                matrix[i][j] = matrix[j][i] = -1
    return matrix


def edges_of(n: int, nonedges: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    banned = {tuple(sorted(pair)) for pair in nonedges}
    return [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in banned]


def sign_pattern_ok(
    matrix: list[list[int]], edges: list[tuple[int, int]], nonedges: list[tuple[int, int]]
) -> bool:
    """(M1): strict inequality on edges, exact zero on non-edges. Diagonal free."""
    edge_set = set(edges)
    non_set = {tuple(sorted(pair)) for pair in nonedges}
    n = len(matrix)
    if any(len(row) != n or matrix[i][j] != matrix[j][i] for i, row in enumerate(matrix) for j in range(n)):
        return False
    for i, j in edge_set:
        if matrix[i][j] >= 0:
            return False
    for i, j in non_set:
        if matrix[i][j] != 0:
            return False
    for i in range(n):
        for j in range(i + 1, n):
            pair = (i, j)
            if pair not in edge_set and pair not in non_set:
                return False
    return True


def spectral_facts(matrix: list[list[int]]) -> dict[str, object]:
    """Numpy inertia and singular values. Zeros are counted at absolute tolerance TOL."""
    array = np.array(matrix, dtype=float)
    eigenvalues = np.linalg.eigvalsh(array)
    singular = np.linalg.svd(array, compute_uv=False)
    ev = [float(x) for x in eigenvalues]
    sv = [float(x) for x in singular]
    return {
        "eigenvalues": ev,
        "singular_values": sv,
        "n_negative": int(np.sum(eigenvalues < -TOL)),
        "corank": int(np.sum(np.abs(eigenvalues) <= TOL)),
        "n_positive": int(np.sum(eigenvalues > TOL)),
        "max_abs_corank_eigenvalue": float(np.max(np.abs(eigenvalues[np.abs(eigenvalues) <= TOL])))
        if np.any(np.abs(eigenvalues) <= TOL)
        else None,
        "numerical_rank": int(np.sum(singular > TOL)),
    }


def _sym_coeff(ui: tuple[int, ...], uj: tuple[int, ...], a: int, b: int) -> int:
    """Coefficient of the (a,b) entry of S in u_i^T S u_j, a <= b."""
    if a == b:
        return ui[a] * uj[a]
    return ui[a] * uj[b] + ui[b] * uj[a]


def strong_arnold_integer(
    kernel: tuple[tuple[int, ...], ...], edges: list[tuple[int, int]]
) -> dict[str, object]:
    """Exact test of (M3) on an integer kernel basis.

    Build the integer matrix of the map S |-> (u_i^T S u_j) over diagonal
    positions and edges. SAP holds when this map has full column rank equal
    to dim Sym_3 = 6, i.e. only S = 0 meets the conditions.
    """
    k = len(kernel[0])
    pairs = [(a, b) for a in range(k) for b in range(a, k)]
    rows: list[list[int]] = []
    n = len(kernel)
    positions = [(i, i) for i in range(n)] + list(edges)
    for i, j in positions:
        rows.append([_sym_coeff(kernel[i], kernel[j], a, b) for a, b in pairs])
    rank = _rank_over_q(rows)
    return {
        "tested": True,
        "holds": rank == len(pairs),
        "constraint_rank": rank,
        "sym_dimension": len(pairs),
        "n_constraints": len(rows),
        "method": "integer kernel basis, rank over Q of u_i^T S u_j on diagonal and edges",
    }


def _rank_over_q(rows: list[list[int]]) -> int:
    """Gaussian elimination over the rationals."""
    if not rows:
        return 0
    matrix = [[Fraction(x) for x in row] for row in rows]
    n_cols = len(matrix[0])
    rank = 0
    for col in range(n_cols):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][col] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [entry / scale for entry in matrix[rank]]
        for r in range(len(matrix)):
            if r == rank or matrix[r][col] == 0:
                continue
            factor = matrix[r][col]
            matrix[r] = [entry - factor * matrix[rank][c] for c, entry in enumerate(matrix[r])]
        rank += 1
    return rank


def support_map_singular_value(
    matrix: list[list[int]], nonedges: list[tuple[int, int]]
) -> dict[str, object]:
    """Smallest singular value of a |-> M X(a), X supported on the non-edges.

    Dimension zero (no non-edges) means the only admissible X is zero, so (M3)
    holds. Numpy is used only as a floating-point cross-check of the integer test.
    """
    if not nonedges:
        return {
            "admissible_dimension": 0,
            "kernel_dimension": 0,
            "smallest_singular_value": None,
            "holds": True,
        }
    array = np.array(matrix, dtype=float)
    n = array.shape[0]
    columns = []
    for i, j in nonedges:
        support = np.zeros((n, n))
        support[i, j] = support[j, i] = 1.0
        columns.append((array @ support).reshape(-1))
    stacked = np.column_stack(columns)
    singular = np.linalg.svd(stacked, compute_uv=False)
    kernel_dim = int(np.sum(singular <= TOL))
    return {
        "admissible_dimension": len(nonedges),
        "kernel_dimension": kernel_dim,
        "smallest_singular_value": float(singular.min()),
        "holds": kernel_dim == 0,
    }


def certify(
    name: str,
    matrix: list[list[int]],
    nonedges: list[tuple[int, int]],
    kernel: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    n = len(matrix)
    edges = edges_of(n, nonedges)
    spectrum = spectral_facts(matrix)
    arnold = strong_arnold_integer(kernel, edges)
    support = support_map_singular_value(matrix, nonedges)
    array = np.array(matrix, dtype=float)
    kernel_array = np.array(kernel, dtype=float)
    residual = float(np.linalg.norm(array @ kernel_array))
    ok = (
        sign_pattern_ok(matrix, edges, nonedges)
        and spectrum["n_negative"] == 1
        and spectrum["corank"] == 3
        and spectrum["numerical_rank"] == n - 3
        and arnold["holds"]
        and support["holds"]
        and residual <= TOL
    )
    return {
        "graph": name,
        "n": n,
        "n_edges": len(edges),
        "nonedges": [list(pair) for pair in nonedges],
        "matrix": matrix,
        "kernel_basis_rows": [list(row) for row in kernel],
        "kernel_residual": residual,
        "sign_pattern_ok": sign_pattern_ok(matrix, edges, nonedges),
        "spectrum": spectrum,
        "strong_arnold": arnold,
        "support_map": support,
        "mu_at_least": 3 if ok else None,
        "certificate_ok": ok,
    }


def main() -> None:
    started = time.perf_counter()
    graphs = [
        certify("K4", k4_matrix(), [], K4_KERNEL),
        certify("octahedral", octahedron_matrix(), octahedron_nonedges(), OCT_KERNEL),
    ]
    elapsed = time.perf_counter() - started
    payload = {
        "group": "S1",
        "track": 5,
        "statement": "mu(G) >= 3",
        "tolerance": TOL,
        "elapsed_sec": elapsed,
        "graphs": graphs,
        "all_ok": all(item["certificate_ok"] for item in graphs),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"elapsed_sec={elapsed:.6f}")
    print(f"all_ok={payload['all_ok']}")
    for item in graphs:
        spectrum = item["spectrum"]
        print(
            item["graph"],
            "neg",
            spectrum["n_negative"],
            "corank",
            spectrum["corank"],
            "pos",
            spectrum["n_positive"],
            "sap",
            item["strong_arnold"]["holds"],
            "rank",
            item["strong_arnold"]["constraint_rank"],
            "support",
            item["support_map"],
            "ev",
            [round(x, 12) for x in spectrum["eigenvalues"]],
        )


if __name__ == "__main__":
    main()
