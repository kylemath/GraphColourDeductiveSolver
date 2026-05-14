"""
framework.py — Discharging framework for Four Colour Theorem proof optimization.

Given a set of discharging rules, computes the set of first-order degree patterns
around vertices that retain positive charge after redistribution. These patterns
form the "unavoidable set" in the classical 4CT proof.

Convention:
  c(v) = 6 - deg(v)            Initial charge at vertex v.
  Total charge = 12            By Euler's formula for planar triangulations.
  Positive transfer = center SENDS charge to neighbor (center's charge decreases).
  Unavoidable set = degree patterns where final charge > 0.

In a minimum counterexample (triangulation, minimum degree 5):
  - Degree-5 vertices have c = 1 (positive, need to discharge)
  - Degree-6 vertices have c = 0 (neutral)
  - Degree-7+ vertices have c < 0 (sinks for charge)
  - No two adjacent degree-5 vertices (this is a reducible configuration)

Agent 1520-M3 / Sub-task S1
"""

from __future__ import annotations

from typing import List, Tuple, Callable, Dict, Optional, Set, Any
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from collections import Counter
import json
import time


# --------------------------------------------------------------------------
# Canonical form utilities
# --------------------------------------------------------------------------

def canonical_necklace(seq: Tuple[int, ...]) -> Tuple[int, ...]:
    """Lexicographically smallest representative under cyclic rotation + reflection.

    Uses bracelet equivalence: two sequences are equivalent if one is a
    cyclic rotation or reversal of the other. In a planar triangulation the
    embedding is unique up to orientation (Whitney), so reflections are valid.
    """
    n = len(seq)
    if n <= 1:
        return seq
    best = seq
    rev = seq[::-1]
    for s in (seq, rev):
        for i in range(n):
            rotated = s[i:] + s[:i]
            if rotated < best:
                best = rotated
    return best


# --------------------------------------------------------------------------
# DegreePattern
# --------------------------------------------------------------------------

class DegreePattern:
    """First-order degree pattern around a vertex in a triangulation.

    In a triangulation the link of a vertex is a cycle, so consecutive
    entries in `neighbors` are always adjacent.
    """
    __slots__ = ('center', 'neighbors', '_hash')

    def __init__(self, center: int, neighbors: Tuple[int, ...]):
        self.center = center
        self.neighbors = neighbors
        self._hash = hash((center, neighbors))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DegreePattern):
            return NotImplemented
        return self.center == other.center and self.neighbors == other.neighbors

    def __hash__(self) -> int:
        return self._hash

    def __repr__(self) -> str:
        return f"DP({self.center}; {','.join(map(str, self.neighbors))})"

    @property
    def k(self) -> int:
        return len(self.neighbors)

    def left(self, i: int) -> int:
        return self.neighbors[(i - 1) % self.k]

    def right(self, i: int) -> int:
        return self.neighbors[(i + 1) % self.k]

    def count_major(self, threshold: int = 7) -> int:
        return sum(1 for d in self.neighbors if d >= threshold)

    def count_minor(self, threshold: int = 7) -> int:
        return sum(1 for d in self.neighbors if d < threshold)

    def has_flanking_major(self, i: int, thr: int = 7) -> bool:
        return self.left(i) >= thr or self.right(i) >= thr

    def has_both_flanking_major(self, i: int, thr: int = 7) -> bool:
        return self.left(i) >= thr and self.right(i) >= thr

    def consecutive_minor_run(self, thr: int = 7) -> int:
        """Length of the longest run of consecutive minor (< thr) neighbors."""
        if self.k == 0:
            return 0
        doubled = self.neighbors + self.neighbors
        best = 0
        run = 0
        for d in doubled:
            if d < thr:
                run += 1
                best = max(best, run)
            else:
                run = 0
        return min(best, self.k)

    def canonical(self) -> DegreePattern:
        return DegreePattern(self.center, canonical_necklace(self.neighbors))

    def degree_histogram(self) -> Dict[int, int]:
        return dict(Counter(self.neighbors))

    def feature_vector(self) -> Dict[str, Any]:
        """Extract numerical features for clustering / analysis."""
        hist = self.degree_histogram()
        return {
            'center': self.center,
            'k': self.k,
            'n_major': self.count_major(),
            'n_minor': self.count_minor(),
            'min_nbr': min(self.neighbors),
            'max_nbr': max(self.neighbors),
            'mean_nbr': sum(self.neighbors) / self.k,
            'deg6_count': hist.get(6, 0),
            'deg7_count': hist.get(7, 0),
            'deg8plus_count': sum(v for k_, v in hist.items() if k_ >= 8),
            'max_minor_run': self.consecutive_minor_run(),
        }

    def to_dict(self) -> dict:
        return {'center': self.center, 'neighbors': list(self.neighbors)}

    @staticmethod
    def from_dict(d: dict) -> DegreePattern:
        return DegreePattern(d['center'], tuple(d['neighbors']))


