# Next steps with Creative Intel / Long Table

Updated 5 October 2026 after Long Table's `2026-10-05-longtable-to-math-navigator-and-audit-belt-vh-and-wp18-analysis.md`, commit `1bebeba`, and the parallel belt review, commit `6d49a25`. This replaces the initial preparation plan. Creative Intel is Long Table in the shared-file message protocol. Team ownership is acknowledged; a posted message does not itself constitute Math acceptance.

## Current objective

Review the new proof claims around VH∃ and the structure of graph 17:1, and obtain explicit acceptance of the completed finite WP18 replay and the joined belt theorem. Prepare a precise future test only after its claims and evidence dependencies are settled. Do not reopen the completed belt opening/termination tasks or launch another census.

## Completed work and remaining dependencies

| Work | Current position | Remaining action |
| --- | --- | --- |
| WP18 P1–P4 | Fully independently reproduced: 961 graphs, 68,890 pairs, every histogram and maximum/minimum; m=3 only on 17:1, m<=2 elsewhere, every admitted start within four moves on these files | Math's written acceptance of the finite statement; producer limitations must be repaired before a future run |
| Missing A_rho tile | Written, independently checked and adopted by Long Table | No re-derivation needed |
| Eight doubled-0 openings and termination | Both parallel teams completed both tasks; root hand review and separate constructive replay pass | Math review of the assembled theorem; no new local gap is being asserted |
| Joined belt theorem | `longtable/swarm/belt-joined.md` passed the audit's hand review; unequal-pole belt holes fill by slides within 2n for every n>=5; equal-pole star also checks | Exact family identification and Florek pole-deletion theorem remain cited dependencies; Math acceptance, not a self-contained re-proof |
| Named belt regression | All 947 unequal starts on existing G5/G8/G11 pass the root strategy, with proper final fillings and fixed poles; Long Table also reports n=6,7,9,10 checks | Distinguish chosen strategy lengths 4/10/14 from shortest lengths 2/4/6 |
| Corrections and reporting | Validation report sent, WP7 narrowed, fan classification located, 21-vertex two-swap mixed escape corrected, F32/F42 identified as root-zero deletion enumeration | WP11 still awaits Math's semantic acceptance; exploratory rank sweeps remain labelled as such |
| WP12 | Withdrawn and unreleased | Keep stopped |

Evidence: `FullWP18Replay.md`, `BeltParallelProofReview.md`, `IndependentWP18AndBeltReview.md`, and their hash manifests. The unrestricted vacancy hypothesis remains unproved; finite passes and the belt family do not establish it. Navigator owns ledger statuses.

## Updated division and order of work

| Priority | Owner | Task and concrete deliverable | Acceptance condition |
| --- | --- | --- | --- |
| 1 | This audit chat | Adversarial review of `longtable/swarm/vh-exists.md`, especially U∃, induction, containment, class quantifiers, and its checker's contract | A named proof gap or a reviewed implication with all quantifiers explicit; separate hand lemmas from the 118-graph observation |
| 2 | This audit chat | Review `longtable/wp18/analysis-17-1.md`: monochromatic diagonal reduction, legal-fan condition, crossing criterion, symmetry argument and vertex-7 distance-three certificate | Reconstruct the combinatorial reduction and independently exclude shorter paths for the cited witness; do not infer all-vertex structure from partial symmetry |
| 3 | This audit chat | Review `longtable/wp18/mechanism.md`: Lemma A and slide-to-swap claims; check the precise scope of its local-data obstruction | Give specific accepted statements or counterexamples; counts alone do not prove the general lemmas |
| Concurrent | Long Table | Retain ownership of joined proof, VH∃ page, mechanism/17:1 notes and checkers; answer review objections and narrow overclaims | Revised pages and a correction message, with own hashes and claim labels kept current |
| Concurrent | Math | Written acceptance/refusal of finite WP18; review joined belt proof with citations and VH∃ implication | Distinguish acceptance of a finite computation, a family theorem, and a universal conjecture |
| After claim review | Long Table, subject to Math's reply | Draft WP19 if Math requests it; freeze candidate statements, algorithms, graph identities, limits, certificates and stopping rules before release | Version-specific written go-ahead and user release before any run; no drafting request is treated as permission to run |
| Throughout | Navigator | Record actual files, review outcomes and remaining dependencies | No upgrade of unrestricted vacancy or compilation status from finite checks or hand review alone |

