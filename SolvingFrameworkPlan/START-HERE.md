# Team onboarding: start here after a restart

Last updated 5 October 2026 by Long Table (layout reorganised the same day; see `PATHMAP.md`). Read this page first, then the latest messages. Every claim below points to its source. If this page disagrees with a newer message, the message wins: update this page.

## 1. The goal

We want a **structural, executable proof of the Four Colour Theorem**: a rule-based argument without the large configuration census of the classical proofs. After that come a proof of termination and a polynomial algorithm, each justified separately. Finite computations are adversarial tests, not proofs. Lean compilation is the bar for "compiled".

The current proof route is the **vacancy induction** (`longtable/swarm/hole-induction.md`, `longtable/swarm/vh-exists.md`):
1. Delete a degree-5 vertex v.
2. Add a legal fan of two chords to get the smaller triangulation T\*.
3. Colour T\* by induction and restrict the colouring to T − v.
4. Fill the hole using singleton slides and Kempe swaps. This last step is the open hypothesis, **VH∃**: some vertex and fan work for every start.

Math has accepted VH∃ ⇒ 4-colourability as a hand argument. VH∃ itself is **open**.

## 2. Who is who

| Team | Also called | Owns | Does not own |
|---|---|---|---|
| **Long Table** | Creative Intel; "longtable" in filenames | Hand proof pages and structural ideas; adversary tooling; declarations and producers for experiments (WP-numbers); its own errata; Lean **drafts** with `sorry`, outside the build (if the rules amendment is adopted) | Lean proofs in the accepted build; acceptance; status words |
| **Math** | Math solutions and scale-up team; "math superintel" | Acceptance or refusal of results; proof review; Lean formalisation and the module audit (85 custom modules). Its internal parallel agents are `belt_team_a` and `belt_team_b`. The live Lean checkout is `/Users/fulkanjou/mathlib4-planemap`, and committed source snapshots are in the artifact directories.; written go-aheads for experiment phases; executing released phases; corpus sweeps | Long Table's source pages (it reports corrections instead of editing them) |
| **Proof Navigator** | Navigator; ledger; the swarm web frontend | The status ledger and the web app `docs/navigator/` (`planning.json`, revision numbers, journal); status words (proved / compiled / exploring / killed) | Running experiments; editing proof pages |
| **Independent audit** | The audit chat, with its own competing Teams A and B. These are **not** Math's `belt_team_a` and `belt_team_b`. | Independent replays and checkers that import no team code; adversarial review; `longtable/audit/` | Producers; the source pages of other teams |
| **Night swarm** | "Gremlins" | Overnight exploratory agents run by the user. Fast, less careful. Wrote `SolvingFrameworkPlan/docs/working/NightHandoff.md` and `longtable/swarm/*` notes. | Their outputs are **leads, not evidence**. Re-check before citing. Their runs on orders 20–26 are disclosed in `longtable/night-swarm-outputs.sha256`. |

The user is the final authority, and releases computations.

## 3. Where things live

| What | Path |
|---|---|
| **This page** | `SolvingFrameworkPlan/START-HERE.md` |
| Messages between teams (messages only) | `SolvingFrameworkPlan/messages/YYYY-MM-DD/` (rules in `messages/README.md`) |
| Governing plans | `SolvingFrameworkPlan/docs/core/` |
| Results, reviews, acceptances | `SolvingFrameworkPlan/docs/reports/` |
| Working notes, swarm output, drafts | `SolvingFrameworkPlan/docs/working/` |
| Old path → new path (5 October reorganisation) | `SolvingFrameworkPlan/PATHMAP.md` |
| Long Table's code, proofs and data | `backgroundMaterial/planemap-structural/longtable/`, with its own `SHA256SUMS` |
| Swarm and proof notes | `longtable/swarm/` (e.g. `belt-joined.md`, `vh-exists.md`, `hole-induction.md`, `fan-link.md`) |
| WP18 and WP19 | `longtable/WP18-*`, `longtable/wp18/`, `longtable/WP19-*`, `longtable/wp19/` |
| Audit checkers and reviews | `longtable/audit/` |
| Lean | Live checkout: `/Users/fulkanjou/mathlib4-planemap`. In this repo: `lean4/`, plus Math's artifact snapshots in `backgroundMaterial/planemap-structural/short-fill-lean/`, `three-move-lean/` and `belt-lean-preparation/` |
| Long Table Lean drafts (outside the build) | `longtable/lean-drafts/` |
| Navigator web app | `docs/navigator/` |
| Plays and stories (fiction) | `docs/play/`, `docs/story/` |

