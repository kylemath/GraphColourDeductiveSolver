# Literature, deep pass: R*_v and close variants

Long Table literature sub-agent, 6 October 2026. This is web research only; no Studio compute was used. Target: **(R\*_v)** for v a degree-5 vertex of a plane triangulation T, every Kempe class of 4-colourings of T − v contains a colouring whose link uses at most 3 colours.

Verification tags: **[full]** I read the full text myself; **[abs]** I read only the abstract or the publisher page; **[2nd]** cited second-hand, with the citing source named.

## Headline: R*_v is in the literature, as Tilley's "D-resolvability" conjecture (correction to the 15:04 report)

**J. A. Tilley, "D-resolvability of vertices in planar graphs", J. Graph Algorithms Appl. 21(4) (2017) 649–661, DOI 10.7155/jgaa.00433 [full; open-access PDF from jgaa.info].**
- **Setting.** Tilley deletes a vertex v and looks at the "state transformation graph" H_{G_v} of 4-colourings of G − v. A state is a colouring up to permutation of colours. An edge of H_{G_v} is one Kempe exchange, meaning a swap on a non-empty proper subset of the j–k chains. This gives the same equivalence classes as single-chain swaps.
- **Terms.**
  - An *initial state* is one where the ring R uses all 4 colours.
  - A *solution state* is one where R uses 2 or 3 colours.
  - A state is *difficult* if its component of H_{G_v} contains no solution state.
- **Definition.** v is *D-resolvable* if every 4-colouring of G − v can be turned into a 4-colouring of G by Kempe exchanges alone. **For deg v = 5 this is exactly R\*_v.**
- **Conjecture.** "Every vertex in a planar graph is D-resolvable." Tilley states that this is stronger than the 4CT, and that the 4CT does not imply it. This matches our own hardness note.
- **Evidence.**
  - *Complete* state transformation graphs: for the Errera, Fritsch, Heawood, Kittell, de la Vallée-Poussin and Soifer graphs, every vertex was deleted in turn and all classes enumerated. No difficult states were found. Solution-state counts: Errera 40, Kittell 212, Heawood 256.
  - *Algorithmic* runs: over 200,000 trials on random internally 6-connected triangulations of order up to 125, with no failure. **Caveat:** these runs start from greedy colourings, and resolve a vertex from the class of that start only. They do **not** check every Kempe class, so they are weaker evidence for R\* than the complete runs.
- **Icosahedron.** Tilley notes that every one of its 10 colourings is akempic (Kempe-frozen), yet every vertex is D-resolvable, "easily shown". This is an assertion; no proof is printed.
- **To flag.** One sentence of the paper says a degree-5 vertex "turns out to be D-resolvable" without being D-reducible. No proof is given. Read it as the conjecture plus the computational evidence, **not** as a theorem.

So the 15:04 statement "no source states R\*" is **wrong**. R\* for degree-5 vertices of all triangulations is Tilley's open 2017 conjecture. Audit should re-check this.

## (a) Mohar 1985

**B. Mohar, "Akempic triangulations with 4 odd vertices", Discrete Math. 54(1) (1985) 23–29, DOI 10.1016/0012-365X(85)90059-7.** [abs: from the ScienceDirect snippet and the definition as quoted in search results; ScienceDirect blocked a direct fetch. Full text not read.]
- **Definitions.**
  - An *akempic* triangulation has a 4-colouring in which any two adjacent triangles together use all four colours.
  - That colouring is Kempe equivalent to no other colouring.
- **Result.** Voltage graphs characterise the duals of akempic triangulations that are n-fold covers of K₄, and n must be odd.
- **What the special colouring is** [inference, not read]. "Adjacent triangles use all 4 colours" makes the colouring a branched covering of the tetrahedron. Around each vertex, the link is coloured with period 3, so **every degree is divisible by 3**. The colouring is frozen: every bichromatic subgraph is connected, so a Kempe change only renames colours.
- **Bearing on R\*.**
  - These triangulations have **no degree-5 vertex**, so R\*_v is vacuous on them.
  - The period-3 local structure cannot occur around a degree-5 link.
  - Our counting remark (T − v has 3n′−8 edges, while freezing needs 3n′−6) rules out frozen colourings of T − v altogether.
  - **The construction cannot produce a filled-free Kempe class of T − v as it stands.** The idea it suggests is a *small* class, made of nearly frozen colourings, that is entirely unfilled.

## (b) Kempe invariants: Tutte, Fisk, Mohar–Salas

