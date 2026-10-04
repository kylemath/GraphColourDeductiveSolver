# A1 — Chromatic polynomials and real roots in $(3,4)$

**Group:** A1, manager M-Algebra
**Date:** 2 October 2026
**Status:** computed on every planar triangulation with $n \le 11$. Not a theorem. The root-bounding approach is killed. This does not kill $P(G,4) > 0$.

## 1. Definitions

Let $T_{n,i}$ be the triangulation `graphs[str(n)][i]` in `compute/data/triangulations_n4_11.json` (plantri counts $1,1,2,5,14,50,233,1249$ for $n = 4,\ldots,11$). Write $a_j$ for the number of partitions of $V$ into $j$ nonempty independent sets, and
\[
P(G,k) = \sum_j a_j\, k(k-1)\cdots(k-j+1).
\]
Real roots are isolated exactly by sympy (`Poly.intervals`, width at most $10^{-15}$). A root in the open interval $(3,4)$ is a Sturm count on $[3,4]$ with the endpoints removed. Tutte's golden identity is checked in $\mathbb{Q}(\sqrt{5})$:
\[
P(T,\varphi+2) = (\varphi+2)\,\varphi^{3n-10}\, P(T,\varphi+1)^2,
\]
where $\varphi = (1+\sqrt{5})/2$, and again by sympy radical simplification. Implementation: `compute/chromatic/a1720_chromatic_db.py`. Stored output: `compute/data/chromatic_polys_n4_11.json`. This report reads `validation`, `summary`, `timing_seconds`, and the record `T_8_13` only.

## 2. Statement

**Computed, for every triangulation on $4 \le n \le 11$ vertices.** $P(G,4) > 0$, the value equals a brute-force colouring count, $P(G,4)/24 = a_3 + a_4$, both golden-identity checks hold, and no non-integer real root is $\ge 4$.

The number of graphs with at least one distinct real root in $(3,4)$ is $0$ for $n \le 7$, then $1,2,22,138$ for $n = 8,9,10,11$.

## 3. Evidence

The database was already computed. It was not rebuilt. Wall clock stored in `timing_seconds` is $39.219$ seconds in total (about $39.2$s), of which $n = 11$ is $29.51$s. Validation flags `K4`, octahedron, icosahedron ($P(4)$, $P(5)$ against brute force, and the golden identity), Petersen, $C_5$, and the wheel on $6$ vertices are all true.

| $n$ | graphs | root in $(3,4)$ | largest non-integer root below $4$ | graph |
|---|---|---|---|---|
| 4 | 1 | 0 | — | — |
| 5 | 1 | 0 | — | — |
| 6 | 2 | 0 | $2.547$ | $T_{6,1}$ |
| 7 | 5 | 0 | $2.678$ | $T_{7,4}$ |
| 8 | 14 | 1 | $3.606$ | $T_{8,13}$ |
| 9 | 50 | 2 | $3.606$ | $T_{9,43}$ |
| 10 | 233 | 22 | $3.606$ | $T_{10,188}$ |
| 11 | 1249 | 138 | $3.617$ | $T_{11,1244}$ |

Witness $T_{8,13}$: `distinct_roots_in_open_3_4` $= 1$, largest non-integer root below $4$ is $3.6064627075993836$, isolating interval
\[
\Bigl[\frac{172205197}{47749058},\; \frac{149476032}{41446715}\Bigr],
\]
and $P(T_{8,13},4) = 72$. The closest root in the database is on $T_{11,1244}$, about $3.617413$.

**Literature.** Gordon F. Royle, *Planar triangulations with real chromatic roots arbitrarily close to four*, arXiv:math/0511304, https://arxiv.org/abs/math/0511304. The abstract states that there are infinite families of planar graphs with real chromatic roots arbitrarily close to $4$. The same search returns the 2008 journal version, https://link.springer.com/article/10.1007/s00026-008-0347-0.

## 4. Result

**Computed** on all triangulations with $n \le 11$. Not a theorem.

## 5. Kill criterion

Track 2's kill criterion — one real chromatic root in $(3,4)$ kills the root-bounding approach — **is met**. The finite witness is $T_{8,13}$. Royle's theorem confirms there is no uniform gap between real chromatic roots of planar triangulations and $4$.

This does **not** kill $P(G,4) > 0$. Every graph in the database has $P(G,4) > 0$, and positivity at the integer $4$ is the Four Colour Theorem for these triangulations.

## 6. Not proved

No statement about all planar triangulations was proved. Absence of non-integer roots $\ge 4$ is only the range $n \le 11$. The computation does not prove, and does not refute, $P(G,4) > 0$ for every planar triangulation.

## 7. Feasibility

**Low** for any root-bounding proof that real chromatic roots of planar triangulations stay $\le 4 - \delta$ for a fixed $\delta > 0$.

## 8. Next steps

Stop the root-bounding approach. Keep positivity $P(G,4) > 0$ for restricted families as a separate task (A2).