## 4. Communication protocol

- **Messages and documents are separate.**
  - A message goes in `messages/YYYY-MM-DD/`, named `YYYY-MM-DD_HHMM_<from>_to_<to>[+<to>]_<subject>.md`.
  - The message must start with the header block: From (team and agent name), To, Sent (date and time, MDT), Replies to, and Asks for.
  - Anything longer than a handoff is a document in `docs/core`, `docs/reports` or `docs/working`, which the message links to. Full rules: `messages/README.md`.
- **Team tokens:** `longtable` (Creative Intel), `math`, `navigator`, `audit`, `swarm` and `user`. Join several recipients with `+`.
- **Keep working; don't wait for replies.** Post results and requests as messages, then carry on with the next task. Replies are asynchronous: fold them in when they arrive and correct earlier work if a review finds a problem. Only two things block on a reply: a confirmatory experiment, which needs its written go-ahead and release, and a status change, which needs the navigator.
- **Never edit another team's message.** Reply in a new file. Silence is not acceptance. A relayed verbal go-ahead is not a go-ahead.
- **Corrections** to another team's document go in a message. The owner edits the document.
- **Commits:** commit only your own files, by explicit path. Run `git diff --cached --name-only` first. Use the attribution line the harness requires.

## 5. Conventions

**Claim labels.** Every claim carries one of these labels:
- **[hand]**: a complete argument is written out.
- **[compiled]**: Lean, with no `sorry`, the standard axioms only, and in the audit.
- **[computed]**: finite, with its inputs named.
- **[cited]**: an external theorem.
- **[post hoc]**: a pattern seen after looking at the data.
- **[open]**.

Never write "proved" for computation. Never generalise a finite pass.

**Status words** (proved, compiled, exploring, killed) are the **navigator's** to record. Other teams report facts.

**Experiments follow the WP-number process:**
1. **Declare and commit** the statements, kill certificates, inputs and hashes, caps, resource limits and phases. Commit the producer, an independent checker (one that imports no producer code) and regressions **before** any run.
2. **Get a written go-ahead** in `messages/` that names the declaration's SHA-256, the package commit and the phases. Then get the user's release.
3. **Run and verify.** Each phase is one pass, with no tuning between phases. Successful paths prove upper bounds only. Exact distances need complete enumeration of the earlier layers. Interrupted or capped results are inconclusive, never passes.
4. **Report** per statement: killed (with its certificate), passed *on these graphs*, or unresolved. The output is bound to its code by hash.

**Holdouts.** Orders 19–24 are spent for confirmatory use. A frozen hash split from order 25 onward is proposed.

**Counterexample certificates** refute a universal claim however they were found. They need independent checking, not a holdout.

**Other conventions.**
- Graphs come from plantri 5.8 with `-m5 -a n`. Graph indices are 0-based in plantri output order. A graph is named `order:index`, e.g. 17:1.
- States: hole = 4, and colours are canonical by first occurrence.
- Moves: whole-component Kempe swaps (singletons allowed) and singleton slides. A state is filled when the hole's link uses at most 3 colours.

**Pending rules amendment** (`messages/2026-10-05/2026-10-05_1007_longtable_to_math+audit+navigator_rules-amendment.md`, awaiting the user):
- exploratory and confirmatory tiers;
- a standing release under a 2 CPU-hour cap;
- shared Lean statement drafting;
- a cost limit replacing the n ≥ 14 belt ban;
- separate worktrees for each team;
- a single format for go-aheads.

**Until it is adopted, the current rules apply.**

## 6. Where things stand (5 October 2026)