# --------------------------------------------------------------------------
# DischargingRule
# --------------------------------------------------------------------------

@dataclass
class DischargingRule:
    """Conditional charge transfer from center vertex to neighbor[i].

    condition(pattern, i) -> True if the rule fires on edge (center, neighbor[i]).
    transfer > 0 means center SENDS charge (center's charge decreases).
    """
    name: str
    condition: Callable[[DegreePattern, int], bool]
    transfer: Fraction

    def fires(self, pattern: DegreePattern, i: int) -> bool:
        return self.condition(pattern, i)


# --------------------------------------------------------------------------
# DischargingEngine
# --------------------------------------------------------------------------

class DischargingEngine:
    """Evaluate charges and compute unavoidable sets."""

    def __init__(self, rules: List[DischargingRule],
                 min_deg: int = 5, max_deg: int = 12):
        self.rules = rules
        self.min_deg = min_deg
        self.max_deg = max_deg

    def initial_charge(self, deg: int) -> Fraction:
        return Fraction(6 - deg)

    def compute_final_charge(self, p: DegreePattern) -> Fraction:
        c = self.initial_charge(p.center)
        for i in range(p.k):
            for rule in self.rules:
                if rule.fires(p, i):
                    c -= rule.transfer
        return c

    def transfer_breakdown(self, p: DegreePattern) -> Dict[str, Fraction]:
        """Per-rule total transfer for a pattern (debugging / analysis)."""
        bd: Dict[str, Fraction] = {}
        for rule in self.rules:
            total = Fraction(0)
            for i in range(p.k):
                if rule.fires(p, i):
                    total += rule.transfer
            if total:
                bd[rule.name] = total
        return bd

    # ----- enumeration -----

    def enumerate_patterns(self,
                           center_degrees: Optional[List[int]] = None,
                           no_adj_5: bool = True) -> List[DegreePattern]:
        """Enumerate canonical bracelet degree patterns."""
        if center_degrees is None:
            center_degrees = [5]

        patterns: List[DegreePattern] = []
        seen: Set[Tuple[int, Tuple[int, ...]]] = set()

        for d in center_degrees:
            lo = 6 if (no_adj_5 and d == 5) else self.min_deg
            for nbrs in product(range(lo, self.max_deg + 1), repeat=d):
                canon = canonical_necklace(nbrs)
                key = (d, canon)
                if key not in seen:
                    seen.add(key)
                    patterns.append(DegreePattern(d, canon))

        return patterns

    def compute_unavoidable_set(self,
                                center_degrees: Optional[List[int]] = None,
                                no_adj_5: bool = True) -> List[DegreePattern]:
        """Return degree patterns with positive final charge."""
        return [p for p in self.enumerate_patterns(center_degrees, no_adj_5)
                if self.compute_final_charge(p) > 0]

    def full_analysis(self,
                      center_degrees: Optional[List[int]] = None,
                      no_adj_5: bool = True) -> Dict[str, Any]:
        """Run complete analysis; return stats dict."""
        t0 = time.time()
        all_pats = self.enumerate_patterns(center_degrees, no_adj_5)
        unavoidable = []
        charges: Dict[DegreePattern, Fraction] = {}

        for p in all_pats:
            c = self.compute_final_charge(p)
            charges[p] = c
            if c > 0:
                unavoidable.append(p)

        elapsed = time.time() - t0

        charge_dist: Dict[str, int] = {}
        major_dist: Dict[int, int] = Counter()
        for p in unavoidable:
            cs = str(charges[p])
            charge_dist[cs] = charge_dist.get(cs, 0) + 1
            major_dist[p.count_major()] += 1

        return {
            'total_patterns': len(all_pats),
            'unavoidable_count': len(unavoidable),
            'unavoidable': unavoidable,
            'charges': charges,
            'charge_distribution': charge_dist,
            'major_distribution': dict(major_dist),
            'elapsed': elapsed,
        }


