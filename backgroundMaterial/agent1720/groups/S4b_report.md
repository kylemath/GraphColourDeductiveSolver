# S4b — Eulerian triangulations are exactly the 3-colourable ones

**Group:** S4b, manager M-Frontier
**Date:** 2 October 2026
**Status:** proved. The kill test was run and was not met.

## 1. Definitions

A *plane triangulation* is a simple graph embedded in the plane so that every face, including the outer face, is a triangle. For $n \ge 3$ vertices this is the same as a maximal simple plane graph, and it has $3n-6$ edges. The cache `compute/data/triangulations_n4_11.json` stores these graphs as `graphs[str(n)][i]`, written $T_{n,i}$.

The graph is *Eulerian* when every vertex degree is even. A *proper 3-vertex-colouring* is a map from the vertices to $\{1,2,3\}$ with distinct values on the two ends of every edge.

A *near-triangulation* is a plane multigraph in which every bounded face is a triangle. A circuit in an embedded graph *crosses itself* at a vertex $v$ when two of its transitions at $v$ alternate in the cyclic order of edges around $v$. A transition is the pair of edges by which the circuit enters and leaves $v$ on one visit.

In `compute/discovery/a1720_s4b.py`: `three_colouring` is the exact backtrack, `sat_three_colourable` is the Glucose3 encoding, and `face_sign_colouring` is the face-labelling construction (opposite cyclic orders of $\{0,1,2\}$ on the two colour classes of the dual).

## 2. Statement

For every simple plane triangulation $G$ on $n \ge 3$ vertices, $G$ admits a proper vertex colouring with three colours if and only if every vertex of $G$ has even degree.

The same sufficient direction holds for every Eulerian near-triangulation. The necessary direction uses that every face is a triangle.

## 3. Evidence