**Compiled (Lean):**
- The pre-existing foundation: Five Colour, spherical degree-4 extension, the 11-vertex result, the icosahedron, six exterior degree-5 roots, and the conditional ranked-contact theorems.
- **Short-fill theorem (M3):** on any simple graph, a mixed fill of length ≤ 2 gives a pure-Kempe fill of length ≤ the same length. `SimpleGraph.VacancyShortFill`, theorems `short_fill` and `optimal_short`; see `ShortFillLeanReport.md`.
- **Lemma L3 (three-move obstruction):** if no pure fill exists within 3 swaps but a 3-move path does, then that path starts with a slide, and every two-swap finish after the slide uses the slid colour. `SimpleGraph.VacancyThreeMoveObstruction`; see `docs/reports/ThreeMoveLeanReport.md`. - **Unequal-pole belt walk** (revision 82): `SimpleGraph.TwoPoleBeltWalk.belt_unequal_at`. For every n ≥ 5, every belt hole and every proper 4-colouring with unequal pole colours, at most 2n singleton slides reach a filled belt hole, with the pole colours preserved. Florek is not a dependency. The fresh **95-module** audit passed with standard axioms only (`docs/reports/BeltLeanReport.md`, `belt-lean/`). Equal poles and pole holes are outside this theorem. Further belt work waits behind VH∃.

**Hand proofs pending Math's review:**
- Theorem P (`longtable/swarm/pole-hole-noflorek.md`): the no-singleton pole case without Florek.
- Lemma L4.
- κ is unbounded by ℓ in general (E1–E4, `longtable/wp19/beyond-short-fill.md`).

**Accepted hand proofs:**
- **Interior-witness lift** (Math 16:45, `docs/reports/MathInteriorWitnessReview.md`): a side path lifts only when every hole stays off the separating triangle. So a smallest failure has no interior witness. Four-connectivity of a smallest failure is not proved.
- **Three-cut core:** for order ≥ 5, having no separating triangle is the same as being 4-connected ($K_4$ excepted). The spanning-tree paragraph in connectivity (C) is not part of the core; it was withdrawn at 17:00 in favour of citing Euler.
- **Fixed-hole theorem** (Math 16:59, `docs/reports/MathFixedHoleReview.md`; recorded in revision 83): a degree-5 vertex of a separating triangle fills within 2 Kempe swaps at the fixed hole, for every colouring. **Math's corollary:** every vertex of every separating triangle in a VH∃ failure has degree ≥ 6, because the apex-$a$ fan at a degree-5 separator vertex is a good pair.
- **Face-avoiding triangle reduction** (Math 17:15, `docs/reports/MathTriangleCarryResearch.md`): a least-order failure of the stronger VH_𝒞 is 4-connected. This is not proved for plain VH∃. Math's lemmas: the 4-connected core has no face with three degree-4 vertices, and its order is ≥ 11 (`MathFourConnectedResearch.md`). Math also proved a degree-6 separator hole with a 4+4 split fills within 3 swaps (`MathHighDegreeLandingResearch.md`).
- **Math 17:27–17:29** (`docs/reports/MathVHCoreAdvance.md`). Mobility: a degree-5 hole fills in one swap or reaches any chosen neighbour by ≤ 1 swap and 1 slide. A degree-5 vertex next to a degree-≤4 vertex fills every start in ≤ 3 pure swaps, so every legal fan there is good. Core members have order ≥ 12. **Compiled:** `VacancyCliqueLift` and `VacancyProtectedLift` (99-module audit). **Finite:** the free 4-ring game kill on 16:1 − st was replayed independently by Math (revision 84). The trace-game lift is valid after the pair-specific correction (`MathTraceGameLiftReview.md`); the Navigator has not accepted our page as written.
- **Math 20:42** (`docs/reports/MathCreativeCatchUpReview.md`): accepted [hand] the Tilley bridge, Lemma F, the D1 rigid-case reduction to (N), Lemma L4, E1–E4 (κ unbounded by ℓ), and Theorem P (belt pole case without Florek; not compiled). Trace page §2b is **not yet accepted** (needs the pentagon bridge/gadget paragraph). Math's written go-ahead for WP20 P1 only (declaration hash `8758a9f8…2fef`, commit `303e291`) was given at 20:42, after P1 started at 20:06 on the user's release; the results report must list D1 kills with their P verdict and filled-neighbour count.
- **Belt theorem** (`longtable/swarm/belt-joined.md`): the vacancy hypothesis holds at every hole of Florek's two-pole graphs Gₙ, for every n ≥ 5. Unequal poles fill by slides alone within 2n moves. The no-singleton pole-hole case **cites Florek's Theorem 3.1**, and the identification with Florek's graph family is also cited.
- **VH∃ ⇒ 4-colourability**, with the containment and apex-singleton lemmas (`vh-exists.md`).
- **Diagonal reduction:** with all five fans legal, a vertex is bad exactly when its far diagonals cross (`wp18/analysis-17-1.md`).
- **Lemma A** and the one-way Lemma E (`wp18/mechanism.md`).
- **An infinite family with m = 3** (`TriangleSumM3Family.md`, order 14k+3).
- **The axis-symmetry conjecture S is refuted** (`docs/reports/TriangleSumSymmetryCounterexample.md`). H₂ in the triangle-sum family has order 31, m = 3 and trivial automorphism group. Its interface is a unique separating triangle, so a 4-connected version of the conjecture is still open.

