# Pathway P-B: walk the hole to a good place (Long Table, 6 Oct 2026, exploratory)

Labels: [hand] = reasoned by hand; [exploratory] = small code, exact on the named graphs only, no evidence for any theorem. Scripts/outputs: `backgroundMaterial/planemap-structural/longtable/explore-vhphi/pathways/pb_*` (stdlib, own code: `pb_lib.py` vacancy game on adjacency only; `pb_struct.py`, `pb_walk.py`, `pb_trace.py`, `pb_hi.py`, `pb_greedy.py`, each with a `.out`). Total CPU about 5 s, one process, orders 14, 17, 42 (42 structural only).

## Claim
For every core triangulation some degree-5 vertex v has a path v = h0, h1, ..., hk through degree-5 vertices with hk "good" (a neighbour of degree <= 4, or all five neighbours of degree 5), so mobility carries any start there and the good-class bound fills.

## Why it might hold, and the first observation [hand]
Mobility (compiled) moves a degree-5 hole to a chosen neighbour in <= 1 swap + 1 slide, or fills. It needs the CURRENT hole to have degree 5, so a walk lives inside the subgraph D5 induced by degree-5 vertices. Along a fixed path in D5 there is nothing to cycle: the hole sequence is a fixed path, length = graph distance. This is exactly the "degree-five region consequence" of `MathMobilityShortFillBridge.md` (for the degree-<=4 class). So the "strictly decreasing quantity" is only graph distance in D5 to a good vertex, and P-B collapses to a graph-theoretic existence statement: some component of D5 contains a good vertex. In a core triangulation (min degree >= 5) the first good class is empty, so only icosahedral vertices (Theorem H, radius <= 3) count.

