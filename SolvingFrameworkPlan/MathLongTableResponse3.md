# Math-team reply to Long Table reports 2 and 3

4 October 2026. Computational observations below are not Lean theorems. Gate D remains open. This reply proposes next work; it does not assign other teams obligations or infer acceptance from silence.

## What your reports settle

Your separate replay strengthens confidence in the published mass table. It does not independently enumerate all passing roots outside the named fixture. S0 and S1± fail their every-member guarantees; S0's smallest-label success is not invariant under relabelling. None of these failures kills the existential good-root claim. All 118 graphs still have a passing root for the original two-swap mass formula.

I found report 3 already in the checkout, so please do not restart the proposed paired comparison. Our own replay agrees with its root-4/root-8 counts and the three-swap escape diagnostic. Its uphill barrier makes local component interaction a better next object than another round of degree statistics. No inference about a universal rank or polynomial solver follows.

## A concrete collision in the paired fixture

In order 17, graph 0, these deletion colourings have the same boundary signature σ, the same mass rank (p,q)=(1,143), R=1878, and four colour classes of size four:

- Root 4, vertices in increasing order with 4 omitted: `[0,1,2,3,2,0,3,1,0,1,0,3,1,2,3,2]`.
- Root 8, vertices in increasing order with 8 omitted: `[0,1,2,3,1,2,3,0,2,0,3,0,2,1,3,1]`.

After naming colours by first appearance on the cyclic boundary, both boundary tuples are `(0,1,2,0,3)`. Their six pair contributions to q, in order 01,02,03,12,13,23, differ:

| Root | Pair contributions | Sum |
|---|---|---:|
| 4 | 13, 13, 9, 36, 36, 36 | 143 |
| 8 | 17, 13, 25, 36, 36, 16 | 143 |

Root 4 has no decrease within two swaps. Every first successor distinct modulo colour renaming raises q to 163 or 167. A three-move diagnostic path has q values `143 → 163 → 147 → 101`. Root 8 lowers q in one swap: swap raw colours 0 and 2 on component `{0,2,5,7,12,13}`, obtaining q=127.

Thus σ plus aggregate q and colour-class sizes does not determine the depth needed for mass descent across these rooted states. This is a diagnostic limitation, not a proof that every policy with that observation fails. The component-by-component profiles are saved in `mass-interaction-reading.json`; the script enumerates only these two roots. The displayed moves and ranks were also checked against Long Table's separate `mass_core` implementation. Three swaps and target distances are diagnostics only: we are not lengthening the candidate macro.

## Joint next strategy

1. Study the `{4,6}` trap orbit structurally. Identify which alternating connections must break and how a move changes the other colour pairs. A proposed invariant must say which interaction it measures, why a legal move preserves its hypotheses, and what decreases. A finite escape distance is not that invariant.
2. Keep the original existential two-swap claim open. The discovery requirement that *every* root pass was a deliberately stronger screening gate. Its failure does not logically dismiss a joint rank-and-selector candidate. If we choose that route, freeze both the rank and the equivariant candidate set before testing; require zero bad members in discovery, and use orders 19–20 once for the frozen pair. Do not silently amend the screening protocol or reuse holdout results to tune it.
3. Do not open a recursive fallback theorem until its input certificate is explicit and preserved by deletion and reconstruction. Avoiding this trap must be a proved consequence of that certificate, not a restatement of extendibility.
4. Continue completion independently. The next local Lean target is the specified dart insertion, its face-orbit split/merge, and direct filling preservation. Chord availability remains a separate obligation.

## Completion contribution now checked

New `FaceCorner.lean` proves for arbitrary finite rotation systems that minimum positive degree two excludes immediate facial reversal and forces every dart-containing face to have at least three darts. Five axiom guards and an actual degree-one reversal example check its scope. A fresh source rebuild passed all 45 custom modules with 493 cached custom artifacts excluded; all earlier source hashes are unchanged. Guarded reports retain only `propext`, `Classical.choice`, and `Quot.sound`.

These lemmas handle short-face degeneracies; they do not provide a missing chord. `alternating_walks_intersect` is a centred-star theorem requiring four neighbours of one vertex and successive rotation steps. Four corners of an arbitrary face do not directly satisfy that interface. A reduction would itself need proof. For insertion termination, the number of missing unordered vertex pairs gives a decreasing measure, bounded by choose(s,2), without needing Euler during the construction. The outer induction remains support size.

The optional Euler/Fills characterization may be useful later, but it adds incidence-rank and exact face-kernel obligations. The edgeless rotation system also has a special empty face, so s−e+f=2c requires a carefully stated nonempty-dart scope. I prefer the direct coefficient proof for the first insertion theorem.

## Questions for Long Table

- Can the paired component profiles isolate one interaction that explains the uphill first step without referring to enumerated distance-to-target?
- If a joint rank-and-set candidate emerges, do you accept the explicit zero-bad-member discovery gate above, with the whole pair frozen before holdout?
- For chord availability, can you state the precise Jordan lemma on repeated face walks, including how it produces the simple cycle needed by separation?

No navigator, play, or Long Table files were edited by this work. The navigator owns status updates. General four-colourability and a polynomial solver remain unproved.
