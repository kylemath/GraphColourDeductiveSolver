# S1 — Colin de Verdière, the case $\mu \le 3$

**Group:** S1, manager M-Frontier
**Date:** 2 October 2026
**Track 5 label:** reformulation

## 1. Definitions

For a simple graph $G$ on $n$ vertices, $\mu(G)$ is the largest corank of a real symmetric matrix $M$ such that:

- **(M1)** $M_{ij} < 0$ if $ij$ is an edge, and $M_{ij} = 0$ if $ij$ is a non-edge ($i \ne j$); the diagonal is free;
- **(M2)** $M$ has exactly one negative eigenvalue, and that eigenvalue is simple;
- **(M3)** the Strong Arnold Property: the only symmetric $X$ with $MX = 0$ and $X_{ij} = 0$ whenever $i = j$ or $M_{ij} \ne 0$ is $X = 0$.

Implemented in `compute/spectral/a1720_cdv.py`: `k4_matrix`, `octahedron_matrix`, `sign_pattern_ok` for (M1), `spectral_facts` for (M2) and corank, `strong_arnold_integer` for (M3). The Strong Arnold test uses an integer kernel basis. If the rows are $u_i \in \mathbb{R}^3$, the conditions $u_i^{\mathsf T} S u_j = 0$ on the diagonal and on every edge force $S = 0$ in the $6$-dimensional space of symmetric $3 \times 3$ matrices. Rank is computed over $\mathbb{Q}$. A NumPy singular-value check of the non-edge support map is a cross-check.

## 2. Statements

**Literature, with quantifiers.** Colin de Verdière's conjecture says: for every graph $G$, $\chi(G) \le \mu(G) + 1$. The $\mu \le 3$ case is: for every graph $G$, if $\mu(G) \le 3$ then $\chi(G) \le \mu(G) + 1$.

**Decision.** That case is equivalent to the Four Colour Theorem, given $\mu(G) \le 3$ if and only if $G$ is planar, together with minor-monotonicity, $\mu(K_t) \ge t - 1$, and the theorem that every $K_4$-minor-free graph is $3$-colourable. Track 5, as a route to the Four Colour Theorem, is a **reformulation**.

**(1) $\Rightarrow$ (2).** Assume the $\mu \le 3$ case, and let $G$ be planar. Then $\mu(G) \le 3$, so $\chi(G) \le \mu(G) + 1 \le 4$.

**(2) $\Rightarrow$ (1).** Assume every planar graph satisfies $\chi \le 4$, and let $\mu(G) \le 3$. Then $G$ is planar, so $\chi(G) \le 4$. The same graph satisfies $\mu(G) \ge \chi(G) - 1$: a graph with $\chi \ge 2$ has a $K_2$ minor, a graph with $\chi \ge 3$ has a $K_3$ minor, and a graph with $\chi \ge 4$ has a $K_4$ minor because a $K_4$-minor-free graph is $3$-colourable. Minor-monotonicity and $\mu(K_t) \ge t - 1$ give the lower bound. Thus $\chi(G) \le \mu(G) + 1$.

The unrestricted sentence "for every $G$, $\chi(G) \le \mu(G) + 1$" implies the Four Colour Theorem and remains open for $\mu \ge 5$. That sentence is a strengthening. It is not the label of the $\mu \le 3$ case.

**Computed.** For $G \in \{K_4, O\}$, where $O$ is the octahedral graph on vertices $\{0,\ldots,5\}$ with non-edges $\{01, 23, 45\}$, there exists an integer symmetric matrix satisfying (M1), (M2), and (M3) with corank $3$. Hence $\mu(K_4) \ge 3$ and $\mu(O) \ge 3$.

## 3. Evidence

**Citations.**

