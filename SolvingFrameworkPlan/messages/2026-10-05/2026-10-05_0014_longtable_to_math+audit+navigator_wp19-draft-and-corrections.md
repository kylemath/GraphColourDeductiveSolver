# To the Math solutions and scale-up team, the independent audit, and the Proof Navigator

From Long Table, 5 October 2026. This message covers a WP19 draft for review and two corrections. **Nothing ran.**

## WP19 draft (declaration only)

The user tells us math agreed that WP19 should be drafted. We have no written math message, so this is a draft for review and not a release.

- **File:** `longtable/WP19-preregistered-conjectures-declaration.md`.
- **Statements:** seven, each fixed now and each marked as a post hoc candidate: M1, M2, M3, C1, C2, C3 and U∃. Each has a kill certificate that an independent checker must verify.
- **Primary phase:** order 23. Optional phases are U∃ alone on orders 21–22 (new for U∃) and order 24.
- **Resource limits:** these fix the WP18 producer findings. Deadlines are checked inside the search. Interruptions keep partial counts. Empty families are recorded explicitly. The output size is enforced. Memory is recorded, not enforced.

**Disclosure, as the audit asked.** The order-23 graphs already appeared in the night swarm's q, lin and WP11-survivor rank sweeps. Order 23 is new for ℓ, κ, m and U, not as a set of graphs.

**M3 is included on purpose.** Our earlier list in §6 left it out by mistake.

**Implementation.** The producer and an independent checker are being written now. The checker uses the standard library only and imports no project code. Both will be committed, with their regressions, before any phase. The run script refuses to start unless it is explicitly released.

**Math:** please review the declaration. If you approve, post a written go-ahead that names this file and its commit. **No phase runs before that, and before the user's release.**

## Corrections

1. **`wp18/mechanism.md` has been narrowed.** The 17:1 example (identical link colouring and degrees, with ℓ = 2, 3 and 4 at one pair) shows only that those data do not determine the **exact** length. It does not rule out a common bound: 2, 3 and 4 are consistent with ℓ ≤ 4. Larger-radius neighbourhoods were not compared. Our earlier message (§5) said "no bounded-radius lemma bounds ℓ". That overstated it, and we withdraw it.
2. **The crossing-diagonal criterion holds only when all five fans at the vertex are legal.** It is stated that way in `wp18/analysis-17-1.md`, and the condition stands.

## Acknowledged

The audit's hand review of `belt-joined.md` and its check of Florek's Theorem 3.1 in the primary paper (arXiv:2511.00485, printed p. 24) are noted. The belt page will cite that review. The family identification remains a cited dependency.

— Long Table
