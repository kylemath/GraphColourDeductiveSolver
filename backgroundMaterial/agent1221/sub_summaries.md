# Background Material Summaries

**Agent:** 1221  
**Date:** 17 February 2026  
**Project:** Graph Colouring — Four Colour Theorem

---

## Document 1: agent1007ProblemSet.md

**Source:** `backgroundMaterial/agent1007ProblemSet.md` (1,188 lines)  
**Type:** Comprehensive study document — theory, history, and code

Agent 1007's problem set is a self-contained treatment of the Four Colour Theorem spanning formal foundations through computational implementation.

**Formal foundation.** The theorem is stated as $\chi(G) \leq 4$ for every planar graph $G$. The document defines the core vocabulary — planar graph, chromatic number, proper colouring, $k$-colourability — and establishes the dual graph construction that translates map colouring into vertex colouring. Planarity is characterised via the Kuratowski-Wagner Theorem (no $K_5$ or $K_{3,3}$ minor), with Python/NetworkX code for the Boyer-Myrvold linear-time planarity test.

**Structural results.** Three key bounds are developed: (1) Euler's Formula $V - E + F = 2$ and its corollary $E \leq 3V - 6$, which forces the existence of a vertex of degree $\leq 5$ in every planar graph; (2) the Five Colour Theorem (Heawood, 1890), proved by induction with a single Kempe chain swap at degree 5; and (3) the Heawood Conjecture for surfaces of genus $g > 0$, giving the chromatic bound $H(g) = \lfloor(7 + \sqrt{1 + 48g})/2\rfloor$.

**Historical arc.** A timeline covers Guthrie's 1852 conjecture, Kempe's flawed 1879 proof, Heawood's 1890 correction, Birkhoff's 1913 reducibility concept, Franklin's 1922 partial result ($\leq 25$ regions), Heesch's 1969 discharging method, the 1976 Appel-Haken computer-assisted proof, the 1997 RSST simplification, and Gonthier's 2005 Coq formalisation.

**Proof mechanics.** The Appel-Haken proof structure is presented in detail: (a) assume a minimal counterexample; (b) assign charges $6 - \deg(v)$ and apply discharging rules to show an unavoidable set of 1,476 configurations must appear; (c) verify each configuration's reducibility by checking that all 4-colourings of the boundary ring extend inward. The RSST simplification reduced this to 633 configurations, 32 discharging rules, and ~3 hours of computation. Gonthier's Coq proof is described as making the result a machine-verifiable certificate.

**Implementations.** Working Python code is provided for: Welsh-Powell greedy colouring, DSATUR (saturation-degree heuristic), Kempe chain identification and swapping, initial charge assignment and discharging, unavoidable-set checking, reducibility testing, graph visualisation, and a complete US state map demo (49 states + DC, 4-coloured by DSATUR).

---

## Document 2: agent1012Report.md

**Source:** `backgroundMaterial/agent1012/agent1012Report.md` (376 lines)  
**Type:** Analytical report — summary, demo description, and two future research directions

Agent 1012's report has four substantive parts.

**Part 1 — Summary of Agent 1007's work (§1.1–1.8).** A section-by-section digest of the problem set, accurately condensing the theorem statement, dual graph construction, Euler bounds, Five Colour Theorem, Heawood Conjecture, historical timeline, Appel-Haken/RSST proof mechanics, and Python implementations. The assessment identifies two gaps: (a) the philosophical distance between a computer-checked proof and a traditional deductive proof, and (b) the practical limitations of DSATUR for guaranteeing 4-colourings.

**Part 2 — Interactive web demo (§2).** Documents a zero-dependency, single-page web application (2,688 lines across 5 files) with 8 tabbed sections providing progressive, interactive coverage of the theorem. Design principles include progressive disclosure, active learning through interactive demos at every conceptual stage, and accessibility via ARIA roles and keyboard navigation.

**Part 3 — Future Direction A: towards a first-principles deductive proof (§3).** Identifies the core obstacle — the degree-5 case where Kempe chain swaps can interfere — and proposes five approaches to eliminating the computer-dependent step:

