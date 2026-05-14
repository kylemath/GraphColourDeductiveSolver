"""
second_order_framework.py — Second-order cascade discharging framework.

Extends the first-order framework to handle charge cascade through degree-6
intermediaries.  In a minimum counterexample to the 4CT:

  1. Degree-5 vertices send charge to neighbours (Phase 1).
  2. Degree-6 neighbours that receive charge must forward it through their
     own major neighbours (Phase 2 — the cascade).

A second-order degree pattern specifies:
  - Centre vertex degree (5)
  - Ring neighbour degrees (first order)
  - For each degree-6 ring neighbour: a summary of its external neighbourhood
    (counts of external deg-5, deg-6, deg-7+ neighbours)

The cascade balance for a deg-6 ring neighbour u_i is:
  net(u_i) = charge_from_centre + n_ext_5 · α − n_total_major · β
where α is the average charge received per adjacent external deg-5 vertex
and β is the average charge forwarded per adjacent major vertex.

Agent 1545-M3 / Sub-task S2
"""

from __future__ import annotations

import json
import sys
import time
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from framework import (
    DegreePattern,
    DischargingEngine,
    DischargingRule,
    build_rsst_rules,
    build_standard_rules,
    build_extended_rules,
    canonical_necklace,
)


# ======================================================================
# Second-order feature
# ======================================================================

@dataclass(frozen=True)
class SecondOrderFeature:
    """Summary of a ring neighbour's external neighbourhood.

    For ring neighbour u_i (degree d_i) adjacent to centre v in a triangulation:
      - 3 internal neighbours: v, u_{i-1}, u_{i+1}
      - d_i − 3 external neighbours
    This class summarises external neighbour degrees by category.

    Triangulation constraint (no two adjacent deg-5):
      For deg-6 neighbour: at most 2 external deg-5 neighbours
      (maximum independent set in a path of length 3).
    """
    n_ext_5: int
    n_ext_6: int
    n_ext_major: int

    @property
    def n_external(self) -> int:
        return self.n_ext_5 + self.n_ext_6 + self.n_ext_major

    def __repr__(self) -> str:
        return f"({self.n_ext_5},{self.n_ext_6},{self.n_ext_major})"


def enumerate_ext_features(neighbor_deg: int,
                           max_ext_5: int = 2) -> List[SecondOrderFeature]:
    """All valid second-order features for a ring neighbour of given degree.

    Args:
        neighbor_deg: Degree of the ring neighbour.
        max_ext_5: Max external deg-5 neighbours (adjacency constraint).
    """
    n_ext = neighbor_deg - 3
    if n_ext <= 0:
        return [SecondOrderFeature(0, 0, 0)]
    features: List[SecondOrderFeature] = []
    for n5 in range(min(max_ext_5, n_ext) + 1):
        for n_maj in range(n_ext - n5 + 1):
            n6 = n_ext - n5 - n_maj
            features.append(SecondOrderFeature(n5, n6, n_maj))
    return features


# ======================================================================
# Extended degree pattern
# ======================================================================

class ExtendedDegreePattern:
    """Second-order degree pattern around a vertex in a triangulation."""

    __slots__ = ('center', 'neighbors', 'ext_features', '_hash', '_base')

    def __init__(self, center: int, neighbors: Tuple[int, ...],
                 ext_features: Tuple[Optional[SecondOrderFeature], ...]):
        self.center = center
        self.neighbors = neighbors
        self.ext_features = ext_features
        self._hash = hash((center, neighbors, ext_features))
        self._base = DegreePattern(center, neighbors)

    @property
    def base_pattern(self) -> DegreePattern:
        return self._base

    @property
    def k(self) -> int:
        return len(self.neighbors)

    def left(self, i: int) -> int:
        return self.neighbors[(i - 1) % self.k]

    def right(self, i: int) -> int:
        return self.neighbors[(i + 1) % self.k]

    def count_major(self, thr: int = 7) -> int:
        return sum(1 for d in self.neighbors if d >= thr)

    def count_deg6(self) -> int:
        return sum(1 for d in self.neighbors if d == 6)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExtendedDegreePattern):
            return NotImplemented
        return (self.center == other.center
                and self.neighbors == other.neighbors
                and self.ext_features == other.ext_features)

    def __hash__(self) -> int:
        return self._hash

    def __repr__(self) -> str:
        parts = []
        for d, f in zip(self.neighbors, self.ext_features):
            if f is not None:
                parts.append(f"{d}{f}")
            else:
                parts.append(str(d))
        return f"EDP({self.center}; {','.join(parts)})"

    def to_dict(self) -> dict:
        feats = []
        for f in self.ext_features:
            if f is None:
                feats.append(None)
            else:
                feats.append({'n5': f.n_ext_5, 'n6': f.n_ext_6, 'nm': f.n_ext_major})
        return {
            'center': self.center,
            'neighbors': list(self.neighbors),
            'ext_features': feats,
        }


