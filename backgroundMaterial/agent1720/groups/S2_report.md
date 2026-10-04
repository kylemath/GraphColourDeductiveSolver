# S2 — Sheaf cohomology (Track 6)

**Group:** S2, manager M-Frontier
**Date:** 2 October 2026
**Status:** killed. No cellular sheaf of vector spaces has $H^0$ equal to the set of proper 4-colourings. The linear stand-in has $H^1(K_4)\neq 0$.

## 1. Definitions

A cellular sheaf of vector spaces $\mathcal{F}$ on a graph $G=(V,E)$ assigns a vector space $\mathcal{F}(v)$ to each vertex, a vector space $\mathcal{F}(e)$ to each edge, and a linear restriction $\rho_{v\subset e}:\mathcal{F}(v)\to\mathcal{F}(e)$ to each incidence. After orienting the edges,
\[
C^0=\bigoplus_v\mathcal{F}(v),\qquad
C^1=\bigoplus_e\mathcal{F}(e),\qquad
(\delta x)_e=\rho_{h(e)\subset e}(x_{h(e)})-\rho_{t(e)\subset e}(x_{t(e)}).
\]
Then $H^0(G;\mathcal{F})=\ker\delta$ and $H^1(G;\mathcal{F})=\operatorname{coker}\delta$. In particular $H^0$ is a vector space.

A proper 4-colouring is a map $V\to\{1,2,3,4\}$ with distinct values on adjacent vertices. Write $P(G)$ for that set. In the script the four colours are the vectors of $\mathbb{F}_2^2$. Functions: `is_proper`, `count_proper` in `compute/topology/a1720_sheaf.py`.

The linear stand-in $\mathcal{L}$ is the constant cellular sheaf with stalk $\mathbb{F}_2^2$ and identity restrictions, so $(\delta x)_{uv}=x_u+x_v$ over $\mathbb{F}_2$. A 0-cochain is a proper 4-colouring if and only if $(\delta x)_e\neq 0$ for every edge. Functions: `coboundary_f2`, `coboundary_real`, `gf2_rank`, `graph_cohomology`.

## 2. Statement

**Killed, for every coefficient field.** There is no cellular sheaf of vector spaces $\mathcal{F}$ on $K_4$ for which the underlying set of $H^0(K_4;\mathcal{F})$ equals $P(K_4)$, and none for which those two sets are in bijection.

**Computed for $\mathcal{L}$.** On $K_4$ and on $K_5$, $\dim H^0=2$ and $\dim H^1=2(|E|-|V|+1)$. The four global sections are the monochromatic assignments. None of them lies in $P(G)$.

## 3. Evidence

Command:

`/Users/fulkanjou/GraphColour/.venv/bin/python compute/topology/a1720_sheaf.py`

Process wall clock $0.13$ s. The arithmetic timer `elapsed_seconds` in the output is $0.00334$ s. Output: `backgroundMaterial/agent1720/groups/S2_results.json`.

**Four-vertex witness.** In $(\mathbb{F}_2^2)^4$,
\[
c_1=((0,0),(0,1),(1,0),(1,1)),\qquad
c_2=((0,0),(1,0),(0,1),(1,1)).
\]
Both are bijective, so both lie in $P(K_4)$. Their sum is $((0,0),(1,1),(1,1),(0,0))$, which repeats a colour on an edge of $K_4$. The zero assignment is not proper. So $P(K_4)$ is not a linear subspace of $(\mathbb{F}_2^2)^4$. The script checks these three claims.

**Why that kills every vector-space sheaf.** The same script counts $|P(K_4)|=24$ and $|P(K_5)|=0$. A vector space over a field has cardinality $1$ (the zero space), a prime power, or infinity: a finite field has order $p^k$ because it is a finite-dimensional vector space over its prime field $\mathbb{Z}/p\mathbb{Z}$, and a $d$-dimensional space over that field then has order $p^{kd}$. An infinite field, or an infinite dimension, yields an infinite space as soon as the dimension is positive. The integer $24=2^3\cdot 3$ is none of these. Hence $P(K_4)$ is not the underlying set of any vector space. But $H^0(K_4;\mathcal{F})$ always is one. This is a proof, not a sample.

**Stand-in.** Numpy `linalg.matrix_rank` on the signed real coboundary (stalk $\mathbb{R}^2$) agrees with Gaussian elimination over $\mathbb{F}_2$. Agreement is expected: $-1=1$ in $\mathbb{F}_2$, and $K_n$ is connected, so $\operatorname{rank}\delta=2(n-1)$.

| graph | planar | $\|P(G)\|$ | $\dim C^0$ | $\dim C^1$ | $\operatorname{rank}\delta$ | $\dim H^0$ | $\dim H^1$ | proper sections |
|---|---|---|---|---|---|---|---|---|
| $K_4$ | yes | $24$ | $8$ | $12$ | $6$ | $2$ | $6$ | $0$ |
| $K_5$ | no | $0$ | $10$ | $20$ | $8$ | $2$ | $12$ | $0$ |

$K_4$ is planar and $4$-colourable. $K_5$ is not planar. The script's count $|P(K_5)|=0$ is the failure of $4$-colourability.

## 4. Result

**Killed.** The vector-space form of Track 6 is false, by the proof in §3. The stand-in is a finite computation on $K_4$ and $K_5$ only.

## 5. Kill criterion

Track 6's test was: $H^1\neq 0$ on some planar graph, or $H^1=0$ on some graph that is not $4$-colourable.

Both of the following are met.

1. The demand that $H^0$ equal $P(G)$ fails on the four-vertex graph $K_4$, for every cellular sheaf of vector spaces. Met, by the cardinality proof. The sum $c_1+c_2$ is the explicit witness that proper $4$-colourings are not a linear subspace.
2. For the stand-in $\mathcal{L}$, $K_4$ is planar and $\dim H^1(K_4;\mathcal{L})=6\neq 0$. Met. Also $\dim H^0(K_5;\mathcal{L})=2\neq 0$ while $|P(K_5)|=0$, so existence of global sections does not detect $4$-colourability.

This is not re-specified. The constant sheaf was the linear stand-in used to run the old kill test, and that test already fires.

## 6. Not proved

Sheaves of sets, abelian groups, and modules are untouched. A sheaf of sets can be arranged so that its limit of sections is $P(G)$: a $4$-element stalk at each vertex and the off-diagonal at each edge. That limit is the colouring problem, so the sentence "global sections are the proper $4$-colourings" is then a reformulation of asking whether $P(G)$ is nonempty. It has no abelian $H^1$. Nothing here proves or refutes the Four Colour Theorem.

An abelian group of order $24$ exists, so the cardinality argument does not kill sheaves of abelian groups.

## 7. Feasibility

**Low** for a proof of the Four Colour Theorem by vanishing of $H^1$ of a vector-space colouring sheaf. No such sheaf has the required $H^0$, and the constant stand-in fails the vanishing test on $K_4$.

## 8. Next steps

Stop Track 6 in the form "global sections equal proper $4$-colourings, and planarity forces $H^1=0$". Do not continue with $\mathcal{L}$: its $H^1$ is two copies of the cycle space, so it is nonzero on every graph that contains a cycle. A set-valued restatement is a reformulation of $4$-colourability. It would become a separate attack only if a cover and a non-abelian cocycle were written whose vanishing is strictly easier than exhibiting a $4$-colouring. No such cover is defined here.