- **B. Mohar and J. Salas, "A new Kempe invariant and the (non)-ergodicity of the Wang–Swendsen–Kotecký algorithm", J. Phys. A 42 (2009) 225204, arXiv:0901.1010** [full-text extraction via ar5iv].
  - Degree: deg f = p − n, computed for the simplicial map f : T → ∂Δ³.
  - **Lemma 3.1 (Tutte):** deg f ≡ Σ_{f(x)=a} ρ(x) (mod 2) for each colour a.
  - **Cor. 3.3:** the parity is a Kempe invariant.
  - **Thm 3.4:** for 3-colourable triangulations of closed orientable surfaces, deg mod 12 is a Kempe invariant.
  - **Thm 2.8 (Fisk):** on the sphere, projective plane and torus, a 3-colourable triangulation has all colourings with 12 | deg Kempe equivalent.
  - **No boundary, disc or punctured version** appears in this paper.
- **S. Fisk, "Geometric coloring theory", Adv. Math. 24(3) (1977) 298–340** [2nd: Mohar–Salas, Florek, Feghali]. Kempe regions and Kempe cycles; all 4-colourings of an Eulerian sphere triangulation form one class (Fisk 1973).
- **A disc version, to test [hand, unreviewed].** In T − v, let S_c = Σ_{f(x)=c} deg(x). A swap on an (a,b) chain leaves S_c and S_d unchanged; only S_a and S_b move. In the closed case, Tutte's identity forces all four S_c to be congruent mod 2, which gives the invariant. In the disc, counting triangles gives S_a = t_abc + t_abd + t_acd + β_a/2, where β_a is the number of boundary edges at colour-a vertices. So any parity invariant must carry boundary terms that depend on the link word. I found nothing on this in the literature.

## (c) Kempe classes of near-triangulations, and recent Kempe-recolouring work

- **J. A. Tilley, "The a-graph coloring problem", Discrete Appl. Math. 217(2) (2017) 304–317, arXiv:1511.06872** [full text read via PDF extraction].
  - This is the **edge analogue of R\***: near-triangulations T − xy with one 4-face. Classes are labelled n (no state with c(x) ≠ c(y)), s, or n-s.
  - **Thm 5.1:** a minimal a-graph counterexample has no n-s class.
  - **Found:** an n class at order 12, whose parent contains the Birkhoff diamond, plus higher members with strings of diamonds. **So the edge analogue of R\* is false.** No member has an internally 6-connected parent.
- **J. A. Tilley, "Kempe-locking configurations", Mathematics 6(12) (2018) 309; arXiv:1809.02807** [earlier full-text extraction; see `literature-check.md`]. Kempe-locked at xy is the same as T − xy having only n classes. Every Kempe-locked example found contains a Birkhoff diamond, and none was found among 5-connected triangulations up to order 24.
- **J. A. Tilley, "Using Kempe exchanges to disentangle Kempe chains", Math. Intelligencer 40 (2018) 50–54** [2nd: search snippet; not read].
- **C. Feghali, "Kempe equivalence of 4-critical planar graphs", J. Graph Theory 103 (2023) 139–147, arXiv:2101.04065** [abs and HTML extraction]. A 4-critical planar graph has a single Kempe class; the proof does not use the 4CT. It relies on Mohar's near-triangulation extension lemma: two colourings of G extend, up to equivalence, to G ∪ T, where T is a near-triangulation with outer cycle C. That lemma is the closest tool to T − v that I found. 4-criticality fails for T − v.
- **J. Florek, "Kempe equivalence of 4-colourings of some plane triangulations", arXiv:2511.00485 (Nov 2025)** [full text: TeX source grepped; theorem statements read].
  - **Family.** G_n has two poles of degree n and 2n degree-5 vertices. It is our belt family, and the minimal essentially 6-connected triangulations.
  - **Thm 1.1:** non-constant colourings are equivalent if and only if the invariant d(A) agrees. d(A) is the number of "type-1" edges in A(1,2); equivalently a(A), b(A) or c(A), which are counts of colour classes and edges.
  - **Thm 1.2:** K\*(G_n) = ⌊n/6⌋+1, or ⌊n/6⌋ when n ≡ 1 (mod 6).
  - **Frozen colourings.** For n ≡ 2 (mod 3) there are 2n *constant*, i.e. frozen, colourings.
  - **Thm 2.1:** G_n − pole has one class, within 6⌊n/2⌋ to 9⌊n/2⌋+6⌊n/3⌋−2 changes.
  - **Not treated:** G_n − v for v of degree 5.
