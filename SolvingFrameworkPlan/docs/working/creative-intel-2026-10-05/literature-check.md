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
