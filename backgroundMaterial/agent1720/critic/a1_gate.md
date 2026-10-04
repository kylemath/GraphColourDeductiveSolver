# Gate: A1 chromatic roots

**Date:** 2 October 2026
**Meeting:** critic with the main planning team
**Report:** `backgroundMaterial/agent1720/groups/A1_report.md`
**Checked against:** `compute/data/chromatic_polys_n4_11.json`, record `T_8_13`

## Accepted

The root-bounding approach is a dead end. `T_8_13` has one real chromatic root in the open interval $(3,4)$, isolating interval $[172205197/47749058,\, 149476032/41446715]$, and $P(T_{8,13},4) = 72$. The database counts of graphs with such a root are $0,0,0,0,1,2,22,138$ for $n = 4,\ldots,11$. Royle's theorem (arXiv:math/0511304) is cited for the infinite statement. The finite witness alone meets Track 2's written kill criterion.

## Refused

- Killing Track 2, or killing $P(G,4) > 0$. Every triangulation in the database has $P(G,4) > 0$. Positivity at the integer $4$ is still the Four Colour Theorem.
- Calling the $n \le 11$ positivity check a theorem.
- Calling the absence of non-integer roots $\ge 4$ a theorem. That absence is only the computed range.

## Left open

A2, positivity for restricted families, was not delivered in this gate. The Kempe reports are not in yet and are not gated here.