# --------------------------------------------------------------------------
# Rule-set builders
# --------------------------------------------------------------------------

def build_basic_rules() -> List[DischargingRule]:
    """R1 only: send 1/5 to each major (degree >= 7) neighbor."""
    return [
        DischargingRule(
            "R1: 1/5 → major nbr",
            lambda p, i: p.center == 5 and p.neighbors[i] >= 7,
            Fraction(1, 5)),
    ]


def build_standard_rules() -> List[DischargingRule]:
    """Six rules inspired by RSST structure."""
    return [
        DischargingRule(
            "R1: 1/5 → major nbr",
            lambda p, i: p.center == 5 and p.neighbors[i] >= 7,
            Fraction(1, 5)),
        DischargingRule(
            "R2: 1/10 → deg-6 flanked by major",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.has_flanking_major(i)),
            Fraction(1, 10)),
        DischargingRule(
            "R3: 1/10 bonus → deg >= 9",
            lambda p, i: p.center == 5 and p.neighbors[i] >= 9,
            Fraction(1, 10)),
        DischargingRule(
            "R4: 1/10 → deg-6 doubly flanked",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.has_both_flanking_major(i)),
            Fraction(1, 10)),
        DischargingRule(
            "R5: 1/20 → deg-6 when >= 3 major",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.count_major() >= 3),
            Fraction(1, 20)),
        DischargingRule(
            "R6: 1/20 bonus → major when >= 4 major total",
            lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                          and p.count_major() >= 4),
            Fraction(1, 20)),
    ]


def build_extended_rules() -> List[DischargingRule]:
    """Twelve rules — more aggressive charge distribution."""
    rules = build_standard_rules()
    rules.extend([
        DischargingRule(
            "R7: 1/10 → isolated deg-6 (both neighbours also 6)",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.left(i) == 6 and p.right(i) == 6),
            Fraction(1, 10)),
        DischargingRule(
            "R8: 1/10 bonus → deg-8",
            lambda p, i: p.center == 5 and p.neighbors[i] == 8,
            Fraction(1, 10)),
        DischargingRule(
            "R9: 1/20 → any deg-6",
            lambda p, i: p.center == 5 and p.neighbors[i] == 6,
            Fraction(1, 20)),
        DischargingRule(
            "R10: 1/20 bonus → major when exactly 2 major",
            lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                          and p.count_major() == 2),
            Fraction(1, 20)),
        DischargingRule(
            "R11: 1/20 → deg-7 between two deg-6",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 7
                          and p.left(i) == 6 and p.right(i) == 6),
            Fraction(1, 20)),
        DischargingRule(
            "R12: 1/20 residual → any major",
            lambda p, i: p.center == 5 and p.neighbors[i] >= 7,
            Fraction(1, 20)),
    ])
    return rules