# ======================================================================
# Cascade engine
# ======================================================================

class CascadeEngine:
    """Evaluate charge with cascade consistency for second-order patterns.

    Two-phase model:
      Phase 1: Centre (deg-5) sends charge to ring neighbours via rules.
      Phase 2: Each deg-6 ring neighbour must forward received charge.

    Parameters:
        alpha: Charge received per external deg-5 neighbour (default 1/5).
        beta:  Charge forwarded per major neighbour available (default 1/5).
    """

    def __init__(self, rules: List[DischargingRule],
                 alpha: Fraction = Fraction(1, 5),
                 beta: Fraction = Fraction(1, 5),
                 min_deg: int = 5, max_deg: int = 12):
        self.rules = rules
        self.alpha = alpha
        self.beta = beta
        self.min_deg = min_deg
        self.max_deg = max_deg
        self._fo_engine = DischargingEngine(rules, min_deg, max_deg)

    def transfer_to_neighbor(self, p: DegreePattern, i: int) -> Fraction:
        """Total charge transferred from centre to neighbour[i] via all rules."""
        total = Fraction(0)
        for rule in self.rules:
            if rule.fires(p, i):
                total += rule.transfer
        return total

    def cascade_balance(self, ep: ExtendedDegreePattern) -> Dict[str, Any]:
        """Compute cascade balance for all neighbours.

        Returns:
            center_charge: Final charge of centre.
            neighbor_nets: List of (deg, net_charge, kind) per neighbour.
            cascade_ok: True iff every neighbour ends at charge ≤ 0.
            fully_discharged: center_ok AND cascade_ok.
        """
        base = ep.base_pattern
        center_charge = Fraction(6 - ep.center)
        neighbor_nets: List[Tuple[int, Fraction, str]] = []

        for i in range(ep.k):
            t = self.transfer_to_neighbor(base, i)
            center_charge -= t

            d_i = ep.neighbors[i]
            f_i = ep.ext_features[i]

            if d_i >= 7 or f_i is None:
                net = Fraction(6 - d_i) + t
                neighbor_nets.append((d_i, net, 'major'))
            else:
                incoming = t + f_i.n_ext_5 * self.alpha
                n_ring_major = ((1 if ep.left(i) >= 7 else 0)
                                + (1 if ep.right(i) >= 7 else 0))
                n_total_major = n_ring_major + f_i.n_ext_major
                outgoing = n_total_major * self.beta
                net = incoming - outgoing
                neighbor_nets.append((d_i, net, 'cascade'))

        worst_idx = max(range(ep.k), key=lambda j: neighbor_nets[j][1])
        cascade_ok = all(nb[1] <= 0 for nb in neighbor_nets)
        center_ok = center_charge <= 0

        return {
            'center_charge': center_charge,
            'neighbor_nets': neighbor_nets,
            'cascade_ok': cascade_ok,
            'center_ok': center_ok,
            'fully_discharged': cascade_ok and center_ok,
            'worst_idx': worst_idx,
            'worst_charge': neighbor_nets[worst_idx][1],
        }

    # ── Enumeration ─────────────────────────────────────────────────────

    def enumerate_extended(self,
                           center_degrees: Optional[List[int]] = None,
                           no_adj_5: bool = True,
                           max_ext_5: int = 2,
                           need_cascade_only: bool = False,
                           ) -> List[ExtendedDegreePattern]:
        """Enumerate second-order patterns.

        Args:
            need_cascade_only: If True, only emit patterns that have at least
                one deg-6 neighbour (others have no cascade issue).
        """
        if center_degrees is None:
            center_degrees = [5]
        base_patterns = self._fo_engine.enumerate_patterns(center_degrees, no_adj_5)

        extended: List[ExtendedDegreePattern] = []
        for bp in base_patterns:
            has_deg6 = any(d == 6 for d in bp.neighbors)
            if need_cascade_only and not has_deg6:
                continue

            feature_lists: List[List[Optional[SecondOrderFeature]]] = []
            for d in bp.neighbors:
                if d == 6:
                    feature_lists.append(enumerate_ext_features(d, max_ext_5))  # type: ignore
                else:
                    feature_lists.append([None])

            for combo in product(*feature_lists):
                extended.append(ExtendedDegreePattern(
                    bp.center, bp.neighbors, tuple(combo)))

        return extended

    # ── Unavoidable-set computation ─────────────────────────────────────

    def compute_unavoidable(self, **kwargs) -> Tuple[List[ExtendedDegreePattern], Dict[str, Any]]:
        """Compute the second-order unavoidable set."""
        t0 = time.time()
        all_pats = self.enumerate_extended(**kwargs)

        unavoidable: List[ExtendedDegreePattern] = []
        center_only = cascade_only = both_fail = 0

        for ep in all_pats:
            res = self.cascade_balance(ep)
            if not res['fully_discharged']:
                unavoidable.append(ep)
                c_ok, cas_ok = res['center_ok'], res['cascade_ok']
                if not c_ok and not cas_ok:
                    both_fail += 1
                elif not c_ok:
                    center_only += 1
                else:
                    cascade_only += 1

        elapsed = time.time() - t0

        # Charge distribution among unavoidable
        charge_dist: Dict[str, int] = {}
        for ep in unavoidable:
            res = self.cascade_balance(ep)
            key = str(res['worst_charge'])
            charge_dist[key] = charge_dist.get(key, 0) + 1

        stats: Dict[str, Any] = {
            'total_second_order': len(all_pats),
            'unavoidable_count': len(unavoidable),
            'center_only_fail': center_only,
            'cascade_only_fail': cascade_only,
            'both_fail': both_fail,
            'charge_distribution': charge_dist,
            'elapsed': elapsed,
        }
        return unavoidable, stats

    # ── Analysis with first-order baseline ──────────────────────────────

    def comparative_analysis(self) -> Dict[str, Any]:
        """Run analysis and compare first-order vs second-order."""
        fo_pats = self._fo_engine.enumerate_patterns(center_degrees=[5])
        fo_unavoidable = [p for p in fo_pats
                          if self._fo_engine.compute_final_charge(p) > 0]

        so_unavoidable, so_stats = self.compute_unavoidable()

        # Group second-order unavoidable by their first-order base pattern
        base_groups: Dict[Tuple[int, Tuple[int, ...]], int] = {}
        for ep in so_unavoidable:
            key = (ep.center, ep.neighbors)
            base_groups[key] = base_groups.get(key, 0) + 1

        return {
            'first_order': {
                'total_patterns': len(fo_pats),
                'unavoidable_count': len(fo_unavoidable),
            },
            'second_order': so_stats,
            'distinct_base_patterns_in_unavoidable': len(base_groups),
            'base_pattern_distribution': {
                str(DegreePattern(k[0], k[1])): v
                for k, v in sorted(base_groups.items(), key=lambda x: -x[1])[:20]
            },
        }


