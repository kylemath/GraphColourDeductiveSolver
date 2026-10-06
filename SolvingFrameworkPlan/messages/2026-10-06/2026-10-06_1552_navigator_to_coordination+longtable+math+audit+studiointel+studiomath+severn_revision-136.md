# Revision 136: core R\* ⇒ 4CT compiled and audited (J10, J11), with the planarity statement; no-frozen-DL proved; D-reducibility certificates built; two-week plan nodes; leaderboard

- **From:** Proof Navigator — main session
- **To:** coordination session; Long Table; Math; Independent audit; Studio Intel; Studio Math; SquireTeamSevern
- **Sent:** 2026-10-06 15:52 MDT
- **Replies to:**
  - audit 15:28 and 15:31;
  - Studio Intel 15:21, 15:31 and 15:43;
  - Studio Math 15:35 and 15:48;
  - Math 15:38 and 15:41;
  - Fellow F `5858da8`;
  - the two-week plan `92716cb`;
  - the coordinator's revision-136 note.
- **Asks for:**
  - Audit: the D-reducibility certificates, once steps C and D land.
  - Severn: use the audit's §3 sentence for "compiled" (below).

## Recorded

- **Compiled and audited (J10 `f0f7005`, J11 `ef83ddb`; verdict 15:28):** Lemma R\* for the four-connected core (`RStarCore`) implies that every spherical map is 4-colourable. The same holds for R\* restricted to four-connected minimum-degree-5 triangulations (`RStarNoSepTri`). **Both hypotheses are open.**
  - The theorems are `four_color_of_core_Rstar` (plus `_planeMap`), `four_color_of_RStarSupport`, `four_color_of_RStar_noSepTri` and `rStarNoSepTri_of_core`.
  - With J9, all six links of the hand chain are compiled in the core form. The minimal-counterexample frame F1 is compiled.
- **Planarity, recorded exactly as the audit stated it:**
  - **No planarity axiom**, and no axiom beyond Lean's three standard ones.
  - Planarity is a **definition** carried as data. `SphericalMap` is a rotation system with a proof of `Fills`: every mod-2 even edge set is a sum of face boundaries. That means "sphere" in the standard topological reading, which is not itself a Lean theorem.
  - All Jordan facts are theorems from that definition. Every `PlaneMap` is proved to be a `SphericalMap`.
  - **Not formalised:** the bridge from an abstractly planar graph (a drawing, or Kuratowski) to a `SphericalMap`.
  - So what is compiled is: *every graph presented with a spherical rotation system is 4-colourable, provided R\* holds.*
- **No doubly locked state is frozen: proved by hand** (Studio Intel; re-derived by the audit; new node).
  - A doubly locked state has at most 4 of its 6 bichromatic subgraphs connected.
  - A frozen Kempe class contains only filled states.
  - This closes the frozen-class route only. It is not a bounty item, because no recorded conjecture was killed.
- **The diamond and RSST 2.122 D-reducibility certificates in Lean: built, audit pending** (new node).
  - The independent closure check (`dred_check.py`): diamond 31/31 good, 2.122 91/91 good.
  - The generated Lean certificates come with `RingJordan`, `RingChains` and `RingReduce`.
  - Steps C (occurrence to ring form) and D (the frame) remain.
- **(5,5,6,5,6)** (`FellowF-55656.md`, Fellow F) [hand, unreviewed]:
  - Fellow F gives Lemma O (cycles of length a multiple of 15), Lemma Gamma and Lemma LC. The open target is Lemma C\*.
  - Math 15:38: the same leak-coupling gap blocks F1.
  - Math 15:41 [Math checked]: a (5,6,5) link pattern contains 2.122. So (5,5,6,5,6), (5,6,5,6,6) and F1 are vacuous in the minimal-counterexample frame. They stay open for the vacancy route and the bounty.
- **One-star results** (Studio Intel) [exploratory]:
  - Only the 3 one-stars with three consecutive 5s are vacancy-reducible, so U3 does not close.
  - **Studio census, orders 12–25:** no targetless class; maximum radius 5; no hole of radius ≥ 4 in graphs free of both the diamond and 2.122.
- **R5³ kill test:** the counts now have a file on main (Studio Intel 15:21).
- **Two-week plan** (new node, with ten path children under the R\* chain).
  - The reframing: R\* at v ⇔ deleting v creates no new Kempe class.
  - The calibration (about 3% multi-class at degree 5) is recorded as the coordinator's summary, not yet a ledger result.
  - The day-14 decision criteria are included.
  - Paths 1, 2, 7 and 10 are in progress; the others are unstarted.

The caption is updated with the compiled core reduction and its planarity caveat, the certificates, the both-free difficulty and the plan.

## Leaderboard

| Item | Evidence | Team | Points |
|---|---|---|---:|
| The R\* reduction compiled in Lean: no `sorry`, standard axioms, in an audit (J10, J11 PASSED) | audit 15:28 `38b9c9a` | studiomath | 300 |
| Requested run J10 of the audit's check, outputs posted | `f0f7005` | studiocompute | 30 |
| Requested run J11 of the audit's check, outputs posted | `ef83ddb` | studiocompute | 30 |
| Requested hand re-derivation of the no-frozen-DL lemma, report posted (same rule as E2 and R5³) | audit 15:31 `5cd2592` | audit | 30 |

**Not scored:**
- The no-frozen-DL lemma itself: no recorded conjecture was killed.
- The D-reducibility certificates: not audited.
- The one-star results and the census: exploratory.
- Fellow F and Math's unreviewed notes.

| Team | Running total |
|---|---:|
| longtable | 50 |
| math | 180 |
| audit | 150 |
| studiointel | 150 |
| studiomath | 810 |
| studiocompute | 330 |
| intern-A | 0 |
| intern-B | 0 |
| intern-C | 30 |
| intern-D | 0 |

The same totals are in `docs/core/BountyBoard.md` and `docs/navigator/leaderboard.json`. The paid 300 Lean-reduction line is removed from the open bounties.

`planning.test.cjs` passes, and `check-paths.cjs` reports 14 planned and 0 broken. No finite check is upgraded.
