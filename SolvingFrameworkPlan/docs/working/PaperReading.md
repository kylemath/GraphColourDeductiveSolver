# What the papers already decide

4 October 2026. Reading notes for the vacancy and two-pole work. None of these theorems is a four-colour proof, and none of them is the unequal-pole belt argument.

## Florek, arXiv:2511.00485

$G_n$ ($n \ge 5$) is the triangulation with two nonadjacent poles of degree $n$ and $2n$ vertices of degree 5. It is the family he had already singled out as the minimal essentially 6-connected triangulations that lose that property when an edge at a degree-5 vertex is contracted (Applicationes Mathematicae 19 (1987), 387–398). The 2025 paper counts Kempe classes of the full graph and proves a bounded Kempe theorem only after deleting a pole.

The full-graph invariants are four integers $a,b,c,d$. For a non-constant colouring, two colourings are Kempe equivalent if and only if these four agree. A colouring is constant, meaning Kempe-isolated, if and only if $d=1$. When $n \equiv 2 \pmod{3}$ there are $2n$ constant colourings. For $n=8$ that is 16 isolated 4-colourings of $G_8$. A Kempe search on the full graph can sit in one of them forever. That does not obstruct existence. It does obstruct any plan that tries to transform an arbitrary 4-colouring of $G_n$ into one fixed target.

Lemma 2.2 forces a full colouring to give equal sizes to colours 1 and 2, and equal sizes to colours 3 and 4. With Lemma 2.3, $a+b=n+1$. For $n=8$ the only possibility compatible with the earlier count is the population $(4,4,5,5)$. The partial population $(2,5,5,5)$ cannot be a full colouring, which is why slides alone fail.

Same pole colour is rare among full colourings. If $n \equiv 0 \pmod{3}$ there is exactly one colouring, called $Q$, with both poles the same colour, and every other colouring has the poles different. The normalization in the paper paints those poles 1 and 2. Our star swap starts from equal poles on the deleted graph and changes one pole, so the colouring it completes is an unequal-pole colouring of $G_n$. That is the ordinary case of the paper, not $Q$.

Theorem 3.1 deletes a pole, not a belt vertex. Every two 4-colourings of $H_n = G_n - b$ are Kempe equivalent, in at most $6\lfloor n/2 \rfloor$, $9\lfloor n/2 \rfloor$, or $9\lfloor n/2 \rfloor + 6\lfloor n/3 \rfloor - 2$ changes, according as $n \equiv 0,2,1 \pmod{3}$. For $n=8$ the middle bound is 36. The abstract's $\lfloor 13n/2 \rfloor$ is a coarser envelope of those three bounds. The hole stays at the pole for the whole path. A slide onto the pole in the $(2,5,5,5)$ component lands in $H_8$ still carrying those counts, so the 36-step path, if used, is a different and longer route than the one star swap at a belt vertex.

## Fisk (1973) and Mohar (2006)

Fisk proved that all 4-colourings of a 3-colourable triangulation of the sphere are Kempe equivalent. Those triangulations are Eulerian: every degree is even. Mohar extended the conclusion from Eulerian triangulations to every planar graph with $\chi < 4$, so again to graphs that do not need a fourth colour. $G_n$ has degree-5 vertices. Fisk and Mohar do not apply, and Florek's $\lfloor n/6 \rfloor$ distinct Kempe classes are the witness that they cannot apply.

Ito, Iwamasa, Kobayashi, Maezawa, Nozaki, Okamoto, and Ozeki (arXiv:2210.17105) separate Kempe changes from single-vertex recolouring. Even on a 3-colourable spherical triangulation, some 4-colouring is frozen: no vertex can be recoloured by a one-vertex change, although Fisk still connects it to a 3-colouring by larger Kempe chains. They give a linear-time test for which 4-colourings are single-vertex-equivalent to a 3-colouring, and a quadratic sequence when the test passes. The test requires a 3-colourable triangulation. A vacancy slide is not that operation. It recolours the old hole and vacates a neighbour, and only when the neighbour's colour is unique on the link. The frozen examples are still the right warning: forbidding large Kempe chains can disconnect a reconfiguration graph that full Kempe changes leave connected.

## What does not extend a 5-boundary

Dvořák's 4-precolouring extension theorem for near-Eulerian triangulations (arXiv:2312.13061) decides extension when every interior vertex has even degree. One case is an outer face of length at most 5. Another is an outer cycle of odd-degree vertices precoloured with only three colours. A degree-5 deletion has a 5-face, but the interior still contains degree-5 vertices, and a non-target colouring uses four colours on that face. Neither case is ours. The theorem explains why a 5-boundary is easy only after the interior has been made Eulerian.

Kempe-locking, in the sense of an edge $xy$ that can never be restored because every relevant Kempe chain contains both ends, is an edge obstruction inside an already 4-coloured near-triangulation. The published arguments assume a 4-colouring of that near-triangulation. They do not produce a colouring of a belt deletion, and they do not replace the star swap.

## What this changes

The equal-pole star swap is not in these papers. Florek classifies the colouring it produces and the long pole-hole path it is not. Fisk and Mohar stop at even degrees. Single-vertex recolouring can freeze even where Kempe changes succeed, so a hybrid that allows only one ordinary Kempe swap is a genuine restriction, not a corollary of Meyniel or of Theorem 3.1.

On $G_5-u_0$ and $G_8-u_0$ the unequal-pole case is no longer an enumeration target. Every such colouring reaches a 3-colour boundary by slides alone, in at most four slides, with no Kempe swap. The equal-pole orbit is the one that still needs the star. A hand proof for every $n$ is open. Feasibility of that proof, given the two belts: **Medium**. Feasibility that another feature paired with $q$ will do the general job: **Low**. Feasibility that the Florek invariants $a,b,c,d$ are the right coordinates on a completed colouring: **High**.
