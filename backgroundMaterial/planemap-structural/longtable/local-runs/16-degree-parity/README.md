# 16 - Parity of the folding degree is constant on Kempe classes (exploratory)

Files: `degree_parity.cpp` (C++17, `clang++ -O2`; all labelled 4-colourings by backtracking, Kempe classes by union-find, folding degree for each of the 4 target faces, candidate tests), `results.txt` (output). Input: `studiointel/gentri/triN.txt`. Total run time of orders 12-22: about 4 s on one core, nice 10.

## 1. Computation (all labelled colourings, 6 Kempe pairs per colouring)

| order | graphs | classes | colourings | mixed-parity classes | multi-class graphs | of those, both parities occur |
|---|---|---|---|---|---|---|
| 12 | 1 | 10 | 240 | 0 | 1 | 0 |
| 14 | 1 | 2 | 480 | 0 | 1 | 1 |
| 16 | 3 | 5 | 2376 | 0 | 2 | 2 |
| 17 | 4 | 20 | 2640 | 0 | 3 | 2 |
| 18 | 12 | 61 | 14256 | 0 | 12 | 11 |
| 19 | 23 | 127 | 37416 | 0 | 23 | 22 |
| 20 | 73 | 433 | 154224 | 0 | 68 | 65 |
| 21 | 191 | 919 | 511536 | 0 | 189 | 184 |
| 22 | 649 | 3819 | 2324616 | 0 | 641 | 637 |

No counterexample: the claim holds on every class of every graph. Orders 12-18 alone give 21 graphs / 98 classes in these files (the python script `docs/wrap/degree_parity_check.py` reproduces this exactly: 21 / 98, 19 multi-class, 16 with both parities), not the 38 / 174 quoted in the task; 21+23 (order 19) = 44, so that figure seems to come from a different count. The |degree| is equal across the four target faces in all colourings here (my counter allows a sign flip; 0 exceptions).

## 2. Simple description

For colour m let F_m = number of faces whose colours avoid m, and o_m = number of vertices of colour m with ODD degree in T. Then for every colouring and every m

    parity(folding degree) = F_m mod 2 = o_m mod 2     (tested on all 2.3M colourings at order 22 and all smaller orders: 0 failures)

The first is immediate (degree = P - N, F_m = P + N). The second: every face contains at most one vertex of colour m, so #faces containing m = sum of deg(v) over colour-m vertices, and F_m = (2n-4) - sum_{c(v)=m} deg(v) = o_m (mod 2).
Not equivalent: parity of the number of vertices of colour m (fails on ~100% at several orders, fails often in general), or parity of n (it is a graph constant; fails whenever both parities occur).

## 3. Proof (it works, and it is short; planarity of K is not needed)

Setup. T a triangulation of the sphere (simple graph), n vertices, 2n-4 faces, each vertex v lies on deg(v) distinct faces; c a proper 4-colouring. c maps the faces onto the 4 faces of a tetrahedron; the folding degree D(c) is the signed number of T-faces over any one target face (it is independent of the target face up to a global sign, by degree theory of the cellular map S^2 -> boundary of a tetrahedron; verified computationally).

Step 1 (counting). For colour m, the target face t_m opposite corner m is covered exactly by the faces avoiding m. With P = positive, N = negative: D = +-(P - N) and F_m = P + N, so D = F_m (mod 2). A face has three distinct colours, hence contains exactly one vertex of colour m or none, so
(faces containing m) = sum over colour-m vertices of deg(v). Hence F_m = 2n - 4 - sum deg(v) = o_m (mod 2). So D(c) = o_m(c) (mod 2) for every m.

Step 2 (Kempe swap). Swap colours a, b on a component K (any component, any size, any boundary). Pick c not in {a,b}. The set of colour-c vertices is not touched, so o_c is unchanged, so by Step 1 D(c) mod 2 is unchanged. Induction over swaps: parity is constant on each Kempe class. QED.

(Side remark: o_a + o_b changes by an even number as well, so no further information comes from them; and since o_m = D mod 2 for all four m, all four o_m have the same parity, consistent with the handshake lemma: sum of o_m = number of odd-degree vertices, even.)

What the hint's face-by-face analysis amounts to: the swap changes the degree by 2*(something) because faces avoiding c are the only ones counted in target t_c, and there P+N is fixed up to the colour-c vertex set. The easy parity proof does not need K's boundary curves. The actual value of D (not only its parity) can change under a swap; the changes are even by this argument, and I did not analyse their size (an obvious extension: is D itself an invariant? Not tested here).

Consequence: parity is a valid Kempe-class invariant, "number of odd-degree vertices in any one colour class mod 2". It separates classes whenever a graph has colourings with different parities (all but a handful of multi-class graphs in the table). It is NOT a complete invariant (e.g. order 22: 3819 classes vs 649 graphs, many graphs have more than two classes).