def build_rsst_rules() -> List[DischargingRule]:
    """32 discharging rules modeled on the RSST (1997) proof structure.

    Robertson-Sanders-Seymour-Thomas use 32 rules in their proof of the Four
    Colour Theorem.  The rules below are a principled reconstruction based on
    the published description and the known proof architecture, NOT a verbatim
    transcription.

    The rules are organized into four groups:
      A (R1-R8):  Degree-based transfer from deg-5 centre to major neighbours.
      B (R9-R16): Transfer to deg-6 neighbours based on flanking / position.
      C (R17-R24): Context rules depending on the centre's major-neighbour count.
      D (R25-R32): Fine-tuning rules for specific positional patterns.

    Convention: all rules fire additively.  The transfer amounts are chosen so
    that (a) every first-order pattern is fully discharged at the centre, and
    (b) the total transfer to any single neighbour stays within a reasonable
    range for cascade analysis.

    Reference: Robertson, Sanders, Seymour, Thomas, "The Four Colour Theorem",
               J. Combin. Theory Ser. B 70 (1997), 2-44.
    """
    rules: List[DischargingRule] = []

    # ── Group A: base transfer to major neighbours ──────────────────────

    rules.append(DischargingRule(
        "RSST-R1: 1/5 → major (≥7)",
        lambda p, i: p.center == 5 and p.neighbors[i] >= 7,
        Fraction(1, 5)))

    rules.append(DischargingRule(
        "RSST-R2: 1/20 bonus → deg≥8",
        lambda p, i: p.center == 5 and p.neighbors[i] >= 8,
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R3: 1/20 bonus → deg≥9",
        lambda p, i: p.center == 5 and p.neighbors[i] >= 9,
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R4: 1/10 bonus → deg≥10",
        lambda p, i: p.center == 5 and p.neighbors[i] >= 10,
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R5: 1/10 bonus → deg≥11",
        lambda p, i: p.center == 5 and p.neighbors[i] >= 11,
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R6: 1/20 bonus → major flanked by two minor",
        lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                      and p.left(i) < 7 and p.right(i) < 7),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R7: 1/20 bonus → deg-7 between two deg-6",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 7
                      and p.left(i) == 6 and p.right(i) == 6),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R8: 1/20 bonus → deg-8 flanked by a minor",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 8
                      and (p.left(i) < 7 or p.right(i) < 7)),
        Fraction(1, 20)))

    # ── Group B: transfer to deg-6 neighbours by flanking ───────────────

    rules.append(DischargingRule(
        "RSST-R9: 1/5 → deg-6 doubly flanked by major",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.has_both_flanking_major(i)),
        Fraction(1, 5)))

    rules.append(DischargingRule(
        "RSST-R10: 1/10 → deg-6 singly flanked by major",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.has_flanking_major(i)
                      and not p.has_both_flanking_major(i)),
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R11: 1/10 → deg-6 between two deg-6 (isolated)",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.left(i) == 6 and p.right(i) == 6),
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R12: 1/20 → any deg-6 (base residual)",
        lambda p, i: p.center == 5 and p.neighbors[i] == 6,
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R13: 1/20 → deg-6 in minor run ≥ 3",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.consecutive_minor_run() >= 3),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R14: 1/10 → deg-6 in minor run ≥ 4",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.consecutive_minor_run() >= 4),
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R15: 1/10 → deg-6 in minor run = 5 (all minor)",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.consecutive_minor_run() >= 5),
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R16: 1/20 → deg-6 when both flanking are also deg-6",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.left(i) <= 6 and p.right(i) <= 6),
        Fraction(1, 20)))

    # ── Group C: context rules (major-count dependent) ──────────────────

    rules.append(DischargingRule(
        "RSST-R17: 1/5 → every nbr when 0 major",
        lambda p, i: p.center == 5 and p.count_major() == 0,
        Fraction(1, 5)))

    rules.append(DischargingRule(
        "RSST-R18: 1/10 → deg-6 adj to major, when exactly 1 major",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.has_flanking_major(i)
                      and p.count_major() == 1),
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R19: 1/10 bonus → the unique major when exactly 1 major",
        lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                      and p.count_major() == 1),
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R20: 1/20 bonus → each major when exactly 2 major",
        lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                      and p.count_major() == 2),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R21: 1/20 → deg-6 when ≥3 major nbrs",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.count_major() >= 3),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R22: 1/20 bonus → each major when ≥3 major",
        lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                      and p.count_major() >= 3),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R23: 1/20 bonus → each major when ≥4 major",
        lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                      and p.count_major() >= 4),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R24: 1/20 → deg-6 flanked by major when ≥2 major",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.has_flanking_major(i)
                      and p.count_major() >= 2),
        Fraction(1, 20)))

    # ── Group D: fine-tuning positional rules ───────────────────────────

    rules.append(DischargingRule(
        "RSST-R25: 1/20 → deg-6 opposite unique major (not adj to it)",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.count_major() == 1
                      and not p.has_flanking_major(i)),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R26: 1/20 → deg-6 when exactly 2 major and deg-6 between them",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.has_both_flanking_major(i)
                      and p.count_major() == 2),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R27: 1/10 → deg-6 doubly flanked, minor run ≥ 2",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.has_both_flanking_major(i)
                      and p.consecutive_minor_run() >= 2),
        Fraction(1, 10)))

    rules.append(DischargingRule(
        "RSST-R28: 1/20 bonus → deg-8+ when flanked by two major",
        lambda p, i: (p.center == 5 and p.neighbors[i] >= 8
                      and p.left(i) >= 7 and p.right(i) >= 7),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R29: 1/20 → deg-6 when 3 consecutive deg-6 and flanked by major",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.has_flanking_major(i)
                      and p.consecutive_minor_run() >= 3),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R30: 1/20 → deg-6 when exactly 2 major, non-adjacent",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                      and p.count_major() == 2
                      and not p.has_flanking_major(i)),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R31: 1/20 bonus → deg-7 when ≥2 major and flanked by deg-6",
        lambda p, i: (p.center == 5 and p.neighbors[i] == 7
                      and p.count_major() >= 2
                      and (p.left(i) == 6 or p.right(i) == 6)),
        Fraction(1, 20)))

    rules.append(DischargingRule(
        "RSST-R32: 1/20 bonus → any major when minor run ≥ 4",
        lambda p, i: (p.center == 5 and p.neighbors[i] >= 7
                      and p.consecutive_minor_run() >= 4),
        Fraction(1, 20)))

    return rules


