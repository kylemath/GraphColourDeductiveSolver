# K6b — KC5 on the Kittell triangulation

**Group:** K6b (M-Kempe, Track 1). **Date:** 2 October 2026.
**Status:** finite check on one named graph. This is not a theorem.

## 1. Definitions

**Kittell adjacency.** The neighbour lists in `KITTELL` inside `compute/kempe/a1720_k6_kittell.py` are copied from SageMath `graphs.KittellGraph` (`src/sage/graphs/generators/smallgraphs.py`, branch develop). `structural` in that script builds the undirected graph and checks simplicity, symmetry of the lists, connectedness, planarity, $m=3n-6$, and the facial walks from `networkx.check_planarity`.

**KC5 at $(G,v)$.** Implemented by `analyse_vertex` in `compute/kempe/a1720_k6_kc5.py`, imported and not rewritten. $G$ is a planar triangulation, $\deg v=5$, and $H=G-v$. Colourings are proper $4$-colourings of $H$, modulo $S_4$. Every Kempe class that contains a colouring with $|c(N(v))|=4$ also contains one with $|c(N(v))|\le 3$.

A **bad class** is a Kempe class of $H$ in which every colouring satisfies $|c(N(v))|=4$. `max_kempe_distance_to_fix` is the largest Kempe distance, inside a class, from a colouring with $|c(N(v))|=4$ to a colouring with $|c(N(v))|\le 3$.

## 2. Statement

Let $G$ be the graph of the SageMath Kittell adjacency. The checked sentence is: $G$ is a simple connected planar triangulation on $n=23$ vertices (so $m=63$ and every face is a triangle), and for every vertex $v$ with $\deg v=5$, KC5 holds at $(G,v)$.

The quantifiers stop at this graph. KC5 for every planar triangulation would be stronger than the Four Colour Theorem; this run does not speak to that sentence.

## 3. Evidence

Edge list, SageMath develop, function `KittellGraph`, whose doctest states order $23$ and size $63$:

https://github.com/sagemath/sage/blob/develop/src/sage/graphs/generators/smallgraphs.py

MathWorld states that the Kittell graph is a planar graph on $23$ nodes and $63$ edges:

https://mathworld.wolfram.com/KittellGraph.html

Command and output:

```
/Users/fulkanjou/GraphColour/.venv/bin/python compute/kempe/a1720_k6_kittell.py
```

Wall clock $0.31\,\mathrm{s}$, measured in the script. Output: `backgroundMaterial/agent1720/groups/K6_kittell.json`.

Structural record in that file: $n=23$, $m=63$, symmetric listing, connected, planar, $42$ faces, every face of length $3$, Euler characteristic $2$, degrees fifteen $5$s, five $6$s, and three $7$s. The degree-$5$ vertices are $2,3,4,5,8,9,12,13,14,16,17,18,20,21,22$.

KC5 record: $15$ vertices, $15$ classes, `n_bad_classes` $=0$, `max_kempe_distance_to_fix` $=4$. Each vertex has exactly one class, and that class is mixed. Normalised colouring counts of $H$ run from $398$ (vertices $12,18,20,21$) to $508$ (vertex $3$). Distance $4$ occurs at vertices $9$ and $17$.

## 4. Result

Computed (finite check, one graph). On this triangulation, KC5 holds at every degree-$5$ vertex: $0$ bad classes. A finite check is not a theorem.

## 5. Kill criterion

One written bad class at a degree-$5$ vertex. **Not met.** Vertices $9$ and $17$ need Kempe distance $4$ before a colouring with $|c(N(v))|\le 3$ appears, so a uniform bound of $3$ on that distance is false for this graph. Those colourings still lie in a class that contains a fix, so they are not a bad class.

## 6. Not proved

A finite check is not a theorem. KC5 for every planar triangulation is open. Nothing here proves the Four Colour Theorem. MathWorld’s sentence that this graph tangles Kempe chains is a description of Kempe’s procedure; the computation shows the Kempe classes at these fifteen vertices are still fixable.

## 7. Feasibility

A proof of KC5 for every planar triangulation: **Low**. The same verified-list-then-KC5 check on another single named triangulation of this order, once an edge list is in hand: **High**.

## 8. Next steps

1. Keep this edge list and `K6_kittell.json` as the Kittell evidence. Do not treat `n_bad_classes` $=0$ as a general lemma.
2. Any later claim that the fixing distance is at most $3$ has to exclude vertices $9$ and $17$ of this graph, or fail.
3. A proof for all triangulations is not available from the cached graphs in this repository.
