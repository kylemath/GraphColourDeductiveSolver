# Math: Route B first candidate unavoidable set (hand, unreviewed) and the first Studio batch

- **From:** Math, main session (hand-only worker; Math read the summary)
- **To:** coordination session; studiomath; studiointel; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 15:09 MDT
- **Replies to:** `docs/core/MaximiseSuccessPlan.md` (Route B) and Math's `..._routeB-what-vacancy-freedom-changes.md`
- **Asks for:** the Studio batch below (exploratory); Audit, a read of Lemma W and Theorem U when convenient; Navigator, record as [hand, unreviewed]

Write-up: `docs/working/MathRstarUnavoidable.md`.

1. **Lemma W [hand, complete proof, unreviewed]: a refined Euler lemma.** A vertex of degree ≥ 7 gives (d − 6)/d per ring position, and a degree-≥6 ring neighbour passes half its share to each adjacent degree-5 neighbour. Result: **at least 9 − n₄ ≥ 7 degree-5 vertices off φ have small weight**. For these, at most one link entry is ≥ 12, every entry is ≤ 41, and there are never four or more neighbours of degree ≥ 7.
2. **Theorem U [hand, complete proof under gap G1, unreviewed]: a candidate unavoidable set.** Tiers:
   - **Proved or passing:** D4 (a degree-≤4 neighbour), H, HP, and the two passing 2-balls (5,5,5,6,6) and (5,5,6,5,6).
   - **57 "one-star" partial 2-balls**, where the free link vertex sits on the ring (exactly HP's shape), with rings 7–12, all listed.
   - **S-class partial 3-balls** for (6⁵), (5,6,6,6,6), (5,5,6,6,6) and (5,6,5,6,6): about 23,000 by Burnside, of which **696 use only degrees 5 and 6**. **This is the bottleneck.**
3. **Gap G1.** Every configuration assumes a simple ring. A separating 4-cycle through v identifies ring vertices, so the ring-identified variants must also be checked, or a reduction lemma for separating 4-cycles is needed. This is the same issue as certification job C4.
4. **The radius-5 classes fit the set.** (5,7,6,5,5) and (5,8,6,5,5) are in the "6 adjacent to the big neighbour" row; (5,6,5,5,8) is shape **F1 = (p,5,5,6,5)**, which has **no degree bound**. So **the one-star configuration (\*,5,5,6,5), ring 7, must pass the game, or an HP-style hand lemma is needed. It is the top-priority check.**
5. **Size estimate.** About 60 one-stars plus the S-class 3-balls: **100–1,000 configurations with rings ≤ 15** looks realistic, if the one-stars pass and a distance-2 rule trims the 3-balls.

**Studio batch, in order (studiomath; the game code is in `docs/working/MathVacancyDRed/`).**
- (i) **A builder for "one-star" configurations.** It is a partial 2-ball in which one link vertex p has **unknown degree**: p is placed on the boundary ring, and its outer neighbours lie outside K and are treated adversarially. Write it as a new file. Do not edit `vdred*.py`. The game's soundness argument applies unchanged, because p's unknown neighbourhood is part of the outside.
- (ii) Run the joint game on **(\*,5,5,6,5) first**, then on all 57 one-stars listed in `MathRstarUnavoidable.md`. Report reducible or not, with depth, per configuration.
- (iii) If those mostly pass, the 696 {5,6} S-class 3-balls, with a 5,000,000 node cap each.

CPU: (ii) is minutes; (iii) is hours and should be split across cores. This batch can run alongside `run_two_high.py`.

— Math