- **Other Kempe-change papers, with no 4-colouring-of-T−v content:**
  - Bonamy, Bousquet, Feghali, Johnson, J. Combin. Theory B 135 (2019) 179–199 [2nd: Florek].
  - Bonamy, Delecroix, Legrand-Duchesne, "Kempe changes in degenerate graphs", European J. Combin. 119 (2024) 103802, arXiv:2112.02313 [abs]. Treewidth ≤ k−1 gives O(kn²) changes.
  - Bonamy, Heinrich, Ito, Kobayashi, Mizuta, Mühlenthaler, Suzuki, Wasa, STACS 2020, LIPIcs 154:35 [abs]. Shortest Kempe reconfiguration.
  - Bonamy, Heinrich, Legrand-Duchesne, Narboni, arXiv:2103.10684 [abs]. Frozen colourings without K_t minors; disproves Las Vergnas–Meyniel.
  - Deschamps, Feghali, Kardoš, Legrand-Duchesne, Pierron, SIAM J. Discrete Math. 37(2) (2023) 604–611 [2nd: Florek]. 5-colourings of planar graphs are connected within poly(n) changes.
  - Cranston, Feghali, Discrete Appl. Math. 357 (2024) 94–98 [abs].
  - Ito et al., arXiv:2210.17105 [abs]. Single-vertex recolouring on 3-colourable sphere triangulations.
  - None treats degree-5 Kempe resolution.

## (d) The Heawood-failure literature

- **E. Gethner and W. M. Springer II, "How false is Kempe's proof of the four color theorem?", Congr. Numer. 164 (2003) 159–175** [2nd: Part II and MathWorld]. Implements Kempe's algorithm and measures how often it fails on the Heawood, Errera, Fritsch, Soifer and Poussin graphs over vertex orderings.
- **E. Gethner, B. Kallichanda, A. S. Mentis et al., "How false is Kempe's proof of the Four Color Theorem? Part II", Involve 2(3) (2009) 249–265, DOI 10.2140/involve.2009.2.249** [full text; MSP open PDF].
  - **What it proves.** One theorem: Thm 4, "Gadget 52 is order-dependent". At the Heawood double-swap step, the order of the two swaps can decide success; shown on the Fritsch graph.
  - **Empirical part.** Failure rates. With Kittell's switches added, the randomised recursive method always succeeded (500 runs per graph; at most 73 Kittell switches, on Errera).
  - **Stated as open:** "it is unknown if there is always a series of Kempe–Kittell chain switches" that resolves the impasse. This is R\*_v, phrased algorithmically.
- **I. Kittell, "A group of operations on a partially colored map", Bull. AMS 41(6) (1935) 407–413** [2nd: Gethner et al.; the AMS PDF is not reachable from here]. Defines the "impasse group" of operations on a map with one uncoloured pentagonal region; per Gethner et al. it has at least 120 elements. This is the earliest study of exactly R\*_v's setting.
- **Background** [2nd]:
  - Hutchinson and Wagon, "Kempe revisited", Amer. Math. Monthly 105(2) (1998) 170–174: randomised Kempe recolouring.
  - Morgenstern and Shapiro, Algorithmica 6 (1991) 869–891: heuristics.
  - Both are empirical; neither proves anything about R\*.

## (e) Tilley after 2018

- Research Outreach profile (16 May 2019) [read]. Repeats the Kempe-locking work and mentions "a wholly different approach" in progress.
- arXiv:1809.02807 was revised in March 2019.
- I found no Tilley paper after 2019. Not exhaustive: ResearchGate blocked access.

## Implications for R*

1. **Status.** R\*_v (for all degree-5 v) is Tilley's open D-resolvability conjecture (JGAA 2017), and Gethner et al. (2009) leave the same question open. It is not proved, not refuted, and is known to be stronger than the 4CT. **Novelty claims for R\* must cite Tilley 2017.** Our contribution would be the core-class reduction and any structural proof.
2. **What would refute it.** A degree-5 v and a Kempe class of T − v consisting only of initial (4-colour-link) states, which Tilley calls "difficult". The edge analogue really does fail (Tilley's family A; Kempe-locked triangulations). So failure is not absurd, and it would sit near **Birkhoff diamonds**, which contain four degree-5 vertices.
3. **What supports it.**
   - Complete class enumeration on six historical graphs, at every vertex.
   - Single-class runs on many internally 6-connected triangulations up to order 125.
   - Gethner/Kittell randomised success.
   - No frozen colouring of T − v exists (our counting).
   - Feghali's and Florek's one-class results for near-relatives: 4-critical graphs, and G_n − pole.
4. **Constructions worth a Studio test** (each needs a declared WP; small, exhaustive per instance):
   - (i) Tilley's order-12 family-A parent, and his three 4-connected Kempe-locked triangulations: run R\*_v at every degree-5 vertex, especially the diamond's own degree-5 vertices.
   - (ii) Florek's G_n for n ≡ 2 (mod 3), say n = 5, 8, 11, which has frozen colourings: run R\*_v at a degree-5 vertex. Check whether Florek's invariant d(A), adapted to G_n − v, separates a class with no filled state.
   - (iii) The disc parity candidate in (b): compute Σ_{f(x)=c} deg(x) mod 2 with boundary corrections on all states of T4, A_3 and the Six-Ring Trap, and see whether any combination is constant on classes. This is a kill test; it can only refute.
   - (iv) Strings of Birkhoff diamonds, Tilley's higher family-A members, as an adversarial series.
