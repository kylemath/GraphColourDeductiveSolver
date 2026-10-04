# Gate: S1 Colin de Verdière

**Date:** 2 October 2026
**Report:** `backgroundMaterial/agent1720/groups/S1_report.md`
**Checked against:** `backgroundMaterial/agent1720/groups/S1_results.json` (`all_ok` true)

## Accepted as a reformulation

The case "\(\mu(G) \le 3\) implies \(\chi(G) \le \mu(G)+1\)" is equivalent to the Four Colour Theorem, given theorems this repository does not prove: \(\mu(G) \le 3\) if and only if \(G\) is planar, minor-monotonicity, \(\mu(K_t) \ge t-1\), and 3-colourability of \(K_4\)-minor-free graphs. One direction is immediate from planarity. The other uses that a graph of chromatic number at least 4 has a \(K_4\) minor, so \(\mu \ge 3\), and the Four Colour Theorem then gives \(\chi \le 4 = \mu+1\).

Track 5 is not killed and not proved. The inequality for \(\mu \le 4\) is cited as a consequence of Hadwiger's conjecture for \(K_6\), which uses the Four Colour Theorem. The case \(\mu \ge 5\) stays open and is a strengthening.

## Accepted as a computation

\(-J\) on \(K_4\) and \(-A\) on the octahedron satisfy the sign pattern, have corank 3 and one negative eigenvalue, and pass the Strong Arnold test (rank 6 over \(\mathbb{Q}\)). So \(\mu(K_4) \ge 3\) and \(\mu(O) \ge 3\). Wall clock 0.08s. Inertia is numerical. This does not prove \(\mu \le 3\) for every planar graph.
