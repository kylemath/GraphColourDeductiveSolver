# K7 — KC5 on the Fritsch triangulation

**Group:** K7 (M-Kempe, Track 1). **Date:** 2 October 2026.
**Status:** finite check on one named graph. A finite check is not a theorem.

## 1. Definitions

**Fritsch adjacency.** The neighbour lists in `FRITSCH` inside `compute/kempe/a1720_k7_locked.py` are the `adjacencyList` of House of Graphs graph 1088 (`graphName` “Fritsch Graph”, canonical form `HEutZhj`). `structural` in that script builds the undirected graph and checks simplicity, symmetry of the lists, connectedness, planarity, $m=3n-6$, and the facial walks from `networkx.check_planarity`.

**KC5 at $(G,v)$.** Implemented by `analyse_vertex` in `compute/kempe/a1720_k6_kc5.py`, imported and not rewritten. $G$ is a planar triangulation, $\deg v=5$, and $H=G-v$. Colourings are proper $4$-colourings of $H$, modulo $S_4$. Every Kempe class that contains a colouring with $|c(N(v))|=4$ also contains one with $|c(N(v))|\le 3$.

A **bad class** is a Kempe class of $H$ in which every colouring satisfies $|c(N(v))|=4$. `max_kempe_distance_to_fix` is the largest Kempe distance, inside a class, from a colouring with $|c(N(v))|=4$ to a colouring with $|c(N(v))|\le 3$.

## 2. Statement

Let $G$ be the graph of the House of Graphs 1088 adjacency. The checked sentence is: $G$ is a simple connected planar triangulation on $n=9$ vertices (so $m=21$ and every face is a triangle), and for every vertex $v$ with $\deg v=5$, KC5 holds at $(G,v)$.

The quantifiers stop at this graph. KC5 for every planar triangulation would be stronger than the Four Colour Theorem; this run does not speak to that sentence.

## 3. Evidence

MathWorld states that the Fritsch graph is the planar graph on nine vertices that tangles the Kempe chains in Kempe’s colouring algorithm, and thus shows how Kempe’s 1879 argument fails, and that the Fritsch graph and the Soifer graph are the smallest such counterexamples. It points to House of Graphs 1088:

https://mathworld.wolfram.com/FritschGraph.html

https://houseofgraphs.org/graphs/1088

The adjacency used is the API field `adjacencyList` at

https://houseofgraphs.org/api/graphs/1088

MathWorld names Gethner and Springer, Congr. Numer. 164 (2003), 159–175, for the smallest-counterexample claim. That paper was not opened here; the sentences above are MathWorld’s.

Command and output:

```
/Users/fulkanjou/GraphColour/.venv/bin/python compute/kempe/a1720_k7_locked.py
```

Wall clock $0.01\,\mathrm{s}$, measured in the script. Output: `backgroundMaterial/agent1720/groups/K7_results.json`.

Structural record: $n=9$, $m=21$, symmetric listing, connected, planar, $14$ faces, every face of length $3$, Euler characteristic $2$, degrees three $4$s and six $5$s. The degree-$5$ vertices are $3,4,5,6,7,8$. The graph is isomorphic to the cached triangulation $T_{9,49}$. The $n\le 11$ census was not rerun.

KC5 record: $6$ vertices, $6$ classes, `n_bad_classes` $=0$, `max_kempe_distance_to_fix` $=2$. Each vertex has exactly one class, and that class is mixed. Each $H=G-v$ has $8$ normalised $4$-colourings. Distance $2$ occurs at every degree-$5$ vertex.

## 4. Result

Computed (finite check, one graph). On this triangulation, KC5 holds at every degree-$5$ vertex: $0$ bad classes. A finite check is not a theorem.

## 5. Kill criterion

One written bad class at a degree-$5$ vertex. **Not met.** Every degree-$5$ vertex needs Kempe distance $2$ before a colouring with $|c(N(v))|\le 3$ appears, so a uniform bound of $1$ on that distance is false for this graph. Those colourings still lie in a class that contains a fix, so they are not a bad class.

## 6. Not proved

A finite check is not a theorem. KC5 for every planar triangulation is open. Nothing here proves the Four Colour Theorem. MathWorld’s sentence is about Kempe’s 1879 procedure. The computation shows that the Kempe classes at these six vertices are still fixable. The isomorphism with $T_{9,49}$ places this graph inside the census already reported by K6.

Tilley, arXiv:1809.02807, states that there is a single $4$-connected Kempe-locked triangulation of order $12$, drawn in his Figure 1. That paper gives no edge list, so that graph was not encoded.

## 7. Feasibility

A proof of KC5 for every planar triangulation: **Low**. KC5 on Tilley’s order-$12$ triangulation, once a published edge list is in hand: **High**.

## 8. Next steps

1. Keep this edge list and `K7_results.json` as the Fritsch evidence. Do not treat `n_bad_classes` $=0$ as a general lemma; the same isomorphism type is $T_{9,49}$.
2. Any later claim that the fixing distance is at most $1$ fails on vertices $3,4,5,6,7,8$ of this graph.
3. Do not transcribe Tilley’s Figure 1. Wait for a published edge list before running KC5 on that order-$12$ triangulation.
