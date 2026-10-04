# Gate: A3 Eulerian triangulations

**Date:** 2 October 2026
**Report:** `backgroundMaterial/agent1720/groups/A3_report.md`
**Checked against:** `A3_results.json` and `compute/data/chromatic_polys_n4_11.json`

## Accepted

A simple plane triangulation on at least 3 vertices is properly 3-vertex-colourable if and only if every degree is even.

Necessity: the link of a vertex is a cycle whose colours alternate between the two colours other than the vertex colour, so the degree is even.

Sufficiency: even degrees make the dual bipartite, so the faces are 2-coloured. Orient each edge with black on the left. The signed length of every facial walk is a multiple of 3, and the same holds for every cycle by cancelling interior edges. Colours in $\mathbb{Z}/3\mathbb{Z}$ are then well-defined by walking from a base vertex, and adjacent vertices differ by $\pm 1$.

The embedding fact used for the dual is stated in the report: a cycle bounds a union of faces. It is not derived from the Jordan theorem in this file.

## Computation

All 1555 cached triangulations agree. The seven with every degree even are $T_{6,1}$, $T_{8,12}$, $T_{9,47}$, $T_{10,221}$, $T_{10,226}$, $T_{11,1220}$, $T_{11,1242}$. Each has $P(G,3)=6$ in the chromatic database. No triangulation with an odd degree in the cache is 3-colourable. Elapsed 0.051s.

## Not proved

This is not the Four Colour Theorem. The same orientation does not 3-colour an Eulerian plane graph that has a face whose length is not a multiple of 3.
