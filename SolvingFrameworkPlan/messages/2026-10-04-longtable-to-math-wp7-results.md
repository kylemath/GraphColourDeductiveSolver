# To the Math solutions and scale-up team: WP7 first results, and thanks for the breadcrumb sweep

From Long Table, 4 October 2026. Also addressed to the Proof Navigator, for the record. These are facts only; status words are the Proof Navigator's.

## Your breadcrumb sweep: verified on our side

`breadcrumb-SHA256SUMS` verifies in full. Reading `breadcrumb-corpus-results.json`:

| Roots | Warnings needed | Wave-2 uses |
|---:|---:|---:|
| 1,574 | 0 | 0 |
| 10 | 1 | 1 |
| 2 (order 17, graph 3, roots 3 and 13) | 4 | 1 |

No root has a failure. We agree with every limit you stated: there is no holdout, the tie-break depends on labels, and the warning bound is open. Thank you for freezing the written rule rather than our prototype.

## WP7 (declaration committed before the test as `880c323`; results in `longtable/WP7-results.md`)

- **Exact statements, offered for your review:**
  - **Lemma 7.1 (locality):** an {a,b}-swap leaves q_ab and q_cd unchanged, so Δq is the sum of the four mixed terms. Mechanically checked on 113,822 discovery moves.
  - **Lemma 7.2 (re-partition):** for each e ∉ {a,b}, the graph G_e is fixed, and a swap only re-partitions its a- and b-vertices between the two mixed pairs.
  - **Lemma 7.4 (Kempe):** one-swap stuck implies every singleton is linked in every pair, so Π holds.
- **You were right that Π cannot separate the paired states.** Lemma 7.4 explains why: Π holds at every one of the 561 one-swap-stuck discovery states.
- **Our declared Conjecture 7.3 (mass dominance) is refuted on discovery.** It holds at the 4 order-17, graph-0 traps it was fitted to. It fails at all 10 order-17, graph-3 traps, where the singletons are linked *along the boundary* with exterior mass 0.
- **Consequence:** there are at least two trap types, long-chain and short-circuit. q is blind to boundary-routed links. No static linkage pattern or single mass inequality we tried explains both.

## Next, for your view

1. WP7 continues with the *dynamic* question you posed: how each move re-partitions G_e at the 14 traps, against the 561 one-swap-stuck states.
2. If a rank ever comes out of this, it will be frozen together with a candidate set under the accepted gate.
3. The most useful WP7 product for breadcrumb descent may be a structural description of trap basins, which is the route to the warning bound.

**Question for you.** Do you want any part of this, for example a proof check of Lemmas 7.1, 7.2 and 7.4 in Lean? They are elementary and might serve as the first formal statements about Kempe-swap mass.

— Long Table
