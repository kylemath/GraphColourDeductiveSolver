"""Chromatic polynomial database for planar triangulations (Agent 1720, group A1).

For every triangulation T_n_i in ``compute/data/triangulations_n4_11.json`` this
script computes

* the exact chromatic polynomial P(G, k) with integer coefficients,
  via the partition numbers a_j = #{partitions of V into j nonempty independent
  sets} and P(G, k) = sum_j a_j k(k-1)...(k-j+1);
* P(G, 4) and a_3 + a_4 (the number of 4-colourings up to colour permutation);
* all real roots, isolated exactly with sympy (rational isolating intervals,
  refined to width <= 1e-15), with multiplicities;
* the number of distinct real roots in the open interval (3, 4) (Sturm count
  via ``Poly.count_roots`` minus roots at the endpoints);
* Tutte's golden identity P(T, phi+2) = (phi+2) phi^(3n-10) P(T, phi+1)^2,
  checked exactly in Q(sqrt 5).

Usage::

    .venv/bin/python compute/chromatic/a1720_chromatic_db.py [max_n]

Output: ``compute/data/chromatic_polys_n4_11.json`` (or ``..._n4_<max_n>.json``).
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "compute" / "data"
K = sp.Symbol("k")

Edge = Tuple[int, int]


# ---------------------------------------------------------------------------
# Chromatic polynomial via partitions into independent sets
# ---------------------------------------------------------------------------

def adjacency_masks(n: int, edges: Sequence[Sequence[int]]) -> List[int]:
    """Return adj[v] as a bitmask of the neighbours of v."""
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def independent_sets(n: int, adj: List[int]) -> List[int]:
    """All nonempty independent sets as bitmasks."""
    out: List[int] = []

    def rec(start: int, cur: int, forbidden: int) -> None:
        for v in range(start, n):
            if not (forbidden >> v) & 1:
                nxt = cur | (1 << v)
                out.append(nxt)
                rec(v + 1, nxt, forbidden | adj[v])

    rec(0, 0, 0)
    return out


def partition_numbers(n: int, edges: Sequence[Sequence[int]]) -> List[int]:
    """a[j] = number of partitions of V into j nonempty independent sets, j=0..n.

    Layered subset DP: g_j[S] = sum over independent T with min(T) = min(S),
    T subset of S, of g_{j-1}[S \\ T].  Every g_j[S] is at most the Bell number
    B_n, so int64 never overflows for n <= 20.
    """
    adj = adjacency_masks(n, edges)
    full = (1 << n) - 1
    ind = independent_sets(n, adj)
    # masks with lowest set bit m
    by_low: Dict[int, np.ndarray] = {}
    for m in range(n):
        upper = np.arange(1 << (n - m - 1), dtype=np.int64)
        by_low[m] = (upper << (m + 1)) | (1 << m)
    targets: List[Tuple[int, np.ndarray]] = []
    for T in ind:
        m = (T & -T).bit_length() - 1
        cand = by_low[m]
        S = cand[(cand & T) == T]
        targets.append((T, S))
    g_prev = np.zeros(1 << n, dtype=np.int64)
    g_prev[0] = 1
    a = [0] * (n + 1)
    for j in range(1, n + 1):
        g = np.zeros(1 << n, dtype=np.int64)
        for T, S in targets:
            g[S] += g_prev[S ^ T]
        a[j] = int(g[full])
        g_prev = g
        if not g.any():
            break
    return a


def falling_coeffs(j: int) -> List[int]:
    """Coefficients (ascending powers) of k(k-1)...(k-j+1)."""
    c = [1]
    for r in range(j):
        new = [0] * (len(c) + 1)
        for d, x in enumerate(c):
            new[d + 1] += x
            new[d] -= r * x
        c = new
    return c


def chromatic_coeffs(n: int, edges: Sequence[Sequence[int]]) -> Tuple[List[int], List[int]]:
    """(ascending integer coefficients of P(G,k), partition numbers a_j)."""
    a = partition_numbers(n, edges)
    coeffs = [0] * (n + 1)
    for j, aj in enumerate(a):
        if aj:
            for d, x in enumerate(falling_coeffs(j)):
                coeffs[d] += aj * x
    return coeffs, a


def eval_poly(coeffs: Sequence[int], x):
    """Horner evaluation, ascending coefficients; works for int/Fraction/Q5."""
    acc = 0 * x
    for c in reversed(coeffs):
        acc = acc * x + c
    return acc


# ---------------------------------------------------------------------------
# Independent checks
# ---------------------------------------------------------------------------

def count_colourings(n: int, edges: Sequence[Sequence[int]], k: int) -> int:
    """Brute-force backtracking count of proper k-colourings (for validation)."""
    nbrs = [[] for _ in range(n)]
    for u, v in edges:
        nbrs[u].append(v)
        nbrs[v].append(u)
    col = [-1] * n

    def rec(v: int) -> int:
        if v == n:
            return 1
        total = 0
        used = {col[w] for w in nbrs[v] if w < v}
        for c in range(k):
            if c not in used:
                col[v] = c
                total += rec(v + 1)
        col[v] = -1
        return total

    return rec(0)


# ---------------------------------------------------------------------------
# Exact arithmetic in Q(sqrt 5)
# ---------------------------------------------------------------------------

class Q5:
    """a + b*sqrt(5) with rational a, b."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def _c(self, o) -> "Q5":
        return o if isinstance(o, Q5) else Q5(o)

    def __add__(self, o):
        o = self._c(o)
        return Q5(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __mul__(self, o):
        o = self._c(o)
        return Q5(self.a * o.a + 5 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def __pow__(self, e: int):
        r, base = Q5(1), self
        while e:
            if e & 1:
                r = r * base
            base = base * base
            e >>= 1
        return r

    def __eq__(self, o):
        o = self._c(o)
        return self.a == o.a and self.b == o.b

    def __repr__(self):
        return f"({self.a} + {self.b}*sqrt5)"


PHI = Q5(Fraction(1, 2), Fraction(1, 2))


def golden_identity_q5(n: int, coeffs: Sequence[int]) -> Tuple[bool, Q5, Q5]:
    """Exact check of P(T,phi+2) = (phi+2) phi^(3n-10) P(T,phi+1)^2 in Q(sqrt5)."""
    lhs = eval_poly(coeffs, PHI + 2)
    p1 = eval_poly(coeffs, PHI + 1)
    rhs = (PHI + 2) * PHI ** (3 * n - 10) * p1 * p1
    return lhs == rhs, lhs, p1


def golden_identity_sympy(n: int, coeffs: Sequence[int]) -> bool:
    """Same identity, independently in sympy (radical simplification)."""
    phi = (1 + sp.sqrt(5)) / 2
    P = sp.Poly(list(reversed(coeffs)), K)
    lhs = P.eval(phi + 2)
    rhs = (phi + 2) * phi ** (3 * n - 10) * P.eval(phi + 1) ** 2
    return sp.expand(lhs - rhs) == 0


# ---------------------------------------------------------------------------
# Roots
# ---------------------------------------------------------------------------

def root_data(coeffs: Sequence[int]) -> Dict:
    """Exact real-root isolation and (3,4) count."""
    P = sp.Poly(list(reversed(coeffs)), K)
    eps = sp.Rational(1, 10**15)
    ivs = P.intervals(eps=eps)
    roots = []
    for (lo, hi), mult in ivs:
        lo, hi = sp.Rational(lo), sp.Rational(hi)
        exact_int = lo == hi and lo.is_integer
        roots.append({
            "approx": float((lo + hi) / 2),
            "interval": [str(lo), str(hi)],
            "multiplicity": int(mult),
            "integer": bool(exact_int),
        })
    p3 = eval_poly(coeffs, 3)
    p4 = eval_poly(coeffs, 4)
    n34 = P.count_roots(3, 4) - (p3 == 0) - (p4 == 0)
    below4 = [r for r in roots if r["approx"] < 4 and not (r["integer"] and r["approx"] == 4)]
    nonint_below4 = [r for r in below4 if not r["integer"]]
    return {
        "real_roots": roots,
        "largest_real_root_below_4": max((r["approx"] for r in below4), default=None),
        "largest_nonint_root_below_4": max((r["approx"] for r in nonint_below4), default=None),
        "largest_nonint_root_interval": (max(nonint_below4, key=lambda r: r["approx"])["interval"]
                                         if nonint_below4 else None),
        "distinct_roots_in_open_3_4": int(n34),
        "roots_ge_4": [r["approx"] for r in roots if r["approx"] >= 4],
    }


# ---------------------------------------------------------------------------
# Validation on known graphs
# ---------------------------------------------------------------------------

def validate() -> Dict[str, bool]:
    """Check the DP against known closed forms and brute force."""
    import networkx as nx

    res: Dict[str, bool] = {}
    k = K
    # K4
    c, _ = chromatic_coeffs(4, [(u, v) for u in range(4) for v in range(u + 1, 4)])
    res["K4"] = sp.expand(sp.Poly(list(reversed(c)), k).as_expr() - k * (k - 1) * (k - 2) * (k - 3)) == 0
    # octahedron
    Oc = nx.octahedral_graph()
    c, _ = chromatic_coeffs(6, list(Oc.edges()))
    target = k * (k - 1) * (k - 2) * (k**3 - 9 * k**2 + 29 * k - 32)
    res["octahedron"] = sp.expand(sp.Poly(list(reversed(c)), k).as_expr() - target) == 0
    # icosahedron: compare with brute force at k=4,5 and with networkx at k=4..6 via counts
    Ic = nx.icosahedral_graph()
    c, a = chromatic_coeffs(12, list(Ic.edges()))
    ico_expr = sp.factor(sp.Poly(list(reversed(c)), k).as_expr())
    res["icosahedron_P4_bruteforce"] = eval_poly(c, 4) == count_colourings(12, list(Ic.edges()), 4)
    res["icosahedron_P5_bruteforce"] = eval_poly(c, 5) == count_colourings(12, list(Ic.edges()), 5)
    res["icosahedron_golden_identity"] = golden_identity_q5(12, c)[0]
    print("icosahedron P =", ico_expr, " P(4) =", eval_poly(c, 4))
    # random-ish small graphs vs networkx deletion-contraction
    for name, G in [("petersen", nx.petersen_graph()), ("C5", nx.cycle_graph(5)),
                    ("wheel6", nx.wheel_graph(6))]:
        G = nx.convert_node_labels_to_integers(G)
        c, _ = chromatic_coeffs(G.number_of_nodes(), list(G.edges()))
        ref = nx.chromatic_polynomial(G)
        x = list(ref.free_symbols)[0]
        res[f"{name}_vs_networkx"] = sp.expand(sp.Poly(list(reversed(c)), x).as_expr() - ref) == 0
    return res


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(max_n: int = 11, sympy_golden_max_n: int = 11) -> None:
    t0 = time.time()
    val = validate()
    print("validation:", val)
    assert all(val.values()), val
    src = DATA / "triangulations_n4_11.json"
    tri = json.loads(src.read_text())["graphs"]
    out = {
        "description": "Chromatic polynomials of planar triangulations T_n_i (index as in "
                       "triangulations_n4_11.json). coeffs = ascending integer coefficients of P(G,k).",
        "script": "compute/chromatic/a1720_chromatic_db.py",
        "validation": val,
        "graphs": {},
        "summary": {},
        "timing_seconds": {},
    }
    for n in range(4, max_n + 1):
        tn = time.time()
        recs = []
        for i, edges in enumerate(tri[str(n)]):
            coeffs, a = chromatic_coeffs(n, edges)
            p4 = eval_poly(coeffs, 4)
            ok_q5, _, p_phi1 = golden_identity_q5(n, coeffs)
            ok_sp = golden_identity_sympy(n, coeffs) if n <= sympy_golden_max_n else None
            rd = root_data(coeffs)
            recs.append({
                "name": f"T_{n}_{i}",
                "coeffs": coeffs,
                "partition_numbers": a,
                "P4": p4,
                "P4_over_24": Fraction(p4, 24).__str__(),
                "a3_plus_a4": a[3] + a[4],
                "P4_over_24_equals_a3_plus_a4": Fraction(p4, 24) == a[3] + a[4],
                "P4_bruteforce": count_colourings(n, edges, 4),
                "P3": eval_poly(coeffs, 3),
                "golden_identity_Q5": ok_q5,
                "golden_identity_sympy": ok_sp,
                "P_phi_plus_1_float": float(p_phi1.a + p_phi1.b * 5 ** 0.5),
                **rd,
            })
        dt = time.time() - tn
        out["graphs"][str(n)] = recs
        out["timing_seconds"][str(n)] = dt
        s = {
            "count": len(recs),
            "all_P4_positive": all(r["P4"] > 0 for r in recs),
            "all_P4_match_bruteforce": all(r["P4"] == r["P4_bruteforce"] for r in recs),
            "all_P4_over_24_equals_a3_plus_a4": all(r["P4_over_24_equals_a3_plus_a4"] for r in recs),
            "min_P4_over_24": min(r["a3_plus_a4"] for r in recs),
            "argmin_P4_over_24": [r["name"] for r in recs if r["a3_plus_a4"] == min(x["a3_plus_a4"] for x in recs)],
            "all_golden_Q5": all(r["golden_identity_Q5"] for r in recs),
            "all_golden_sympy": (all(r["golden_identity_sympy"] for r in recs)
                                 if n <= sympy_golden_max_n else None),
            "num_with_root_in_open_3_4": sum(r["distinct_roots_in_open_3_4"] > 0 for r in recs),
            "any_root_ge_4_nonint": any(any(abs(x - round(x)) > 1e-9 for x in r["roots_ge_4"]) for r in recs),
            "max_nonint_root_below_4": max((r["largest_nonint_root_below_4"] or 0) for r in recs),
            "argmax_nonint_root_below_4": max(recs, key=lambda r: r["largest_nonint_root_below_4"] or 0)["name"],
            "min_abs_P_phi_plus_1": min(abs(r["P_phi_plus_1_float"]) for r in recs),
        }
        out["summary"][str(n)] = s
        print(f"n={n}: {len(recs)} graphs in {dt:.1f}s  {s}", flush=True)
    out["timing_seconds"]["total"] = time.time() - t0
    path = DATA / f"chromatic_polys_n4_{max_n}.json"
    path.write_text(json.dumps(out))
    print(f"wrote {path}  total {out['timing_seconds']['total']:.1f}s")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
