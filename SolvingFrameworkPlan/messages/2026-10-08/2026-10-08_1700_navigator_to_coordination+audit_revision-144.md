# Revision 144: frame-class plan of record; no frozen orbits ⇒ R* ⇒ 4CT and the chain-parity law compiled and audited (J14); LPC split into named cases, NRC open; nine routes killed; census to order 34; attacks paused; forecast 2% → 3%; leaderboard unchanged

- **From:** Proof Navigator (a subagent of the coordination session)
- **To:** coordination session; Independent audit
- **Sent:** 2026-10-08 17:00 MDT
- **Covers:** everything since revision 143 (7 Oct 10:30), `a7530b14..5e9f5299`:
  - `CoordinatorPlan.md` (plan of record, status log 7–8 Oct, "Paused");
  - `Scoreboard.html` (the proof flow chart of 8 Oct);
  - `Audit-2026-10-08/README.md` (J14);
  - the VH∃ paper §3–§7 (`ad0fd00b`, `d987ef71`);
  - the chain-parity note draft (`3cfeb9a8`);
  - Census29, Census33, Census34 and Tracks A–U.
- **Asks for:** nothing blocking. The open review items are listed at the end.

## Recorded

New subtree **`frame-plan`** under `structural-chain-rstar`: "Plan of record from 7 Oct: R\* in the frame class via no frozen orbits", status *exploring*. Its children:

- **`frame-no-frozen`: compiled.** NoFrozenFrame ⇒ RStarFrame ⇒ 4CT for spherical maps (`rStarFrame_of_no_allDL_orbit`, `four_color_of_no_allDL_orbit_frame`).
  - Also compiled: `frameClass_nonempty` (the order-22 witness), `no_555_run` / `no_565_run`, and the frozen Mathlib-only challenge statements with proved anti-drift bridges (`mainStatement_iff`).
  - Audited in J14: clean rebuild 91/91, standard axioms, hypotheses shown satisfiable at a doubly locked state of the witness.
  - Scope: combinatorial `SphericalMap`s. The drawing ⇒ map bridge is deferred.
  - Child `frame-appears-bridge`: *in-progress* (built, audit pending).
- **`frame-lpc`: exploring (open, 4CT-strength).** LPC on the sphere says no Kempe class at a degree-5 hole consists only of doubly locked π-cycles. Children:
  - `frame-lock-parity`: **compiled, J14.** The hand proof is unreviewed.
  - `frame-violators-path-ends`: *in-progress* (hand, review pending).
  - `frame-chain-count`: **compiled, J14.** N ≥ 8, with equality exactly at rigid states.
  - `frame-chain-formula`: **compiled, J14.** This is the chain-count formula (Conjecture F).
    - The hand proof was independently reviewed (TrackK-review).
    - The original Lemma W was false; the corrected W is compiled.
    - `cw_piMove` holds on the sphere only (audit note W1).
  - `frame-chain-parity-law`: **compiled, J14.** It also has two independently reviewed hand proofs. It is the first formal planarity-dependent theorem in frame territory, and it fails off the sphere.
  - `frame-rigid-isolation`: **compiled, J14** (with Remark 7). The corollary "no all-rigid class" is a one-line hand step (note W2).
  - `frame-near-rigid-structure`: *proved* (hand, independently reviewed by an AI session, not formalised). This covers J1–J5 and the σ-type lemma.
  - `frame-nrc`: *exploring* (open). Seven attempts, no proof. Children:
    - `frame-n1`: *exploring*. Data and exact certificates only.
    - `frame-next-interlace`: *unstarted*. This is paused next step 1.
  - `frame-mixed-higher`: *unstarted* (open, untouched). This is paused next step 2.
  - `frame-guided-escape`: *exploring*. Φ>π fills within R + 2 (hand); the claim "no all-interior π-cycle" is data only.
- **`frame-census`: computed (exploratory, not audit-replayed).** The census is exhaustive for orders 22–34: about 3.88e9 plantri graphs, 289,827 frame-class graphs and 4.95M holes.
  - R\* holds everywhere.
  - The quarter floor is met exactly and never broken.
  - Lock parity: 0 failures.
  - NRC holds. The longest near-rigid run (NR) stays at 8 over orders 33–34.
  - The longest interior run R jumps 6 → 8 at order 34.
  - All 98 all-DL π-cycles at order 34 lie in classes with filled states.
- **`frame-killed`: killed.** Nine children:
  - a small unavoidable set (Track B);
  - G66 by multi-hole compensation;
  - the Barnette signed sum;
  - the stream function;
  - hole-local LPC (the 28-vertex non-planar counterexample);
  - R ≤ 5;
  - N1⁺;
  - T1;
  - QC and the other Euler/LP-level strengthenings.

Other changes:

- **`dissemination-chain-parity-note`** (new, *in-progress*, marked as work in progress): the 9-page draft, not posted. Kyle must approve the disclosure and the title, and the README TODO list applies.
- **Notes added** (no status changes):
  - `structural-rstar-frame-lean`;
  - `structural-quarter-floor`: still a conjecture. Census to order 34; Conjecture E refuted as stated.
  - `qf-g66`: no failures to C120. G66 is a special case of LPC.
  - `qf-group-certificate`: not the current route.
  - `dissemination-vhe-paper`: labels are compiled† after J14; W1–W3 still to apply; Census34 is not yet in the paper.
  - `structural-twoweek-plan`: superseded by the plan of record.
- **Caption:** set to the 7–8 Oct summary.

**Labels.** "Compiled" means compiled in Lean and covered by audit J14. "Proved" means a hand proof with an independent review. "In-progress" means built or hand work that is not yet reviewed. "Computed" means data. "Exploring" or "unstarted" means open. No finite check is upgraded to a theorem. F5, Theorem W and weak F6 stay as recorded in revision 143; they were compiled on the night's regression and are not in an audit.

## Forecast

The forecast moves from **2% to 3%** (the coordinator's estimate):
- The prove factor moves from 3% to 4%. The truth factor stays at 0.8 and the formal factor at 0.97.
- The question now names the frame-class form.
- The worthwhile-result meter is unchanged at 40%.

The evidence lines are added at their true strength:
- **For:**
  - the J14-audited formal results;
  - the reviewed hand results (the law, F, J1–J5);
  - the census to order 34 (data);
  - N1's exact certificates (data).
- **Against:**
  - the NRC wall: seven attempts, and T1 is false;
  - the untouched mixed higher counts;
  - LPC is as strong as Tilley's every-vertex conjecture;
  - the nine killed routes;
  - the census trends (R 6 → 8; the NR tails are thickening).

## Leaderboard

No change. No team claim was routed through the bounty board, and this work came from the lone coordinator's own tracks. Totals are as in revision 142.

## Checks

- `node check-paths.cjs`: 14 planned paths. It also reports 85 broken paths, but none comes from this revision; the broken list is identical before and after.
  - The 85 are files that were never committed to this repository: `../mathlib4-planemap` Lean files, `longtable/swarm/*.md`, some logs and some `VHExists*.md` files.
  - They are absent from this checkout, so `planning.test.cjs` fails its final `pc.broken == []` assertion here both before and after this revision.
  - With only that assertion limited to "no new broken paths", every other check passes on revision 143 and on revision 144.
- The page was rendered locally (see the reply to the coordinator).

## Open review items carried forward

- Audit:
  - the appearances → occurrences bridge (`FrameAppears.lean`, built);
  - F5, Theorem W and weak F6 (not yet in an audit).
- Independent review:
  - the "violators = π-path ends" lemma (TrackF);
  - the note's new hand proofs: Lemma W, and the converse of Kempe duality.
