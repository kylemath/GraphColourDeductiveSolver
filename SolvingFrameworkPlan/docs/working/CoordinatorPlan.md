# Coordinator plan (from 7 October 2026)

The Studio session is the lone coordinator (Kyle, 7 Oct). This file is the plan of record. Each Navigator revision should say which tracks moved.

## Target

R\* in the frame class: every connected spherical triangulation with minimum degree 5, no separating triangle, and no `Occ` of the Birkhoff diamond or of RSST 2.122 (either orientation) has a pure-clean vertex of degree 5. `four_color_of_RStarFrame` (FrameF3.lean) already compiles R\* ⇒ 4CT.

Scope gap: the compiled statement is 4CT for combinatorial `SphericalMap`s (rotation systems). 4CT for topologically drawn planar graphs (e.g. OpenAI's `OAI.PlanarL1.IsPlanar`: injective points, simple arcs with disjoint interiors) would need a separate drawing ⇒ combinatorial-map bridge. Cost revised down (OpenAIMathScan.md, 7 Oct): OpenAI's Barnette formalisation (`lean/OAI/Combinatorics/Hamiltonian/`, Mathlib-only, agent-written, unaudited) has `PlaneEmbedding.exists_exact_dual` (drawing ⇒ algebraic dual + Euler, no Jordan curve theorem needed), and `alonamaloh/schoenflies-lean` gives Jordan–Schoenflies. Remaining: algebraic dual ⇒ rotation system (`SphericalMap`), plus porting (they use Lean v4.34.1; StudioMathLean uses v4.35.0-rc3). Off the critical path until R\* moves; a Comparator-style frozen challenge file for R\*/4CT is queued for Track C.

Honest baseline: forecast p = 0.02. Every result proved so far (F5, weak F6, `pureClean_of_hole4`) is about holes with three consecutive degree-5 link vertices. Those holes contain a diamond, so they never occur in the frame class.

## Tracks and kill rules

| Track | Goal | Success | Kill rule |
|---|---|---|---|
| A: break it | Adversarial search inside the frame class for failures of R\*, then the quarter floor, B′ and G66⁰ | A verified counterexample (publishable) or a documented null over a stated search budget | — (always worth running) |
| B: unavoidable hole types | Discharging census: which link-degree words must occur at degree-5 vertices of frame-class triangulations; then PureClean per type, adding reducible exclusions where needed | ≤ ~20 hole types, each with PureClean proved | > ~100 types, or a type with no local handle and no candidate exclusion |
| C: formal discipline | Every claim labelled formal / hand / data / killed; nightly full regression; independent review of hand proofs before the Navigator | — | — |
| D: bank a result | Short paper: Theorem W, F5, weak F6, D-resolvability framework, Lean reduction (partial result, honest scope) | Draft ready for Kyle | — |

Go/no-go review every two weeks (next: 21 Oct 2026) against these kill rules.

## Budget (coordinator's decision, 7 Oct)

- Agents: at most 6 running at once (workflow guideline < 10).
- Studio CPU (16 cores, 128 GB): coordinator-started compute runs under `nice -n 10` and uses at most 8 worker processes in total. Jobs BO/BP keep their current workers. The Studio is shared with Kyle's EEGLearn project (Python multiprocessing jobs); EEGLearn has priority, so 4CT compute stays nice'd and within the cap even when the machine looks idle.
- Update 7 Oct 16:20 (Kyle: EEG analysis nearly done): the cap is raised to 14 worker processes in total, still under `nice -n 10`. Drop back to 8 if EEGLearn jobs restart or the load average stays above ~20.
- Lean regression: one full `check.sh` run per day (about 10 minutes).

## Status log

**7 Oct, Track B verdict: amber, leaning kill** (TrackB/README.md). Proved unavoidable set: 59 hole types (78 without F2), using certified one-step discharging; the optimum for one-step rules is exactly 59. Rigorous lower bound 9; the empirical minimum is at least 13 and still rising. **66666 is forced into every S** (all IPR fullerene duals are frame-class, and their only hole type is 66666), and no hole type in the frame class has PureClean proved.
Consequence: **G66 is on the critical path.** R\* in the frame class implies PureClean at some 66666 hole of every IPR dual, which by `pureClean_of_no_allDL_orbit` is G66⁰ there. Fullerenes are a test bed where 3-edge-colourability is known independently (Kardoš: fullerenes are Hamiltonian). Next: a dedicated G66 track. Two-step discharging and the order 29–31 census are deferred.

**7 Oct, later.** Track A: no counterexample to R\* in the frame class (census orders 22–28, every degree-5 vertex PureClean, two engines; flip search to n = 37, 57,800 evaluations). The quarter floor is tight: 58 classes sit at exactly 1/4, all built from one 4-state zero-winding π-block (Conjecture E). Track C: `rStarFrame_of_no_allDL_orbit`, `no_555_run` / `no_565_run`, a frame-class witness, and frozen Comparator-style challenge files with anti-drift bridges, all compiled with standard axioms. Track F: no G66 failure at fullerene duals (C60–C100 exhaustive); multi-hole and orbit-level G66 routes are **killed**. New exact **lock-parity lemma**, and the candidate **LPC** (a class whose unfilled states all obey lock parity contains a filled state), which is 4CT-strength and combinatorial. Track E: the Barnette signed-sum route is **killed**. The only flipping phase is i^H (Heawood/Scheim), which is local to the ring word, and no phase can flip on both the lock involution and Kempe cubes.
Current frontier: falsify or prove LPC; formalise lock parity.

**7 Oct, evening.** Lock parity is **formal** (`QuarterLockParity.lean`; full regression 87/87, standard axioms). The census is now exhaustive to order 32 (Census29/: 21,931 frame-class graphs at orders 22–32 from 283M plantri graphs). R\* holds at every degree-5 vertex, the quarter floor is reached exactly and never broken, and lock parity has 0 failures on 8.4e8 states. There are 17 all-DL π-cycles, each inside a class that has filled states. Conjecture E is false as stated: equality classes have sizes 12/16/24 and some are not block repetitions; the surviving form is "union of w = 0 π-cycles with no τ state". The census-only minimum hitting set grows 6 → 9 by order 32 (new forced word 558+58+), consistent with Track B's amber verdict. Track F's LPC reformulation: no Kempe class consists entirely of all-DL π-cycles.

**7 Oct, night (end of day 1).**
- Positive π-cycles exist in the frame class from n = 37 (max w = 8 at n = 53), but only inside giant classes, and they are paid for by a few huge negative cycles. No class has Σw > 0 to n = 56 (TrackA task 3).
- Stream-function experiment (TrackG): no state-level potential exists, and the class-level potential is the floor itself. σ-escape holds on all 1,429 all-DL cycles, consistent with Job BL.
- **LPC at frame-like holes off the sphere (TrackF §9): no counterexample** in 1.11M evaluations on five surfaces, with 2,772 violator-free cycle classes. LPC-¼ holds. New data conjecture: a violator-free class containing an all-DL cycle has F/N ≥ 3/8. The smallest test bed is an RP² class of 72 states with 28 filled.
- Next: hand analysis of the smallest violator-free cycle classes (why do they have filled states, using duality only?); paper update with day-1 results; F2 deferred.

**8 Oct, early (TrackH).** LPC cannot be proved from hole-local facts. There is an explicit non-planar 28-vertex graph where D1/D2, P1–P3 and lock parity hold at every state, yet one Kempe class is a single all-DL π-cycle with no filled state (verified by three engines). Whatever makes LPC true lives away from the hole. Candidate global input: H3, a per-partition edge balance on closed triangulated surfaces (c₁ − β₁ = χ, etc.), which the counterexamples violate. The 3/8 data conjecture is broken (0.364 at χ = −1). New sphere-only data conjecture, **rigid isolation**: if c is a rigid DL state on a triangulated sphere (minimal two-colour component counts, so every Tait cycle passes through the hole), then π(c) is not rigid. Evidence: 0/22,053 real states, and 0/17,059 in an exhaustive chord model to N = 15. It is false on RP², so it is genuinely spherical. It rules out classes made only of rigid states, a sub-case of LPC.

**8 Oct (TrackI): chain-parity law [hand, unreviewed; 580k checks].** On the sphere, for every DL state c, N(π(c)) − N(c) ≡ [π(c) is DL] (mod 2), where N is the total number of Kempe chains. The proof passes through Lemma 5 (switching parity), whose key step, Lemma R, is band surgery on S² with non-crossing matchings. Corollary: **rigid isolation** (a rigid DL state never maps to a rigid one), so no Kempe class consists only of rigid states, and N alternates in parity along every all-DL π-cycle. It visibly fails on RP², where the far side of X is a Möbius band and the outer matching crosses. This is the first planarity-dependent result in frame territory. Not yet excluded: closed all-DL classes in which N alternates. Next: an independent adversarial review of RigidIsolation.md, then Lean, then the "near-rigid LPC" search.

**8 Oct (TrackH review): CONFIRMED with corrections.**
- The counterexample is confirmed, but the graph is not 4-colourable (χ = 5). The logic still holds: local facts can hold at every state of a class with no filled state. Its link degrees are 5,8,11,8,8, not as stated, and it was not minimised.
- H0 needs the hypothesis "s is DL" (the literal statement fails at non-DL states).
- H3 is confirmed (0 failures on 44.9M partition checks).
- Rigid isolation is confirmed as data on 59,441 fresh sphere rigid states.
- TrackH's "torus 0, Klein 0" is wrong: rigid → rigid steps occur on the torus (23), the Klein bottle (1) and RP² (29), which strengthens the "genuinely spherical" reading.

**8 Oct (TrackI review): Theorem 6 (chain-parity law) and rigid isolation are CORRECT.**
- Status: hand proof, independently reviewed.
- Gaps: three small ones (G1: the far-side regions are discs, via the Jordan region tree plus Schoenflies; G2: induct on an innermost pair of the target matching; G3: list every place planarity is used). Remark 7 is unproved.
- Data: 0 failures in 2.22M fresh sphere DL states, of which 775,987 have K with holes.
- Off-sphere correction: on RP², Lemma R step 2 (band surgery) fails on its own; on the torus, the failures come through Lemma 2 and Euler.
- Next: patch the write-up, then Lean (seek a combinatorial route via the existing ring/Jordan lemmas).

**8 Oct (TrackK): Conjecture F proved [hand, unreviewed].**
- No-hole case: Tutte's parity theorem plus Fisk's degree (arXiv:1912.07205), with Euler on Tait 2-factor regions.
- Hole case: fill the pentagon with the two lock diagonals.
- Data: every step checked, 0 failures on 165k sphere states.
- Off the sphere: the residue is exactly 2·(total genus of the 2-factor regions) mod 4, with 0 mispredictions on 14.5k torus states.
- F + Lemma W gives Theorem 6 and Remark 7 by a second, independent route. Next: review F and W.

**8 Oct: Lemma W formal (`ChainMod4.lean`, corrected statement with a boundary term β; β = 0 for π at DL states and for link-free swaps), and `chainParityLaw_of_F` formal.** So Theorem 6 (Route Q) now rests on Conjecture F alone, and F is all of its planarity. Two statement subtleties: F's `hand` must be read along the face orientation (`handS`), and it assumes no isolated vertices. The original W as written was false (Δcw can be odd). Coordinator recompiled; standard axioms.

**8 Oct: Conjecture F proof CORRECT on independent review** (TrackK-review: no wrong step; gaps K1–K4 are presentational: put the hand orientation and the no-isolated-vertices hypothesis into the statement, cite the corrected W, and spell out the Prop 1 topology). 0 failures on 998k fresh hole states. Torus residue = 2G confirmed (G_i = 1 iff every curve of S_i separates). The chain-parity law now has two reviewed hand proofs, and Route Q needs only F in Lean. Next: formalise F (Tutte's identity on SphericalMap).

**8 Oct (TrackJ): near-rigid structure pinned down; target NRC.**
- [hand] J1–J5: a near-rigid closed class consists of π-cycles alternating 8/9 chains, every 9-state is in-shape, and the extra chain Z is a perfect matching. On the sphere Z = σ in 26,481/26,481 states.
- Examples exist at every rung of the general-graph ladder, including 4-colourable graphs with all edges in triangles and H3 (43 graphs, n = 34–38). So the target needs planarity itself.
- **NRC (open):** on a triangulated sphere no π-cycle consists of DL states with N ≤ 9. Data: 0 such cycles in 473k holes; the longest run is 7 and has grown 4 → 7 over orders 27–32.
- Next: a planar proof attempt on NRC, starting from the σ-type lemma, in the style of Track I.

**8 Oct: Conjecture F, Theorem 6 (chain-parity law), rigid isolation and Remark 7 are FORMAL** (`TutteSides.lean`: Tutte's identity via ZMod 2 linear algebra, no topology; `ChainF.lean`: `conjectureF`, `chainParityLaw_sphere`, `rigid_isolation`, `remark7`; hypotheses: triangulated SphericalMap, no isolated vertices). Coordinator full regression: 91/91 modules, exit 0, every axiom line a subset of [propext, Classical.choice, Quot.sound]; SHA256SUMS 40/40. This is the first formal planarity-dependent theorem in frame territory.

**8 Oct (TrackL): σ-type lemma proved [hand, unreviewed]** by Euler counting only (Lemma E = H3 constants (2,3,3) on the sphere, plus a star identity for Kempe swaps). So in-shape states have the extra chain in α–μ (Z = σ). It breaks on RP², where the constants become (1,2,2). **NRC is still open:** Euler-level information cannot settle it, because the near-rigid alternation is a consistent orbit of the χ-recursion, so a Jordan-level input is needed. No monotone quantity was found among 16 candidates. Smallest open claims: NRC′ (the two-step map u ↦ π²(u) on rigid states has no periodic orbit) and Q-e (does NRC hold under H3's sphere constants plus the parity law?). Note: TrackL cites J1–J3 as reviewed; they are not yet, so they go into the review with SigmaType.md.

**8 Oct (TrackJL review): J1–J5, Lemma E, the star identity, Lemma S and S1/S2 are all CORRECT on the sphere** (from-scratch engine; up to 446M states, 0 failures). Fixes:
- J3: define rigid as Lean `RigidAt`.
- J4: "N(Zc) ≥ 9" holds on the sphere, not in any graph.
- TrackL's RP² remark: σ-type fails there 36/1,760 except at in-shape states.
- TrackL §2.2: the merge happens in α_cB_c.
None of these affects the near-rigid structure. NRC is still open; independent data agree that runs are ≤ 7.

**8 Oct (TrackM, owner's discharge idea): guided escape.**
- Scalar "discharge" scores and directional sweeps all fail as rules.
- What works is lock descent plus π on plateaus (Φ>π): 0 failures on 8M sphere DL starts, including adversarial ties, worst case 7 swaps (the BFS optimum is ≤ 4).
- [hand] Φ>π fills within R+2 swaps, where R is the longest run of interior DL states along a π-orbit.
- Candidate lemma **π-run bound R ≤ 5** on the sphere. Observed R ≤ 4 in the census and 5 on BV. It is 4CT-strength.
- Heawood-type interference is necessary for every failure but not sufficient.
- Off the sphere Φ>π fails even in classes that have filled states.

**8 Oct (TrackN, Q-e):** no R-cycle (a π-cycle of DL states with N ≤ 9) was found in any graph once Lemma E's sphere constants (2,3,3) hold at the cycle states, with or without the parity law (2.37M annealing evaluations plus exact MILP edge surgery). Every law-respecting cycle has a minimal skeleton of ≥ 3n−8 edges, the RP² count (+3 over the sphere). **Conjecture N1 (data):** no R-cycle satisfies the (2,3,3) constants at all its states, in any graph. If true, NRC is Euler-level, which is Lean-friendly. Caveat: one lineage of law cycles, all from an RP² seed. By-product [hand]: rigid isolation already follows from Lemma E plus the star identity. Next: torus/Klein-seeded law cycles (do they need +3(2−χ)?) and a proof attempt on N1.

**8 Oct (TrackO): R ≤ 5 is REFUTED.** R = 6 at p32.r62#15615 h11 (exhaustive frame census) and R = 7 from flip search (n = 31, min degree 5, not frame class), both two-engine verified. The qualitative claim (no all-interior π-cycle) holds everywhere. **Trend warning:** max R in the frame census grows with order (0,0,1,2,2,3,3,4,4,5,6 at orders 22–32), together with the near-rigid run length (5,6,6,7 at orders 29–32). Outside the frame class R stays ≤ 5 to n = 60 in random spheres. Long runs keep the N, N−1 alternation but are not always near-rigid (BV: N = 10–14). Order 33 census launched to watch the trend.

**8 Oct (TrackP).**
- The single-lineage caveat is broken: law R-cycles were found in 7 new lineages (sphere, torus, Klein; all 10-cycles).
- Surface memory is refuted: excess e = |E(G−h)| − (3n−11) reaches 2 from sphere, torus and Klein seeds alike, and 3 only on the RP² lineage.
- **N1 survives in refined form N1⁺: every law R-cycle has e ≥ 2.** Three e = 2 cycles are two-engine verified, and 0 lineages reach e = 0. Genus-2 seeds produced no law cycle.
- Part B [hand]: identity P1 says e equals the total cycle rank of the pair graphs at rigid states, so N1 ⇔ no law R-cycle with zero spare two-coloured cycles. Also P2 (monodromy: every edge is cut by some swap) and an edge-role cut balance. No contradiction yet; the missing input is component-level.
- Next: exact add+delete MILP on the e = 2 skeletons (can e = 1 occur?) and a component-level e ≥ 1 argument.

**8 Oct (Census33): order 33 is exhaustive** (764,855,802 plantri graphs → 58,194 frame-class graphs, 979,741 holes).
- R\* holds at every hole. The quarter floor is reached exactly (8,556 holes) and never broken.
- Lock parity: 0 failures on 3.3e8 sampled states.
- There are 25 all-DL π-cycles, all of length 20, all inside classes with filled states. NRC holds.
- **Max R stays at 6, but max NR rises 7 → 8** (NR by order 22–33: 1,3,3,4,4,4,5,5,6,6,7,8). The NR = 8 record is an alternation 8,9,…,9 entered from a non-DL state; NRC needs a closed run of ≥ 10. The trend continues to be watched.

**8 Oct (TrackQ).**
- **N1⁺ (e ≥ 2) is FALSE.** An exact e = 1 law R-cycle exists (n = 29, torus lineage), two-engine verified.
- **e = 0 is impossible** for all three skeletons (CP-SAT and HiGHS optimal, with LP certificates), and no e = 0 appears across 44 sampled lineage cycles. N1 (e ≥ 1) survives with exact certificates.
- [hand] Lemma Q-S reduces N1 to σ-type law R-cycles.
- Constraints on any proof:
  - it must use the exact count 3nv − 8;
  - 3-state windows are realisable at e = 0;
  - sphere runs of 7 have e = 0;
  - so it needs ≥ 8 consecutive states or the orbit's closure.
- Leads: a Laman/Henneberg potential, or a universal LP-dual certificate over the orbit.

**8 Oct (TrackR): no universal LP-dual certificate for N1.**
- Exact price/packing forms of the certificates (R1, R2): every σ-type cycle needs ≥ 5 consecutive states.
- Rotation-uniform templates certify nothing. The tag-word lemma [hand] says the 8 link chains carry identical tags at every state, so the structural objects carry no phase.
- State-specific prices certify e ≥ 1 but memorise lineages; they fail leave-one-out.
- The Laman/Henneberg lead is negative.
- **Conclusion:** N1/NRC needs component- or Jordan-level input, the same wall as P-B4 and Q-§2.7.

**Strategy note (coordinator, 8 Oct):** five consecutive attempts (L, N, P, Q, R) on NRC hit the same wall. Next: bank the formal chain-parity law in the paper; run the order-34 census to watch NR (8 at order 33); and return to a Jordan-level attack modelled on TrackI's proof of rigid isolation, rather than further Euler- or LP-level work.

