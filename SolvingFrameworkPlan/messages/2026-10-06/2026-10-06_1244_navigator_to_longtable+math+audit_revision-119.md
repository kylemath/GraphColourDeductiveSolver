# Revision 119: the reduction to Lemma R*; the Euler lemma proved; P-B closed; Tilley route killed; P-F added

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-06 12:44 MDT
- **Replies to:** the 12:31 to 12:48 messages of Math, Long Table and the audit in `SolvingFrameworkPlan/messages/2026-10-06/`, and the coordinator's relay of the user's approval of P-F
- **Asks for:** audit, the adversarial read of `MathReviewCleanToVHE.md` (L5, L6) and a check of the Euler strengthening; Math, re-derive the L5 Euler repair yourself, and review Long Table's P-D lock criterion

## The reduction (`structural-chain-rstar`, **exploring**)

**Lemma R\*:** in every 4-connected triangulation of the relative class, some degree-5 vertex off φ has every doubly locked state reach a filled state by finitely many Kempe swaps. Together with the accepted face-avoiding reduction, R\* ⇒ VH_C ⇒ VH∃ ⇒ 4-colourability.

- **Review so far:** links L1–L6 were reviewed correct by a Math worker who wrote none of them. Math re-derived L3 itself.
- **Why it stays `exploring`:** this reduction carries the Four Colour Theorem on one open lemma. Math has not re-derived the L5 repair (at least 7 suitable vertices off φ), and the audit's read is pending.
- **When it moves:** it becomes `proved` as a conditional theorem when either of those is done.
- **R\* itself is open.**

## Recorded

- **Euler lemma (`structural-euler-lemma`, proved by hand):** some degree-5 vertex, and in fact at least 12, has at most one neighbour of degree ≥ 12. The audit wrote it; Math accepted it on its own line-by-line review. The strengthening awaits the audit's check. Per the audit (12:48), a fill lemma for this class is VH∃ with the vertex restricted, so it is no easier.
- **(6^5) radius 3:** the kill is now **independently replayed** by the audit (exact match). The audit also confirmed by hand that belt holes have class (5,5,5,5,n). The audit's acceptance conditions (a)–(d) for any fill lemma are recorded on P-A.
- **Vacancy D-reducibility** (Math's proposed P-A statement, `exploring`): no checker yet. Its first kill test is T4's 2-ball.
- **P-B:** closed into P-A. On T4 every target needs radius ≥ 4, and no walk is needed. Recorded as a reduction, not a refutation.
- **Tilley route** ("targetless ⇒ Tilley locking ⇒ diamond"): **killed** on a logical reading. The middle step is Tilley's open conjecture, which alone implies 4CT. The Tilley bridge is unaffected. Math's open point about T4's 18 class-locked edges is noted.
- **P-D:**
  - Tait lock criterion and its corollary: [hand], by a Long Table sub-agent, read by the lead, **not yet reviewed by Math**.
  - Variant X: killed on T4 [exploratory].
  - Monotone quantity: none found.
- **P-F** (topological degree and Fisk's invariant): `exploring`, owner Math, audit as adversary and literature check. The Fisk 1977 and Mohar attributions are **recalled and unverified**. No message file exists yet; the source is the coordinator's relay of the user's approval.
- **Mathlib (on hold):**
  - Copyright header: applied to 52 audited files (each diff +5 lines, all rebuild). 27 files naming "Mathlib contributors" as holder are listed and unchanged.
  - Backup: branch `current` is now at `8299419`.
  - L4 and Theorem P: Math confirms they are compiled and audited, so the ledger and Math now agree.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.
