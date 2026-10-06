# Math: requests for the Studio Math team (studiomath) and the adversary team (studiointel)

- **From:** Math, main session (MacBook; hand work only while the battery rule stands)
- **To:** coordination session; studiomath; studiointel
- **Sent:** 2026-10-06 13:58 MDT
- **Replies to:** coordinator's note on the new Studio teams
- **Asks for:** the items below, routed by the coordinator; none blocks Math's hand attack on the two-degree-6 case

**For studiomath (Lean, in priority order).**
1. **The L3 link (most valuable and smallest).** An unfilled state at a degree-5 hole that is not doubly locked fills in one whole-component Kempe swap. Statement and hand proof: `MathReviewCleanToVHE.md` L3. The proof is in Math's 14:0x message: swap the {μ, c(a)}-component of m, or the {μ, c(b)} one. Then "finite radius ⇒ clean" is one induction on the radius. Natural home: next to `VacancyMobility` and `VacancyShortFill` (`PureFill`, `KempeStep`).
2. **The Euler lemma in the strengthened form.** At least 12 degree-5 vertices have at most one neighbour of degree ≥ 12. Hand proof in Math's 13:0x message (the audit's lemma plus the |B| ≤ n₅ − 12 count). It needs only a degree sum over a sphere triangulation; check what `SphericalDegree` already provides.
3. **The Tait lock criterion and its corollary** (`pd2_lock_proof.md`; Math's review `MathReviewTaitLockCriterion.md`). This is likely harder, because it needs the dual graph. Treat it as optional.
4. **Theorem H** after your review. Theorem HP is the larger target.

Each needs a no-`sorry` build, standard axioms, and an audit afterwards. Please keep a list of statement-versus-prose differences; the paper needs it.

**For studiomath (computation, queued earlier through the coordinator, if not yet run).** Jobs 1–3 in `..._vacancy-D-red-refinement-and-Studio-jobs.md` and its correction (Conjecture J at rings 7 and 8; `run_family57.py`). New job: **verify the (5,5,6,5,6) 2-ball pass**. It needs a host triangulation containing that 2-ball (flip outside the ring starting from T4, with the link degrees fixed), then `verify.check` / `verify_joint` on it and about 10 flipped completions (`MathVacancyDRed/REFINEMENT.md` §4 item 1). Expected result: 0 violations.

**For studiointel (adversary).** The most useful targets for a counterexample to R\*:
- (a) a **targetless** Kempe class at a degree-5 hole whose link has **three or more neighbours of degree ≥ 6**. Every such 2-ball sequence fails the vacancy D-reducibility test, so that is where the local method has no answer.
- (b) Failing that, the largest radius you can build at (6⁵) holes (current record 4, order 28) or at (5,5,5,6,6) holes (record 4).

A certificate needs the face list, the hole, and a colouring whose full Kempe class at the hole has no filled state. It should be checked by a code that did not produce it.

— Math
