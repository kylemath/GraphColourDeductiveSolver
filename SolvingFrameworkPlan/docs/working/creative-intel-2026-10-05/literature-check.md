# Literature check for the core brainstorm

Long Table (Creative Intel), 5 October 2026, 17:52 MDT. **[cited]** items below come from abstracts and search summaries. Full papers have not been read. Check the details before any page relies on them.

## 1. Inoue, Kawarabayashi, Miyashita, Mohar, Thomassen, Thorup (2026)

"The Four Color Theorem with Linearly Many Reducible Configurations and Near-Linear Time Coloring", arXiv:2603.24880. Submitted 25 March 2026, revised 1 October 2026. The user remembered a paper of this kind from 2022; this is the matching paper found.

**What it claims (abstract).**
- Every planar triangulation contains linearly many pairwise non-touching **D-reducible** configurations, or pairwise non-crossing **obstructing cycles of length at most 5**.
- This gives a near-linear-time 4-colouring algorithm, improving the quadratic algorithm of Robertson, Sanders, Seymour and Thomas (1996).
- The method is discharging by combinatorial curvature. Reductions are also found in flat (curvature-zero) regions.

**Relevance to us.**
- Their obstructing cycles of length $\le5$ are the same cut sizes as our trace-game reductions: 3-cycles accepted, 4-cycles corrected by Math, 5-cycles pending. Their definition of "obstructing" should be read; it may say which 5-cycles allow reductions, which bears on our wheel exclusion.
- Their result is census-based: many D-reducible configurations. It is the opposite of our structural aim, but it shows that easy local spots are abundant, even in flat regions. VH∃ needs only one good spot, but reducibility is not VH-goodness.
- **Possible bridge.** D-reducibility means every boundary colouring extends after Kempe changes on the ring. If D-reducible configurations imply VH-good pairs inside them, that would turn their unavoidability into VH∃. But that is a census-based proof, which the goal statement excludes. Record it only as a fallback.

## 2. Tilley, "Kempe-locking configurations" (Mathematics 6(12):309, 2018; arXiv:1809.02807, "The Birkhoff diamond as double agent")

**What it says (abstract).**
- **Definition.** A triangulation is Kempe-locked with respect to an edge $xy$ when, for every 4-colouring of $T-xy$ with $x$ and $y$ the same colour, no sequence of Kempe interchanges makes their colours differ.
- **Claim.** A minimum counterexample must have the Kempe-locking property. Tilley defines Kempe-locking configurations, and fundamental ones.
- **Conjecture**, supported by an extensive search: the Birkhoff diamond is the only fundamental Kempe-locking configuration. Every rare Kempe-locked triangulation found contained one.

**Relevance to us.**
- **Idea E.** Our fill condition at $(v,\tau)$ in $T^\ast$ terms (Corollary 3.3) is that both chord-edge diamonds have equal tips. Tilley's locking concerns the reverse of this, separating the colours of the two ends of an edge, but in the same Kempe-class language. A precise translation is open.
- **Fixtures for risk control (idea F).** Kempe-locked triangulations, and Birkhoff diamonds, are natural adversarial fixtures for VH∃ and VH_𝒞. They need a declared WP.

## 3. Mohar and Salas (2009); Fisk

Mohar and Salas, "A new Kempe invariant and the (non)-ergodicity of the Wang–Swendsen–Kotecký algorithm", J. Phys. A, 2009 (arXiv:0901.1010).

**What it says.**
- For **three-colourable** triangulations of closed orientable surfaces, the degree of a 4-colouring mod $12$ is a Kempe invariant.
- Fisk: on the sphere, projective plane or torus, if the triangulation is three-colourable, all 4-colourings with degree divisible by $12$ are Kempe-equivalent.

**Correction to brainstorm idea B.** Three-colourable means Eulerian, so every degree is even. Minimum-degree-5 triangulations have degree-5 vertices, so this invariance **does not apply** as stated. The local degree vector with a hole is still well defined. Whether any global part is invariant under our moves is open, and less likely than the brainstorm suggested.

## Sources

- https://arxiv.org/abs/2603.24880
- https://arxiv.org/abs/1809.02807 ; https://www.mdpi.com/2227-7390/6/12/309
- https://arxiv.org/abs/0901.1010
- Steinberger, an unavoidable set of D-reducible configurations: https://arxiv.org/abs/0905.0043 (background)

---

# Full-text reading (17:57)

**Method.** Neither PDF could be rendered locally: no poppler, and no Python PDF library. Both papers were read through their arXiv HTML versions with targeted extraction (WebFetch). Definitions and theorem statements below are close quotations from that extraction. Proof details were not read line by line. Treat them as **[cited, to verify]**.

## Inoue, Kawarabayashi, Miyashita, Mohar, Thomassen, Thorup, arXiv:2603.24880v3

- **Obstructing cycle:** "a cycle of length at most 4 with at least one vertex on each side, or of length 5, with at least 2 vertices on each side." A triangulation is **internally 6-connected** if it has no obstructing cycle.
  - **This is exactly our reduction set.** Separating 3- and 4-cycles have one or more vertices per side, and 5-cycles need at least two per side, which is our wheel exclusion. If the trace-game reductions (§2 accepted by Math after correction; §2b pending) are accepted, **a least VH^tr failure is internally 6-connected in their sense.**
