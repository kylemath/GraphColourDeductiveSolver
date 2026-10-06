# N-Counter: an attempt to falsify (N) with structure

Long Table (N-Counter), 6 October 2026. EXPLORATORY, post hoc, undeclared. Nothing staged or committed. Labels: [computed] = run by my own code, exploratory; [hand] = argued here; [data] = taken from another team's file and re-read with my code; [lead] = plausible, unproved. Status words stay with the Navigator.

Scripts (all in `backgroundMaterial/planemap-structural/longtable/explore-vhphi/`, all `ncounter_*.py`; they share no code with Math's `test_N.py`/`nlab.py`): `ncounter_lib.py` (graph/Kempe/Case code), `ncounter_p17.py` (own plantri-based enumeration, orders <= 17), `ncounter_case.py`, `ncounter_types.py`, `ncounter_xclaim.py`, `ncounter_bothI.py`, `ncounter_walk.py`, `ncounter_walk2.py`, `ncounter_res23.py`, `ncounter_flip.py`. plantri 5.8 was re-fetched, SHA-256 verified (e78a9441...29b8), built in the scratchpad. CPU: single process throughout, each job under about a minute.

## 0. Result

1. **No counterexample to (N) was found.** The search was exhaustive only within these scopes: plantri orders 12, 14, 15, 16, 17 (all min-degree-5 triangulations, all degree-5 x, all ring rotations/directions) and Math's disc lists for orders 17 to 23 (all discs with the rigid six-forest structure, read as data; their exhaustiveness at n >= 19 is Math's claim, not re-checked by me). Nothing at n >= 24.
2. **Reproduced independently [computed].** Triply locked rigid states exist at n <= 17 only on 17:1 (my plantri indexing: graph 1, x = 5 and x = 15, 4 states, 8 counting both ring directions; none at 12, 14, 15, 16). In all of them both neighbours are separable (class sizes 13/14), and exactly one neighbour is Case II (explicit three swaps). This matches the source and MathNPinchT3.
3. **New: "exactly one neighbour is Case II" is false at n = 23 [computed on Math's res_23 discs].** Of the 14 triply locked discs: 8 have both neighbours Case II, 4 have one of each, 2 discs have BOTH neighbours Case I; both are nevertheless separable (the chain {D,beta} breaks at c3, "Ia"). So the Case I/II dichotomy of MathNPinchT3 5.2 is not the invariant. The finer invariant is Ia versus Ib (section 2).
4. **No local flip survives [computed + hand]:** every single edge flip and every pair of flips (min degree 5 kept, x and ring untouched, colouring kept) of each of the 8 + 14 triply locked states either breaks properness, breaks rigidity, or leaves a rigid state with an unlocked fan. Never a rigid triply locked state (section 3). The reason is an exact transfer rule (section 3).
5. **A blocking pattern found in data (lead for a proof) [computed]:** over every rigid disc of orders 17 to 23, a neighbour c' that is locked at u0 occurs only when the original fan at u4 is separable; c'' locked at u2 only when the original fan at u3 is separable (about 207 cases each, 0 exceptions). And a neighbour of type Ib (below) never occurs when fans u3 and u4 are both locked. Either statement would imply (N). I could not prove either.

## 1. Task 1: local reformulation, and what Math's generator covers

**What determines the Case of c' [hand, from MathNPinchT3 5.2, re-derived in code].** After the swap of K2 the whole question is a walk by swaps of pairs avoiding D (the apex colour) at x coloured D: c' -> c1 (swap the [alpha,gamma]-component Q4 of u4) -> c2 (swap the [alpha,beta]_1-component E34 of u3,u4) -> c3 (swap the [beta,gamma]_2-component of u4). Every step is decided by connectivity of ring vertices in one pair graph, which in a rigid state is a spanning tree (or two trees) glued with the swapped pieces. So the Case is a function of the "token pattern" of ring connections (Lemma M of MathNPinchT3: exactly two non-adjacent ring connections per colouring), not of any other detail of the disc. A counterexample is therefore a disc in which the token pattern is the locked branch at every step of the walk, for both neighbours.

**Can it be assembled locally?** The relevant vertices are the five ring vertices and the unique tree paths among them (P13, P14 and the paths in [beta,gamma], [D,alpha] after swaps), together with the pieces K2, K0, Q4, E34. These are not a bounded disc: the paths run through whole colour classes. The completion condition (every other vertex of degree >= 5) enters only through exc_i >= 0, which by I2 reads n_i <= (n-4)/3 (n_alpha <= (n-3)/3); this has slack from n = 19 on. I found no local obstruction to completing a local disc, but I also never constructed a locally consistent both-Ib disc, so this is untested in either direction.

**Math's generator (`MathNDiscSearch`) [data, read].** It grows T-x inward from the ring, prunes by properness, six forests with target (1,2,2,1,1,1), the Prop 3 size/excess targets, degree >= 5 on closed vertices, ring chords forbidden; discs with separating triangles are allowed; counts up to reflection. It covers every rigid six-forest disc to n = 23 (n = 22 took 114 s, n = 23 533 s) and was not checked against an independent census above 18. It does not cover n >= 24, and it depends on Prop 3 being right (hand-proved). I used its output files `out_17..23.txt` and `res_23.txt` as input data and re-checked every structural claim I use with my own code (rigidity, locks, classification).

## 2. Task 2: classification at n <= 17 and in the whole rigid family

**Own enumeration [computed], `ncounter_p17.py`.** For each of the plantri -m5 graphs (order 17: 4 graphs), each degree-5 vertex x without a ring chord, each rotation and direction of the ring word D a D b g: all proper colourings of T-x with that ring, rigid test (six forests, comps 1,2,2,1,1,1), then the three fans by full Kempe-class BFS in G = T - x y. Result: 12, 14, 15, 16: 0 triply locked; 17: 8 labelled (4 states times the two ring directions), all on 17:1, fan classes of size 6, c' and c'' separable, exactly one of them Case II. (The rigid-state counts per x are in the run output; for example graph 1 x = 5 has 12 rigid labelled states of which 4 are triply locked.)

**Type refinement, `ncounter_types.py`.** For a neighbour c' (mirror for c''): FO (u0 !~ u3 in [beta,D'], one swap), S1 (unlock after Q4), II (Case II), Ia (Case I and the chain {D,beta} is broken at c3, so separable after three D-free swaps plus the x-swap), Ib (Case I and c3 intact; the walk must continue). Tallied against the lock pattern (u1,u3,u4 as L/U) of the original state c, over all rigid discs of Math's lists:

| n | rigid discs | LLL states | neighbours at LLL | Ib neighbours at LLL |
|---|---|---|---|---|
| 17 | 75 | 2 discs | (II,Ia) 1, (Ia,II) 1 | 0 |
| 23 | 78005 | 14 | pairs (II,II) 8, (II,Ia) 2, (Ia,II) 2, (Ia,Ia) 2 | 0 |
| 18 to 22 | 74 to 15840 | 0 | vacuous | 0 |

At n = 23 the table row `('LLL','Ia','Ia') 2` is the pair of discs in which both neighbours are Case I; both are separable. So Case I does not imply locked; the sequence continues one more swap.

Over all rigid discs of orders 17 to 23, Ib occurs hundreds of times (n = 23: about 700 neighbours) and (Ib,Ib) pairs occur (n = 21: 18 at pattern UUU, 18 at LUU, 4 at LLU, 4 at LUL; n = 23: 244 at UUU, 20 at LUU, plus smaller), always with the original state having an unlocked fan among u3, u4. Patterns of the original fans seen with (Ib,Ib): LLU, LUL, LUU, ULU, UUL, UUU; never LLL (and {u3,u4} locked implies u1 locked, ULL never occurs, as at class level in the source).

**The 14 order-23 states [computed], `ncounter_res23.py`:** (II,II) in 8 of 14, mixed II/I in 4, (I,I) in 2 (both Ia); all 28 neighbours separable.

**Observation X [computed] (`ncounter_xclaim.py`).** For every rigid disc whose c' is Case I, c' is locked at u0 only if the original fan at u4 is separable (fan patterns of those cases: LLU, ULU, UUU only). Counts of c' locked: n = 17: 9; 21: 21; 22: 33; 23: 144 (none at 18, 19, 20); mirror image for c'' and fan u3 with identical counts. 0 exceptions, 0 truncated (cap 3000). Since c' locked and c locked at all fans never co-occurred, a counterexample would need a new kind of state.

**The walk lives partly inside the fan classes [computed], `ncounter_walk.py`, `ncounter_walk2.py`.** For every rigid disc with a walk: c' is in the Kempe class of c at fan u1 (always), c' and c1 lie in the class at fan u3 (always; [hand]: both moves are swaps of pairs avoiding beta, with x not in the graph, i.e. legal in G at u3). c2 (and c3 in Case I) lies in the class of c at fan u4 in some states and not in others. [hand] If c' is Case II and c2 lies in the class at u4 then c is separable at u4: in c2 with x coloured beta, the [beta,gamma]-component of u4 does not contain x (Case II: it misses u2, the only ring neighbour of x of colour gamma), so swapping it gives c(x) != c(u4). [computed] the data are stronger: in all 29/241/831 walks at n = 17/20/21, c2 in the class at u4 occurs only when the fan at u4 is separable (patterns with L in the third letter always show '0000').