**Citation.** Mu-Tsun Tsai and Douglas B. West, "A new proof of 3-colorability of Eulerian triangulations", [faculty.math.illinois.edu/~west/pubs/eultri.pdf](https://faculty.math.illinois.edu/~west/pubs/eultri.pdf). The host did not answer; the text below was checked against the archived file [web.archive.org/web/20230329072456](https://web.archive.org/web/20230329072456/https://faculty.math.illinois.edu/~west/pubs/eultri.pdf). They prove that every Eulerian near-triangulation is $3$-colourable, by a noncrossing Eulerian circuit. Heawood stated the triangulation case in 1898 without proof. The write-up here is that argument.

**Proof.** First suppose $c$ is a proper $3$-colouring and $v$ is any vertex. In a triangulation the neighbours of $v$, in cyclic order, are pairwise adjacent. Their colours lie in the two colours other than $c(v)$, and successive neighbours receive different colours, so the colours alternate. The degree of $v$ is even.

Conversely, assume every degree is even. The two lemmas below are stated for near-triangulations; a plane triangulation is one.

*Lemma A.* Every Eulerian plane graph has a noncrossing Eulerian circuit.

A connected graph has an Eulerian circuit if and only if every degree is even. Among those circuits, choose $C$ with as few self-crossings as possible, and suppose it still crosses at $v$ on transitions $\{e,e'\}$ and $\{f,f'\}$, with $e'$ immediately after $e$ and $f'$ immediately after $f$. Let $P$ be the trail of $C$ from $e'$ through to $f$. Reverse $P$. The new transitions at $v$ are $\{e,f\}$ and $\{e',f'\}$, which do not alternate, so that crossing is gone. At every vertex other than $v$, each transition is the same unordered pair of edges, because reversing a trail swaps the order of arrival and departure but not the pair. At $v$, any new crossing uses one of the two new pairs. A visit that alternates with $\{e,f\}$ or with $\{e',f'\}$ already alternated with $\{e,e'\}$ or with $\{f,f'\}$ before the reversal, and a visit that alternates with both new pairs alternated with both old pairs. Distinct new crossings come from distinct old crossings at $v$, which the reversal removed. The number of crossings falls, contradicting the choice of $C$.

*Lemma B.* An Eulerian near-triangulation has a number of edges divisible by $3$.

Induct on the number of bounded faces. If there are none, there are no edges. Otherwise let $F$ be a bounded face that uses an edge of the outer face, and delete the three edges of $F$. Each of the three vertices loses two edges, so every degree stays even. Every surviving bounded face is still a triangle, and each component is an Eulerian near-triangulation with fewer bounded faces. The inductive hypothesis applies to each component. Three edges were deleted.

*Lemma C.* In a noncrossing Eulerian circuit of an Eulerian near-triangulation, every subcircuit has length divisible by $3$.

Induct on the number of faces enclosed by a subcircuit $C'$. A single face is a triangle, of length $3$. Let $H$ be the subgraph formed by $C'$ and everything in its interior. The full circuit may enter that interior. Because $C'$ does not cross itself, each such piece leaves at the same outer vertex of $H$ at which it enters, and is a shorter subcircuit. Those pieces contribute even degree at every vertex of $H$, and $C'$ does too, so $H$ is Eulerian. Its bounded faces are triangles, so Lemma B gives $|E(H)| \equiv 0 \pmod{3}$. Subtracting the incursions, each of length divisible by $3$, leaves the length of $C'$.

Now colour the vertices by walking along a noncrossing Eulerian circuit and repeating the colours $1,2,3$. Each return to a vertex closes a subcircuit whose length is a multiple of $3$, so the colour agrees with the colour already given. Every edge is one step of the circuit, so its ends receive two successive colours.

**Computation.** Command:

`/Users/fulkanjou/GraphColour/.venv/bin/python compute/discovery/a1720_s4b.py`

Wall clock $0.1845$ s. Output: `backgroundMaterial/agent1720/groups/S4b_results.json`.

The cache holds $1555$ graphs, $n = 4,\ldots,11$, with the plantri counts $1,1,2,5,14,50,233,1249$. Backtrack and Glucose3 agree on every graph. Exactly $7$ graphs are Eulerian, and those $7$ are exactly the $3$-colourable ones:

$T_{6,1}$, $T_{8,12}$, $T_{9,47}$, $T_{10,221}$, $T_{10,226}$, $T_{11,1220}$, $T_{11,1242}$.

On each of them the face-sign labelling returned a proper $3$-colouring. The counts of Eulerian graphs for $n = 4,\ldots,11$ are $0,0,1,0,1,1,2,2$.

$T_{4,0}$ is $K_4$, with degrees $(3,3,3,3)$. Both predicates fail. That is not a disagreement.

## 4. Result

**Proved**, for every simple plane triangulation. The cache check is a finite comparison on $n \le 11$, with no disagreement.

## 5. Kill criterion

One simple plane triangulation on $n \ge 3$ vertices that is $3$-vertex-colourable and has a vertex of odd degree, or that has all degrees even and is not $3$-vertex-colourable.

Not met. The proof says no such triangulation exists. The cache contains none.

## 6. Not proved

The Four Colour Theorem is not proved. A triangulation with an odd degree need not be $3$-colourable: $K_4 = T_{4,0}$ has chromatic number $4$. There is no Eulerian circuit to colour.

The triangular-face hypothesis cannot be dropped. The multigraph formed by doubling every edge of $K_4$ is plane and Eulerian (every degree is $6$) and still has chromatic number $4$, because the underlying simple graph is $K_4$. Its faces are not all triangles.

## 7. Feasibility

**Low** for a proof of the Four Colour Theorem along this route. The circuit uses three colours, and it exists only when every degree is even. **High** for the equivalence itself: the argument above has no remaining case.

## 8. Next steps

Close the route. A larger plantri census cannot break a proof that has no bound on $n$. Do not treat the seven cache examples as the theorem. The dual of an Eulerian triangulation is a cubic bipartite polyhedral graph; a Hamilton cycle in that dual is Barnette's conjecture, which is a different route and was not tested.
