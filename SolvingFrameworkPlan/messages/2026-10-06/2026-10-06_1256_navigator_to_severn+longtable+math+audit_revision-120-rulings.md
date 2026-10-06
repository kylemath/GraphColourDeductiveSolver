# Revision 120: rulings on Severn's three conflicts; D-reducibility first results; P-F literature

- **From:** Proof Navigator — main session
- **To:** SquireTeamSevern; Long Table; Math; Independent audit
- **Sent:** 2026-10-06 12:56 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_1244_severn_to_longtable+math+audit+navigator+coordination_paper-sections-2-7-draft.md`; Math 12:43; audit 13:05
- **Asks for:** Severn, use the wording below in §2–§7; the audit, replay the vacancy D-reducibility game; Long Table, apply the 1in geometry margin (the coordinator's decision)

## Rulings for the paper

1. **Fixed swap budgets.** The ledger stands, and `START-HERE.md` §6 was too broad; I have corrected it.
   - **Use in the paper:** "slides alone (k = 0) and one Kempe swap then slides (k = 1) fail at the frozen 21-vertex hole; whether a uniform fixed swap budget suffices for every colouring is open". Node `structural-swap-budget` stays `exploring`.
   - **Do not write:** "every fixed budget is killed".
2. **Five Colour: [compiled].** Its modules (`FiveColorTheorem`, `FiveColor`, `SphericalFiveColor`, `FiveColorSeparation`, `FiveColorExtension`, `FiveColorExamples`, test `PlaneMapFiveColor`) are in the 105-module audit manifest, which I checked. I corrected `f5-lean` to `compiled`; "proved" predates that status word.
   - **Scope:** graphs presented as a plane or spherical map.
   - **Test change:** the test's "never downgrade" guard now allows proved → compiled.
3. **The 4-connected core has order ≥ 12.** `MathVHCoreAdvance.md` item 5 (accepted by Math, 5 October 17:29) excludes orders 10 and 11, which supersedes Proposition 9's 11. The ledger and `START-HERE.md` agree.

**Euler lemma:** it is in the ledger as [hand] since revision 119; keep it.

**Changes since the ledger you used (117):**
- L4 and Theorem P are compiled **and audited**.
- The R\* reduction is `exploring`, not a theorem.
- P-B is closed into P-A.
- P-C is killed as stated.
- The Tilley locking route is killed.
- The D-reducibility results below are pending.

The claim-by-claim check runs on the full draft, before the user is asked to post.

## Vacancy D-reducibility (Math 12:43): [computed, exploratory, pending the audit]

- **Reducible:**
  - T4's 2-ball: depth 7, where the real radius is 4.
  - The icosahedral 2-ball: depth 3, a machine version of Theorem H.
- **Not reducible:** the pentakis (6⁵) 2-ball.
- **Soundness argument:** Math's hand reading only. The audit is asked for an independent implementation and an adversarial read.
- **Not shown:** that every ball type passes, or any unavoidable family.

## P-F (audit 13:05)

**Literature, corrected:**
- The mod-12 Kempe invariant is Mohar and Salas 2009 (J. Phys. A 42, 225204), Theorem 3.4.
- "All 4-colourings Kempe equivalent" is Mohar 2006; its page range is unverified.
- Fisk 1977 (Adv. Math. 24) is as cited by them; that it is the right Fisk paper is not verified.
- All three need three-colourable triangulations, which minimum-degree-5 graphs never are.

**Data** (orders 12–18, exploratory): only degree parity is a Kempe-class invariant.

## P1

The `--all` check had done 18,345 of 25,381 at 12:53. There is no result yet.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). The only status change is `f5-lean` proved → compiled, a relabel to the stronger word on audit evidence. No finite check is upgraded.
