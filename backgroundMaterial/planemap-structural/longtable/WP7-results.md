# WP7 results: chain sizes and overlap

Long Table, 4 October 2026. This follows [WP7-declaration.md](WP7-declaration.md), which was committed before the test (`880c323`). The run is `wp7_test.py`, which writes `wp7-discovery.json`, on orders 12–18 only. Orders 19–20 remain untouched. These are facts, not status claims.

## Exact statements

**Lemma 7.1 (locality).** A swap on an {a,b}-component leaves q_ab and q_cd unchanged, so Δq is the sum of the four mixed terms. The proof sketch is in the declaration. It was also checked mechanically on all 113,822 moves from non-target states in the discovery range, with no exceptions.

**Lemma 7.2 (re-partition).** For each e ∉ {a,b}, the swap leaves the graph G_e unchanged and only re-partitions its a- and b-vertices between the {a,e} and {b,e} subgraphs. See the declaration for the proof sketch.

**Lemma 7.4 (classical; one-swap stuck implies full lock).** If some singleton v on B and some colour z ≠ c(v) have v's {c(v), z}-component meeting B only at v, then swapping that component removes c(v) from B. That reaches a target, which lowers R, since p drops from 1 to 0 and 6n² + 1 > q.

So a state with no one-swap decrease has every singleton linked in every pair: L = 9 in report 3's notation. In particular Π holds. This is Kempe's own argument.

Observed in the discovery range:
- Π holds at all 561 one-swap-stuck states and all 14 two-swap-stuck states, as Lemma 7.4 requires.
- Π also holds at 1,725 states that descend in one swap.

## Conjecture 7.3: refuted

The declared conjecture was: two-swap stuck ⟹ Π and m_sing > m_rep.

| Discovery states (non-target) | Predicate holds | Predicate fails |
|---|---:|---:|
| Two-swap stuck | 4 | **10** |
| One-swap stuck only | 44 | 517 |
| Descends in one swap | 376 | 10,763 |

- **All 10 violations are at order 17, graph 3** (roots 3 and 13, five trap states each), the trap set that did not shape the conjecture.
- **There, Π holds but the minimum exterior mass over singleton-linking chains is 0** *[erratum, 4 October: an earlier version said every such chain has exterior mass 0; the implemented statistic is `min(link_mass)`. With boundary pattern A,B,A,C,D under full singleton lock, the B–C and B–D chains each need at least two exterior vertices, and only the remaining singleton pair can connect along the boundary. One short link is not all links short. This does not revive 7.3. Found by the math team's review.]*. The singletons are joined directly along the boundary cycle, while the largest repeated-colour chain has exterior mass 3. The 4 traps that satisfy the predicate are the order-17, graph-0 traps it was fitted to.

So 7.3 fails as a necessary condition. It is also unspecific: 376 states that descend in one swap satisfy it.

## What this says about the trap

- **There are at least two kinds of trap in the discovery range:**
  - **Long-chain traps** (order 17, graph 0): each singleton pair is linked by a heavy exterior chain, and every repeated-colour swap merges mass into the other repeated-colour pairs.
  - **Short-circuit traps** (order 17, graph 3): the singletons are linked through the boundary itself, so q sees almost no mass in the singleton pairs at all.
- **No linkage pattern can separate traps from ordinary stuck states.** Lemma 7.4 forces the full lock at every one-swap-stuck state. The paired fixture also shows that equal linkage with different sizes can go either way.
- **No single inequality on chain masses does it either**, judging by the two trap types. A size-based explanation would have to treat boundary-routed links differently from exterior links. Under the q formula, that is exactly the distinction being lost: a link through the boundary contributes 0.

## Suggested next steps (for joint decision)

1. **WP7 continues on Lemma 7.2.** Rather than a static predicate, describe the *re-partition* of each G_e under each move at the 14 traps against the 561 one-swap-stuck states. This asks why every re-partition merges. It is the dynamic version of the question the math team posed.
2. **For rank design (WP8, conditional).** Short-circuit traps suggest q undercounts links that run along the boundary. Any new rank would need to weigh them explicitly. It must be declared and frozen with a candidate set before testing, under the accepted gate.
3. **Breadcrumb descent** already passes every root in the corpus (the math team's sweep). WP7's best contribution to it may be a reason why warnings stay few: both trap types are isolated states or small basins (at most 4 warnings). A structural description of trap basins is the route to the warning bound.
