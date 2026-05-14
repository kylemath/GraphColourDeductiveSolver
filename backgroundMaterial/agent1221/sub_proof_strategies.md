# Agent 1221 Report: Deep Evaluation of Proof Strategies for the Four Colour Theorem

**Agent:** 1221 (Mathematical Analyst)  
**Date:** 17 February 2026  
**Project:** Graph Colouring — Sub-Proof Strategy Analysis  
**Input:** Agent 1012 Report (five proof strategies), Agent 1007 Problem Set, independent research  

---

## Table of Contents

1. [Preamble](#1-preamble)
2. [Strategy 1: Algebraic — The Chromatic Polynomial](#2-strategy-1-algebraic--the-chromatic-polynomial)
3. [Strategy 2: Flow-Theoretic — Tutte's Conjectures](#3-strategy-2-flow-theoretic--tuttes-conjectures)
4. [Strategy 3: Topological — Exploiting the Jordan Curve Theorem](#4-strategy-3-topological--exploiting-the-jordan-curve-theorem)
5. [Strategy 4: Refined Discharging with Fewer Configurations](#5-strategy-4-refined-discharging-with-fewer-configurations)
6. [Strategy 5: Proof-Theoretic — Extracting Structure from Coq Proof](#6-strategy-5-proof-theoretic--extracting-structure-from-coq-proof)
7. [Agent 1221's Additional Strategy Ideas](#7-agent-1221s-additional-strategy-ideas)
8. [Comparative Summary](#8-comparative-summary)
9. [Recommended Research Programme](#9-recommended-research-programme)

---

## 1. Preamble

Agent 1012 identified five strategies towards a human-readable proof of the Four Colour Theorem (4CT). This report provides an independent deep evaluation of each, including mathematical depth analysis, independent feasibility assessment, risk analysis, synergy mapping, and concrete next steps. I then propose six additional strategies drawing on spectral graph theory, probabilistic methods, matroid theory, the Hadwiger conjecture, representation theory, and game-theoretic formulations.

Throughout, I use 4CT to denote the Four Colour Theorem, $\chi(G)$ for the chromatic number of $G$, $P(G, k)$ for the chromatic polynomial, and standard graph-theoretic notation.

---

## 2. Strategy 1: Algebraic — The Chromatic Polynomial

### 2.1 Mathematical Depth

The chromatic polynomial $P(G, k)$ is defined by the deletion-contraction recurrence

$$P(G, k) = P(G - e, k) - P(G / e, k)$$

for any edge $e$, with $P(\overline{K_n}, k) = k^n$ for the edgeless graph. For a planar graph $G$, the 4CT is equivalent to $P(G, 4) > 0$.

**Key results in the literature:**

- **Birkhoff-Lewis (1946):** For any planar triangulation $T$ on $n$ vertices, $P(T, k) > 0$ for all real $k \geq 5$. The proof uses the Birkhoff-Lewis equations, which express $P(T, k)$ in terms of the boundary colourings of a ring surrounding a configuration. The gap between $k \geq 5$ and $k \geq 4$ has resisted closure for 80 years.

- **Thomassen (1997):** The roots of chromatic polynomials of planar graphs are dense in the interval $(32/27, \infty)$. This is discouraging: it means one cannot simply show roots avoid a neighbourhood of 4 by abstract density arguments.

- **Royle (2008):** Extensive computational study of chromatic roots of planar graphs. Found no real root in the interval $(3, 4)$ for any tested graph, consistent with the conjecture that all real chromatic roots of planar graphs lie in $(-\infty, 0] \cup \{1\} \cup [2, 3) \cup \{4, 5, \ldots\}$, but disproof of the stronger "no roots in $(3, 4)$" conjecture remains possible.

- **Jackson (1993):** Proved that chromatic polynomials of 3-connected graphs have no roots in the interval $(1, 32/27]$. This is the best unconditional result bounding roots away from small integers for structured classes.

- **Sokal (2001, 2004):** Connected chromatic roots to the partition function of the Potts model in statistical mechanics. Showed that the complex zeros of $P(G, q)$ for planar graphs are dense in the complex plane, which severely constrains analytic approaches.

**The machinery required is deep.** One needs:
1. Real algebraic geometry (the structure of real roots of multivariate polynomial families).
2. The theory of stable polynomials (Borcea-Brändén theory), which characterises polynomials with roots confined to half-planes.
3. Potential theory and the distribution of zeros of graph polynomials.
4. Transfer matrix methods for computing $P(G, k)$ for families of planar graphs.

**Key open problems blocking progress:**
- **The Beraha conjecture** (partially resolved): the accumulation points of real chromatic roots of planar graphs are the Beraha numbers $B_n = 4\cos^2(\pi/n)$, which include $B_\infty = 4$. If $4$ is an accumulation point of roots from below, then no uniform gap $P(G, 4) > \epsilon > 0$ can hold — one would need a qualitative argument that $P(G, 4) > 0$ despite roots approaching 4.
- **Absence of a positivity certificate:** Even if all real roots lie below 4, proving $P(G, 4) > 0$ requires either bounding the polynomial from below at $k=4$ or establishing a combinatorial identity showing $P(G, 4)$ counts something manifestly positive.

### 2.2 Feasibility Assessment

**Agent 1012's assessment:** Medium feasibility, High elegance, Near-term incremental results possible.

**Agent 1221's assessment: I largely agree, with a downward adjustment on near-term prospects for the full result.**

- *Medium feasibility* is correct for the programme as a whole. The Birkhoff-Lewis gap ($k \geq 5$ to $k \geq 4$) has stood for 80 years despite substantial effort, which suggests a fundamental obstruction rather than mere lack of attention.
- *High elegance* is correct. A proof that $P(G, 4) > 0$ for all planar $G$ via root distribution would be one of the most beautiful results in combinatorics.
- *Near-term incremental results* are possible — but I note they are incremental in the sense of constraining root distributions further, not in the sense of approaching the 4CT. The distance between "we know roots avoid $(3, 3.5)$" and "roots avoid $(3, 4)$" is technically and conceptually enormous. Each improvement requires qualitatively new ideas.

**Revised assessment:** Medium-Low feasibility for 4CT itself, High elegance, Near-term incremental results possible but far from the goal.

### 2.3 Risk Analysis

**Fundamental barriers:**
1. **Sokal's density result.** Complex chromatic roots are dense in $\mathbb{C}$ for planar graphs. Any argument must carefully distinguish real from complex roots. The standard tools of complex analysis (argument principle, Rouché's theorem) become treacherous when roots are dense everywhere in the complex plane.
2. **The Beraha numbers.** $B_n = 4\cos^2(\pi/n) \to 4$ as $n \to \infty$. If the Beraha numbers are indeed accumulation points of real chromatic roots of planar triangulations, then any bound of the form $P(G, 4) \geq f(n) > 0$ must have $f(n) \to 0$, making the argument inherently delicate.
3. **Combinatorial explosion in deletion-contraction.** Computing $P(G, k)$ exactly requires exponential time. Any proof via chromatic polynomials must work with structural properties of $P$, not with explicit computation.
4. **No known positivity mechanism.** Unlike the permanent (which counts perfect matchings and is manifestly non-negative for bipartite graphs), $P(G, 4)$ has no known interpretation as a manifestly positive quantity for planar $G$. Finding such an interpretation would be a breakthrough in itself.

**What could go wrong:** The entire programme could be blocked by the discovery of a planar graph family whose real chromatic roots accumulate at 4 from below. While this would not disprove the 4CT (since $P(G, 4) > 0$ is a strict inequality), it would make any analytic proof via root bounds essentially impossible.

### 2.4 Synergies

- **With Strategy 2 (Flows):** The Tutte polynomial $T(G; x, y)$ unifies the chromatic polynomial ($P(G, k) = (-1)^{|V|-c(G)} k^{c(G)} T(G; 1-k, 0)$) and the flow polynomial. Insights about one polynomial may transfer to the other via this duality.
- **With Strategy 4 (Discharging):** Discharging could be used to establish structural properties of near-triangulations that constrain their chromatic polynomial behaviour, providing "input" to an algebraic argument.
- **With Strategy 5 (Proof mining):** The 633 reducibility checks in the Coq proof implicitly verify that certain chromatic polynomial evaluations are positive. Extracting the algebraic content of these checks could suggest general positivity patterns.

### 2.5 Concrete Next Steps

1. **Survey and catalogue** all known results on real chromatic roots of planar graphs, with emphasis on the interval $[3, 4]$. Create a database of chromatic polynomials for planar triangulations up to ~25 vertices using the transfer matrix method.
2. **Investigate stable polynomial theory.** Determine whether the Borcea-Brändén theory (which characterises polynomials preserving half-planes under linear operators) can be applied to chromatic polynomials of planar graphs. Specifically: is there a linear operator that maps $P(G, k)$ to a polynomial with only real roots, all $\leq 4$?
3. **Study the connection to the Potts model partition function.** In statistical mechanics, the $q$-state Potts model partition function at zero temperature on a planar graph $G$ equals $P(G, q)$. Phase transition analysis might reveal why $q = 4$ is critical.
4. **Attempt to prove** $P(G, 4) > 0$ for restricted classes of planar graphs (e.g., planar graphs of treewidth $\leq k$, Apollonian networks, stacked triangulations) as test cases.

---

## 3. Strategy 2: Flow-Theoretic — Tutte's Conjectures

### 3.1 Mathematical Depth

By Tutte's duality theorem, a planar graph $G$ is $k$-colourable if and only if its planar dual $G^*$ admits a nowhere-zero $k$-flow. Here a **nowhere-zero $k$-flow** on a graph $H$ is an orientation of the edges together with an assignment $\phi: E(H) \to \{1, 2, \ldots, k-1\}$ satisfying Kirchhoff's current law (flow conservation) at every vertex modulo $k$. (Equivalently, the values lie in $\mathbb{Z}_k \setminus \{0\}$ and satisfy $\sum_{e \text{ in}} \phi(e) = \sum_{e \text{ out}} \phi(e) \pmod{k}$ at every vertex.)

**Key results:**

- **Tutte's conjectures:** (a) Every bridgeless graph has a nowhere-zero 5-flow (the **5-flow conjecture**, 1954). (b) Every bridgeless graph without a Petersen minor has a nowhere-zero 4-flow (the **4-flow conjecture**, 1966). The 4CT for planar graphs is equivalent to the nowhere-zero 4-flow theorem for planar duals.
- **Seymour (1981):** Every bridgeless graph has a nowhere-zero 6-flow. This was the first major result toward Tutte's conjectures.
- **Thomassen (2012):** Every 8-edge-connected graph has a nowhere-zero 3-flow, confirming Jaeger's weak 3-flow conjecture.
- **Lovász, Thomassen, Wu, Zhang (2013):** Every 6-edge-connected graph has a nowhere-zero 3-flow.
- **DeVos, Neumann-Lara, and others:** Partial results on the 5-flow conjecture for graphs with certain structural properties.

**The machinery required:**
1. Matroid theory (the flow space of a graph is the cycle matroid of the dual).
2. Group-valued flows and the group connectivity framework (Jaeger, Linial, Payan, Tarsi). The number of nowhere-zero flows over any abelian group of order $k$ depends only on $k$, not on the group structure.
3. Algebraic topology of graph embeddings (the flow lattice as a sublattice of $\mathbb{Z}^E$).
4. The theory of graph minors (Robertson-Seymour), particularly for the 4-flow conjecture where excluding the Petersen minor is critical.

**Key open problems blocking progress:**
- **The 5-flow conjecture** remains open after 70+ years. Closing the gap from 6-flow (Seymour) to 5-flow would be major progress but still insufficient for 4CT.
- **The 4-flow conjecture for planar graphs** is equivalent to 4CT, so any progress here is literally progress on 4CT. But the flow formulation has not yet yielded techniques substantially different from the colouring formulation.
- **Circular flows:** Goddyn, Tarsi, and Zhang studied circular flows (where the values lie in a real interval modulo integers). The circular flow number $\Phi_c(G)$ is a refinement of the integer flow number. For planar graphs, 4CT is equivalent to $\Phi_c(G^*) \leq 4$ for all bridgeless planar $G^*$. Tightening bounds on $\Phi_c$ for planar graphs is an active area.

### 3.2 Feasibility Assessment

**Agent 1012's assessment:** Medium feasibility, High elegance, Possibly tied to open conjectures.

**Agent 1221's assessment: I agree on elegance but lower the feasibility slightly.**

The flow formulation is mathematically beautiful and reframes 4CT as a statement about linear algebra over $\mathbb{Z}_4$, which has significant appeal. However, the formulation is *provably equivalent* to 4CT, so any proof via flows must confront the same fundamental difficulties. The advantage is that the flow language connects to algebraic topology, matroid theory, and linear algebra in ways that the colouring language does not — but these connections have been explored for decades without breakthrough on the planar case.

The key concern is that the strongest unconditional results (Seymour's 6-flow, Thomassen's and Lovász et al.'s 3-flow under high edge-connectivity) all require either weakening the conclusion (6 instead of 4) or strengthening the hypothesis (high edge-connectivity). For the 4CT, we need *exactly* 4-flow for *all* bridgeless planar graphs, with no room for either relaxation.

**Revised assessment:** Medium-Low feasibility, High elegance, Progress tied to resolving major open conjectures.

### 3.3 Risk Analysis

**Fundamental barriers:**
1. **Equivalence to 4CT.** The flow formulation does not simplify the problem; it reformulates it. Any proof must eventually grapple with the same local structures (degree-5 vertices, Kempe chain interactions) that make the colouring formulation hard.
2. **The Petersen obstruction.** The Petersen graph is the unique smallest bridgeless graph with no nowhere-zero 4-flow. For non-planar graphs, the 4-flow conjecture requires excluding the Petersen graph as a minor. For planar graphs, the Petersen minor is automatically excluded (by Kuratowski's theorem, since the Petersen graph is non-planar), but the structural reason why planarity prevents the obstruction is not well understood in flow terms.
3. **The integrality gap.** Fractional (real-valued) flows are easy to construct, but the integrality constraint ($\phi(e) \in \{1, 2, 3\}$ for a 4-flow) introduces combinatorial complexity that resists continuous techniques.

**What could go wrong:** The flow formulation might turn out to be "just as hard" as the colouring formulation, in the sense that any flow-based proof inevitably reduces to case analysis comparable to the Appel-Haken/RSST approach.

### 3.4 Synergies

- **With Strategy 1 (Chromatic Polynomial):** The flow polynomial $F(G, k)$ counts nowhere-zero $k$-flows. For planar graphs, $F(G^*, k) = P(G, k) / k$ (up to normalisation). Root distribution results for one polynomial directly constrain the other.
- **With Strategy 3 (Topological):** Flows are topological objects — they live in the cycle space $H_1(G; \mathbb{Z}_k)$. The topological structure of the planar embedding constrains the cycle space in ways that might be exploitable.
- **With Strategy 4 (Discharging):** The discharging method in the dual graph has a natural interpretation as redistributing "flow capacity." A flow-aware discharging scheme might yield smaller unavoidable sets.

### 3.5 Concrete Next Steps

1. **Study circular flow numbers** of planar graph families. Determine whether $\Phi_c(G) < 4$ for broad classes of bridgeless planar graphs, aiming to identify which graphs are "hardest" to flow.
2. **Investigate the group connectivity framework.** Jaeger et al. showed that group connectivity (a strengthening of having a nowhere-zero flow) has better structural properties. Determine whether planar graphs have stronger group connectivity than mere 4-flow existence.
3. **Connect to integer programming.** A nowhere-zero 4-flow is a feasible solution to a system of linear equations over $\mathbb{Z}_4$ with exclusion constraints. Modern integer programming techniques (cutting planes, branch-and-bound) might yield structural insights.
4. **Explore the connection between flows and tensions.** A proper $k$-colouring induces a nowhere-zero $k$-tension on the graph; tensions and flows are dual in the algebraic sense. Understanding this duality more deeply might reveal why 4 is the right number.

---

## 4. Strategy 3: Topological — Exploiting the Jordan Curve Theorem

### 4.1 Mathematical Depth

The 4CT is a statement about planar graphs — objects defined by their embeddability in $\mathbb{R}^2$ (or equivalently $S^2$). Yet the known proofs use planarity only through its combinatorial consequences (Euler's formula, the existence of low-degree vertices, the structure of faces). Agent 1012 correctly identifies this as a missed opportunity.

**Key results:**

- **Lipton-Tarjan Planar Separator Theorem (1979):** Every $n$-vertex planar graph has a separator $S$ with $|S| \leq 2\sqrt{2n}$ such that removing $S$ leaves no component larger than $2n/3$. Moreover, $S$ can be found in linear time.
- **Tree decomposition:** The separator theorem implies planar graphs have treewidth $O(\sqrt{n})$. For graphs of treewidth $w$, every NP-hard problem (including optimal colouring) can be solved in time $O(n \cdot k^w)$ by dynamic programming — but for $w = O(\sqrt{n})$ and $k = 4$, this is still $4^{O(\sqrt{n})}$, which is better than brute force but not polynomial.
- **Robertson-Seymour structure theorem for planar graphs:** Planar graphs are $K_5$-minor-free and $K_{3,3}$-minor-free. The Graph Minor Theory provides deep structural characterisations of minor-closed families.
- **Thomassen (1994):** Every planar graph is 5-list-colourable. The proof is inductive and uses planarity via the existence of a short facial walk. This is arguably the most topological proof about colouring planar graphs, though it gives 5 colours, not 4.
- **Thomassen (1997, 2007):** Results on exponentially many 5-list-colourings of planar graphs.

**The machinery required:**
1. The theory of tree decompositions and treewidth.
2. Algorithmic aspects of planar separators (nested dissection, recursive decomposition).
3. Homotopy and homology of planar graphs (Kempe chains as paths in the dual graph; their interactions are governed by planarity via the Jordan Curve Theorem).
4. The topological theory of graph embeddings on surfaces.

**Key open problems blocking progress:**
- **Extension complexity of 4-colouring across separators.** Given a separator $S$ in a planar graph and a proper 4-colouring of the "outside," can we always extend it to the "inside"? This is not true in general — the restriction of a 4-colouring to $S$ might not extend. The question is whether *some* 4-colouring of the outside always has an extendable restriction, which is what the 4CT guarantees but which we want to prove constructively.
- **Kempe chain interactions across separators.** In a planar graph, two Kempe chains for different colour pairs cannot cross (by the Jordan Curve Theorem — each Kempe chain, together with the edges of the planar embedding, forms a curve that separates the plane). This non-crossing property is the topological content of planarity that is currently underexploited. Understanding it better is critical.

### 4.2 Feasibility Assessment

**Agent 1012's assessment:** Low-Medium feasibility, High elegance, Partial results plausible.

**Agent 1221's assessment: I agree on feasibility and elegance, and I am slightly more optimistic about the value of partial results.**

The divide-and-conquer approach via separators is conceptually clean but faces the fundamental problem that the separator can have $O(\sqrt{n})$ vertices, and the number of possible 4-colourings of the separator is $4^{O(\sqrt{n})}$. Showing that at least one such colouring extends to both sides requires understanding the "extension space" — the set of boundary colourings that extend to the interior. This set has been studied under the name **colour flow** in the literature, and its structure is known to be complex.

However, I am more optimistic about the topological non-crossing property of Kempe chains. The fact that Kempe chains for different colour pairs cannot cross in a planar embedding is a powerful constraint that is barely used in the current proof. Specifically:

**Observation (Agent 1221):** In Kempe's original argument, the failure occurs when two Kempe chains for colours $(a, b)$ and $(a, c)$ starting from different neighbours of a degree-5 vertex $v$ intersect, preventing independent swaps. In a planar graph, these chains form paths in the plane, and by the Jordan Curve Theorem, if the $(a,b)$-chain from $w_1$ reaches $w_3$, then the $(a,c)$-chain from $w_2$ is confined to one side of it. This constraint limits the possible configurations that can actually arise at degree-5 vertices and might reduce the case analysis to human-checkable size.

**Revised assessment:** Low-Medium feasibility for the full programme, Medium-High elegance, Partial results on Kempe chain non-crossing are potentially valuable.

### 4.3 Risk Analysis

**Fundamental barriers:**
1. **Separator size.** $O(\sqrt{n})$ is too large for direct case analysis. Even for $n = 100$, a separator might have $\sim 15$ vertices, giving $4^{15} \approx 10^9$ boundary colourings to consider.
2. **Extension is NP-hard in general.** Determining whether a partial colouring of a graph extends to a full proper $k$-colouring is NP-complete for $k \geq 3$, even for planar graphs. So the separator approach requires exploiting specific structural properties of the separator, not just its size.
3. **Lack of topological tools for graph colouring.** Despite 170 years of work on the 4CT, no proof has successfully leveraged deep topological tools (homotopy groups, sheaf theory, etc.). This suggests either that the problem is fundamentally combinatorial at its core, or that the right topological framework has not yet been found.

**What could go wrong:** The topological approach might produce beautiful structural results about Kempe chains in planar graphs without actually proving 4CT. The non-crossing property constrains the geometry of Kempe chains but may not constrain it enough to eliminate all hard cases.

### 4.4 Synergies

- **With Strategy 4 (Discharging):** The separator theorem could be used to decompose the discharging argument. Instead of a global discharging argument on the entire graph, one could apply discharging independently within each piece of a separator decomposition, potentially reducing the number of configurations needed per piece.
- **With Strategy 1 (Chromatic Polynomial):** The chromatic polynomial of a graph decomposes nicely along separators: if $S$ is a clique separator, then $P(G, k) = P(G_1, k) \cdot P(G_2, k) / P(K_{|S|}, k)$. For non-clique separators, the relationship is more complex but still structured.
- **With Strategy 2 (Flows):** The topological structure of the planar embedding directly constrains the cycle space (and hence the flow space) of the graph.

### 4.5 Concrete Next Steps

1. **Formalise the Kempe chain non-crossing property.** State and prove a precise theorem: in a planar triangulation $T$ with a proper 4-colouring, the Kempe chains for colour pairs $(a,b)$ and $(c,d)$ with $\{a,b\} \cap \{c,d\} = \emptyset$ do not interleave around any vertex. Determine the full set of topological constraints.
2. **Study the extension problem for small separators.** For a cycle separator of length $\ell \leq 10$, enumerate the 4-colourings of the cycle and determine which extend to the interior of a near-triangulation. Look for patterns that generalise.
3. **Connect to Thomassen's 5-list-colouring proof.** Thomassen's proof uses the existence of a short boundary and pre-colours two adjacent vertices. Determine whether a similar structural argument can be pushed to 4 colours for specific boundary structures.
4. **Investigate homological methods.** The cycle space $H_1(G; \mathbb{Z}_2)$ of a planar graph is generated by facial cycles. Kempe chains define elements of this homology. Determine whether the non-crossing constraint is a consequence of a deeper homological obstruction.

---

## 5. Strategy 4: Refined Discharging with Fewer Configurations

### 5.1 Mathematical Depth

The discharging method is the engine of both the Appel-Haken and RSST proofs. The mathematical content is:

1. **Charge assignment:** Assign charge $c(v) = 6 - \deg(v)$ to each vertex $v$ of a planar triangulation $T$. By Euler's formula, $\sum_v c(v) = 12 > 0$.

2. **Discharging rules:** Redistribute charge according to local rules (e.g., "every vertex of degree $\geq 7$ sends charge $1/2$ to each adjacent vertex of degree 5"). The rules preserve total charge.

3. **Unavoidability argument:** After discharging, every vertex must have non-negative final charge (since total charge is 12 and we need the discharging to "explain" where the positive charge goes). If we can show that the only way for a vertex to retain positive charge is to be surrounded by one of $N$ specific configurations, then the set of $N$ configurations is **unavoidable**.

4. **Reducibility testing:** Each configuration in the unavoidable set must be shown to be **reducible** — i.e., it cannot appear in a minimum counterexample. This is done by verifying that any 4-colouring of the boundary ring can be extended to the interior via Kempe chain arguments (or more precisely, via D-reducibility or C-reducibility checks).

**Key results:**

- **Appel-Haken (1976):** 487 discharging rules, 1476 configurations (later revised to 1,936).
- **RSST (1997):** 32 discharging rules, 633 configurations. The rules are simpler, more elegant, and easier to verify.
- **Steinberger (2010):** Explored the trade-off between rule complexity and configuration count. Showed that more sophisticated rules can reduce the number of configurations.
- **Hliněný (2015):** Used computer search to find small unavoidable sets for related problems (list colouring, choosability).
- **Lower bounds on unavoidable sets:** Surprisingly, no good lower bound is known on the minimum number of reducible configurations in an unavoidable set. It is not known whether $N = 1$ is achievable (this would mean every planar triangulation contains a single specific reducible configuration, which would give a trivial inductive proof).

**The mathematics is not deep but is technically demanding.** The discharging rules are elementary (linear combinations of local degree conditions), and the reducibility checks are finite computations. The difficulty is the *optimisation problem*: finding the right rules and the smallest unavoidable set.

### 5.2 Feasibility Assessment

**Agent 1012's assessment:** High feasibility, Medium elegance, Computational experiments feasible now.

**Agent 1221's assessment: I agree. This is the most immediately actionable strategy.**

The key question is: what is the minimum $N$ such that there exists an unavoidable set of $N$ reducible configurations, with discharging rules of bounded complexity? The current record is $N = 633$ (RSST). The question is whether $N$ can be pushed below, say, 50, at which point each reducibility check might be human-verifiable.

**Empirical evidence suggests significant room for improvement:**
- RSST's 32 rules are already much simpler than Appel-Haken's 487. The reduction from 1,476 to 633 configurations came primarily from better rules, not from deeper mathematical insight.
- Steinberger's work showed that more sophisticated (but still elementary) rules can further reduce the count. The limit of this approach is unknown.
- Modern SAT solvers and automated reasoning tools are dramatically more powerful than the tools available in 1997. A systematic computer search for optimal discharging rule sets is now feasible.

**The elegance concern is real.** Even if $N$ drops to 20, the proof would still involve 20 separate reducibility checks, each requiring pages of Kempe chain argument. The proof would be "human-readable" in the sense that a determined mathematician could check it in a few weeks, but it would not be "elegant" in the sense of revealing *why* four colours suffice.

**Revised assessment:** High feasibility, Medium elegance, Immediate computational progress possible. The most promising near-term path.

### 5.3 Risk Analysis

**Fundamental barriers:**
1. **Possible lower bound on $N$.** It is conceivable that $N$ has a non-trivial lower bound — perhaps $N \geq 100$ for any discharging-based proof. No such bound is known, but its existence would limit the strategy.
2. **Rule complexity vs. configuration count trade-off.** As rules become more sophisticated, they become harder to verify. At some point, verifying the discharging rules themselves might require computer assistance, defeating the purpose.
3. **Reducibility verification.** Even if the unavoidable set shrinks, each reducibility check must still verify that a specific configuration cannot appear in a minimum counterexample. For large ring sizes (the RSST configurations have rings of up to 14 vertices), this verification involves checking up to $4^{14} \approx 2.7 \times 10^8$ boundary colourings. Kempe chain arguments can reduce this, but the reduction is configuration-specific.

**What could go wrong:** The minimum $N$ for "natural" discharging rules might be much larger than 20. If $N \geq 100$, the proof remains computer-dependent even after optimisation.

### 5.4 Synergies

- **With Strategy 5 (Proof mining):** If the Coq proof's 633 configurations can be clustered into a small number of "types" via proof mining, this would suggest which configurations are redundant and guide the search for smaller unavoidable sets.
- **With Strategy 3 (Topological):** The planar separator theorem could be used to restrict the class of configurations that need to be considered. If separator-based arguments handle all cases except those near degree-5 vertices, the discharging approach only needs to handle a restricted class.
- **With modern AI tools:** Large language models and neural network-guided search could explore the space of discharging rules more efficiently than exhaustive enumeration.

### 5.5 Concrete Next Steps

1. **Implement a flexible discharging framework.** Build a software system that takes a set of discharging rules, computes the unavoidable set they imply, and tests each configuration for reducibility. The RSST code exists but is tightly coupled to their specific rules.
2. **Use SAT/SMT solvers to search for optimal rules.** Encode the discharging problem as a constraint satisfaction problem: given a target unavoidable set size $N$, find a set of rules that makes exactly $N$ configurations unavoidable, all of which are reducible.
3. **Study the theoretical minimum.** Investigate whether there is an information-theoretic or structural lower bound on the size of unavoidable sets of reducible configurations. Does every unavoidable set of reducible configurations need to include configurations of ring size $\geq r$ for some $r > 6$?
4. **Develop "human-friendly" reducibility proofs.** For each configuration in a small unavoidable set, develop the simplest possible Kempe chain argument establishing its reducibility, aiming for arguments that fit on a single page.

---

## 6. Strategy 5: Proof-Theoretic — Extracting Structure from Coq Proof

### 6.1 Mathematical Depth

Gonthier's Coq formalisation of the 4CT is a landmark in formal verification. The proof, developed using the SSReflect extension to Coq, is a fully machine-verified certificate. The mathematical content is the same as the RSST proof — discharging with 32 rules and 633 configurations — but the formalisation exposes every logical step.

**Key aspects of the Coq proof:**

- **Size:** The formalisation comprises approximately 60,000 lines of Coq code (the "Four Colour" library), including a substantial development of graph theory from scratch.
- **Structure:** The proof breaks into (a) a formalisation of planar graph theory, (b) the discharging argument, and (c) the 633 reducibility verifications, each encoded as a computation that Coq checks.
- **Computational content:** The reducibility checks are encoded as decision procedures. Coq's kernel verifies that these procedures return "true" for each configuration. The logical content of *why* each returns "true" is implicit in the execution trace.

**Proof mining** (Kohlenbach, 2008) is a programme in mathematical logic that extracts quantitative content from non-constructive proofs. Specifically, from a proof of $\forall x \exists y\, P(x, y)$, proof mining extracts explicit bounds on $y$ in terms of $x$. The Coq 4CT proof is constructive (it computes a 4-colouring, in principle), so classical proof mining is less directly applicable, but related techniques for simplifying and compressing proofs are relevant.

**LLM-based proof analysis** is a nascent field (2024–2026). Recent work has trained models on Lean 4 and Coq proof corpora to suggest proof steps, fill in proof gaps, and identify structural similarities between proof branches. The 633 reducibility checks in the 4CT proof are an ideal target: they are structurally similar (each verifies that a specific ring can be coloured from any boundary colouring) and might collapse into a small number of parameterised templates.

### 6.2 Feasibility Assessment

**Agent 1012's assessment:** Medium feasibility, Medium elegance, Requires engineering effort.

**Agent 1221's assessment: I agree on feasibility and the need for engineering effort, but I rate the elegance higher if the project succeeds.**

If the 633 reducibility checks can be collapsed into, say, 5 parameterised lemma families, the resulting proof would be substantially more transparent. The 5 lemma families would each be a general statement about how Kempe chains interact in configurations with specific structural properties (e.g., "In any configuration with a ring of size $\leq k$ and at most $m$ internal vertices of degree $\leq 5$, every boundary 4-colouring extends to the interior via at most $j$ Kempe chain swaps"). Such a result would be both elegant and insightful.

The main obstacle is that proof mining from Coq proofs requires expertise in both formal verification and proof theory. The 4CT Coq proof is particularly opaque because much of it consists of computations (the reducibility checker running on each configuration) rather than deductive steps.

**Revised assessment:** Medium feasibility, Medium-High elegance (if successful), Significant engineering effort required. Most promising as a complement to Strategy 4.

### 6.3 Risk Analysis

**Fundamental barriers:**
1. **Computational content vs. logical content.** The Coq proof's reducibility checks are computations, not deductive arguments. Extracting logical content from a computation is fundamentally difficult — it is analogous to decompilation. The "proof" that configuration 347 is reducible is "the reducibility checker returns true on this input," which conveys no mathematical insight.
2. **Lack of intermediate structure.** The 633 configurations were not designed to have a common structure; they were found by computer search to cover the unavoidable set. There is no a priori reason to expect them to cluster into a small number of types.
3. **Scale of the Coq development.** 60,000 lines of Coq code is a substantial corpus. Understanding and modifying it requires months of dedicated effort by someone fluent in both Coq and graph theory.

**What could go wrong:** The 633 configurations might be genuinely irreducibly diverse — each requiring a qualitatively different Kempe chain argument. In this case, no amount of proof mining would reduce the proof to human-readable size.

### 6.4 Synergies

- **With Strategy 4 (Fewer Configurations):** If proof mining reveals that, say, 500 of the 633 configurations are reducible by the same argument, then one only needs 133 + 1 = 134 separate checks, which is a major improvement. Combined with a better discharging scheme (Strategy 4), the total might drop below 50.
- **With LLM/AI assistance:** Modern LLMs can parse Coq proof scripts, identify recurring patterns, and suggest generalisations. A focused project using AI to analyse the 4CT Coq proof could yield rapid progress.
- **With Strategy 1 (Algebraic):** The reducibility checks implicitly establish that certain chromatic polynomial evaluations are positive. Extracting these algebraic consequences could feed into the chromatic polynomial programme.

### 6.5 Concrete Next Steps

1. **Obtain and compile Gonthier's Coq proof.** Ensure it compiles with a modern version of Coq (it was originally developed for Coq 8.0 and may require porting). The Mathematical Components library now maintains a version.
2. **Instrument the reducibility checker.** Modify the Coq code to output a trace of each reducibility check: which Kempe chains are swapped, in what order, and which boundary colourings are "hard" (requiring the most swaps). This trace is the raw data for pattern analysis.
3. **Cluster the 633 configurations.** Using the instrumented traces, apply clustering algorithms (k-means on feature vectors derived from the trace, or graph similarity metrics on the configurations themselves) to identify families of "similar" configurations.
4. **For each cluster, attempt to write a parameterised lemma** in Coq that covers all configurations in the cluster. Verify that the lemma is correct and measure the reduction in proof size.
5. **Explore LLM-based proof compression.** Fine-tune an LLM on the 4CT Coq proof and ask it to identify generalisations of specific reducibility arguments.

---

## 7. Agent 1221's Additional Strategy Ideas

### Strategy 6: Spectral Graph Theory — Eigenvalue Bounds on Chromatic Number

#### 7.1.1 Core Idea

The chromatic number $\chi(G)$ is bounded below by several spectral quantities:

$$\chi(G) \geq 1 + \frac{\lambda_1}{\lambda_n}$$

where $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_n$ are the eigenvalues of the adjacency matrix $A(G)$ (this is the **Hoffman bound**). Equivalently, $\chi(G) \geq 1 - \lambda_1 / \lambda_n$. For the Laplacian $L(G) = D(G) - A(G)$ with eigenvalues $0 = \mu_1 \leq \mu_2 \leq \cdots \leq \mu_n$, we have $\chi(G) \geq n / (n - \mu_n)$.

**The programme:** Show that for every planar graph $G$, these spectral bounds never force $\chi(G) \geq 5$. This would not directly prove 4CT, but it would establish that spectral methods are *consistent* with 4CT. More ambitiously, develop spectral upper bounds: show that certain spectral conditions (which all planar graphs satisfy) imply $\chi(G) \leq 4$.

#### 7.1.2 Key Results and Open Problems

- **Hoffman (1970):** The bound $\chi(G) \geq 1 + \lambda_1/|\lambda_n|$ is tight for certain graph families (Kneser graphs, Paley graphs) but is generally loose for sparse graphs.
- **Wilf (1967):** $\chi(G) \leq 1 + \lambda_1(G)$, where $\lambda_1$ is the largest eigenvalue. For planar graphs, $\lambda_1 \leq O(\sqrt{n})$, so this bound is useless for proving $\chi \leq 4$.
- **Spectral radius of planar graphs:** The spectral radius of a planar graph on $n$ vertices satisfies $\lambda_1 \leq \sqrt{8(n-2)} + 1$ (Hong, 1993). For $n \geq 3$, this exceeds 4, so spectral radius alone cannot prove 4CT.
- **Colin de Verdière's invariant $\mu(G)$:** This spectral invariant satisfies $\mu(G) \leq 3$ iff $G$ is planar (Colin de Verdière, 1990). Moreover, $\mu(G) \geq \chi(G) - 1$ is conjectured but unproven — if true, it would imply $\chi(G) \leq \mu(G) + 1 \leq 4$ for planar graphs, proving 4CT. This conjecture is one of the most important open problems connecting spectral graph theory to colouring.

#### 7.1.3 Feasibility and Risks

**Feasibility: Low-Medium.** The Colin de Verdière conjecture $\chi(G) \leq \mu(G) + 1$ would prove 4CT as a corollary, but the conjecture is wide open and considered very hard. Without it, spectral methods give bounds that are too loose for sparse graphs.

**Risk:** Spectral bounds are inherently "continuous" — they capture average behaviour of the graph, not worst-case local structure. The 4CT is driven by local structure (degree-5 vertices, Kempe chain interactions), which spectral methods may be unable to see.

**Elegance: Very High.** A proof via Colin de Verdière's invariant would be one of the most elegant results in graph theory.

#### 7.1.4 Synergies

- With Strategy 1: The spectral radius is related to the growth rate of the chromatic polynomial's coefficients, providing another angle on root distribution.
- With Strategy 3: Colin de Verdière's invariant is defined in terms of a spectral optimisation over matrices respecting the graph structure, with topological constraints (transversality conditions). This is inherently topological.

#### 7.1.5 Concrete Next Steps

1. Survey the status of the Colin de Verdière conjecture $\chi(G) \leq \mu(G) + 1$. Identify the specific obstacles.
2. Compute $\mu(G)$ for all planar triangulations up to ~15 vertices. Verify that $\mu \leq 3$ and study the gap $\mu + 1 - \chi$.
3. Investigate whether weaker spectral bounds (e.g., using the signless Laplacian or normalised Laplacian) can be sharpened for planar graphs.

---

### Strategy 7: Probabilistic Methods — The Lovász Local Lemma and Entropy Compression

#### 7.2.1 Core Idea

The **Lovász Local Lemma (LLL)** provides conditions under which a random assignment avoids all "bad events" simultaneously. For graph colouring, a bad event $A_v$ at vertex $v$ is "all $k$ colours appear in the neighbourhood of $v$, leaving no free colour." If these bad events have bounded probability and limited dependency, LLL guarantees a proper colouring exists.

More precisely, consider a random 4-colouring of a planar graph $G$ (each vertex independently assigned a colour from $\{1,2,3,4\}$ uniformly at random). The probability that vertex $v$ has the same colour as a specific neighbour is $1/4$. The event $B_e$ = "edge $e = \{u,v\}$ is monochromatic" has $\Pr[B_e] = 1/4$. The dependency graph of the events $\{B_e\}$ has degree at most $2\Delta(G) - 2$ (each edge shares a vertex with at most $2\Delta - 2$ other edges). By the symmetric LLL, if $e \cdot p \cdot (d+1) \leq 1$, a proper colouring exists, where $p = 1/4$ and $d = 2\Delta - 2$. This gives $\chi(G) \leq 4$ when $e \cdot (2\Delta - 1)/ 4 \leq 1$, i.e., $\Delta \leq (4/e - 1)/2 \approx 0.24$, which is useless for $\Delta \geq 1$.

**The problem is clear:** the naive application of LLL to graph colouring requires $k \gg \Delta$, not $k = O(1)$. The best LLL-based results give $\chi(G) \leq \lceil \Delta / \ln \Delta \rceil$ for large $\Delta$ (Johansson, 1996, for triangle-free graphs), which is far from the constant bound needed for 4CT.

#### 7.2.2 The Entropy Compression Method

**Entropy compression** (Esperet-Parreau, 2013; Grytczuk-Kozik-Micek, 2013) is a refined probabilistic technique that goes beyond LLL by tracking the information content of the random process. Instead of merely showing a good colouring exists, it shows that a randomised algorithm must find one because the "compressed log" of a failed execution would have negative entropy.

For graph colouring, the idea is: run a randomised colouring algorithm (assign random colours, then use local resampling to fix conflicts). If the algorithm always terminates, a proper colouring exists. Entropy compression shows termination by proving that the execution trace can be encoded in fewer bits than the random bits consumed — a contradiction if the algorithm runs forever.

#### 7.2.3 Feasibility and Risks

**Feasibility: Low.** Current probabilistic methods require $k \gg \Delta$ or $k \gg \text{mad}(G)$ (maximum average degree) for general graphs. For planar graphs, $\text{mad}(G) < 6$, so one would need to show $4 \gg 6$, which is false. Specialised probabilistic arguments for planar graphs would need to exploit planarity-specific structure (e.g., the non-existence of dense minors), which is exactly what probabilistic methods are bad at.

**Risk:** The probabilistic method is fundamentally about showing that a random object has positive probability of satisfying constraints. For $k = 4$ colours and $\Delta$ up to 5, the probability of a random 4-colouring being proper is exponentially small but positive (this is what 4CT asserts). The LLL and entropy compression need the probability to be "large enough" in a quantifiable sense, and for planar graphs with $k = 4$, it is not.

**Elegance: High** (if it worked, which seems unlikely).

#### 7.2.4 An Alternative Probabilistic Angle: Random Contractions

A more promising probabilistic approach: start with a random 5-colouring (which exists by the Five Colour Theorem) and show that with positive probability, a random sequence of Kempe chain swaps reduces it to a 4-colouring. This would not require the colouring to be random — only the sequence of swaps. The analysis would require understanding the Markov chain on proper colourings induced by Kempe chain swaps (the **Kempe chain dynamics**).

**Key result:** Vigoda (2000) showed that the Markov chain on proper $k$-colourings (using single-vertex recolouring steps) mixes rapidly for $k > 11\Delta/6$. For Kempe chain dynamics, less is known, but Mohar and Salas (2009) studied this for specific graph families.

**For planar graphs with $\Delta \leq 5$:** The threshold $11\Delta/6 \approx 9.2$ is far above 4. However, the Kempe chain Markov chain has larger steps (swapping entire chains) and might mix faster. Understanding the Kempe chain dynamics specifically for planar graphs is a concrete research direction.

#### 7.2.5 Synergies

- With Strategy 3 (Topological): The topological non-crossing of Kempe chains constrains the Markov chain on colourings, potentially enabling better mixing time bounds.
- With Strategy 4 (Discharging): A probabilistic argument could complement discharging by showing that "most" configurations are easily reducible, leaving only a small exceptional set for case analysis.

#### 7.2.6 Concrete Next Steps

1. Analyse the Kempe chain Markov chain on proper 4-colourings of planar graphs. Determine whether it is connected (i.e., whether any two proper 4-colourings of a planar graph can be connected by a sequence of Kempe chain swaps). **Note:** Las Vergnas and Meyniel (1981) showed that the 5-colouring Kempe chain graph is connected for planar graphs. The corresponding statement for 4-colourings is open and important.
2. If the Kempe chain dynamics are connected for 4-colourings, study the mixing time. Rapid mixing would imply a randomised algorithm for 4-colouring, which is weaker than 4CT but algorithmically useful.
3. Investigate entropy compression specialised to planar graphs. Can planarity-specific properties (bounded density, excluded minors) yield entropy compression arguments that work for $k = 4$?

---

### Strategy 8: Matroid Theory and the Critical Group

#### 7.3.1 Core Idea

The **graphic matroid** $M(G)$ of a graph $G$ has the edges of $G$ as ground set and the spanning forests as bases. The **dual matroid** $M^*(G) = M(G^*)$ for planar graphs corresponds to the graphic matroid of the planar dual. The number of nowhere-zero $k$-flows on $G$ (and hence the number of proper $k$-colourings of $G^*$ for planar $G$) is a matroid invariant — it equals the evaluation of the Tutte polynomial $T(G; 0, 1-k)$ up to sign.

A less explored connection is via the **critical group** (also called the **sandpile group** or **Jacobian**) of a graph. The critical group $K(G)$ is a finite abelian group associated to $G$, defined as the cokernel of the reduced Laplacian matrix: $K(G) = \mathbb{Z}^{n-1} / \text{Im}(L_0)$, where $L_0$ is the Laplacian with one row and column deleted. Its order equals the number of spanning trees: $|K(G)| = \tau(G)$.

**The programme:** The structure of $K(G)$ (its invariant factors, its rank as a $\mathbb{Z}$-module, its $p$-Sylow subgroups) encodes combinatorial information about $G$ that might constrain the chromatic number. Specifically:

- If $K(G)$ has a $\mathbb{Z}_4$-quotient for every planar graph $G$, this would be related to the existence of a $\mathbb{Z}_4$-flow, which is the 4CT for planar graphs by Tutte duality.
- The **chip-firing game** on $G$ (which gives a combinatorial model for $K(G)$) has deep connections to divisor theory on algebraic curves (Baker-Norine theorem, 2007). For planar graphs, this might yield tropical geometry approaches.

#### 7.3.2 Key Results

- **Baker-Norine (2007):** A Riemann-Roch theorem for graphs, relating the rank of a divisor on a graph to the order of the critical group. This provides an analogy between graph colouring and algebraic geometry.
- **Klivans (2018):** Comprehensive study of the critical group and its connections to various graph invariants.
- **Backman (2017):** Connected the Tutte polynomial to the critical group via "fourientations" (partial orientations of edges), providing a combinatorial interpretation that might be relevant to flows.
- **Manjunath-Sturmfels (2012):** Developed the theory of "monomials and their standard pairs" for the lattice ideal associated to the Laplacian, connecting graph colouring to commutative algebra.

#### 7.3.3 Feasibility and Risks

**Feasibility: Low.** The connections between the critical group and the chromatic number are indirect. The critical group's order is the number of spanning trees, which is related to the Tutte polynomial but not directly to the chromatic polynomial at $k = 4$. Making these connections precise enough to prove 4CT would require substantial new theory.

**Risk:** The critical group might encode "the wrong information" — it captures global connectivity properties of $G$ (how many spanning trees, which cycles are independent) but not the local structure (degree-5 vertices, Kempe chains) that drives 4CT.

**Elegance: Very High.** A proof connecting 4CT to the Riemann-Roch theory of graphs would unify combinatorics, algebra, and geometry.

#### 7.3.4 Synergies

- With Strategy 2 (Flows): The critical group is directly related to $\mathbb{Z}_k$-flows. The Smith normal form of the Laplacian determines which $k$ admit nowhere-zero $k$-flows.
- With Strategy 6 (Spectral): The eigenvalues of the Laplacian determine the order of the critical group via $|K(G)| = \frac{1}{n}\prod_{i=2}^{n} \mu_i$.

#### 7.3.5 Concrete Next Steps

1. Compute the Smith normal form of the Laplacian for all planar triangulations up to ~15 vertices. Determine whether the invariant factor decomposition of $K(G)$ constrains the chromatic number.
2. Investigate whether the Baker-Norine Riemann-Roch theorem yields colouring bounds for planar graphs. Specifically, does the "gonality" of a planar graph (the minimum degree of a divisor of rank 1) relate to its chromatic number?
3. Study the $\mathbb{Z}_4$-rank of $K(G)$ for planar graphs. If every planar graph has a $\mathbb{Z}_4$-quotient of sufficient rank, this might yield a flow-based proof of 4CT.

---

### Strategy 9: The Hadwiger Conjecture Route

#### 7.4.1 Core Idea

**Hadwiger's Conjecture (1943):** Every graph with $\chi(G) \geq k$ contains $K_k$ as a minor.

The contrapositive: if $G$ has no $K_k$ minor, then $\chi(G) \leq k - 1$.

For $k = 5$: every $K_5$-minor-free graph is 4-colourable. Since planar graphs are $K_5$-minor-free (and $K_{3,3}$-minor-free) by Wagner's theorem, Hadwiger's conjecture for $k = 5$ implies the 4CT.

**The remarkable fact:** Hadwiger's conjecture for $k = 5$ was proved by Robertson, Seymour, and Thomas (1993) — but their proof *uses the 4CT as an ingredient*. Specifically, they show that every $K_5$-minor-free graph is either planar or has a specific decomposition involving planar pieces, and then apply 4CT to each piece.

**The programme:** Prove Hadwiger's conjecture for $k = 5$ without using 4CT. This would yield 4CT as a corollary, via a completely different route. Such a proof would need to establish that $K_5$-minor-free graphs are 4-colourable using the structure of minor-free graphs directly, without reducing to the planar case.

#### 7.4.2 Key Results

- **Hadwiger's conjecture for $k \leq 4$:** Proved by Hadwiger (1943) for $k \leq 3$ (elementary) and by Dirac (1952) for $k = 4$. No computer assistance needed.
- **$k = 5$:** Robertson-Seymour-Thomas (1993), using 4CT.
- **$k = 6$:** Robertson-Seymour-Thomas (1993), proved *equivalent* to the 4CT. Specifically, $H(6)$ (Hadwiger for $k=6$) is equivalent to: every $K_6$-minor-free graph is 5-colourable. They proved this by showing every such graph has a vertex of degree $\leq 4$ or a specific structure, and used 4CT for planar subgraphs.
- **$k \geq 7$:** Wide open. The best unconditional result is $\chi(G) \leq O(k \sqrt{\log k})$ for $K_k$-minor-free graphs (Kostochka, 1984; Thomason, 1984, 2001).

#### 7.4.3 Feasibility and Risks

**Feasibility: Low-Medium.** A 4CT-independent proof of Hadwiger for $k=5$ would be a major achievement. The Robertson-Seymour-Thomas decomposition shows that $K_5$-minor-free graphs are "almost planar" (they can be obtained from planar graphs by clique-sums), so the difficulty is in colouring planar graphs, which brings us back to 4CT. A proof that avoids this reduction would need genuinely new ideas about the structure of minor-free graphs.

**Risk:** It is possible that Hadwiger for $k=5$ is *inherently* as hard as 4CT — that any proof must, at some level, solve the same problem. The Robertson-Seymour-Thomas result suggests this.

**Elegance: Very High.** Hadwiger's conjecture is widely regarded as one of the most important open problems in graph theory. A self-contained proof for $k=5$ would be a landmark.

#### 7.4.4 Synergies

- With Strategy 3 (Topological): Minor-free graph theory is deeply topological (graph minors are defined by topological operations: deletion and contraction).
- With Strategy 6 (Spectral): Spectral bounds for minor-free graphs are tighter than for general graphs. Van der Holst, Laurent, and Schrijver connected Colin de Verdière's invariant to graph minors: $\mu(G) \leq k - 1$ iff $G$ has no $K_k$-minor (conjectured, proved for $k \leq 5$).

#### 7.4.5 Concrete Next Steps

1. Study the Robertson-Seymour-Thomas proof of Hadwiger for $k=5$ in detail. Identify precisely where 4CT is invoked and what structural property of planar graphs is used.
2. Determine whether the proof can be restructured to use the Five Colour Theorem instead of 4CT, yielding a weaker but 4CT-independent result: "every $K_5$-minor-free graph is 5-colourable." (This is already known unconditionally, but a proof via the Hadwiger framework might suggest how to push to 4 colours.)
3. Investigate whether the decomposition of $K_5$-minor-free graphs into planar pieces can be refined so that each piece has additional structure (e.g., bounded treewidth) that makes 4-colouring easy without 4CT.

---

### Strategy 10: Representation Theory and Symmetric Functions

#### 7.5.1 Core Idea

The chromatic polynomial $P(G, k)$ can be expressed using the **chromatic symmetric function** $X_G$ introduced by Stanley (1995):

$$X_G = \sum_{\kappa \text{ proper}} x_{\kappa(v_1)} x_{\kappa(v_2)} \cdots x_{\kappa(v_n)}$$

where the sum is over all proper colourings $\kappa: V(G) \to \mathbb{Z}_{>0}$ and $x_i$ are formal variables. The chromatic symmetric function generalises the chromatic polynomial: $P(G, k) = X_G|_{x_1 = \cdots = x_k = 1, x_{k+1} = x_{k+2} = \cdots = 0}$.

$X_G$ is a symmetric function in infinitely many variables and can be expanded in various bases of the ring of symmetric functions: the power sum basis $\{p_\lambda\}$, the Schur basis $\{s_\lambda\}$, and others. The coefficients in these expansions encode combinatorial information about $G$.

**The programme:** The Stanley-Stembridge conjecture (now a theorem, resolved by Hikita, 2024) states that $X_G$ is **$e$-positive** (i.e., has non-negative coefficients in the elementary symmetric function basis $\{e_\lambda\}$) for incomparability graphs of $(3+1)$-free posets. For planar graphs:

1. Determine whether $X_G$ has specific positivity properties for planar $G$.
2. Use the representation-theoretic interpretation of the Schur expansion (each coefficient $c_\lambda$ is the multiplicity of an irreducible $S_n$-representation in a certain module) to prove structural results about $P(G, k)$.
3. The key identity: $P(G, k) = \sum_\lambda c_\lambda \cdot s_\lambda(1^k)$, where $s_\lambda(1^k) = \prod_{(i,j) \in \lambda} (k + j - i)/(h(i,j))$ is the number of semistandard tableaux. If $c_\lambda \geq 0$ for all $\lambda$ (Schur positivity), then $P(G, k) > 0$ for all $k \geq n$, which is too weak. But specific structural results about *which* $\lambda$ appear might give $P(G, 4) > 0$.

#### 7.5.2 Key Results

- **Stanley (1995):** Introduced $X_G$ and showed it distinguishes trees (conjectured; still open for general graphs).
- **Gasharov (1996):** Proved the Stanley-Stembridge conjecture for Schur positivity (weaker than $e$-positivity) for $(3+1)$-free posets.
- **Hikita (2024):** Resolved the Stanley-Stembridge $e$-positivity conjecture.
- **Orellana-Scott (2014):** Connected $X_G$ to the representation theory of the symmetric group and the partition algebra.
- **Crew-Spirkl (2020):** Studied the chromatic symmetric function of planar graphs, with partial results on its structure.

#### 7.5.3 Feasibility and Risks

**Feasibility: Low.** The chromatic symmetric function is a powerful invariant but is notoriously difficult to work with for specific graph classes. The connection between Schur positivity of $X_G$ and the chromatic polynomial at specific integers is indirect. Moreover, $X_G$ is a much richer object than $P(G, k)$ — it encodes more information — and this extra information makes it harder to analyse, not easier.

**Risk:** The representation-theoretic approach might yield beautiful structural results about $X_G$ for planar graphs without implications for 4CT. The positivity of $P(G, 4)$ might not follow from any natural positivity property of $X_G$.

**Elegance: Very High.**

#### 7.5.4 Synergies

- With Strategy 1 (Chromatic Polynomial): $X_G$ is a lift of $P(G, k)$ to the ring of symmetric functions. Any result about $X_G$ descends to a result about $P(G, k)$.
- With Strategy 6 (Spectral): The eigenvalues of the adjacency matrix appear in the power-sum expansion of $X_G$ for regular graphs.

#### 7.5.5 Concrete Next Steps

1. Compute $X_G$ for all planar triangulations up to ~12 vertices. Determine the Schur expansion and look for patterns in the coefficients.
2. Investigate whether the $e$-positivity results for $(3+1)$-free posets extend to planar graphs (which are generally not $(3+1)$-free, so this is non-trivial).
3. Study whether the "immanant" interpretation of the chromatic symmetric function (via the representation theory of $GL_n$) yields positivity results relevant to 4CT.

---

### Strategy 11: Game-Theoretic Formulation — The Maker-Breaker Colouring Game

#### 7.6.1 Core Idea

The **graph colouring game** (Bodlaender, 1991; Zhu, 1999) is played by two players, Alice (Maker) and Bob (Breaker), who alternately colour vertices of a graph $G$ with colours from $\{1, \ldots, k\}$. Alice wants to complete a proper $k$-colouring; Bob wants to force a vertex with no legal colour. The **game chromatic number** $\chi_g(G)$ is the minimum $k$ for which Alice has a winning strategy.

**Key results:**
- **Zhu (2008):** $\chi_g(G) \leq 5$ for all planar graphs (i.e., Alice can always win with 5 colours on planar graphs).
- **Kierstead-Trotter (1994):** $\chi_g(G) \leq 33$ for planar graphs (first bound).
- **Current best:** Zhu's bound of $\chi_g(G) \leq 5$ for planar graphs is tight — there exist planar graphs with $\chi_g = 5$.
- **The 4CT implies** $\chi_g(G) \leq 4$ is false (since $\chi_g > \chi$ is possible), so the game chromatic number does not directly yield 4CT.

**However, a modified game is relevant.** Consider the **cooperative colouring game** where both players cooperate to colour $G$ with 4 colours, but they must colour vertices in a prescribed order (modelling a sequential algorithm). If for every vertex ordering, a proper 4-colouring can be achieved by a greedy strategy enhanced with Kempe chain repairs, this would constructively prove 4CT. This is essentially what Agent 1012's SPARK algorithm attempts.

#### 7.6.2 A More Promising Game-Theoretic Angle

**The Kempe swap game:** Start with an arbitrary proper 5-colouring of a planar graph $G$ (which exists by the Five Colour Theorem). Define a game where the single player (Maker) performs Kempe chain swaps, trying to reduce the number of colours used to 4. The game is won if Maker can always achieve this.

This formulation is equivalent to asking: is the **Kempe equivalence class** of any proper 5-colouring of a planar graph always connected to a proper 4-colouring via Kempe chain swaps?

**Key result:** Meyniel (1978) showed that for $k \geq \chi(G) + 1$, any two proper $k$-colourings of $G$ are connected by a sequence of Kempe chain swaps. For planar graphs, this gives connectivity for $k \geq 5$ (assuming 4CT). Without 4CT, we know connectivity for $k \geq 6$ (since $\chi \leq 5$ is unconditional).

**The question:** Are all proper 5-colourings of planar graphs Kempe-equivalent to some proper 4-colouring? This would prove 4CT constructively.

#### 7.6.3 Feasibility and Risks

**Feasibility: Medium.** The Kempe swap game is a concrete combinatorial question. For small planar graphs, it can be checked computationally. A structural argument about why Kempe swaps can always eliminate a colour would need to understand the global topology of the "colour space" of a planar graph.

**Risk:** The Kempe equivalence landscape for 4-colourings of planar graphs is known to be complex. Fisk (1977) showed that the 4-colourings of a planar triangulation modulo Kempe swaps form a group related to $\mathbb{Z}_2$-homology. This structure might be too complex for a direct game-theoretic argument.

**Elegance: Medium-High.**

#### 7.6.4 Synergies

- With Strategy 3 (Topological): Kempe swap connectivity is a topological question about the "reconfiguration graph" of colourings. The topological non-crossing of Kempe chains in planar graphs constrains this reconfiguration graph.
- With Strategy 7 (Probabilistic): If the Kempe swap Markov chain mixes rapidly, a random sequence of swaps will quickly find a 4-colouring (if one exists), providing both a probabilistic proof and an algorithm.

#### 7.6.5 Concrete Next Steps

1. **Computationally verify** that every proper 5-colouring of every planar triangulation on $\leq 15$ vertices can be reduced to a 4-colouring by Kempe chain swaps.
2. **Study the Kempe reconfiguration graph** for 4-colourings of planar graphs. Determine its diameter, connectivity, and structure.
3. **Investigate the Fisk theory** of Kempe equivalence classes for planar triangulations. Determine whether Fisk's algebraic structure can be exploited to show that 4-colourings are always reachable.
4. **Develop a theory of "colour elimination":** given a proper 5-colouring, provide a systematic strategy (a winning strategy in the Kempe swap game) for eliminating one colour.

---

## 8. Comparative Summary

| # | Strategy | Feasibility | Elegance | Near-Term Progress | Key Obstruction |
|---|----------|-------------|----------|--------------------|-----------------|
| 1 | Chromatic Polynomial | Medium-Low | High | Incremental | Beraha numbers approaching 4; Sokal density |
| 2 | Flow-Theoretic | Medium-Low | High | Tied to open conjectures | Equivalent to 4CT; integrality gap |
| 3 | Topological | Low-Medium | Medium-High | Partial results on Kempe chains | Separator size; extension NP-hard |
| 4 | Fewer Configurations | **High** | Medium | **Immediate** | Possible lower bound on $N$ |
| 5 | Proof Mining | Medium | Medium-High | Engineering-dependent | Computational vs. logical content |
| 6 | Spectral (Colin de Verdière) | Low-Medium | Very High | Incremental | $\chi \leq \mu + 1$ conjecture open |
| 7 | Probabilistic | Low | High | Kempe dynamics accessible | $k = 4$ too small for LLL |
| 8 | Matroid / Critical Group | Low | Very High | Exploratory | Indirect connection to $\chi$ |
| 9 | Hadwiger Conjecture | Low-Medium | Very High | Structural | May be inherently as hard as 4CT |
| 10 | Representation Theory | Low | Very High | Exploratory | $X_G$ too rich to control |
| 11 | Game-Theoretic (Kempe Swap) | Medium | Medium-High | Computational verification | Complexity of reconfiguration graph |

---

## 9. Recommended Research Programme

Based on this analysis, I recommend a **two-track programme** with clear priorities:

### Track A: Near-Term (High-Feasibility)

**Primary: Strategy 4 (Refined Discharging)** — the most immediately actionable path. Build a modern computational framework for searching over discharging rule sets, targeting a reduction from 633 to $\leq 50$ configurations. Complement with Strategy 5 (Proof Mining) to identify redundancies in the existing 633 configurations.

**Secondary: Strategy 11 (Kempe Swap Game)** — computationally verify the Kempe reducibility conjecture for small planar graphs and develop structural lemmas about colour elimination.

### Track B: Long-Term (High-Elegance)

**Primary: Strategy 9 (Hadwiger for $k=5$ without 4CT)** — study the Robertson-Seymour-Thomas proof in detail and identify whether 4CT can be replaced with weaker structural results.

**Secondary: Strategy 6 (Colin de Verdière)** — investigate $\chi \leq \mu + 1$ for planar graphs and related spectral approaches.

**Exploratory: Strategy 3 (Topological)** — develop the theory of Kempe chain non-crossing in planar graphs. This is the strategy most likely to yield fundamentally new insights about *why* four colours suffice.

### Cross-Cutting Theme

Across all strategies, the interaction between **Kempe chains and planarity** emerges as the central mathematical question. The Jordan Curve Theorem constrains Kempe chain geometry; the discharging method identifies where Kempe chains are needed; the game-theoretic formulation asks whether Kempe swaps can always succeed; and the spectral/algebraic approaches encode Kempe chain properties in algebraic invariants. A deep understanding of Kempe chains in planar graphs is the foundation on which all strategies ultimately rest.

---

*Agent 1221 — Graph Colouring Project*  
*17 February 2026*
