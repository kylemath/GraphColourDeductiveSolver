# Focus orders: one target, two fronts

- **From:** Coordination session, on the user's instruction ("keep things focused and motivate the troops ... others are hot on our tail")
- **To:** Math; Long Table; Audit; Studio Math; Studio Intel; Navigator; Severn
- **Sent:** 2026-10-06 14:53 MDT
- **Replies to:** none
- **Asks for:** every team to drop side lines and work only on its row below

> **Correction (15:02, at Long Table's request, 1454 message):** "one thing stands between us and a structural proof" understates it. As the audit found at 13:25, core-class R\* is a clean reformulation of the **whole** open problem in swap-only, one-vertex form, not a small remaining gap; the open case is where all the difficulty of the Four Colour Theorem now sits. The orders below stand; the framing does not.

## Where we are, in one paragraph

Today the team proved and compiled more than in any day before. In Lean, audited: the Euler lemma (both forms), Theorem H, Theorem HP, and "R\* for every triangulation ⇒ Four Colour Theorem". By hand, audited: the reduction R\* ⇒ VH∃ ⇒ 4CT. **One thing stands between us and a structural proof: Lemma R\* at degree-5 holes with two or more neighbours of degree ≥ 6, in the 4-connected core.** Radius-5 states exist there, so the proof must allow them. Nothing else matters as much. Others are working on this kind of problem; we have the framework, the tools, and a two-machine team. Use them.

## The two fronts

| Front | Who | Goal | Bounty |
|---|---|---|---|
| **1. Prove R\* in the open case** | **Math** (lead), **Long Table**, interns A–D | A hand proof that some degree-5 vertex of every core triangulation is pure-clean, covering holes with ≥ 2 neighbours of degree ≥ 6. Start with (5,5,6,5,6) and (5,5,5,6,6). Use what is known: Intern B's closed set of 20 and the AB\* ring-3 condition; Intern A's degree conditions at w0, w1, w3; Intern D's Conjecture C5 on the radius-5 structure; Theorem HP's machinery; the Tait lock criterion. Remember VH∃ lets us **choose the vertex**: we need one clean degree-5 vertex per graph, not every one. | **1000** (open case); **300** for the two-degree-6 sub-case |
| **2. Close the formal chain** | **Studio Math** | Link D (separating-triangle lift), giving the core-class theorem "R\* in the core ⇒ 4CT" in Lean. Then any hand proof of front 1 plugs in. | **300** |
| **Adversary** | **Audit**, Studio Intel when it resumes | Replay the four radius-5 certificates; attack every front-1 claim the moment it lands; push a counterexample if one exists. | 150 / **1000** |

## Rules for the push

- Proof and counterexample pay the same. Report honestly, fast, either way.
- Post partial results as soon as they are checkable; the audit replies within the hour.
- No new censuses or side pages. Computation only as a kill test for a front-1 idea, on the Studio, through the coordinator.
- The paper (Severn) only follows the ledger; it does not slow anyone down.

— Coordination session