The audit owns its reports, scripts and coordination files. Long Table owns the source proof pages and future declaration/producer. Edit only the owner's files; send objections in a new addressed message. The two competing belt teams have finished. Team A receives the promised lead credit for the first complete reviewed candidate; Team B supplied a different checked argument. No further team work is launched by this plan.

## U∃ review: exact questions

U∃ asks for one degree-five vertex and one legal fan such that every Kempe class of the smaller fan triangulation contains an unlocked member: a colouring whose restriction to the original deletion fills in one Kempe swap. The reviewed route must justify:

1. Why a colouring of the smaller graph can be chosen by induction without circular use of the desired theorem on the original graph.
2. Why every relevant smaller-graph class is covered, and why its Kempe path transfers to legal component swaps in the original deletion.
3. Why “each class has an unlocked member” suffices even though not every start is itself unlocked. A result about immediate fill length is not a result about the total excursion length.
4. Why all legal-fan, simplicity, degree-four Jordan-split and small-order conditions are satisfied.
5. What the 41 failing pairs and 118 successful graphs actually say. The graph-level existential observation is post hoc and supplies no universal proof.

The audit should review the actual checker implementation before reproducing the claimed U∃ totals. Reuse existing graph files; do not launch a fresh-order test.

## Claims that need narrowing now

Long Table's statement that identical link colours and degrees at one pair show that “no bounded-radius lemma bounds fill length” is stronger than the evidence. Lengths 2, 3 and 4 with those same data show that those data do not determine the exact length. They neither exclude a common upper bound nor establish equality of coloured radius-r neighbourhoods for arbitrary fixed r. A bound of four, for example, is consistent with all three values. Request a precise replacement in the message and source page; do not repeat the broad claim as a proved obstruction.

Likewise, the crossing-diagonal criterion is explicitly conditional on all five fans being legal. Preserve that condition when summarising it. A post hoc correlation with degree sequences or an edge flip is not a proof of why every degree-five vertex is bad.

## Future declaration, not a release

Long Table proposes WP19 on order 23: M1 (mixed length<=4), M2 (fixed-hole Kempe length<=mixed length+1), C1 (m<=2 for orders>=18), C2 (m<=3), C3 (m>=3 implies degree sequence 5^12 6^k), and U∃. These are candidates formulated after existing observations. The earlier M3 (“every two-move fill has a two-swap fill”) is absent from the proposed list; the draft must explicitly include it or say it is not tested.

Order 23 is new for these proposed move/class statistics, but not an untouched graph sample: the user's overnight swarm already produced q/lin exploratory sweeps on orders 20–26. Disclose that exposure. Do not claim a pristine held-out graph set merely because WP18 ended at order 22. U∃ was formulated using data through order 20; later test design must record all relevant prior graph and statistic exposure.

Before a run, repair the known producer limitations: checks inside long enumeration/BFS work rather than only between starts, enforce memory/output limits, preserve partial information on interruption, define empty families, and bind declarations and code by hash. Successful paths prove upper bounds; exact distances require complete earlier layers. The min-over-pairs statistic also needs every pair accounted for, with unresolved bounds treated explicitly. Freeze negative regressions and source/input hashes.

Nothing new runs until the agreed written review and release are in hand. No n>=14 belt enumeration, Lean work, new rank fitting or reopened WP12 is part of this plan.

## Next checkpoint

The next audit handoff should contain the U∃ implication review, diagonal/witness review, narrowed mechanism claims, and any corrections requested from Long Table. Separately record Math's actual acceptance decisions and its reply on whether to draft WP19. Only then settle the future test package and seek its release. Keep the existing belt proof and WP18 evidence as completed deliverables with their remaining acceptance/citation dependencies explicit.
