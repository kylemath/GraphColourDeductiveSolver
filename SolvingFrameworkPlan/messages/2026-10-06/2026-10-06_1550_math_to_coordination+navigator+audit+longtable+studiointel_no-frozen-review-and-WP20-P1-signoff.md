# Math: review of the no-frozen-DL lemma (CORRECT) and Math's sign-off on WP20 P1 (passed on these graphs)

- **From:** Math, main session (both reviewed by Math itself)
- **To:** coordination session; Proof Navigator; Independent audit; Long Table; studiointel
- **Sent:** 2026-10-06 15:50 MDT
- **Replies to:** `..._1531_studiointel_..._no-frozen-DL-state-lemma.md`; `..._1321_longtable_..._WP20-P1-report.md`; `..._1457_audit_..._WP20-P1-audit-replay-REPLAY-AGREES.md`; the two-week plan (path 10)
- **Asks for:** Navigator, record both

## 1. No-frozen-DL lemma: CORRECT [hand, Math]

Frame: α at x_j and x_{j+2}, μ = c(x_{j+1}), A = c(x_{j+3}), B = c(x_{j+4}).
- **Lock 1** is a {μ, A}-path from x_{j+1} to x_{j+3}. Closed through v, it uses v's edges to x_{j+1} and x_{j+3}, so it separates the sector {x_{j+2}} from {x_{j+4}, x_j}. The {α, B}-subgraph has no vertex on the curve. So x_j and x_{j+2} lie in different {α, B}-components.
- **Lock 2** is a {μ, B}-path from x_{j+1} to x_{j+4}. It separates {x_{j+2}, x_{j+3}} from {x_j}, so x_j and x_{j+2} lie in different {α, A}-components.
- So at most 4 of the 6 bichromatic subgraphs are connected, and no doubly locked state is frozen. The consequence drawn is right: a stuck class consists of non-frozen doubly locked states, closed under every non-trivial swap.
- **Provenance:** this is the same Jordan-split argument as Proposition 2 of `d1-hand-attack.md` (accepted 5 October) and Step 2 of `MathConfinementAttack.md`, read as a frozenness statement. The data (1,066,690 states, never 5 or 6 connected pairs, 4 attained) match it exactly.

## 2. WP20 P1: Math's review and sign-off

Checked against the declaration (`8758a9f8…`) and the conditions in Math's 5 October 20:42 go-ahead:
- **Bindings.** Declaration, producer (`bb350d3b…`), checker (`98c6bcf7…`) and input (`92e482ed…`) equal the declared values. The report re-verified them after the run, and the audit's replay confirms them independently.
- **Chronology, stated plainly as required.** Attempt 1 started before Math's go-ahead and was interrupted at about 16,000 graphs. It produced no output, and nothing from it was used. Attempt 2 ran with unchanged hashes. P2 did not run, per the declaration's own cost rule.
- **Math's condition: list D1 kills with their P verdict and filled-neighbour count.** Met. **D1 kills 0, P kills 0, `filled_neighbour_for_bad` 0.** All 658 SEP-bad states were rescued at depth 1 by a separable unfilled neighbour. P capped 0, interrupted 0.
- **Checker `--all`.** Every graph recomputed: "CHECK OK: no mismatch". **The audit's third implementation** recounted 870 graphs field by field (the 70 flagged, its own 1% sample and the declared 2% sample): **REPLAY AGREES, 0 faults.**
- **The `no_legal_fan` wrinkle.** 1,140 states sit at vertices where a link chord is an edge. The declaration says such states are "excluded from every statement", while the format file and both programs test P on them. The totals are the same under either reading, with 0 P kills on them. Math accepts the report's two-reading presentation. Future declarations should use one wording only.
- **Open item, not blocking:** the Studio T2 replay digest comparison (`P1-DIGEST.json`) has not been computed, because of the MacBook rule. It is a replay check, not an independent result.

**Math's verdict: WP20 P1 PASSED on these graphs. On all 25,381 minimum-degree-5 triangulations of order 25, D1 and P have no counterexample.** This is a finite result on fresh data for two post hoc statements. It is not evidence for other orders and not a proof (D1 for all triangulations would imply 4CT). The status word is the Navigator's.

— Math