def build_aggressive_rules() -> List[DischargingRule]:
    """Twenty rules — pushes discharge as far as first-order info allows."""
    rules = build_extended_rules()
    rules.extend([
        DischargingRule(
            "R13: 1/5 → deg-6 when 0 major nbrs",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.count_major() == 0),
            Fraction(1, 5)),
        DischargingRule(
            "R14: 3/20 → deg-6 flanked by major, when >= 2 major",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.has_flanking_major(i) and p.count_major() >= 2),
            Fraction(3, 20)),
        DischargingRule(
            "R15: 1/10 → deg-6 when exactly 1 major",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.count_major() == 1),
            Fraction(1, 10)),
        DischargingRule(
            "R16: 1/5 → deg >= 10",
            lambda p, i: p.center == 5 and p.neighbors[i] >= 10,
            Fraction(1, 5)),
        DischargingRule(
            "R17: 3/20 bonus → deg-8 flanked by deg-6",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 8
                          and (p.left(i) == 6 or p.right(i) == 6)),
            Fraction(3, 20)),
        DischargingRule(
            "R18: 1/10 → deg-6 when minor run >= 3",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 6
                          and p.consecutive_minor_run() >= 3),
            Fraction(1, 10)),
        DischargingRule(
            "R19: 1/20 → any neighbor when >= 3 major",
            lambda p, i: p.center == 5 and p.count_major() >= 3,
            Fraction(1, 20)),
        DischargingRule(
            "R20: 1/10 → deg-7 when >= 3 major",
            lambda p, i: (p.center == 5 and p.neighbors[i] == 7
                          and p.count_major() >= 3),
            Fraction(1, 10)),
    ])
    return rules