# ======================================================================
# Main analysis
# ======================================================================

def run_cascade_analysis(name: str, rules: List[DischargingRule],
                         alpha: Fraction = Fraction(1, 5),
                         beta: Fraction = Fraction(1, 5),
                         max_deg: int = 12,
                         verbose: bool = True) -> Dict[str, Any]:
    """Run second-order cascade analysis with a given rule set."""
    engine = CascadeEngine(rules, alpha=alpha, beta=beta, max_deg=max_deg)
    result = engine.comparative_analysis()

    if verbose:
        fo = result['first_order']
        so = result['second_order']
        print(f"\n{'=' * 65}")
        print(f"Rule set: {name}  (α={alpha}, β={beta})")
        print(f"{'=' * 65}")
        print(f"First-order:  {fo['total_patterns']:>7d} patterns, "
              f"|U₁| = {fo['unavoidable_count']}")
        print(f"Second-order: {so['total_second_order']:>7d} patterns, "
              f"|U₂| = {so['unavoidable_count']}")
        print(f"  ├─ centre-only fail:  {so['center_only_fail']}")
        print(f"  ├─ cascade-only fail: {so['cascade_only_fail']}")
        print(f"  └─ both fail:         {so['both_fail']}")
        print(f"Distinct base patterns in U₂: {result['distinct_base_patterns_in_unavoidable']}")
        print(f"Elapsed: {so['elapsed']:.2f}s")

        if result['base_pattern_distribution']:
            print(f"\nTop base patterns in unavoidable set:")
            for pat, cnt in list(result['base_pattern_distribution'].items())[:10]:
                print(f"  {pat:>35s}  → {cnt:>5d} second-order extensions")

    return result


