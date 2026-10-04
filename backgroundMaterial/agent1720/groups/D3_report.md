# D3 — Signed Tait count

**Group:** D3, manager M-Duality
**Date:** 2 October 2026
**Status:** the sign identity is proved for every triangulation. The census on $n\le 8$ agrees with the proof. The identity restates existence.

## 1. Definitions

Let $T$ be a triangulation on $n\ge 4$ vertices. Its plane dual $T^*$ is the cubic graph whose vertices are the faces of the embedding returned by `networkx.check_planarity`. The construction is `dual_rotation` in `compute/flows/a1720_alon_tarsi.py`. Dual vertex $i$ is face $i$, and its planar rotation is the boundary order of that face (`traverse_face`: the face lies to the right of each directed edge).

A **Tait colouring** is a proper edge-colouring of $T^*$ with colours $\{0,1,2\}$. At a vertex, the three incident colours in rotation order form a permutation of $(0,1,2)$. The **sign** of the colouring is the product, over all vertices of $T^*$, of the inversion signs of those permutations (`permutation_sign`, `colouring_sign`). The **signed Tait count** is the sum of these signs (`tally`). The unsigned **Tait count** is the number of colourings.

The dual has $V=2n-4=2(n-2)$ vertices. Reversing every rotation, or relabelling the three colours by a permutation $\tau$, multiplies the sign by $(-1)^V=1$ or by $\mathrm{sgn}(\tau)^V=1$. For $n\ge 4$ the dual is $3$-connected, so Whitney's theorem gives a unique embedding up to reflection, and the sign is an invariant of the abstract coloured dual.

The Klein group $K=\mathbb{Z}_2\times\mathbb{Z}_2$ is written as $\{0,1,2,3\}$ under XOR. `MAP` sends the nonzero elements to Tait colours by $1\mapsto 0$, $2\mapsto 1$, $3\mapsto 2$. A proper vertex colouring $\psi:V(T)\to K$ induces the Tait colour $\mathrm{MAP}(\psi(u)+\psi(v))$ on the dual edge that crosses $uv$ (`klein_edge_colours`).

## 2. Statement

For every triangulation $T$ on $n\ge 4$ vertices, and every Tait colouring $\varphi$ of $T^*$,
\[
\mathrm{sign}(\varphi)=(-1)^n.
\]
Equivalently, the signed Tait count equals $(-1)^n$ times the Tait count.

In particular, for every cached triangulation with $n\le 8$: every Tait colouring of that one dual has the same sign; the common sign is $+1$ for even $n$ and $-1$ for odd $n$; and both signs occur in the family.

## 3. Evidence

Command: `/Users/fulkanjou/GraphColour/.venv/bin/python compute/flows/a1720_alon_tarsi.py 8`

Wall clock $0.898$s. Output: `backgroundMaterial/agent1720/groups/D3_results.json`. One process. The Tait counts agree with `D1_results.json` on this range. Reversing one rotation negates the signed count, and reversing every rotation preserves it, on all $23$ duals.

| $n$ | graphs | Tait min–max | signed count | common sign |
|---|---|---|---|---|
| $4$ | $1$ | $6$–$6$ | $+6$ | $+1$ |
| $5$ | $1$ | $6$–$6$ | $-6$ | $-1$ |
| $6$ | $2$ | $6$–$24$ | $+6$ to $+24$ | $+1$ |
| $7$ | $5$ | $6$–$30$ | $-30$ to $-6$ | $-1$ |
| $8$ | $14$ | $6$–$72$ | $+6$ to $+72$ | $+1$ |

No graph has both signs. $K_4$, the dual of $T_{4,0}$, has $6$ Tait colourings, all of sign $+1$. On one $4$-colouring of each of the $1555$ cached triangulations with $n\le 11$, the face-sign product below equals $(-1)^n$ and the descent count equals $3n-6$ ($0$ failures, $0.808$s inside the same run).

**Proof.** Transport of a Tait colouring to $K\setminus\{0\}$ makes the three colours at each vertex of $T^*$ sum to $0$, so the colouring is a nowhere-zero $K$-flow. Face potentials exist: every facial triangle of $T$ is the star of a vertex of $T^*$ and has colour-sum $0$, and those triangles generate the cycle space. The resulting vertex colouring of $T$ induces the original edge colours. Adding a constant does not change the edge colours, and any other bijection from $K\setminus\{0\}$ to $\{0,1,2\}$ is a global relabelling, which preserves the sign because $V$ is even. It is enough to use `MAP`.