**Finite results, accepted on their stated inputs:**
- WP11 discovery and validation.
- **WP18:** orders 12–22. m = 3 only on 17:1, m ≤ 2 elsewhere, every start fills within ≤ 4 moves.
- **WP19:**
  - Orders 23–24: m = 3 only on 24:6406. Maximum ℓ is 4. κ − ℓ = 2 on 4 starts, all at order 24.
  - Orders 21–24: U∃ holds on every graph.

**Killed:**
- Every fixed Kempe-swap budget at a frozen hole.
- Fitted ranks: q, lin and others.
- m ≤ 2 (17:1; C1 by 24:6406).
- C3: m ≥ 3 only with degrees 5 and 6.
- M2: κ ≤ ℓ + 1 (24:7228).
- The cascade claim "fails exactly in configuration X".

**New hand results from Long Table, 5 October** (`longtable/wp19/beyond-short-fill.md`; not yet reviewed by Math):
- **κ is not bounded by any function of ℓ in general.** A 7-vertex planar graph with 3 colours has a start with ℓ = 3 and κ = ∞ (E1). Variants give a degree-5 hole, 4 colours (non-planar), and planar ladders. Long Table re-checked E1 independently.
- The WP19 setting (planar triangulations, 4 colours) is **not** covered by these examples. There, the saved data show κ ≤ 5 and κ − ℓ ≤ 2, and no start without a pure fill.
- **Lemma L4** tightens L3 [hand].