def main() -> None:
    print("=" * 65)
    print("SECOND-ORDER CASCADE DISCHARGING FRAMEWORK")
    print("Agent 1545-M3 / Sub-task S2")
    print("=" * 65)

    rule_sets = {
        "Standard (6 rules)": build_standard_rules(),
        "Extended (12 rules)": build_extended_rules(),
        "RSST-style (32 rules)": build_rsst_rules(),
    }

    all_results: Dict[str, Any] = {}
    for name, rules in rule_sets.items():
        all_results[name] = run_cascade_analysis(name, rules)

    # Sensitivity to cascade parameters
    print(f"\n{'=' * 65}")
    print("SENSITIVITY ANALYSIS — varying α and β")
    print(f"{'=' * 65}")
    rsst = build_rsst_rules()
    for alpha_n, alpha_d in [(1, 5), (1, 10), (3, 20)]:
        for beta_n, beta_d in [(1, 5), (1, 10), (3, 20)]:
            a, b = Fraction(alpha_n, alpha_d), Fraction(beta_n, beta_d)
            eng = CascadeEngine(rsst, alpha=a, beta=b)
            _, stats = eng.compute_unavoidable()
            print(f"  α={a}, β={b}  →  |U₂| = {stats['unavoidable_count']:>6d}  "
                  f"(cascade_fail={stats['cascade_only_fail']})")

    # Summary
    print(f"\n{'=' * 65}")
    print("SUMMARY")
    print(f"{'=' * 65}")
    print(f"{'Rule set':<26s} {'|U₁|':>5s} {'|U₂|':>7s} {'Distinct':>8s}")
    print("-" * 50)
    for name, res in all_results.items():
        fo_u = res['first_order']['unavoidable_count']
        so_u = res['second_order']['unavoidable_count']
        distinct = res['distinct_base_patterns_in_unavoidable']
        print(f"{name:<26s} {fo_u:>5d} {so_u:>7d} {distinct:>8d}")
    print(f"\nRSST reference: 633 configurations (ring sizes 5-14)")
    print("Note: |U₂| counts second-order patterns; 'Distinct' counts")
    print("unique first-order base patterns that appear in U₂.")

    # Export
    out_path = Path(__file__).resolve().parent / "second_order_results.json"
    export: Dict[str, Any] = {}
    for name, res in all_results.items():
        export[name] = {
            'first_order_unavoidable': res['first_order']['unavoidable_count'],
            'second_order_total': res['second_order']['total_second_order'],
            'second_order_unavoidable': res['second_order']['unavoidable_count'],
            'distinct_base': res['distinct_base_patterns_in_unavoidable'],
            'cascade_only_fail': res['second_order']['cascade_only_fail'],
        }
    with open(out_path, 'w') as f:
        json.dump(export, f, indent=2)
    print(f"\nResults → {out_path}")


if __name__ == '__main__':
    main()