- **Theorem 1.1:** planar graphs are 4-colourable in $O(n\log n)$ time.
- **Theorem 3.3 / Corollary 3.4:** in linear time one finds linearly many non-touching separating 3- or 4-cycles, or obstructing cycles, or induced reducible configurations from $\mathcal D$.
- **Discharging.**
  - Initial charge $10(6-d(v))$, total $120$, with Steinberger's $84$ rules.
  - **Theorem 5.1:** if $G$ is internally 6-connected and $B_{12}(v)$ is flat (all final charges zero), then $B_{14}(v)$ contains an induced configuration from $\mathcal D$.
  - $\mathcal D$ has $8202$ D-reducible configurations, each of diameter $\le4$ and ring size $\le18$.
  - D-reducibility is checked by computer, by iterating "improving" Kempe changes on ring colourings.
- **Kempe chains in the algorithm.** $O(\log n)$ Kempe changes per constant-factor reduction, with randomised or derandomised choice. Obstructing cycles are handled by the techniques of Robertson–Sanders–Seymour–Thomas, organised as a component hierarchy (their §13).
- **Birkhoff diamond:** the four-degree-5-vertex diamond is D-reducible. Low-degree lemma: a vertex of degree $3$ is $0$-extendible, and a vertex of degree $4$ is $1$-extendible.
- Code: https://github.com/near-linear-4ct (configurations and discharging rules in separate repositories).

**What it means for us.**
- (a) Our structural reductions land exactly where their discharging starts, so the two programmes share a core.
- (b) Their core argument is a census of $8202$ configurations. That is the route our goal excludes, unless VH-goodness of a few configurations can replace D-reducibility.
- (c) "Improving Kempe change" is the same move vocabulary as ours: ring colourings at the boundary of a configuration, Kempe changes outside it.

## Tilley, "The Birkhoff Diamond as Double Agent" (arXiv:1809.02807; published as "Kempe-Locking Configurations", Mathematics 2018)

- **Kempe-locked w.r.t. $xy$:** in every 4-colouring of $G_{xy}=T-xy$ with $c(x)=c(y)$, there are precisely three Kempe chains containing both $x$ and $y$. So no interchange ever separates their colours, and since every step keeps $c(x)=c(y)$, no sequence does either.
- **Kempe-locking configuration** $K_{xy}$: delete $u,v$ from $G_{xy}$, where the boundary is the 4-cycle $uxvy$. It is **fundamental** when no proper subgraph is a Kempe-locking configuration of another triangulation.
- **Proved:** a minimum counterexample is Kempe-locked with respect to **every** edge. The argument is contraction: colour $T/xy$, uncontract, and separate $x$ and $y$ by Kempe changes.
- **Conjecture:** a Birkhoff diamond with endpoints $x,y$ is necessary, but not sufficient, for Kempe-locking at $xy$. If true, it conflicts with the diamond's reducibility; this is the "double agent".
- **Search scope:** all 4-connected triangulations of orders $6$–$17$; random samples of $10^5$ at orders $18$–$20$; all $9733$ 5-connected triangulations of orders $12$–$24$. **No 5-connected Kempe-locked triangulation was found.** Every locked example contained a Birkhoff diamond.
- Per the extraction, the endpoints of a Kempe-locked edge have degree $\ge6$. I have not verified whether this is proved or observed.

## A bridge we had not noticed [hand]

**$T^\ast_{\tau_y}=T/xy$.** At a degree-5 vertex $x$ with fan apex $y$, the chords join $y$ to the two far neighbours of $x$. That is exactly the contraction of $xy$, because the near neighbours of $x$ are already adjacent to $y$. Legality of the fan is simplicity of the contraction, that is, no separating triangle through $xy$. So **VH$(x,\tau_y)$ quantifies over the colourings of $T/xy$**, which are Tilley's colourings of $G_{xy}$ with $c(x)=c(y)$, once $x$ is uncoloured.

**[hand] One direction.**
- Take a start $c$ and put $c(x)=c(y)$; this is proper on $G_{xy}$ by the apex-singleton lemma.
- A Tilley Kempe sequence on $G_{xy}$ that separates $x$ from $y$ becomes a sequence of pure swaps at the hole $x$. A change whose component avoids $x$ is the same swap. A change through $x$ splits, after deleting $x$, into components of $(T-x)[a,b]$, which are swapped one after another, as in containment Lemma 3.1.
- At the end, $c(x)\neq c(y)$ and $x$ is properly coloured in $T$, so the link of $x$ misses $c(x)$, which is a fill.
- **So if $T$ is not Kempe-locked at $xy$ for a given start, that start has a pure fill at $x$.**

The converse fails: our moves are richer, with slides and holes moving away from $x$.

**Consequences.**
- VH∃ is a **strictly more flexible** version of "some edge at a degree-5 vertex is not Kempe-locked for every colouring".
- Tilley's data (no 5-connected locked triangulations to order $24$) and his Birkhoff-diamond conjecture are evidence about **pure** goodness of apex fans. They apply directly to our core, which is internally 6-connected and hence 5-connected away from neighbourhoods.
- **A candidate route.** Prove "a degree-5 vertex $x$ and a neighbour $y$ with no Birkhoff diamond on $xy$ give a pure-good apex fan". Then handle the Birkhoff diamond, which is D-reducible, by a separate VH argument. This is still census-free: one configuration. Its plausibility rests on Tilley's conjecture, which is open.