## 3. Task 3: modifications

**Flips [computed], `ncounter_flip.py`.** All edges not incident to x and not on a face with x, with both faces and both end-vertices of degree >= 6 (so that min degree 5 survives), the new edge not already present, colouring kept. 8 triply locked states at 17 (24 single flips, 48 two-flip combinations) and 14 at 23 (66 single, 368 two-flip). Outcomes: single flips: 8 + 34 improper (the two apexes have the same colour), 16 + 32 not rigid; two-flip: 16 + 32 rigid but a fan unlocked; none rigid and triply locked. Rigid structure after two flips is possible (both flips in the same complementary class), the locks are not.

**[hand] The blocking rule for flips.** Flip ab -> cd with a,b coloured p,q. c and d are adjacent to both, so their colours are the complementary pair r,s and properness forces them distinct. In a rigid state the pair [p,q] is a forest, so deleting ab raises comps_pq by 1; adding cd to [r,s] either lowers comps_rs by 1 (a merge) or closes a cycle. The rigid vector (1,2,2,1,1,1) has complementary pairs (D alpha, beta gamma) = (1,1), (D beta, alpha gamma) = (2,1), (D gamma, alpha beta) = (2,1). A cycle destroys rigidity (Lemma F: all six pairs are forests). A merge needs comps_rs >= 2, so rs is [D,beta] or [D,gamma], and then comps_Db or comps_Dg drops to 1; but first-order locks at u1/u3/u4 force both to be >= 2 (Prop 2). Hence no single flip keeps a rigid triply locked state at first order. Only compensating pairs of flips restore the vector, and in the 416 combinations tried, one fan always unlocks (second-order, not explained).

**Vertex insertion [hand, not run].** Inserting a vertex of colour i changes n by 1 and n_i by 1; I2 then requires exc_i to fall by 2 and each other exc_j to rise by 1; the total change +1 equals the Euler change of sum(deg-5), so there is no counting obstruction; none was tested either. The disc generator at n = 18 to 23 is the exhaustive version of "insert vertices and keep the six forests"; it produced no triply locked state at 18 to 22 and 14 at 23, all with both neighbours separable.

**Does any modification keep the state rigid and make both neighbours Case I?** Yes, but only in the weak sense: at n = 23 there are two triply locked rigid discs with (Ia, Ia); both neighbours are Case I and still separable via the chain {D,beta} (or {D,gamma}) breaking at c3. No modification found makes both neighbours Ib while keeping the state rigid triply locked: not by flips, and not anywhere in the 78 005 rigid discs of order 23 or the lower orders.

## 4. The invariant that blocks, and leads

What the data say blocks a counterexample is not a counting identity but a link between the neighbour walk and the third fan:

- (L1) [hand + data] Neighbour c' of type Ib or locked, with c locked at u4, never occurs. In the same way c'' locked and c locked at u3. Both would give (N).
- (L2) [hand] Observation: c' and c1 lie in the Kempe classes of c at the fans u1, u3; so the walk's first two steps are moves inside classes that are locked in a triply locked state, and the third and fourth steps (E34, then the swap of [beta,gamma]) are legal in G at u4 for a state in which x has the colour of the swapped vertex. A lemma of the form "if the walk reaches Ib then the class at u4 contains c2, and from c2 one of the two Case II/Ia moves is legal in G at u4" would prove (L1). The data show c2 in the class at u4 whenever c is separable at u4 in the cases checked, but I could not show the implication in either direction.
- (L3) The counting automaton of MathNPinchT3 5.4 has a closed locked orbit, so no purely counting argument closes Case I; the geometric input needed is exactly why c2 cannot lie outside class(u4) when c' is locked.

## 5. What is not shown

- (N) is not proved and not refuted. No claim that the pattern in (L1) is a theorem.
- The scope is the rigid six-forest family to n = 23 and 17-vertex plantri graphs; the family at n >= 24 is untouched (both neighbours Ib needs a locked branch at each of at least two further steps; plausible slack grows with n).
- The type Ib/Ia split depends on my reconstruction of Math's walk. The walk is deterministic (one binary choice per step), but a counterexample could also lock the D-free class differently; the Case I definition only follows the one locked branch, not the full D-free class. The full-class lock tests (Kempe BFS, cap 3000, never truncated) are what the tables use for lock status.
- Flip and two-flip results used the colouring of the original state and kept it; recolouring after the flip was not tried.
