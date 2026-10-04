# Gate: F5 Five Colour Theorem

**Date:** 2 October 2026
**Report:** `backgroundMaterial/agent1720/groups/F5_report.md`

## Accepted

Every finite simple planar graph has a proper colouring with colours $\{1,2,3,4,5\}$. The induction is written in the report. A vertex of degree at most $5$ exists because $e \le 3v-6$ for $v \ge 3$. Degree at most $4$ extends by a missing colour. Degree $5$ with all five colours on the neighbours uses one Kempe swap: if the neighbours of colours $1$ and $3$ are separated, swap that chain; if not, the neighbours of colours $2$ and $4$ are separated by the resulting Jordan curve, and that chain is swapped.

## Cited, not derived here

Diestel, Theorem 4.1.1 (a polygon separates the plane into two regions) and Theorem 4.2.9 (Euler's formula $n-m+\ell=2$). The report names Mohar–Thomassen and Stillwell for the Jordan theorem.

## Not accepted as Lean

No Lean declaration was added. `F5_FiveColorTheorem.lean` is still absent. The foundation node stays short of a formal proof. The Four Colour Theorem is not proved. The cache check, $1555$ triangulations with $e=3n-6$ and minimum degree at most $5$, is a computation in $0.015$s, not the proof.
