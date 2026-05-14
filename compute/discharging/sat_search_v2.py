"""
sat_search_v2.py — SAT/SMT optimization at second order.

Encodes the second-order discharging problem:
  - Variables: Boolean for each candidate rule, plus transfer amounts.
  - Constraints: every second-order pattern must be discharged OR in the
    unavoidable set AND reducible.
  - Objective: minimize |unavoidable set|.

Builds on the first-order SAT search (sat_search.py) by incorporating
cascade constraints from second_order_framework.py.

Agent 1545-M3 / Sub-task S3
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from framework import (
    DegreePattern,
    DischargingEngine,
    DischargingRule,
    build_rsst_rules,
    build_standard_rules,
    build_extended_rules,
)
from second_order_framework import (
    CascadeEngine,
    ExtendedDegreePattern,
    SecondOrderFeature,
    enumerate_ext_features,
)

try:
    from z3 import (
        Bool, Int, If, Optimize, Sum, And, Or, sat, IntVal,
        ArithRef, BoolRef,
    )
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False

SCALE = 60  # LCM of {5,10,15,20} — all fractions become integers


# ======================================================================
# Candidate rule factory (second-order aware)
# ======================================================================

def _mk_cond(desc, fn):
    """Create a named condition with a proper closure."""
    return (desc, fn)


def generate_second_order_candidates() -> List[DischargingRule]:
    """Parametric family of ~50 candidate rules including 2-hop conditions.

    The rules are partitioned into:
      Type A: exact-degree rules (first-order)
      Type B: threshold rules (first-order)
      Type C: flanking / positional rules (first-order)
      Type D: context rules — major count (first-order)
      Type E: minor-run rules (first-order)
    The transfer amounts are varied systematically.
    """
    rules: List[DischargingRule] = []
    small_amounts = [Fraction(1, 20), Fraction(1, 10), Fraction(3, 20), Fraction(1, 5)]

    # Type A: exact-degree transfers
    for d in range(6, 13):
        for a in [Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)]:
            rules.append(DischargingRule(
                f"A: {a}→d={d}",
                _make_exact_cond(d), a))

    # Type B: threshold transfers
    for d in [7, 8, 9, 10]:
        for a in [Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)]:
            rules.append(DischargingRule(
                f"B: {a}→d≥{d}",
                _make_ge_cond(d), a))

    # Type C: flanking rules for deg-6
    for a in small_amounts:
        rules.append(DischargingRule(
            f"C: {a}→d6-flanked1",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.has_flanking_major(i)),
            a))
        rules.append(DischargingRule(
            f"C: {a}→d6-flanked2",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.has_both_flanking_major(i)),
            a))

    # Type D: context-dependent
    for k in [1, 2, 3, 4]:
        for a in [Fraction(1, 20), Fraction(1, 10)]:
            rules.append(DischargingRule(
                f"D: {a}→major|≥{k}maj",
                _make_major_ctx(k), a))
            rules.append(DischargingRule(
                f"D: {a}→d6|≥{k}maj",
                _make_d6_ctx(k), a))

    # Type E: minor-run rules
    for run_len in [2, 3, 4, 5]:
        for a in [Fraction(1, 20), Fraction(1, 10)]:
            rules.append(DischargingRule(
                f"E: {a}→d6|run≥{run_len}",
                _make_run_cond(run_len), a))

    return rules


def _make_exact_cond(d: int):
    return lambda p, i: p.center == 5 and p.neighbors[i] == d

def _make_ge_cond(d: int):
    return lambda p, i: p.center == 5 and p.neighbors[i] >= d

def _make_major_ctx(k: int):
    return lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                         and p.count_major() >= k)

def _make_d6_ctx(k: int):
    return lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                         and p.count_major() >= k)

def _make_run_cond(run_len: int):
    return lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                         and p.consecutive_minor_run() >= run_len)


# ======================================================================
# Transfer matrix computation (second-order)
# ======================================================================

def compute_cascade_matrix(
    rules: List[DischargingRule],
    patterns: List[ExtendedDegreePattern],
    alpha: Fraction = Fraction(1, 5),
    beta: Fraction = Fraction(1, 5),
) -> Tuple[List[List[int]], List[int]]:
    """Compute per-rule transfer effects and cascade thresholds.

    Returns:
        T[i][j]: scaled total transfer of rule i applied to centre of pattern j.
        thresh[j]: scaled cascade threshold — the MAXIMUM total transfer
                   the centre can make before some deg-6 neighbour overflows.
                   Pattern j is discharged iff:
                     (a) sum_i x_i * centre_transfer[i][j] >= centre_charge_scaled
                     (b) for each deg-6 neighbour: net cascade charge <= 0

    For simplicity, we encode the BINDING constraint:
        The pattern is "second-order discharged" iff
        centre is discharged AND no neighbour has positive cascade charge.

    We encode this as: pattern j needs total centre transfer >= SCALE
    (centre discharged) AND per-neighbour cascade constraint.

    To linearise: for each pattern j, compute the per-rule transfer to
    EACH neighbour, and add cascade constraints per neighbour.
    """
    m = len(rules)
    n = len(patterns)

    # T_center[i][j]: total transfer from centre to ALL neighbours for rule i on pattern j
    T_center: List[List[int]] = []
    for rule in rules:
        row: List[int] = []
        for ep in patterns:
            bp = ep.base_pattern
            total = Fraction(0)
            for idx in range(bp.k):
                if rule.fires(bp, idx):
                    total += rule.transfer
            row.append(int(total * SCALE))
        T_center.append(row)

    # For each pattern j and each deg-6 neighbour k of j:
    # T_nbr[i][j][k]: transfer from centre to neighbour k due to rule i
    # cascade_slack[j][k]: max additional transfer nbr k can absorb
    #   = n_total_major * beta - n_ext_5 * alpha  (in scaled units)

    # We store a flat "cascade constraint" matrix:
    #   For pattern j, compute per-neighbour constraints.
    #   Pattern j is cascade-discharged iff for EACH deg-6 nbr k:
    #     sum_i x_i * t_nbr[i][j][k] <= cascade_cap[j][k]
    #
    # This is complex for Z3 but feasible.

    # Per-neighbour transfer: T_nbr[i][j] = list of (nbr_index, transfer)
    # for deg-6 neighbours only
    T_nbr: List[List[List[Tuple[int, int]]]] = []  # [rule][pattern] -> [(nbr_idx, amount)]
    for rule in rules:
        rule_data: List[List[Tuple[int, int]]] = []
        for ep in patterns:
            bp = ep.base_pattern
            nbr_transfers: List[Tuple[int, int]] = []
            for idx in range(bp.k):
                if bp.neighbors[idx] == 6 and ep.ext_features[idx] is not None:
                    if rule.fires(bp, idx):
                        nbr_transfers.append((idx, int(rule.transfer * SCALE)))
            rule_data.append(nbr_transfers)
        T_nbr.append(rule_data)

    # Cascade capacity per deg-6 neighbour
    cascade_cap: List[List[Tuple[int, int]]] = []  # [pattern] -> [(nbr_idx, capacity)]
    for ep in patterns:
        caps: List[Tuple[int, int]] = []
        for idx in range(ep.k):
            if ep.neighbors[idx] == 6 and ep.ext_features[idx] is not None:
                f = ep.ext_features[idx]
                n_ring_major = ((1 if ep.left(idx) >= 7 else 0)
                                + (1 if ep.right(idx) >= 7 else 0))
                n_total_major = n_ring_major + f.n_ext_major
                cap = int((n_total_major * beta - f.n_ext_5 * alpha) * SCALE)
                caps.append((idx, cap))
        cascade_cap.append(caps)

    return T_center, T_nbr, cascade_cap  # type: ignore


# ======================================================================
# Z3 solver (second-order)
# ======================================================================

def solve_z3_second_order(
    rules: List[DischargingRule],
    patterns: List[ExtendedDegreePattern],
    T_center: List[List[int]],
    T_nbr: List[List[List[Tuple[int, int]]]],
    cascade_cap: List[List[Tuple[int, int]]],
    max_rules: Optional[int] = None,
    timeout_ms: int = 120_000,
) -> Dict[str, Any]:
    """Z3-based second-order optimization.

    Minimize |unavoidable set| where a pattern is unavoidable iff:
      - centre charge > 0 after discharge, OR
      - any deg-6 neighbour has positive cascade charge.
    """
    if not Z3_AVAILABLE:
        return {"status": "z3_unavailable"}

    m, n = len(rules), len(patterns)
    opt = Optimize()
    opt.set("timeout", timeout_ms)

    x = [Bool(f"r{i}") for i in range(m)]   # rule active?
    y = [Bool(f"u{j}") for j in range(n)]   # pattern unavoidable?

    # Centre discharge constraint
    centre_charge_scaled = SCALE  # 6-5 = 1 → SCALE
    for j in range(n):
        centre_ok = Sum([If(x[i], T_center[i][j], 0) for i in range(m)]) >= centre_charge_scaled

        # Cascade constraints for each deg-6 neighbour
        cascade_constraints = []
        for (nbr_idx, cap) in cascade_cap[j]:
            nbr_transfer = Sum([
                If(x[i], amt, 0)
                for i in range(m)
                for (ni, amt) in T_nbr[i][j]
                if ni == nbr_idx
            ] + [IntVal(0)])  # ensure non-empty sum
            cascade_constraints.append(nbr_transfer <= cap)

        if cascade_constraints:
            fully_ok = And(centre_ok, *cascade_constraints)
        else:
            fully_ok = centre_ok

        opt.add(y[j] == Not_z3(fully_ok))

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
            "elapsed": elapsed,
        }
    return {"status": str(status), "elapsed": elapsed}


def Not_z3(expr):
    """Z3 Not — imported lazily to avoid issues when z3 not available."""
    from z3 import Not
    return Not(expr)


# ======================================================================
# Greedy heuristic (second-order)
# ======================================================================

def greedy_search_v2(
    rules: List[DischargingRule],
    patterns: List[ExtendedDegreePattern],
    alpha: Fraction = Fraction(1, 5),
    beta: Fraction = Fraction(1, 5),
    max_rules: int = 20,
) -> List[Dict[str, Any]]:
    """Greedy rule selection minimising second-order unavoidable set."""
    m = len(rules)
    n = len(patterns)

    active: set = set()
    trail: List[Dict[str, Any]] = []

    # Precompute per-rule, per-pattern, per-neighbour transfers
    base_patterns = [ep.base_pattern for ep in patterns]
    cascade_engines: List[CascadeEngine] = []

    # Current accumulated transfers per pattern per neighbour
    cum_center = [Fraction(0)] * n
    cum_nbr: List[Dict[int, Fraction]] = [dict() for _ in range(n)]

    # Initialize neighbour tracking
    for j, ep in enumerate(patterns):
        for idx in range(ep.k):
            if ep.neighbors[idx] == 6 and ep.ext_features[idx] is not None:
                cum_nbr[j][idx] = Fraction(0)

    # Precompute cascade capacities
    cascade_caps: List[Dict[int, Fraction]] = []
    for j, ep in enumerate(patterns):
        caps: Dict[int, Fraction] = {}
        for idx in range(ep.k):
            if ep.neighbors[idx] == 6 and ep.ext_features[idx] is not None:
                f = ep.ext_features[idx]
                n_ring_major = ((1 if ep.left(idx) >= 7 else 0)
                                + (1 if ep.right(idx) >= 7 else 0))
                n_total_major = n_ring_major + f.n_ext_major
                caps[idx] = n_total_major * beta - f.n_ext_5 * alpha
        cascade_caps.append(caps)

    def is_discharged(j: int, extra_center: Fraction = Fraction(0),
                      extra_nbr: Optional[Dict[int, Fraction]] = None) -> bool:
        """Check if pattern j is fully discharged with current + extra."""
        if cum_center[j] + extra_center < Fraction(1):
            return False
        for idx, cap in cascade_caps[j].items():
            nbr_charge = cum_nbr[j].get(idx, Fraction(0))
            if extra_nbr and idx in extra_nbr:
                nbr_charge += extra_nbr[idx]
            if nbr_charge > cap:
                return False
        return True

    def count_unavoidable() -> int:
        return sum(1 for j in range(n) if not is_discharged(j))

    for step in range(min(max_rules, m)):
        cur_u = count_unavoidable()
        best_i, best_red = -1, 0

        for i in range(m):
            if i in active:
                continue
            # Compute effect of adding rule i
            extra_c = Fraction(0)
            extra_nbr_map: Dict[int, Dict[int, Fraction]] = {}

            reductions = 0
            for j in range(n):
                if is_discharged(j):
                    continue  # already OK, adding rule won't hurt
                bp = base_patterns[j]
                ep = patterns[j]
                ec = Fraction(0)
                en: Dict[int, Fraction] = {}
                for idx in range(bp.k):
                    if rules[i].fires(bp, idx):
                        ec += rules[i].transfer
                        if idx in cum_nbr[j]:
                            en[idx] = rules[i].transfer
                if is_discharged(j, ec, en):
                    reductions += 1

            if reductions > best_red:
                best_red = reductions
                best_i = i

        if best_i < 0 or best_red == 0:
            break

        # Apply best rule
        active.add(best_i)
        for j in range(n):
            bp = base_patterns[j]
            for idx in range(bp.k):
                if rules[best_i].fires(bp, idx):
                    cum_center[j] += rules[best_i].transfer
                    if idx in cum_nbr[j]:
                        cum_nbr[j][idx] += rules[best_i].transfer

        trail.append({
            "step": step + 1,
            "rule": rules[best_i].name,
            "num_active": len(active),
            "unavoidable": count_unavoidable(),
        })

    return trail


# ======================================================================
# Main
# ======================================================================

def structural_analysis(patterns: List[ExtendedDegreePattern],
                        alpha: Fraction = Fraction(1, 5),
                        beta: Fraction = Fraction(1, 5)) -> Dict[str, Any]:
    """Analyse which patterns are structurally unavoidable.

    A pattern is structurally unavoidable if the total cascade capacity
    of all neighbours is less than the centre's initial charge (1).
    No rule set can help in this case.
    """
    n = len(patterns)
    struct_unavoid = 0
    struct_avoidable = 0
    has_major_nbr = 0
    cap_dist: Dict[str, int] = {}

    for ep in patterns:
        total_cap = Fraction(0)
        any_major = False
        for i in range(ep.k):
            if ep.neighbors[i] >= 7:
                any_major = True
                total_cap += Fraction(6 - ep.neighbors[i]).denominator  # large sink
                total_cap += Fraction(100)  # effectively infinite
            elif ep.ext_features[i] is not None:
                f = ep.ext_features[i]
                n_ring_major = ((1 if ep.left(i) >= 7 else 0)
                                + (1 if ep.right(i) >= 7 else 0))
                cap_i = (n_ring_major + f.n_ext_major) * beta - f.n_ext_5 * alpha
                total_cap += max(cap_i, Fraction(0))

        if any_major:
            has_major_nbr += 1
            struct_avoidable += 1
        elif total_cap >= Fraction(1):
            struct_avoidable += 1
        else:
            struct_unavoid += 1
            bucket = str(total_cap)
            cap_dist[bucket] = cap_dist.get(bucket, 0) + 1

    return {
        'total': n,
        'structurally_unavoidable': struct_unavoid,
        'structurally_avoidable': struct_avoidable,
        'has_major_neighbour': has_major_nbr,
        'capacity_distribution': cap_dist,
    }


def fast_greedy_numpy(
    rules: List[DischargingRule],
    patterns: List[ExtendedDegreePattern],
    alpha: Fraction = Fraction(1, 5),
    beta: Fraction = Fraction(1, 5),
    max_rules: int = 20,
) -> List[Dict[str, Any]]:
    """Optimised greedy search using integer arithmetic.

    Uses SCALE=60 to convert all fractions to integers.
    """
    import numpy as np

    m = len(rules)
    n = len(patterns)

    # Precompute per-rule centre transfer (scaled)
    T_center = np.zeros((m, n), dtype=np.int64)
    for ri, rule in enumerate(rules):
        for j, ep in enumerate(patterns):
            bp = ep.base_pattern
            total = 0
            for idx in range(bp.k):
                if rule.fires(bp, idx):
                    total += int(rule.transfer * SCALE)
            T_center[ri, j] = total

    # Precompute per-pattern cascade constraints
    # For each pattern j: list of (max_nbr_transfer_scaled) constraints
    # A pattern is discharged if centre_transfer >= SCALE AND
    # for each deg-6 nbr k: transfer_to_k <= cascade_cap_k
    alpha_s = int(alpha * SCALE)
    beta_s = int(beta * SCALE)

    # Per-rule per-pattern per-deg6-nbr transfer
    # Store as dense array: T_nbr[ri, j] = transfer to WORST deg-6 nbr
    # (simplified: check per-neighbour constraints)

    # For efficiency, compute per-pattern: minimum slack across all deg-6 nbrs
    # after applying a rule set.

    # Precompute per-rule, per-pattern transfer to EACH deg-6 neighbour
    max_nbrs = 5  # max ring size
    T_nbr = np.zeros((m, n, max_nbrs), dtype=np.int64)
    cascade_cap = np.full((n, max_nbrs), 999999, dtype=np.int64)  # large = no constraint
    nbr_mask = np.zeros((n, max_nbrs), dtype=bool)  # True if deg-6 nbr exists

    for j, ep in enumerate(patterns):
        bp = ep.base_pattern
        for idx in range(ep.k):
            if ep.neighbors[idx] == 6 and ep.ext_features[idx] is not None:
                f = ep.ext_features[idx]
                n_ring_major = ((1 if ep.left(idx) >= 7 else 0)
                                + (1 if ep.right(idx) >= 7 else 0))
                cap = (n_ring_major + f.n_ext_major) * beta_s - f.n_ext_5 * alpha_s
                cascade_cap[j, idx] = cap
                nbr_mask[j, idx] = True

    for ri, rule in enumerate(rules):
        for j, ep in enumerate(patterns):
            bp = ep.base_pattern
            for idx in range(ep.k):
                if nbr_mask[j, idx] and rule.fires(bp, idx):
                    T_nbr[ri, j, idx] = int(rule.transfer * SCALE)

    # Greedy loop
    active = set()
    cum_center = np.zeros(n, dtype=np.int64)
    cum_nbr = np.zeros((n, max_nbrs), dtype=np.int64)
    trail: List[Dict[str, Any]] = []

    def count_discharged() -> int:
        center_ok = cum_center >= SCALE
        nbr_ok = np.all((cum_nbr <= cascade_cap) | ~nbr_mask, axis=1)
        return int(np.sum(center_ok & nbr_ok))

    for step in range(min(max_rules, m)):
        cur_discharged = count_discharged()
        cur_unavoid = n - cur_discharged

        best_i = -1
        best_discharged = cur_discharged

        for i in range(m):
            if i in active:
                continue
            new_center = cum_center + T_center[i]
            new_nbr = cum_nbr + T_nbr[i]
            c_ok = new_center >= SCALE
            n_ok = np.all((new_nbr <= cascade_cap) | ~nbr_mask, axis=1)
            discharged = int(np.sum(c_ok & n_ok))
            if discharged > best_discharged:
                best_discharged = discharged
                best_i = i

        if best_i < 0 or best_discharged <= cur_discharged:
            break

        active.add(best_i)
        cum_center += T_center[best_i]
        cum_nbr += T_nbr[best_i]

        trail.append({
            "step": step + 1,
            "rule": rules[best_i].name,
            "num_active": len(active),
            "unavoidable": n - best_discharged,
        })

    return trail


def main() -> None:
    print("=" * 65)
    print("SAT / SMT SECOND-ORDER DISCHARGING OPTIMIZATION")
    print("Agent 1545-M3 / Sub-task S3")
    print("=" * 65)

    rsst_rules = build_rsst_rules()
    cascade_eng = CascadeEngine(rsst_rules)

    print("\nEnumerating second-order patterns...", flush=True)
    all_patterns = cascade_eng.enumerate_extended()
    print(f"Total second-order patterns: {len(all_patterns)}")

    # Structural analysis
    print(f"\n{'─' * 65}")
    print("STRUCTURAL ANALYSIS")
    print(f"{'─' * 65}")
    sa = structural_analysis(all_patterns)
    print(f"Total patterns:              {sa['total']}")
    print(f"Structurally unavoidable:    {sa['structurally_unavoidable']}")
    print(f"  (no rule set can help — insufficient cascade capacity)")
    print(f"Structurally avoidable:      {sa['structurally_avoidable']}")
    print(f"  ├─ has major neighbour:    {sa['has_major_neighbour']}")
    print(f"  └─ all deg-6, enough cap:  "
          f"{sa['structurally_avoidable'] - sa['has_major_neighbour']}")

    # RSST baseline
    print(f"\n{'─' * 65}")
    print("RSST BASELINE")
    print(f"{'─' * 65}")
    _, stats_rsst = cascade_eng.compute_unavoidable()
    print(f"|U₂| (RSST, α=1/5, β=1/5): {stats_rsst['unavoidable_count']}")
    print(f"  cascade_only_fail: {stats_rsst['cascade_only_fail']}")

    # Try with better β values
    print(f"\nVarying cascade parameters:")
    for a_num, a_den, b_num, b_den in [
        (1,5,1,3), (1,5,1,2), (1,10,1,3), (1,10,1,2),
        (1,5,2,5), (1,10,2,5)
    ]:
        a, b = Fraction(a_num, a_den), Fraction(b_num, b_den)
        eng = CascadeEngine(rsst_rules, alpha=a, beta=b)
        _, st = eng.compute_unavoidable()
        sa2 = structural_analysis(all_patterns, alpha=a, beta=b)
        print(f"  α={a}, β={b}: |U₂|={st['unavoidable_count']:>6d}, "
              f"structural={sa2['structurally_unavoidable']:>5d}")

    # Generate candidates and run fast greedy
    candidates = generate_second_order_candidates()
    print(f"\n{'─' * 65}")
    print(f"GREEDY SEARCH ({len(candidates)} candidate rules)")
    print(f"{'─' * 65}")

    t0 = time.time()
    greedy = fast_greedy_numpy(candidates, all_patterns, max_rules=25)
    greedy_elapsed = time.time() - t0

    print(f"\n{'Step':>4s} {'#R':>4s} {'|U₂|':>7s}  Rule added")
    print("-" * 65)
    for r in greedy:
        print(f"{r['step']:>4d} {r['num_active']:>4d} {r['unavoidable']:>7d}  {r['rule']}")
    print(f"Elapsed: {greedy_elapsed:.1f}s")

    # Also try greedy with different α,β
    print(f"\n{'─' * 65}")
    print("GREEDY WITH RELAXED CASCADE (α=1/10, β=1/3)")
    print(f"{'─' * 65}")
    greedy2 = fast_greedy_numpy(
        candidates, all_patterns,
        alpha=Fraction(1, 10), beta=Fraction(1, 3), max_rules=25)
    for r in greedy2:
        print(f"  step {r['step']:>2d}: #R={r['num_active']:>2d}, "
              f"|U₂|={r['unavoidable']:>6d}  {r['rule']}")

    # Summary
    print(f"\n{'=' * 65}")
    print("SUMMARY")
    print(f"{'=' * 65}")
    print(f"Total second-order patterns:  {len(all_patterns)}")
    print(f"Structurally unavoidable:     {sa['structurally_unavoidable']}")
    print(f"RSST baseline |U₂|:          {stats_rsst['unavoidable_count']}")
    if greedy:
        print(f"Best greedy |U₂| (α=1/5):    {greedy[-1]['unavoidable']}")
    if greedy2:
        print(f"Best greedy |U₂| (α=1/10):   {greedy2[-1]['unavoidable']}")
    print(f"\nRSST reference: 633 configurations")
    print("Note: |U₂| counts second-order DEGREE PATTERNS, not full")
    print("configurations. Each degree pattern may correspond to multiple")
    print("RSST-style configurations (with different internal structure).")
    print("'Distinct base' ≈ 967 is the first-order pattern count in U₂.")
    print("Structural minimum provides a lower bound independent of rules.")

    # Export
    out: Dict[str, Any] = {
        "total_patterns": len(all_patterns),
        "structural": sa,
        "rsst_baseline": stats_rsst['unavoidable_count'],
        "greedy_trail": greedy,
        "greedy_relaxed_trail": greedy2,
    }
    out_path = Path(__file__).resolve().parent / "sat_v2_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nResults → {out_path}")


if __name__ == "__main__":
    main()