# --------------------------------------------------------------------------
# Analysis driver
# --------------------------------------------------------------------------

def run_analysis(name: str, rules: List[DischargingRule],
                 max_deg: int = 12, verbose: bool = True) -> Dict[str, Any]:
    engine = DischargingEngine(rules, min_deg=5, max_deg=max_deg)
    result = engine.full_analysis(center_degrees=[5])

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"Rule set: {name}  ({len(rules)} rules)")
        print(f"{'=' * 60}")
        print(f"Neighbor degree range: 6 .. {max_deg}")
        print(f"Total canonical patterns:  {result['total_patterns']}")
        print(f"Unavoidable set size:      {result['unavoidable_count']}")
        print(f"Elapsed:                   {result['elapsed']:.3f}s")

        print(f"\n  Charge distribution (unavoidable):")
        for ch, cnt in sorted(result['charge_distribution'].items(),
                              key=lambda x: Fraction(x[0])):
            print(f"    c* = {ch:>6s}  :  {cnt:>5d} patterns")

        print(f"\n  Major-neighbor count (unavoidable):")
        for k_, cnt in sorted(result['major_distribution'].items()):
            print(f"    {k_} major  :  {cnt:>5d} patterns")

    result['rule_count'] = len(rules)
    result['name'] = name
    return result


def main() -> Dict[str, Any]:
    print("=" * 60)
    print("DISCHARGING FRAMEWORK — Four Colour Theorem")
    print("Agent 1520-M3 / Sub-task S1")
    print("=" * 60)

    results: Dict[str, Any] = {}

    for label, builder in [
        ("Basic (1 rule)", build_basic_rules),
        ("Standard (6 rules)", build_standard_rules),
        ("Extended (12 rules)", build_extended_rules),
        ("Aggressive (20 rules)", build_aggressive_rules),
    ]:
        results[label] = run_analysis(label, builder())

    # --- summary table ---
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    base = results["Basic (1 rule)"]['unavoidable_count']
    print(f"{'Rule set':<28s} {'#R':>3s} {'|U|':>6s} {'Reduction':>10s}")
    print("-" * 50)
    for label, res in results.items():
        n = res['unavoidable_count']
        pct = f"{100 * (1 - n / base):.1f}%" if base else "—"
        print(f"{label:<28s} {res['rule_count']:>3d} {n:>6d} {pct:>10s}")

    print(f"\nRSST reference: 633 configurations with 32 rules (max ring 14)")
    print("Note: degree-pattern count is a coarsening of full configurations.")
    print("Each pattern may correspond to multiple RSST-style configurations.")

    # --- export ---
    export_path = "/Users/kylemathewson/GraphColour/compute/discharging/analysis_results.json"
    export: Dict[str, Any] = {}
    for label, res in results.items():
        export[label] = {
            'rule_count': res['rule_count'],
            'total_patterns': res['total_patterns'],
            'unavoidable_count': res['unavoidable_count'],
            'charge_distribution': res['charge_distribution'],
            'major_distribution': {str(k_): v for k_, v in res['major_distribution'].items()},
        }
    with open(export_path, 'w') as f:
        json.dump(export, f, indent=2)
    print(f"\nResults written to {export_path}")

    # --- export unavoidable set for clustering ---
    ext_unavoidable = results["Extended (12 rules)"]['unavoidable']
    patterns_path = "/Users/kylemathewson/GraphColour/compute/discharging/unavoidable_patterns.json"
    with open(patterns_path, 'w') as f:
        json.dump([p.to_dict() for p in ext_unavoidable], f)
    print(f"Unavoidable patterns written to {patterns_path}")

    return results


if __name__ == '__main__':
    main()
