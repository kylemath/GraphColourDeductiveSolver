"""
sat_search.py — SAT/SMT-based discharging rule optimization.

Encodes the discharging optimization problem: given a parametric family of
candidate rules, find the subset that minimizes the unavoidable set size.

Encoding (in scaled integer units, ×20 of original charge):
  Initial charge of degree-5 center = 20 units.
  A pattern is "discharged" iff total transfer >= 20.
  Unavoidable set = patterns where total transfer < 20.
  Objective: minimize |unavoidable set|.

Provides both Z3 Optimize and a greedy fallback.

Agent 1520-M3 / Sub-task S2
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure sibling import works when run from this directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from framework import (
    DegreePattern,
    DischargingEngine,
    DischargingRule,
)

try:
    from z3 import Bool, If, Optimize, Sum, sat
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False

SCALE = 20  # common denominator; all amounts are multiples of 1/20


# ======================================================================
# Candidate-rule factory (closures avoid lambda capture pitfalls)
# ======================================================================

def _cond_exact(d: int):
    return lambda p, i: p.center == 5 and p.neighbors[i] == d

def _cond_ge(d: int):
    return lambda p, i: p.center == 5 and p.neighbors[i] >= d

def _cond_flanked6():
    return lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                         and p.has_flanking_major(i))

def _cond_double_flanked6():
    return lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                         and p.has_both_flanking_major(i))

def _cond_major_ctx(k: int):
    return lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                         and p.count_major() >= k)

def _cond_deg6_ctx(k: int):
    """Send to deg-6 when center has >= k major neighbours."""
    return lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                         and p.count_major() >= k)

def _cond_any_nbr():
    return lambda p, i: p.center == 5


def generate_candidate_rules() -> List[DischargingRule]:
    """Systematic parametric family of ~35 candidate rules."""
    rules: List[DischargingRule] = []
    amounts = [Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)]

    # --- Type A: exact-degree rules ---
    for d in range(6, 13):
        for a in amounts:
            rules.append(DischargingRule(
                f"A: {a} → deg={d}", _cond_exact(d), a))

    # --- Type B: threshold rules ---
    for d in [7, 8, 9]:
        for a in amounts:
            rules.append(DischargingRule(
                f"B: {a} → deg>={d}", _cond_ge(d), a))

    # --- Type C: flanking rules ---
    for a in [Fraction(1, 20), Fraction(1, 10)]:
        rules.append(DischargingRule(
            f"C: {a} → flanked-6", _cond_flanked6(), a))
        rules.append(DischargingRule(
            f"C: {a} → double-flanked-6", _cond_double_flanked6(), a))

    # --- Type D: context-dependent rules ---
    for k in [2, 3, 4]:
        for a in [Fraction(1, 20), Fraction(1, 10)]:
            rules.append(DischargingRule(
                f"D: {a} → major when >={k} major", _cond_major_ctx(k), a))

    for k in [1, 2, 3]:
        for a in [Fraction(1, 20), Fraction(1, 10)]:
            rules.append(DischargingRule(
                f"D: {a} → deg6 when >={k} major", _cond_deg6_ctx(k), a))

    return rules


# ======================================================================
# Transfer matrix
# ======================================================================

def compute_transfer_matrix(
    rules: List[DischargingRule],
    patterns: List[DegreePattern],
) -> List[List[int]]:
    """T[i][j] = total transfer of rule i on pattern j, in units of 1/20."""
    mat: List[List[int]] = []
    for rule in rules:
        row: List[int] = []
        for p in patterns:
            total = Fraction(0)
            for idx in range(p.k):
                if rule.fires(p, idx):
                    total += rule.transfer
            row.append(int(total * SCALE))
        mat.append(row)
    return mat


# ======================================================================
# Z3 solver
# ======================================================================

def solve_z3(
    rules: List[DischargingRule],
    patterns: List[DegreePattern],
    T: List[List[int]],
    max_rules: Optional[int] = None,
    timeout_ms: int = 60_000,
) -> Dict[str, Any]:
    if not Z3_AVAILABLE:
        return {"status": "z3_unavailable"}

    m, n = len(rules), len(patterns)
    opt = Optimize()
    opt.set("timeout", timeout_ms)

    x = [Bool(f"r{i}") for i in range(m)]
    y = [Bool(f"p{j}") for j in range(n)]

    for j in range(n):
        total = Sum([If(x[i], T[i][j], 0) for i in range(m)])
        opt.add(y[j] == (total < SCALE))

    if max_rules is not None:
        opt.add(Sum([If(x[i], 1, 0) for i in range(m)]) <= max_rules)

    obj = opt.minimize(Sum([If(y[j], 1, 0) for j in range(n)]))

    t0 = time.time()
    status = opt.check()
    elapsed = time.time() - t0

    if str(status) == "sat":
        model = opt.model()
        active = [i for i in range(m) if model.evaluate(x[i])]
        unavoid = [j for j in range(n) if model.evaluate(y[j])]
        return {
            "status": "sat",
            "active_rules": active,
            "active_rule_names": [rules[i].name for i in active],
            "num_active": len(active),
            "unavoidable_count": len(unavoid),
            "unavoidable_indices": unavoid,
            "elapsed": elapsed,
        }
    return {"status": str(status), "elapsed": elapsed}


# ======================================================================
# Greedy heuristic (fallback)
# ======================================================================

def greedy_search(
    rules: List[DischargingRule],
    patterns: List[DegreePattern],
    T: List[List[int]],
    max_rules: int = 15,
) -> List[Dict[str, Any]]:
    m, n = len(rules), len(patterns)
    active: set = set()
    cum = [0] * n
    trail: List[Dict[str, Any]] = []

    for step in range(min(max_rules, m)):
        best_i, best_red = -1, 0
        cur_u = sum(1 for j in range(n) if cum[j] < SCALE)

        for i in range(m):
            if i in active:
                continue
            new_u = sum(1 for j in range(n) if cum[j] + T[i][j] < SCALE)
            red = cur_u - new_u
            if red > best_red:
                best_red = red
                best_i = i

        if best_i < 0 or best_red == 0:
            break

        active.add(best_i)
        for j in range(n):
            cum[j] += T[best_i][j]

        trail.append({
            "step": step + 1,
            "rule": rules[best_i].name,
            "num_active": len(active),
            "unavoidable": sum(1 for j in range(n) if cum[j] < SCALE),
        })

    return trail


# ======================================================================
# Pareto frontier (greedy, fast)
# ======================================================================

def pareto_frontier_greedy(
    rules: List[DischargingRule],
    patterns: List[DegreePattern],
    T: List[List[int]],
) -> List[Tuple[int, int]]:
    """(num_rules, min_unavoidable) pairs from greedy search."""
    trail = greedy_search(rules, patterns, T, max_rules=len(rules))
    return [(r["num_active"], r["unavoidable"]) for r in trail]


# ======================================================================
# Main
# ======================================================================

def main() -> None:
    print("=" * 60)
    print("SAT / SMT DISCHARGING OPTIMIZATION")
    print("Agent 1520-M3 / Sub-task S2")
    print("=" * 60)

    engine = DischargingEngine([], min_deg=5, max_deg=12)
    patterns = engine.enumerate_patterns(center_degrees=[5])
    print(f"\nDegree patterns (deg-5 center, nbrs 6..12): {len(patterns)}")

    rules = generate_candidate_rules()
    print(f"Candidate rules in parametric family:        {len(rules)}")

    print("\nComputing transfer matrix ...", flush=True)
    T = compute_transfer_matrix(rules, patterns)
    print("Done.")

    # --- Greedy ---
    print(f"\n{'─' * 60}")
    print("GREEDY SEARCH (adds rules one at a time, max reduction first)")
    print(f"{'─' * 60}")
    greedy = greedy_search(rules, patterns, T, max_rules=20)

    print(f"\n{'Step':>4s} {'#R':>4s} {'|U|':>6s}  Rule added")
    print("-" * 60)
    for r in greedy:
        print(f"{r['step']:>4d} {r['num_active']:>4d} {r['unavoidable']:>6d}  {r['rule']}")

    # --- Z3 (if available) ---
    z3_results: Dict[str, Any] = {}
    if Z3_AVAILABLE:
        print(f"\n{'─' * 60}")
        print("Z3 OPTIMIZATION  (exact solver, various budgets)")
        print(f"{'─' * 60}")
        for budget in [3, 5, 8, 10, 15, None]:
            label = f"≤{budget} rules" if budget else "unlimited"
            print(f"  {label:>14s} ... ", end="", flush=True)
            res = solve_z3(rules, patterns, T, max_rules=budget, timeout_ms=120_000)
            z3_results[str(budget)] = res
            if res["status"] == "sat":
                print(f"|U| = {res['unavoidable_count']:>5d},  "
                      f"active = {res['num_active']:>2d},  "
                      f"time = {res['elapsed']:.1f}s")
            else:
                print(f"status={res['status']},  time={res.get('elapsed', 0):.1f}s")

        # Show rules for the smallest budgets
        for budget in [3, 5]:
            key = str(budget)
            if key in z3_results and z3_results[key]["status"] == "sat":
                print(f"\n  Best ≤{budget} rules:")
                for rn in z3_results[key]["active_rule_names"]:
                    print(f"    • {rn}")
    else:
        print("\nZ3 not installed — greedy results only.")

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print("PARETO FRONTIER (greedy)")
    print(f"{'=' * 60}")
    frontier = [(0, len(patterns))] + pareto_frontier_greedy(rules, patterns, T)
    print(f"{'#Rules':>6s}  {'|U|':>6s}")
    print("-" * 14)
    for k, u in frontier:
        print(f"{k:>6d}  {u:>6d}")

    # --- Export ---
    out = {
        "num_patterns": len(patterns),
        "num_candidate_rules": len(rules),
        "candidate_rule_names": [r.name for r in rules],
        "greedy_trail": greedy,
        "pareto_frontier": [{"rules": k, "unavoidable": u} for k, u in frontier],
        "z3_results": {
            k: {kk: vv for kk, vv in v.items() if kk != "unavoidable_indices"}
            for k, v in z3_results.items()
        } if z3_results else None,
    }
    out_path = Path(__file__).resolve().parent / "sat_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults → {out_path}")


if __name__ == "__main__":
    main()
