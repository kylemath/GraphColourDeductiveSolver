# Gate: A2 degeneracy positivity

**Date:** 2 October 2026
**Report:** `backgroundMaterial/agent1720/groups/A2_report.md`
**Spot-check:** stored \(T_{6,1}\) has \(P(4)=96\), \(P(5)=780\), \(P(6)=4080\).

## Proved in the report

- A \(d\)-degenerate graph on \(n\) vertices satisfies \(P(G,k) \ge \prod_{i=1}^{n}(k-\min(d,i-1))\) for integers \(k \ge d\), hence \(P(G,k)>0\) for integers \(k \ge d+1\).
- Every outerplanar graph is \(2\)-degenerate, and a maximal outerplanar graph on \(n \ge 3\) vertices is a \(2\)-tree with \(P(G,k)=k(k-1)(k-2)^{n-2}\). So \(P(G,4)>0\).
- Every series-parallel graph, in the two-terminal sense used in the report, is \(2\)-degenerate. So \(P(G,4)>0\).
- Every simple planar graph is \(5\)-degenerate, so \(P(G,k)>0\) for integers \(k \ge 6\). Every simple planar graph on at most \(11\) vertices is \(4\)-degenerate, so \(P(G,k)>0\) for integers \(k \ge 5\).
- Every \(3\)-tree, including every stacked triangulation, satisfies \(P(G,k)=k(k-1)(k-2)(k-3)^{n-3}\), so \(P(G,4)=24\).

## Not proved

\(P(G,4)>0\) for every planar graph. That is the Four Colour Theorem. \(P(G,5)>0\) for every planar graph is Heawood's Five Colour Theorem and is only cited. The spot-check shows the degeneracy product at \(k=4\) can be \(0\) while \(P(G,4)\) is still positive: on the octahedron the product is \(0\) and \(P=96\).