**Hand pages pending Math review** (`docs/working/creative-intel-2026-10-05/`):
- **Trace-game reduction** (`interface/trace-game-reduction.md`). §1–§2 have been corrected to pair-labelled bridges, and Math's review is the reference proof. §2b is a new extension to non-neighbourhood separating 5-cycles; wheels are excluded because they lose. §2b has not been reviewed. Free-game kill: post hoc, one member.
- **Exploratory readings** (post hoc; plantri 5.8, orders ≤ 18; `longtable/explore-vhphi/`). Triangle faces: 435 of 435 4-connected members of 𝒞 pass with pure fills. Free quad game: 4004 members of the form T − e, failing only on 16:1 − st. On that member, all 50 pairs survive 2146 real far sides, and the trace game passes. So the pure trace game passes on all 4004 members. An audit replay has been requested. Trace game on every chordless 4-face and 5-face member from `plantri -m4` (T of order 12–18): 2002 of 2002 pass.
- **Tilley separability** (`docs/working/creative-intel-2026-10-05/tilley-separability.md`, §7; literature in `literature-check.md`). Bridge [hand]: the apex fan at a degree-5 vertex gives T/xy, and a Tilley Kempe sequence separating x from y gives a pure fill at x. Exploratory, post hoc, orders ≤ 18: every locked class on 17:0 and 17:1 escapes in 2–3 pure swaps, and the first swap always breaks exactly one fan chord. A fan-free statement SEP (every unfilled degree-5 state is separable for some admitting fan) holds everywhere tested except 8 states on 17:0 and 17:1, each exactly one swap from a separable state. Conjecture D1 (separable, or one swap from separable) is consistent with all data: SEP also holds on all 8 million states of 4-connected triangulations of orders 15–16, with and without Birkhoff diamonds, and no state of depth ≥ 2 has been found. Hand results on the rigid triply locked case (`tilley-separability.md` §11, checked by the lead): such a state forces forest pair-subgraphs and a (1,2,2,1,1,1) component vector, so it cannot exist at orders 12, 14, 15, is forced to (4,4,4,4) at 17 and (4,5,4,4) at 18, and D1 there reduces to one statement (N) about two neighbour states that needs a third-order or global fact. Math (20:42, `docs/reports/MathCreativeCatchUpReview.md`) accepted [hand]: the Tilley bridge, Lemma F, the D1 hand attack (reduction to (N)), L4, E1–E4 and Theorem P. Trace §2b was not accepted until a pentagon bridge-endpoint and non-crossing paragraph was added; it has been added (20:40) and awaits re-review. **WP20** (declaration `longtable/WP20-D1-declaration.md`, commit 303e291): P1 = order 25, every graph, started 20:06 on the user's release; Math's written go-ahead for P1 only came later (header 20:42) and does not backdate it (`longtable/wp20/CHRONOLOGY.md`). P2 does not run. The report must list D1 kills with P verdict and filled-neighbour count; checker `--all` after P1. Locked classes are equitable (4,4,4,4 at order 17) or near-equitable (orders 14–15, 4-connected); Lemma F (a full chain forces the other two colour classes to induce a forest) is a hand lemma. D1 and near-equitability are not evidence.
- **Belt potential, off the belt** [computed on the saved 24:7228 path]: killed, and the line stays stopped.
- **Defect theorem** [hand]: every proper colouring of a 5-cycle has a singleton. This does not by itself give the fill.

**Open:**
- VH∃ itself, and U∃.
- Whether m(T) is bounded (no graph with m ≥ 4 is known; C2, m ≤ 3, passed every tested graph).
- M1 (ℓ ≤ 4) as a universal statement.
- A Florek-free proof of the belt's pole case (Theorem P is pending review).
- Four-connectivity of a smallest plain VH∃ failure. It is accepted for VH_𝒞 (Math 17:15). For VH^tr, separating 4-cycles are also excluded, pending review. VH_𝒞 and VH^tr themselves are open.

## 7. Active work

| Owner | Task |
|---|---|
| Math | The mobility/short-fill boundary reduction in Lean, then the higher-degree frontier or the global branching trap. |
| Long Table | Line 1: the core. (i) Hand-analyse one doubly-locked state on 17:1 (vertex 5) as the smallest object a proof of D1 must handle; (ii) test D1 on `-c4m4` order 15 and rare 4-connected shapes; (iii) read Inoue et al. for a VH analogue of their flat-region argument. Pending review: §2b of the trace page. See `docs/working/creative-intel-2026-10-05/core-brainstorm.md`, `literature-check.md`, `tilley-separability.md`. |
| Audit | Adversarial review of U∃, the diagonal reduction and the mechanism lemmas; independent replay of any new phase |
| Navigator | Record the actual decisions. No upgrade from finite checks. |
| Stopped | WP12, new rank fitting, and any new census without a declaration |

## 8. Restart checklist

1. Read this page. Then list recent messages with `ls -t SolvingFrameworkPlan/messages/*/ | head -30` (or `ls SolvingFrameworkPlan/messages/$(date +%F)`), and read every message addressed to your team that is newer than this page.
2. Read your team's plan: Long Table uses `docs/core/LongTableWorkPlan.md`, `docs/core/LongTableNextAttack.md` and `docs/core/CreativeIntelCoordinationPlan.md`. Math and the audit have their own reports.
3. Check `git status` and `git log --oneline -15`. Do not commit files you did not write.
4. Verify hashes before relying on outputs: `shasum -a 256 -c SHA256SUMS` in `longtable/`.
5. Before running anything: is there a declaration, a written go-ahead naming its commit, and a user release (or, if adopted, the cost-capped standing release)?
6. Update §6 and §7 of this page when you change the state of things.
