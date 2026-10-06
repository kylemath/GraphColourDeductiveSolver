# Ring-connection automaton at (6,6,6,6,6) holes (MathSixFiveHole.md section 6, next step)

Math research worker, 6 October 2026. Labels: [hand], [computed], [open]. Compute: own Python (`auto.py`, `fix.py`, `fixJ.py`, `rankJ.py`, `real.py`, `real2.py`, `cmp.py`, `grow.py`, `climb.py` in the session scratchpad `auto/`, not committed) plus the previous worker's `six2` binary for bulk radius counts; about 9 CPU-minutes, one core. Nothing else edited, nothing committed.

## Verdict, first

1. **[computed] The section-9 automaton cannot give a bound R.** Abstract state = link colouring, 10-ring colouring, and for each of the three colour splits {p,q}|{r,s} a jointly non-crossing partition of the ring vertices into outside {p,q}- and {r,s}-joins. In this game the adversary (who picks unknown outside joins) has a **closed trap: 5,650 abstract nodes on 370 ball colourings, containing a lock-consistent start for every one of the 74 patterns**. So no number of steps is forced, for any R. All 370 trap colourings satisfy the Lemma 1 endpoint conditions, and in every trap node the lock of that node's split is present: the adversary simply keeps the state doubly locked.
2. **[computed] The trap is real information loss, not a bug.** Soundness check on all 2,338 real DL states at (6^5) holes of orders 22 and 23 (exact outside joins read off the graph): the abstract bound is never below the true radius. But 764 real states (696 of radius 2 and **68 of the 69 radius-3 states**) have all three of their actual splits inside the trap. Even with the exact outside structure at the start, the automaton cannot certify radius <= 3 for them. The reason is that after a swap the other two splits must be reset, because the swap recolours the outside part of the component.
3. **[computed] How many outside joins the trap needs.** If the adversary may use at most J outside joins per split: J <= 2 gives no trap, and every pattern is resolved within **7 steps** (game value 7; the patterns resolved by steps 2..7 are 18, 34, 52, 67, 72, 74). J = 3 traps 66 patterns and J = 4 traps all 74. Conditional only; no hypothesis on G is known that gives J <= 2.
4. **[computed, new] Radius 4 at a (6^5) hole.** I grew random min-degree-5 triangulations (vertex insertions plus edge flips away from N[v]) from the order-22/23 radius-3 graphs. There is an **order-28 triangulation (min degree 5, no separating triangle, sphere checked) with a (6,6,6,6,6) hole carrying a DL state of radius 4** (ring pattern dgdgdbabgb; radius histogram over 121 DL states: 117 of radius 2, 3 of radius 3, 1 of radius 4). Confirmed by `six2` and by my independent Python Kempe-graph BFS. So sup radius at (6^5) holes is >= 4, the same as the known overall value (T4). Hill-climbing from it (8 rounds of 150 mutants, up to order 34) found nothing above 4 and no unreachable (targetless) state.
5. **[computed] Obstruction realisation: not achieved.** An honest infinite trap would be a targetless state. None was found in about 2,200 grown (6^5) holes at orders 24 to 32, and none at orders <= 23. The abstract trap relies on the resets in item 2, and real graphs do not use them: 63 of the 69 radius-3 states at orders 22 and 23 have a geodesic whose first swap lies inside the ball, and such a swap leaves the whole outside unchanged.

## 1. The automaton [hand definitions, computed enumeration]

Ball = v, link x_0..x_4, ring w_0 m_1 w_1 m_2 w_2 m_3 w_3 m_4 w_4 m_0 (x_t ~ w_{t-1}, m_t, w_t). The outside region is a disc bounded by the ring; chords are outside edges.

