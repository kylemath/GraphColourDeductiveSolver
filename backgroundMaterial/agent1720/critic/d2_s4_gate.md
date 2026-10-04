# Gate: D2 and S4

**Date:** 2 October 2026

## D2 — accepted

`penrose_eval` returns a Tait count. It does not use a sign. On every cached triangulation with \(n \le 11\), the Levi-Civita sign-sum of the plane dual equals \((-1)^n\) times the Tait count. `mismatches` is empty. Elapsed 0.81s. \(K_{3,3}\) cancels for all 64 rotation systems (sign-sum 0, Tait count 12). Track 4, read as non-vanishing of that evaluation, is Tait's reformulation of the Four Colour Theorem.

The library flags the Pappus graph as planar. It is not. That bug is recorded. It does not affect the triangulation census.

## S4 — accepted as recommendations, not proofs

Three routes, each feasibility Low:

- Hajós at \(k=5\): every graph with no \(K_5\) subdivision is 4-colourable. Catlin killed the cases \(k \ge 7\). No counterexample among 1253 graphs of order at most 7 (66 are not 4-colourable, and each has a \(K_5\) subdivision) or among the 1555 cached triangulations. Elapsed 25.2s.
- Odd Hadwiger at \(t=5\) only. The general statement is cited as killed; this case is not opened as a proof.
- Every snark has a Petersen minor. This is stronger than the Tait restatement that every snark is non-planar.

Hadwiger for \(K_5\) and the Penrose evaluation are restatements. Tait's claim that every planar cubic polyhedral graph is Hamiltonian is false (Tutte, 1946).

The icosahedron is a triangulation of minimum degree 5. The sentence "every planar triangulation has a vertex of degree at most 4" is dead.

West's note on Eulerian triangulations was not downloaded: the server did not connect within 75 seconds.