## Hand examples [exploratory for every number; the structural reading is [hand]]
- A_3 (17 vertices): D5 has two components, {pole + ring 0} and {ring 2 + cap}, and each pole is icosahedral. So from any degree-5 hole the walk is <= 1 step. But the walk goes to a WORSE place: max pure Kempe radius is 2 at the ten ring holes and 3 at the two poles (`pb_hi.out`). On the period-60 witness (rings 01023|23101|02323, cap 1, `pb_trace.out`) the pole has R = 3; mobility to ring vertex 1, 3 or 4 is a bare slide and lands at R = 2, to vertices 0 or 2 is swap+slide and lands at R = 1. So even here the target class is not the best place; Theorem H is a bound, not an optimum.
- T4 (one flip from A_3; 17 vertices, hole 4 has radius 4): D5 is ONE component of 12 vertices, but it has NO icosahedral vertex (and no degree <= 4): the single flip destroys both poles (`pb_struct.out`). So the walk is possible everywhere and has no target. Max pure radius is 4 at all 12 holes (`pb_hi.out`): no hole is a "good place" even by radius. From the radius-4 state at hole 4 (link word 0,1,3,2,3) the pure fill takes 4 swaps; a hole walk (`pb_greedy.out`) goes 4 -> 0 -> 3 -> 7: swap{1,3}+slide, swap{1,2}+slide, swap{2,3}+slide, i.e. 3 hole-moves = up to 6 elementary moves, worse than the 4 pure swaps (the full vacancy game's shortest path is 4, `pb_trace.out`; it is 3 for only 8 of the 26 radius-4 pairs).

## Candidate decreasing quantities
1. Distance in D5 to a good vertex: decreases trivially, but a target exists only if D5 has an icosahedral vertex. DEAD as a general rule: T4 (order 17), the order-14 bicapped hexagonal antiprism (D5 connected, 12 vertices, no icosahedral vertex) and the 42-vertex Goldberg-Coxeter (2,0) icosahedron (D5 = 12 isolated vertices: after one step the hole sits on a degree-6 vertex, where no mobility is compiled). Smallest stuck example found: order 14 [exploratory; not a census, I did not search below it].
2. Pure radius R of the current state as the potential: [exploratory] on T4 and A_3, every state at a degree-5 hole with R >= 2 has a hole-move (swap+slide or slide, to a degree-5 neighbour) with strictly smaller R, and the R-greedy walk from all 26 radius-4 pairs on T4 never cycles and ends in <= 4 hole-moves. This survived but is circular: R already falls by one pure swap, so it adds no information, and the choice rule depends on the colouring (14 of the 26 radius-4 (hole,state) pairs of `pb_hi.out` have successors of radius only 3 or 4 on the first step). R = 1 states stay R >= 1 under hole-moves (a final swap is needed), which is not a stuck case.
3. Locked-class count, number of degree-5 neighbours, colour-class sizes: not run; after finding 1 and 2 no colouring-independent quantity looked usable [hand, untested].

## Kill test and consistency check [exploratory]
`pb_walk.py`: all 12 degree-5 holes x all canonical states x every degree-5 neighbour, T4 and A_3: 1576 + 1800 unfilled pairs, 0 mobility failures (kinds slide / swap+slide / swap-fills), consistent with the compiled mobility theorem on these two graphs only. Mixed game over all holes, all 1296 (T4) and 1650 (A_3) states: unreached = 0; (pure radius, mixed distance) differ only at 8 T4 states (4 vs 3).

## Coordinator's extra input: walk toward a (6,6,6,6,6) or (5,5,5,5,5) hole (Math's class table, `MathPathwaysPAPC.md`)
[hand] A (6^5) hole has no degree-5 neighbour by definition, so it is an isolated vertex of D5: a mobility walk (which only passes through degree-5 holes) can never ARRIVE at one from another degree-5 hole, and from it the first step lands on a degree-6 hole where no mobility is compiled. So nothing can decrease along such a walk; the walk is not even defined. Toward (5^5): that is the icosahedral class already treated (needs D5 to contain it; T4 and order 14 do not). To reach (6^5) one needs a degree-6 mobility step, i.e. variant (a) below, plus a distance quantity through degree-6 vertices that nobody has.
[exploratory] `pb_class.py`/`pb_class.out`: link classes of deg-5 holes: T4 {(5,5,5,5,6):2, (5,5,5,6,6):8, (5,5,6,6,6):2}, hence NO (5^5) and NO (6^5) hole, and Math's table puts the first two classes at max radius 4 (consistent with the all-4 holes of `pb_hi.out`); A_3 {(5,5,5,6,6):10, (5^5):2}; order 14 {(5,5,5,5,6):12}; order 42 {(6^5):12}. So on T4 and order 14 the "easy" classes (max radius <= 3) are absent altogether, and no walk target exists, whatever the walk rule.
Consequence: the target classes are not unavoidable (Math, pentakis; here also T4), so P-B needs a target among the radius-4 classes, i.e. it is no easier than Conjecture R on those.

## Not checked
No colouring walks on the order-42 or order-14 graphs beyond structure (order 14 radius table only); no proof of mobility; hand verification of each swap in the traces was NOT done (code only); no degree-6 mobility; no other graphs.

## Verdict: MUTATED (the walk as stated is a fixed path and cannot cycle; what is dead is the target)
The walk is sound where D5 meets a good vertex, but that is a graph condition that fails on T4, order 14 and isolated-pentagon graphs. Next variants: (a) P-B': extend mobility to a degree-6 hole under a local hypothesis (a singleton neighbour colour) so the walk can cross degree-6 vertices; (b) P-B'': enlarge the good class to mixed link types (e.g. five-ring with one or two degree-6 neighbours) proved by a Theorem-H style hand argument, with T4 holes as the test (all have max radius 4, so the bound for such classes is at least 4 on these graphs); (c) fold into P-A: the discharging must produce a vertex in a class that is non-empty in T4.

## Update (6 Oct, afternoon)
Long Table research subagent, `date` = Tue 6 Oct 2026 12:35 MDT (machine clock). New scripts and outputs only: `explore-vhphi/pathways/pb2_lib.py`, `pb2_mob6.py`, `pb2_walk6.py`, `pb2_two.py`, `pb2_belt.py`, each with a `.out` file. Own code, stdlib, one process, about 53 CPU-seconds in total. Every number is [exploratory, these graphs only]: exact over all canonical states on T4 (order 17), order 14 (= belt G_6) and A_3, and on the belts G_5..G_14 (one belt hole and the pole). The pentakis dodecahedron (order 32; all 12 degree-5 holes are (6^5)) is SAMPLED only: up to 150 distinct states per hole from a random Kempe walk.

**Definition.** k-mobility at a hole h of degree d: for every state and every chosen neighbour y, at most k Kempe swaps in G-h make y's colour a singleton on N(h). The hole then moves by giving h that colour and uncolouring y. A fill met on the way also counts.

### Line A: degree-6 mobility. Verdict: it works almost always, but there is still no target, and on T4 no target exists at all
- [hand] A move with 0 swaps works exactly when y's colour is already a singleton on the link. Every failure needs y's colour at least twice on the 6-cycle link.
- **T4, holes of degree 6.** There are 2412 unfilled (state, neighbour) pairs. With at most 1 swap: 2086 succeed (842 bare moves, 514 after one swap, 730 one-swap fills). With 2 swaps: 302 more. **24 fail even with 2 swaps (1.0%).** So 1-mobility and 2-mobility both fail at degree 6.
  - The 24 failures sit at holes 2, 8, 9, 10 and 11, in states of pure radius 3, 4 or 5.
  - Their link patterns (y first, a = y's colour): abacdc, abacbd, abacad, ababcd, abcacd. So y's colour occurs 2 or 3 times on the link.
  - Order 14, A_3 and the pentakis sample have **0** failures with at most 2 swaps.
  - At degree-5 holes (T4, A_3, order 14) every pair succeeds with at most 1 swap, consistent with compiled mobility.
- **Radius by hole on T4.** The maximum pure radius per hole is 4 at all 12 degree-5 holes. At the 5 degree-6 holes it is **3, 3, 4, 4, 5** (holes 2 and 11, 10 and 8, 9). **No hole of T4, of either degree, has maximum radius at most 2.**
- **Walk with degree-6 moves allowed.** One hole-move is at most 1 swap followed by a slide to any neighbour. Start from each of T4's 26 radius-4 states.
  - With degree-5 moves only: 12 states reach radius <= 2 in 1 hole-move and 14 need 2.
  - With degree-5 and degree-6 moves: 24 states need 1 hole-move and 2 need 2. The radius-greedy walk never cycles.
  - But one hole-move costs up to 2 elementary moves, so 1 hole-move plus radius 2 is still at most 4. No elementary gain. The earlier finding stands: mixed-game distance differs from pure radius at only 8 T4 states, and there by 1.
- **Decreasing quantity: none found apart from R itself (circular).**
- **Precise obstruction to any colouring-independent target on T4.** Every hole of T4 has maximum radius >= 3. Any target class that meets T4 therefore carries a bound of at least 3. A walk to it costs >= 1 move, so it never beats the direct radius of 4. Degree-6 holes are no refuge: the worst hole of T4 is the degree-6 hole 9, at radius 5.

### Line B: Wernicke two-hole game. Verdict: the choice helps every radius-4 state, but the worst case is still 4
- **Game.** Both ends of a 5-5 or 5-6 edge are uncoloured. Moves are Kempe swaps in G-{u,v}. Filling either end with a free colour is free, after which the exact one-hole radius of the other end is paid. d2 = least number of swaps to a full colouring.
- **Maximum d2.** T4: **4** (44 two-hole states have d2 = 4: 32 at 5-5 edges and 12 at 5-6 edges). Order 14: 2. A_3: 3. So the worst case equals the one-hole worst case on all three graphs.
- **Uncolouring a partner of a one-hole state** (an added move: the vacancy game has no uncolour move). Refilling the partner with its old colour is one option, so d2 <= R always.
  - On T4, each of the 26 radius-4 states improves when the best Wernicke partner is uncoloured: **8 reach d2 = 2 and 18 reach d2 = 3. None stays at 4.**
  - Over all degree-5 states the gain is at most 2.
  - Which end to fill first: filling the degree-5 end first is optimal in most states (T4: 2990 of 4582 two-hole states). Swaps before any fill are needed in 120 + 600 states, counting those where neither end can be filled at the start.
- **Reading.**
  - [exploratory] On T4, the d2 = 4 two-hole states are exactly the uncolourings of one-hole states of radius >= 4 at an unlucky partner. They come from the pairs (R, d2) = (4, 4) and (5, 4); no one-hole state of radius <= 3 maps to d2 = 4.
  - So whether the two-hole game helps depends on choosing the partner from the colouring. That choice is not colouring-independent, the same defect as R-greedy.
  - [hand] The gain comes from the extra uncolour move, which changes the game. It is not a target for the vacancy game itself.

### Coordinator input: the audit's 12:40 lemma class (a degree-5 hole with at most one neighbour of degree >= 12)
- [hand] VH∃ is existential, so an unavoidable class needs no walk. On every graph here with maximum degree < 12, every degree-5 hole is in the class.
- [exploratory] Maximum radius at class holes: T4 **4** (all 12), order 14: 2, A_3: 2 or 3.
- **Belt G_n**, where the one free neighbour is the pole, of degree n. The belt holes are all in the class.
  - Belt-hole maximum pure radius: 1 (n = 5, 7) and **2** (n = 6, 8, 9, 10, 11, 12, 13, 14).
  - The pole hole (degree n, not in the class): maximum radius 1, 2, 1, 3, 3, 3, 3 for n = 5..11, and 4 for n = 12, 13, 14.
  - So the high-degree neighbour is not what makes holes hard here. The class's hard case is bounded-degree T4-type structure, and its bound must be >= 4. This confirms the coordinator's reading.

### Proposed target, or the obstruction
**No colouring-independent target class can beat the direct bound on T4. A target class for P-B needs a fill bound of at least 4, which is the open Conjecture R on those classes.** P-B adds nothing beyond "some degree-5 hole of the unavoidable class has bounded radius". It reduces to P-A, with the class from the audit's 12:40 lemma and a bound of at least 4. Recommend closing P-B as a separate pathway.

**Not checked.**
- No hand proof of any of these counts; no hand check of the traces.
- No degree-6 graphs beyond T4, A_3 and the pentakis sample. No order-22/23 (6^5) graphs: plantri and gen_tri are not on this machine. Pentakis was not enumerated in full.
- No two-hole game on the belts.
- Belt pole data are exact, but only one belt hole was computed per n; the other belt holes were assumed equivalent by symmetry.
- No search for 1-mobility at degree 6 under an extra local hypothesis that would exclude the 24 failures.