- **Outside structure of a split [hand].** Fix a split S = {p,q}|{r,s}. Two outside paths, one coloured {p,q} and one {r,s}, are vertex-disjoint, so their ring endpoints cannot interleave. Two {p,q}-paths with interleaving ends meet, so their ends lie in one block. Hence the outside joins of S form a non-crossing partition of the ring vertices with blocks of one colour pair. Runs of consecutive ring vertices in the same pair are already joined along the ring. With 2m alternating arcs the number of structures is 1, 3, 12, 55, 273 for m = 1..5 [computed].
- **Cross-split constraints [hand].** Any pair from one split and any pair from another split share exactly one colour. So chains from different splits may cross at a shared-colour vertex, and planarity gives no pairwise constraint between splits. In particular the Jordan curve v x_1 P_1 x_3 ({b,g}) blocks only {a,d}-chains (same split as lock 1), and v x_1 P_2 x_4 ({b,d}) blocks only {a,g}-chains (same split as lock 2, which is the F split; this is exactly Theorem H Step 4). The phrase in MathSixFiveHole section 6, "only ring vertices on the same side of both curves can be joined outside by a {p,q}-path", is true only for {p,q} = {a,d} (by P_1) or {a,g} (by P_2). **The split {a,b}|{g,d} is not constrained by the locks at all.**
- **Transitions [hand].** A Kempe swap of a {p,q}-component K (ball part plus outside joins) leaves the outside structure of its own split unchanged (vertex sets of the {p,q}- and {r,s}-subgraphs do not change). The other two splits are unknown after the swap unless K contains no ring vertex. A link-only K changes no ring colour and no outside colour, so all three structures persist.
- **Game and decomposition [hand].** We pick swaps, the adversary picks unknown structures, and the target is a link with <= 3 colours. Because the three splits are independent, the value function splits as W_k = OR over splits T of g^k_T(c, S_T). The recursion is g^k_T(c,S) = filled(c) or g^{k-1}_T(c,S) or (some link-only move m has g^{k-1}_T(c_m, S)) or (some ring-touching T-move to c' has g^{k-1}_T(c',S), or for some other split T' every structure S' gives g^{k-1}_{T'}(c',S')). Initial: radius <= k for pattern c iff for some split T every lock-consistent S_T has g^k_T. This makes the full game a finite computation: 146,735 abstract nodes, 3,425 (colouring, split) groups.
- **Trap [computed].** Greatest fixpoint of "not winnable": 5,650 nodes. For every pattern and every split there is a lock-consistent start inside it. Depth-bounded runs agree: unresolved patterns at k = 1..5 are 74, 74, 74, 74, 74.

## 2. Real graphs against the automaton [computed]

Orders 22 and 23 (all min-degree-5 triangulations, `gen_tri`): 60 graphs with a (6^5) hole, 2,338 DL states. Radius 2 for 2,269 and 3 for 69 (agrees with MathSixFiveHole). Ring patterns: the same 69 as before. Table of (true radius, abstract bound from exact initial structures, which splits are trapped):

| true radius | abstract bound | states |
|---|---|---|
| 2 | 2 | 1,497 |
| 2 | 3 or 4 | 76 |
| 2 | none (all 3 splits trapped) | 696 |
| 3 | 3 | 1 |
| 3 | none | 68 |

**Erratum to MathSixFiveHole item 4 / section 3 [computed, from that worker's own `six` output and from my code].** The stated dichotomy "radius 2 iff some ball-contained component breaks the lock" is false in one direction. **282 radius-2 states (all at orders 22, 23) have no ball-contained breaker** (output lines `rad=2 ... nlocal=0`). Only these two hold: a ball-contained breaker implies radius 2, and no radius-3 state has a ball-contained breaker.

**Geodesics [computed].** Count of states with some first swap lying inside the 15 ball vertices on a shortest route: radius 2, 1,987 with / 282 without; radius 3, 63 with / 6 without.

## 3. The five unseen patterns [computed]

At order 24 (379 grown graphs, my analyser, same frame as the earlier worker's; the 69-pattern sets agree exactly at orders 22 and 23), **gadgdababd occurs, in 53 DL states**. The other four (gadbdabagb, gadbdabagd, gadgdabagb, gadgdabagd) are still unseen. In all four both locks must enter x_3 and x_4 through the same vertex w_3 = b, with P_1 leaving x_1 through w_0 = g and P_2 through w_1 = d. A Jordan exclusion of them is [open]. Caution: `six2` pattern strings are unreliable on my grown graphs, because their faces are not consistently oriented. Its radius and DL counts do not depend on orientation.

## 4. The radius-4 witness (order 28, hole v = 0) [computed]

Faces (vertex triples): 0 1 2, 0 2 3, 0 3 4, 0 4 5, 0 5 1, 1 2 6, 1 6 7, 1 7 8, 1 8 5, 2 3 9, 2 9 10, 2 10 6, 3 4 11, 3 11 12, 3 12 9, 4 5 13, 4 13 14, 4 14 11, 5 8 15, 5 15 13, 8 7 27, 16 7 27, 17 16 27, 7 6 18, 7 18 16, 6 10 18, 10 9 26, 18 10 24, 9 12 26, 12 23 25, 16 18 24, 19 17 23, 19 17 24, 17 20 21, 17 21 15, 20 23 25, 20 22 21, 12 11 25, 11 14 22, 15 21 13, 21 22 14, 21 14 13, 20 17 23, 23 12 26, 17 16 24, 19 10 24, 11 22 25, 22 20 25, 19 23 26, 19 10 26, 17 15 27, 15 8 27.
Degrees: 15 of degree 5, 11 of 6, one 7, one 8; 78 edges; every vertex link is a single cycle; no separating triangle. Link of 0 = 1,2,3,4,5, all of degree 6.

## 5. Killed lines

- **K-A1 "the planar-connectivity automaton on the 74 patterns bounds the radius".** Killed: closed adversary trap (item 1). The killing mechanism is the reset of the two splits not swapped.
- **K-A2 "the Jordan curves of P_1, P_2 restrict all outside two-colour joins".** Killed [hand]: they restrict only the {a,d}- and {a,g}-chains. The {a,b}|{g,d} split is free.
- **K-A3 "radius <= 3 at all (6^5) holes" (the data guess in MathSixFiveHole).** Killed [computed]: radius 4 at order 28.
- **K-A4 "radius 2 iff a ball-contained breaker".** Killed: 282 counterexamples (section 2).
- **K-A5 "the five unseen patterns are Jordan-excluded".** Killed for gadgdababd (realised at order 24). The other four are [open].

## 6. Ledger and what a working automaton would need

[hand]: outside structures are per-split non-crossing partitions; no pairwise cross-split constraint; the lock curves constrain only their own split; the W_k decomposition. [computed]: trap (5,650 nodes / 370 colourings / all 74 patterns); soundness and trap membership of the real states at orders 22 and 23; J <= 2 gives value 7; radius 4 at order 28; gadgdababd realised; erratum on the dichotomy. [open]: Jordan exclusion of the four unseen patterns; any bound R at (6^5) holes; existence of a targetless (6^5) state.
**Needed for a bound:** information that survives a swap. Candidates: (i) per ring vertex, which colours occur among its outside neighbours (an in-ball swap then leaves everything fixed); this is useless without degree bounds on the ring, since a high-degree ring vertex can see all colours. (ii) Joint realisability of the three splits by one outside colouring, which is not characterised here. Without such persistence, the per-split planar information provably (item 1) cannot bound the radius.