Let a face have colours $\alpha,\beta,\gamma$ in boundary order. Let $\varepsilon$ be the inversion sign of the edge colours $(\mathrm{MAP}(\alpha+\beta),\mathrm{MAP}(\beta+\gamma),\mathrm{MAP}(\gamma+\alpha))$, and let $\sigma$ be the inversion sign of $(\alpha,\beta,\gamma)$. A cyclic shift is a $3$-cycle, hence even, so both signs depend only on the oriented face. The function `local_lemma` checks all $24$ ordered triples and gives $\varepsilon=\sigma\cdot(-1)^{\alpha+\beta+\gamma}$.

The product of the parity factors is $(-1)^{\sum_v\deg(v)\psi(v)}$. Modulo $2$ the exponent counts edges with one end in $\psi^{-1}(\{1,3\})$. Write $e_{\mathrm{cross}}$ for that cut and $e_{02}$, $e_{13}$ for the edges joining those pairs. Then $3n-6=e_{\mathrm{cross}}+e_{02}+e_{13}$. Each face uses three distinct colours, so it contains exactly one edge of type $02$ or $13$, and each such edge lies on two faces. With $F=2n-4$ faces, $e_{02}+e_{13}=n-2$, hence $e_{\mathrm{cross}}=2n-4$ is even. The parity product is $+1$, and the Tait sign equals $\prod_F\sigma(F)$.

On an oriented triangle of three distinct integers the increasing cyclic order is an even permutation and has one descending edge; the opposite orientation has two. Thus $\sigma(F)=(-1)^{d(F)+1}$ with $d(F)$ the number of descents, and
\[
\prod_F\sigma(F)=(-1)^{\sum_F d(F)+F}.
\]
Here $F$ is even. Each undirected edge is traversed once in each direction and exactly one direction descends, so $\sum_F d(F)=3n-6$. Therefore $\prod_F\sigma(F)=(-1)^{3n-6}=(-1)^n$.

Every Tait colouring has sign $(-1)^n$. The signed count equals $(-1)^n$ times the Tait count.

**Citation.** M. N. Ellingham and L. Goddyn, “List edge colourings of some 1-factorable multigraphs”, Combinatorica 16 (1996) 343–352, https://link.springer.com/article/10.1007/BF01261320. A $d$-regular graph is $1$-factorable precisely when it is $d$-edge-colourable. The paper, by the Alon–Tarsi method, confirms the list-edge-colouring conjecture for $d$-regular $d$-edge-colourable planar graphs. Planar cubic $3$-edge-colourable graphs are therefore $3$-edge-choosable.

## 4. Result

**Proved:** $\mathrm{sign}(\varphi)=(-1)^n$ for every Tait colouring of the dual of every triangulation on $n\ge 4$ vertices. The signed count equals $(-1)^n$ times the Tait count.

**Computed:** the same identity on all $23$ cached triangulations with $n\le 8$, with no internal cancellation. Across that family both signs occur ($T_{4,0}$ has sign $+1$, $T_{5,0}$ has sign $-1$).

**Literature-settled:** planar cubic $3$-edge-colourable graphs are $3$-edge-choosable (Ellingham–Goddyn 1996). The argument takes a colouring as input. The sign identity is the corresponding non-cancellation: once a colouring exists, every colouring contributes the same sign, so an Alon–Tarsi coefficient equal to $\pm$ the Tait count is nonzero.

The signed count is nonzero exactly when a Tait colouring exists. For these duals, existence is $4$-colourability of $T$. The identity restates existence. It is a reformulation of the Four Colour Theorem in Tait's form, not a proof of non-vanishing.

## 5. Kill criterion

“Some dual with $n\le 8$ has two Tait colourings of opposite sign.” Not met: `mixed_sign_graphs` is empty.

“Every Tait colouring in the whole $n\le 8$ family has one common sign.” Met, and the statement is killed: $T_{4,0}$ has sign $+1$ and $T_{5,0}$ has sign $-1$.

“The sign identity proves the signed count is nonzero.” Met as a kill of that hope. The identity equates the signed count with $(-1)^n$ times the Tait count, so non-vanishing is existence.

## 6. Not proved

Nothing here proves that a Tait colouring exists for an arbitrary triangulation. The Four Colour Theorem is not proved, and Ellingham–Goddyn is cited, not re-proved. The census by itself covers only $n\le 8$; the general identity is the proof in §3. The monomial coefficient in the line-graph polynomial was not expanded as a separate polynomial.

## 7. Feasibility

**Low** for a proof of non-vanishing, or of the Four Colour Theorem, that starts from this sign. The signed count has been identified with the Tait count. **Medium** for a later Lean transcription of §3. **High** for the census to keep matching the proof on larger $n$; that check is no longer a source of new information.

## 8. Next steps

Stop this node. The sign is evaluated, and the evaluation restates existence. A further attack has to produce a colouring, or a nonzero quantity that is not identified with the Tait count. Extending the enumeration past $n=8$ does not change the identity. Do not treat cubic duals as $4$-edge-connected, and do not read the Ellingham–Goddyn theorem as a proof that a Tait colouring exists.
