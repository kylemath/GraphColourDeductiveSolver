# Math / Creative Intel coordination plan

Updated 5 October 2026. This chat is Math. The user released autonomous continuation; Creative Intel / Long Table is resting. Addressed messages are posted in the shared messages directory for its next session.

## Accepted work

- WP11 validation: complete semantic replay of the frozen orders 19–20 output, including exact state sets, endpoint completeness, rank indices, survivor identities and both quantifiers. Accepted in the validation-complete Math reply.
- WP18: complete independent reproduction on all 961 graphs and 68,890 vertex/fan pairs. Only 17:1 has m=3; all other graphs have m<=2; every admitted start has mixed distance at most four on these files. Accepted in `8dffb45`.
- Belt: both competing teams completed the missing doubled-0 openings and termination. The joined hand proof is accepted within its stated citation scope: unequal-pole holes fill within 2n slides for every n>=5, equal poles use the star argument, and the nonsingleton pole-hole case cites Florek's theorem. Team A earned first-reviewed-proof credit; Team B supplied an alternate checked argument. No n>=14 belt census was released. Belt Lean work was subsequently accepted in the follow-up below.
- VH∃: the conditional induction route, containment, unlocking quantifiers and one-slide elimination are accepted in `MathVHAndMechanismReview.md`. The universal hypothesis remains open. An independent check reproduces the old 118-graph U∃ observation.
- M3: the general short-fill theorem is accepted in `MathShortFillTheorem.md`: on any finite simple graph with a finite palette, ℓ≤2 implies κ=ℓ at the original hole. Both parallel teams independently accepted the stronger scope.
- Graph 17:1: the legal-fan diagonal reduction and vertex-7 exact-distance-three certificate are accepted. Identical link colours and degrees do not determine exact distance; the broader neighbourhood-bound claim was withdrawn.

## Execution under frozen package e7172ca

The declaration is `backgroundMaterial/planemap-structural/longtable/WP19-preregistered-conjectures-declaration.md`, digest `56d1c97b8b913822822fe0ce5c8b4f2d05827c9845a1810c61037619e4b85a9e`. Producer/checker hashes and imported dependencies were checked, and their regressions passed. No source or statement is tuned between phases. Written releases are `8dffb45` (P1/P2) and `81b2bf7` (P3 after P1 cost).

| Phase | Scope | Current position |
| --- | --- | --- |
| P1 | All 2,070 order-23 graphs; seven statements | Producer, certificate checker and complete independent replay passed. m=1 on 302 graphs, m=2 on 1,768; U∃ throughout. No kill, interruption, truncation or unresolved pair. |
| P2 | U∃ only, all 843 order-21/22 graphs | Producer, certificate checker and complete independent replay passed. U∃ throughout. Other statistics are secondary data, not fresh tests. |
| P3 | All 7,290 order-24 graphs; seven statements | Complete independent replay and certificate checker passed. 24:6406 has exact m=3 and two degree-seven vertices, killing C1/C3. 24:7228 has an admitted start with ℓ=3 and κ=5, killing M2. U∃ holds throughout; M1/C2 passed on these graphs. No interruption, truncation or unresolved pair. |

Order 23/24 graphs were exposed to the overnight swarm's exploratory rank sweeps; the move/class statistics are fresh. Passes are finite computations. The supplied certificate checker alone does not establish positive histograms, upper bounds or U∃; Math's complete replay does that separately.

## Work division for this session

| Owner | Remaining deliverable |
| --- | --- |
| Math root | Completed all released phases, independent replays, certificate checks, lossless archives and reports. The consolidated commit/handoff includes both counterexample reviews. |
| Both existing parallel teams | Completed independent reviews of M3 and the two order-24 counterexamples. Each checked every one of the 70 lower-bound pair witnesses for 24:6406 and independently established exact ℓ=3/κ=5 for 24:7228. |
| Creative Intel / Long Table, next session | Withdraw killed M2/C1/C3 statements; integrate the general M3 theorem; explain the two saved counterexamples by hand before proposing any new test. Own corrections to source mechanism prose: remove the false converse after Lemma F (explicit 17:0 counterexample supplied), and separate a uniform all-start bound from existential VH∃. Keep its proof pages and source hashes current. No overnight execution is assigned. |
| Navigator, next session | Record actual acceptance scopes and remaining dependencies from Math's messages; retain exploring status for the unrestricted vacancy hypothesis. |

## Stops and limits

WP12 stays withdrawn. No extension past WP19's released phases, new rank sweep or new census is authorized by this plan. The follow-up authorizes the two specified Lean tasks. WP11 validation is now independently accepted: all 1,307 tables and 221,249 colouring orbits replay, with 259 existential survivors and 38 all-root survivors on orders 19–20. This remains finite G1/two-move evidence. Do not upgrade any universal vacancy claim from finite passes or a belt-family proof.

The final handoff contains the P1/P2/P3 result package, three killed conjectures on two order-24 graphs, exact resource/interruption accounting, independent replay bindings, both counterexample reviews and the separately labelled general M3 hand theorem. Evidence is `MathWP19Results.md`, `MathWP19Counterexamples.md`, `MathShortFillTheorem.md` and the frozen output manifest. Existing user release is sufficient; do not ask the sleeping user to reconfirm it.

## Long Table follow-up (commit 0fd7b23)

Math accepts the corrected mechanism statements. The requested full distance-gap distributions, P1/P2/P3 bindings and near-miss lists are in the follow-up-data reply. They use saved declared outputs only. Navigator revision 75 records the prior acceptances and kills.

1. **A, primary:** consolidate the independently compiled general M3 proofs into `VacancyShortFill`, add exact standard-axiom guards and a fresh 83-module source audit (the frozen 79 plus VacancySlide, short-fill and their two tests). Both teams compiled independent full proofs; the consolidated83-module audit passed. Task A is complete; see `ShortFillLeanReport.md`.
2. **B, next:** both existing teams independently formalize the actual unequal-pole belt walk with the 2n bound and n=5 cap. Transitions and termination must be derived from the graph and colouring definitions. This remains in progress.
3. **C, hand result:** both teams reviewed the triangle-clique-sum argument and the existing seed certificates. `TriangleSumM3Family.md` proves a chain of k copies of 17:1 has order 14k+3 and exact m=3. No new order was generated or searched. Universal boundedness remains open.

Long Table retains the hand analysis of the two order-24 witnesses. Math will post the compiled theorem with its precise printed statement and audit hashes when the fresh audit passes; Navigator should distinguish this from the separately accepted infinite-family hand theorem.
