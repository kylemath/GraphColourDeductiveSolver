# Gate: D3 sign identity

**Date:** 2 October 2026
**Report:** `backgroundMaterial/agent1720/groups/D3_report.md` §3
**Checked against:** `compute/flows/a1720_alon_tarsi.py` (`local_lemma`, `orientation_audit`) and `D3_results.json`

## Accepted

For every triangulation on \(n \ge 4\) vertices, every Tait colouring of the dual has sign \((-1)^n\). The signed count equals \((-1)^n\) times the Tait count.

The 24 ordered triples of distinct Klein colours satisfy \(\varepsilon = \sigma \cdot (-1)^{\alpha+\beta+\gamma}\). `local_lemma` checks them and is called from `self_test` in the run that wrote `D3_results.json`. The cut between odd labels \(\{1,3\}\) and even labels \(\{0,2\}\) has size \(2n-4\), so the parity product is \(+1\). Each undirected edge descends in exactly one direction, there are \(3n-6\) edges, and the number of faces \(2n-4\) is even, so the product of the face signs is \((-1)^n\).

Facial triangles of a connected plane graph generate the cycle space over \(\mathbb{F}_2\), up to the one relation that the sum of all faces is zero. Every face has Klein colour-sum zero, so a Tait colouring is a coboundary. The write-up uses that generation as a standard fact about plane graphs.

The orientation audit on one 4-colouring of each of the 1555 cached triangulations with \(n \le 11\) returned no failures (0.808s). The full Tait census for \(n \le 8\) has no mixed signs. Those checks agree with the identity. They are not the proof.

## Not proved

A Tait colouring of an arbitrary triangulation dual is not shown to exist. The signed count is nonzero exactly when a colouring exists, so the identity restates the Four Colour Theorem in Tait's form. Ellingham–Goddyn 1996 is a consequence for graphs that are already 3-edge-coloured. It is not re-proved here.