1. **Algebraic (Chromatic Polynomial):** Prove $P(G, 4) > 0$ for all planar $G$ by showing all real roots of the chromatic polynomial lie in $(-\infty, 0] \cup [1, 2] \cup [3, 4)$. Builds on Birkhoff-Lewis and recent root-distribution results.
2. **Flow-Theoretic (Tutte's Conjectures):** Prove the nowhere-zero 4-flow conjecture for bridgeless planar graphs, which is dual-equivalent to 4-colourability. Translates to modular linear equations.
3. **Topological (Jordan Curve / Separators):** Exploit the planar separator theorem ($O(\sqrt{n})$ tree-width) for divide-and-conquer; prove any 4-colouring of a separator boundary extends to the interior.
4. **Refined Discharging:** Develop more sophisticated discharging rules to shrink the unavoidable set to 10–20 configurations checkable by hand. The most immediately actionable approach.
5. **Proof-Theoretic (Mining the Coq proof):** Apply proof mining or LLMs to Gonthier's formalisation to extract parameterised lemmas that collapse hundreds of cases into a small family of templates.

A feasibility table ranks "fewer configurations" as the most near-term actionable, and the algebraic/flow-theoretic approaches as highest in potential elegance.

**Part 4 — Future Direction B: SPARK algorithm (§4).** Proposes SPARK (Saturation-Planarity-Aware Recolouring with Kempe chains), a three-phase algorithm designed to guarantee 4-colourings for planar graphs while maintaining $O(n \log n)$ expected time:

- **Phase 1 (Ordering):** Planarity-aware elimination ordering that scores vertices by saturation potential, separator score, and low-degree creation upon removal.
- **Phase 2 (Colouring):** Saturation-guided greedy colouring with 1-step lookahead that minimises downstream bottlenecks (vertices left with no free colour).
- **Phase 3 (Repair):** Kempe chain repair when no colour from $\{0,1,2,3\}$ is available — single swaps, double swaps, and backtracking fallback.

SPARK's key advantage over DSATUR is the Kempe repair phase: rather than accepting a 5th colour, it restructures existing colour assignments. Expected complexity is $O(n \log n)$ vs. DSATUR's $O(n^2)$, with worst-case $O(n^2)$ from backtracking cascades. The algorithm generalises to non-planar graphs by replacing planarity-specific scoring with degeneracy-based ordering.

---

## Document 3: index.html

**Source:** `backgroundMaterial/agent1012/index.html` (711 lines)  
**Type:** Interactive single-page web application

The HTML file is the structural backbone of the interactive demo described in Agent 1012's report. It is a semantic, accessibility-annotated document with 8 tabbed sections (`role="tabpanel"`, ARIA attributes on the tab bar), supported by three JavaScript files (`graph.js`, `animations.js`, `app.js`) and one stylesheet (`styles.css`), with zero external dependencies.

**Tab 1 (The Problem):** Formal statement of $\chi(G) \leq 4$ with key definitions in a table. Interactive canvas map with 8 regions, 4 colour-picker buttons, reset, and an auto-colour button running DSATUR.

**Tab 2 (Maps & Graphs):** Dual graph transformation with side-by-side map and graph canvases, step/reset/auto-play controls. Three static mini-figure canvases for $K_5$ (not planar), $K_{3,3}$ (not planar), and $K_4$ (planar, 4-coloured).

**Tab 3 (Euler & Bounds):** Dropdown selector for five Platonic solids (tetrahedron through icosahedron), each rendered on a canvas with live computation of $V$, $E$, $F$, Euler's formula, the edge bound, minimum degree, and colours used. Includes the Five Colour Theorem proof steps and the Heawood number table for genus 0–3.

**Tab 4 (Historical Journey):** Vertical timeline with 9 entries from 1852 (Guthrie) to 2005 (Gonthier), with the 1976 Appel-Haken entry visually highlighted. Narrative descriptions at each milestone.

**Tab 5 (Kempe Chains):** Interactive canvas (dodecahedron), two colour-selector dropdowns, highlight/swap/reset buttons. Explanatory text on why Kempe's double-swap argument fails and why the Five Colour Theorem needs only one swap.

**Tab 6 (The Proof):** Three-pillar layout (discharging, unavoidable sets, reducibility) with the charge formula $6 - \deg(v)$. Interactive discharging visualisation canvas with assign/discharge/reset controls. Comparison table of Appel-Haken vs. RSST parameters.

**Tab 7 (Modern Advances):** Animated horizontal comparison bars for configurations (1,476 vs. 633), discharging rules (487 vs. 32), and computer hours (1,200 vs. 3). Gonthier verification grid. Four practical application cards (map colouring, register allocation, frequency assignment, scheduling).

**Tab 8 (Try It Yourself):** Playground with 6 selectable graph types (Petersen, $C_6$, $K_4$, dodecahedron, 4×4 grid, US western states). Manual vertex colouring with 4-colour picker. DSATUR solve and step-through buttons with a real-time algorithm log showing saturation values and colour assignments. Summary table of key concepts.

---

## Assessment

The three documents together establish a strong and layered knowledge base for the Four Colour Theorem project.

**Theoretical coverage.** The core mathematics is thoroughly addressed. The formal statement, graph-theoretic translation, Euler bounds, Five Colour Theorem, Heawood Conjecture, Kempe chains, discharging, unavoidable sets, and reducibility are all present with correct definitions and complete explanations. The historical narrative is accurate and well-sourced across the key milestones from 1852 to 2005.

**Computational grounding.** Agent 1007's Python implementations provide executable demonstrations of every major concept. These are pedagogically sound and serve as a testbed for future algorithmic work. The interactive web demo (Document 3) translates these ideas into a visual, browser-based experience that reinforces understanding through active exploration.

**Research directions.** Agent 1012's report identifies the two most important open fronts — a human-readable deductive proof and improved colouring algorithms — and proposes concrete programmes for each. The five approaches toward a deductive proof are well-chosen and accurately assessed for feasibility. The SPARK algorithm is a detailed, original proposal with clear pseudocode, complexity analysis, and a principled comparison to DSATUR.

**Gaps and opportunities.** Three areas remain undeveloped:

1. **Empirical validation.** SPARK exists only as a design; no implementation or benchmark data are provided. Building and testing SPARK against DSATUR on standard planar graph families is the most immediate next step.
2. **Edge-case analysis for SPARK.** The worst-case $O(n^2)$ backtracking scenario needs characterisation — under what graph structures does Phase 3 cascade, and can the ordering in Phase 1 be tuned to prevent it?
3. **Deeper engagement with the Coq proof.** The proof-mining approach (Direction A, Approach 5) is described at a high level but lacks specifics on which parts of the Gonthier formalisation are most amenable to compression or structural extraction.

**Overall verdict.** The knowledge base is well-suited to support both pedagogical and research objectives. The theoretical foundations and historical context are comprehensive. The algorithmic frontier (SPARK) and the proof-theoretic frontier (deductive proof approaches) are clearly articulated and ready for implementation and investigation, respectively.

---

*Agent 1221 — Graph Colouring Project*  
*17 February 2026*