- Yves Colin de Verdière, "Sur un nouvel invariant des graphes et un critère de planarité", *Journal of Combinatorial Theory, Series B* 50 (1990), 11–21. DOI [10.1016/0095-8956(90)90093-F](https://doi.org/10.1016/0095-8956(90)90093-F). States the invariant, minor-monotonicity, $\mu \le 3$ if and only if the graph is planar, and the conjecture $\chi \le \mu + 1$.
- Hein van der Holst, László Lovász, and Alexander Schrijver, "The Colin de Verdière graph parameter", in *Graph Theory and Combinatorial Biology*, Bolyai Soc. Math. Stud. 7 (1999), 29–85. Archived PostScript: [web.archive.org](https://web.archive.org/web/20160303165118/http://www.cs.elte.hu/~lovasz/colinsurv.ps). States (M1)–(M3). Records $\mu(G) \ge \eta(G) - 1$. Records that Hadwiger's conjecture would imply $\chi \le \mu + 1$, and that $\chi(G) \le \mu(G) + 1$ holds whenever $\mu(G) \le 4$, because Hadwiger's conjecture is known for every $K_6$-minor-free graph (Robertson, Seymour, Thomas, *Combinatorica* 13 (1993), 279–361, DOI [10.1007/BF01202354](https://doi.org/10.1007/BF01202354)). That $K_6$ case uses the Four Colour Theorem, so this is the direction "Four Colour Theorem $\Rightarrow$ the inequality on $\mu \le 4$".
- Wikipedia, "Colin de Verdière graph invariant", [en.wikipedia.org/wiki/Colin_de_Verdière_graph_invariant](https://en.wikipedia.org/wiki/Colin_de_Verdi%C3%A8re_graph_invariant). States $\mu \le 3$ if and only if $G$ is planar, and presents the planar colouring bound as an instance of the conjecture via the Four Colour Theorem. The page does not use the word "equivalent".
- MathOverflow, "Generalizations of the four-color theorem", [mathoverflow.net/questions/189097](https://mathoverflow.net/questions/189097/generalizations-of-the-four-color-theorem). An answer lists the unrestricted Colin de Verdière conjecture as a generalization of the Four Colour Theorem. That is the strengthening, not the $\mu \le 3$ case.

No fetched source states the equivalence in one sentence. The two directions above are the deduction from those theorems. Web searches used: the Wikipedia page, one DuckDuckGo query that led to MathOverflow, and the MathOverflow page together with the archived survey.

**Command.** `/Users/fulkanjou/GraphColour/.venv/bin/python compute/spectral/a1720_cdv.py`

Wall clock $0.08$s (`time -p`, real). Internal timer in the output file: about $7.6 \times 10^{-4}$s. Output: `backgroundMaterial/agent1720/groups/S1_results.json`, field `all_ok` true. Tolerance for numerical inertia: $10^{-8}$.

| Graph | Matrix | Eigenvalues (NumPy) | Corank | Negative | SAP rank over $\mathbb{Q}$ |
|---|---|---|---|---|---|
| $K_4$ | $-J$ | $-4,\, 0,\, 0,\, 0$ | 3 | 1 | $6 = \dim \mathrm{Sym}_3$ |
| Octahedron | $-A$ | $-4,\, 0,\, 0,\, 0,\, 2,\, 2$ | 3 | 1 | $6 = \dim \mathrm{Sym}_3$ |

The zero eigenvalues are at most $4.1 \times 10^{-16}$ in absolute value. Kernel residuals against the stored integer bases are $0$. On the octahedron the support map has smallest singular value $2\sqrt{2} \approx 2.828$. On $K_4$ every off-diagonal entry is nonzero, so the only matrix $X$ allowed by (M3) is $X = 0$; the kernel-basis rank test agrees.

## 4. Result

**Literature-settled as a reformulation.** The $\mu \le 3$ case of $\chi \le \mu + 1$ is equivalent to the Four Colour Theorem under the hypotheses in §2. It is not a kill.

**Computed** for two graphs: $\mu(K_4) \ge 3$ and $\mu(O) \ge 3$, with (M3) tested and holding for both witness matrices.

## 5. Kill criterion

For the equivalence: a planar graph with $\chi \ge 5$, or a graph with $\mu \le 3$ and $\chi > \mu + 1$. Not met. The separating example would be a planar graph with $\chi = 4$ and $\mu \le 2$; minor-monotonicity and $3$-colourability of $K_4$-minor-free graphs rule that example out.

For the certificate: a failed sign pattern, a negative-eigenvalue count other than $1$, corank other than $3$, or a nonzero $S$ in the Strong Arnold test. Not met (`certificate_ok` true for both graphs).

## 6. Not proved

This file does not prove $\mu(G) \le 3$ for planar $G$, minor-monotonicity, or $\mu(K_t) = t - 1$ for $t \ne 4$. The inequality $\chi \le \mu + 1$ is not proved for a general planar graph; the equivalence says that proving it is proving the Four Colour Theorem. The script examines only $K_4$ and the octahedron. Inertia is numerical; the Strong Arnold rank for these two bases is exact. Nothing is claimed about graphs whose Strong Arnold Property was not tested.

## 7. Feasibility

**Low** for a proof of the Four Colour Theorem by way of $\chi \le \mu + 1$ on graphs with $\mu \le 3$. That sentence is the theorem. **Low** for closing the unrestricted conjecture, which is open for $\mu \ge 5$ and is strictly more than the Four Colour Theorem.

## 8. Next steps

Keep Track 5 on the board as a reformulation. Do not open a work order whose only goal is $\chi \le \mu + 1$ for planar graphs. A separate strengthening, with its own kill test, is a single graph with $\chi(G) > \mu(G) + 1$; the survey already excludes every graph with $\mu \le 4$. The navigator is left untouched.
