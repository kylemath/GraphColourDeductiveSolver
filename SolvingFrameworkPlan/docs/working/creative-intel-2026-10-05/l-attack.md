# L-Attack: Conjecture L (lock persistence under F) is false as stated; explicit chains of length 6 and of infinite length

Team L-Attack (Long Table, Creative Intel), 6 October 2026. Exploratory. Labels: [hand] = every step written out; [computed] = exact finite computation, reproducible from the named scripts; [lead]; [conjecture]. No git add/commit. CPU used: about 12 CPU-minutes total, at most 2 processes, graphs of order <= 27.

Scripts (all in `backgroundMaterial/planemap-structural/longtable/explore-vhphi/`, stdlib only):
`lattack_verify.py` (definitions + verifier + self-test), `lattack_search.py` (hill-climb and random baseline), `lattack_witness.py` (self-contained recheck of the two witnesses, does not import the verifier), `lattack_sym.py` (exhaustive census on C5-symmetric triangulations A_r), `lattack_sym_component.py`, `lattack_radius.py`, `lattack_symradius.py` (Kempe-distance to a filled state).

## 0. Headline [computed, exact]

1. **A chain of length 6 exists** on a 20-vertex plane triangulation (degrees 3..8), hole v of degree 5. Found by the prototype hill-climb of section 5 (tag `b`, about 19 CPU-s). It is rechecked by two independent codes (`lattack_verify.verify`, and `lattack_witness.py`, which prints the explicit lock paths at every step). So Conjecture L with N = 5 is refuted.
2. **Infinite chains exist.** On the triangulation A_3 (17 vertices, 12 of degree 5 and 5 of degree 6, 5-fold symmetric about v) there are colourings s of T-v whose F-orbit has period 60 (raw) and every one of the 60 states is doubly locked. Since F-iterates then repeat forever, s, F(s), F^2(s), ... are all doubly locked: **chain length infinity**, so L is false for every N. Same on A_4 (22 vertices) and A_5 (27 vertices): exhaustive enumeration of all colourings gives 120, 120, 360 raw colourings (x0 colour fixed) with chain length >= 40 (cap); A_2 (icosahedron) has none.
3. This does **not** touch VH-exists or the clean-vertex statement: in A_3 the whole Kempe class of such an s (100 canonical states) contains 40 filled states, and the Kempe distance from s to a filled state is 2 or 3 (A_4, A_5: 2 on the 12 sampled). Conjecture L was only a route to cleanliness; the route needs the closure under *all* swaps, which is not a property of the F-orbit alone. The implication "L implies every degree-5 vertex is clean" is therefore vacuous, not wrong.

Witness W6 (rotation system as ccw faces; v = 16; colours 0..3 on T-v). Faces: [1,16,5] [2,4,6] [2,33,22] [3,16,8] [4,2,22] [4,14,21] [4,22,14] [5,31,1] [5,33,6] [6,4,11] [6,10,20] [6,11,34] [6,20,5] [6,33,2] [8,13,17] [8,14,3] [9,14,8] [10,1,31] [10,6,34] [11,10,34] [11,17,13] [13,1,10] [13,8,16] [13,10,11] [14,17,21] [16,1,13] [16,3,5] [17,9,8] [17,11,21] [17,14,9] [20,31,5] [21,11,4] [22,3,14] [31,20,10] [33,3,22] [33,5,3].
Colours (vertex:colour): 1:2 2:2 3:2 4:0 5:0 6:3 8:3 9:2 10:0 11:2 13:1 14:1 17:0 20:1 21:3 22:3 31:3 33:1 34:1. Link of v: x0..x4 = 5, 1, 13, 8, 3 (**corrected 6 Oct 09:30 after the audit's replay**: the report first said 13, 8, 3, 5, 1, which is the same cyclic ring started at another vertex; the colours and repeat indices below are those of the ring read from x0 = 5, a rotation with no effect on the result); link colours at steps 0..5: (0,2,1,3,2), (0,1,2,3,2), (2,1,2,3,0), (2,1,3,2,0), (1,2,3,2,0), (1,2,3,0,2); repeat index 4,2,0,3,1,4 (so +3 each step, Prop. 1 of MathVHLine confirmed on it); at step 6 the new lock Q is missing. F^5(s) is not a renaming of s (Hamming distance 9 of 19), consistent with the chain ending.
Witness A_3 and its colouring are in `lattack_witness.py` (A3_FACES, A3_V, A3_COL) with a period check.

## 1. Definitions (my own statement) [hand]

State s at a degree-5 hole v, link x0..x4 in rotation order: proper 4-colouring of T-v with exactly 4 colours on the link; then exactly one colour repeats, at x_j, x_{j+2} (adjacent link vertices differ), j the repeat index. Put m = x_{j+1} (middle single), a = x_{j+3}, b = x_{j+4}. **Doubly locked**: m and a lie in one component of the subgraph of T-v induced by colours {col m, col a}, and m and b in one component of the subgraph induced by {col m, col b}. (j = 0, link (al,be,al,ga,de): a be-ga path x1~x3 and a be-de path x1~x4; this is Step 1 of MathConfinementAttack.) **F(s)**: with al = col x_j, c = col x_{j+3}, swap al<->c on the {al,c}-component of x_{j+2}. **Chain length** of s: the largest k with s, ..., F^{k-1}(s) all doubly locked. F is applied literally, and the chain stops if an iterate fails to have a 4-colour link.

## 2. Verifier and validation (task 1) [computed]

`lattack_verify.py` checks the triangulation (symmetric, simple, every traced face a triangle, Euler), deg v = 5, properness on T-v, then recomputes locks and F from scratch. Self-test sampler: random triangulations (stack, then edge flips), orders 12-20, random DFS 4-colourings with 60 random Kempe swaps.
- Theorem A index shift (repeat index of F(s) = j+3) holds in all ~5000 locked samples, 0 exceptions: my definitions agree with Math's structural statements.
- Chain-length frequencies among locked states (order 12-20, ~1500 locked): chain 1: 94%, 2: 3.7%, 3: 2.4%, 4: 0.07%, never 5 in that sample. This does **not** reproduce the split Math reports (about 60/7/7/1.4%); the unbiased sampler gives mostly chain 1. Orders 10-18 with other flip counts give the same picture (chain 1: 93-98%). I believe Math's numbers include the hill-climb steps ("accept if not shorter"), but I cannot confirm. The maxima agree (4 by plain sampling, 5 rare). The random baseline of section 5 (orders 12-18) finds chain 4 about 5 times per 30000 sampled states and no 5 in 3 x 60 s; one 20 s run found one 5.

## 3. Hand analysis (task 2)

**Lemma 1 (bookkeeping)** = Prop. 1/Cor. 2 of MathVHLine; I re-derived the link sequence (repeat index 0,3,1,4,2; swapped colours gamma, beta, delta, gamma, beta; link after five steps = link of s with (beta gamma delta) cyclically renamed) and the edge sequence: the swapped component at step k always contains the link edge x_{j+2}x_{j+3}, and these edges are 23, 01, 34, 12, 40, 23, ... each of the five link edges once per five steps. [hand]

**Lemma 2 (what each new lock must cross), step 0 -> 1** [hand]. Notation s0 = (al,be,al,ga,de), P1 the be-ga path x1~x3, P2 the be-de path x1~x4, K0 the al-ga component of x2 (contains x3, misses x0 by the C2 curve). s1 = (al,be,ga,al,de), middle single x4, its locks: P2 (inherited, untouched since K0 has no be/de vertex) and Q0, a de-ga path x4~x2 in s1. The closed curve v,x1,P1,x3,v separates x2 from x4 in the plane, so Q0 meets P1 in an interior vertex (x1 is be, x3 is al in s1) which must be ga in s1, i.e. a vertex of P1 that was ga in s0 and lies outside K0. Same argument one step later: R1 (the new be-ga lock of s2, joining x2 to x0) must cross P2 at a be vertex of P2 that is outside the al-be component swapped at step 1. In general: each new lock must use a vertex of the previous-but-one lock path of the shared colour that the intervening swap did not recolour. This is the exact "gap" Math's lead describes; it is a **necessary** condition and, by W6 and A_r, it can be satisfied six times and forever.

**(a) Mechanism bounding the chain: none exists** [computed]. Any Jordan/counting argument that bounded chain length by an absolute N would be contradicted by W6 (N >= 6) and by A_3..A_5 (all N). The planar obstruction at "step 5 or 6" is local to the instance (in W6 the failing step is step 6, the lock Q at x_{j+1} missing; there is nothing structural forcing it). **What would be needed to make L true:** an extra hypothesis that excludes A_r-type configurations, e.g. closure under all Kempe swaps (not only F), see below.

**Lemma 3 (periodic orbits)** [hand]. F is injective on states s with s, F(s) doubly locked (MathCleanVertexAttack Claims 1-2: B(F(s)) = s). On a finite graph, if s, F(s), ..., F^{p-1}(s) are doubly locked and F^p(s) = s (or any earlier state of the orbit), the chain is infinite. Likewise if F^5(s) is a colour renaming of s and s..F^4(s) are locked, F^5(s) is locked (locks are invariant under colour renaming, F commutes with renaming), so the chain is infinite. A_3 realises the first alternative with p = 60 (period 15 x 4 on raw states, divisible by 15 as Cor. 2 predicts), and F^5(s) is **not** a renaming of s there (Hamming distance 8 of 16): the orbit closes only after four rounds, so "F^5 = renaming" was the wrong thing to look for (it kills K1's proposed test but not the existence of infinite orbits).

**Lead on why A_r works [lead, not proved]:** the 5-fold rotation about v of A_r maps link x_i to x_{i+1}, and all rings are antiprism strips, so the lock paths wrap around v along rings; the new lock Q needed at each step can run along a ring. I did not turn this into a theorem; r = 3, 4, 5 are the only cases checked (r = 6 would exceed order 30), and r = 2 (icosahedron) fails.

**Conjecture L repaired [conjecture].** The data indicate the true local obstruction lives in Kempe distance, not in F-chains. Define the radius r(s) = least number of Kempe swaps from s to a filled state (link <= 3 colours; infinite iff the Kempe class of s is targetless, in the setting with no protected face). Found values: W6 has r(s0) = 2; A_3 has r in {2,3}; A_4, A_5 have 2 on the colourings tested. **Conjecture R** (open, replacing L): there is an absolute R with r(s) <= R for every doubly locked state at a degree-5 hole of a triangulation. R = infinity at some state is exactly a targetless component at v, so R is no easier than clean-vertex existence, but it is falsifiable at small order by search (section 5, S2).

## 4. Killed lines

- K-L5: "L with N = 5" (or any N): refuted by W6 and A_r. The implication "L => clean vertex" stays true but unusable.
- K-sampling: "random sampling at orders <= 30 is evidence for L": the samplers never visit symmetric structures; A_3 is a 17-vertex triangulation with degrees 5, 6 and sampling found chain <= 4 at orders 12-20 (I did not measure how rare such symmetric graphs are).

## 5. Constructive search design (task 3), pre-registrable

Prototype: `lattack_search.py`. Everything below is what the code does; parameters are the file's constants.

**State space.** (faces, v, col): a simple plane triangulation given as oriented triangles, order 8..NMAX = 30, v a vertex of degree 5 (label never changes), col a proper 4-colouring of T-v whose link has 4 colours. Initial states: stack to n in [12,18] random faces then 8n random flips; v a uniformly chosen degree-5 vertex; random DFS colouring + 60 Kempe swaps; retry until the link uses 4 colours.

**Objective (smooth).** S = k + 1/(1+d), k = chain length, d = d1 + d2 of the first failing iterate s_k where d1, d2 are the cheapest m~a and m~b paths counted as the number of internal vertices outside the lock pair colours (0-1 BFS); d = 1000 if s_k has lost its 4-colour link. S lies in (k, k+1/2].

**Moves** (one per step, illegal ones resampled): (i) Kempe swap of a random bichromatic component (prob .5); (ii) edge flip, not touching v, new diagonal not already an edge, endpoints of the diagonal differently coloured, flipped edge's endpoints of degree >= 4 (prob .3); (iii) stack a new vertex into a face not containing v, taking the unique 4th colour (prob .1; order < 30); (iv) delete a degree-3 vertex not adjacent to v (prob .1). Properness, simplicity, triangulation, deg v = 5 verified invariant on 12000 random moves (0 violations).

**Acceptance.** Accept if S' >= S (plateau moves allowed). Restart from a fresh initial state after STALL = 400 consecutive non-improving steps.

**Seeds.** `random.Random("lattack|hc|<tag>")`; the baseline uses `"lattack|rs|<tag>"`. Proposed tags: `t001` to `t040` for the hill-climb, same tags for the baseline. Deterministic given the tag (rerun of tag b reproduced 150115 evaluations exactly).

**Budget caps.** One process per tag, `time.process_time()` cap 120 CPU-s per tag, at most 2 workers, so 40 tags cost 40 CPU-min. Orders <= 30 throughout. No plantri.

**Kill / result classes (pre-register these).** Search S1 (this prototype): KILL = a state with chain >= 6 that `lattack_verify.verify` confirms and `lattack_witness.py`-style recheck confirms; this has now been reached (W6) so S1 is closed as a refutation of L. Everything else is a **result** only: max chain per tag and the distribution of per-restart best chains.

**Pre-registered follow-up S2 (after the finding above), not run:** same state space and moves, objective S2 = r(s) via BFS over Kempe swaps of T-v to depth <= 6 and <= 20000 canonical states, tie-broken by number of unfilled states in the BFS ball; s0 must be doubly locked; KILL-2 = an exhaustively closed Kempe class of T-v with no filled state (a targetless component at v, to be rechecked with the project's protected-face definition by the Long Table), RESULT = max r reached. Same seeds and caps; variants S2a (min degree >= 4) and S2b (min degree >= 5, i.e. only degree-5 and 6 triangulations such as A_r; order <= 30) to answer the objection that W6 has two degree-3 vertices. For S2b a flip/stack/delete move set is too coarse; use a generator of the 5-fold symmetric families (rings of 5m vertices) plus Kempe swaps.

**Prototype validation (3 tags x 60 CPU-s each, hill-climb vs random sampling at the same CPU budget, orders 12-18, 2 processes).**

| | tag a | tag b | tag c |
|---|---|---|---|
| hill-climb max chain (confirmed by verify) | 5 | 6 | 6 |
| hill-climb objective evaluations | 476k | 150k | 157k |
| hill-climb restarts with best chain 3 / 4 / 5 / 6 | 249 / 142 / 11 / 0 | 78 / 48 / 3 / 1 | 94 / 35 / 4 / 1 |
| random sampling max chain | 4 | 4 | 4 |
| random states sampled (locked: chain >= 1) | 32k (4.2k) | 30k (4.0k) | 31k (4.1k) |
| random states with chain 4 | 6 | 4 | 4 |

So at equal CPU the climb reaches chains 5-6 where sampling stays at 4, and reproduces 3, 4, 5 deterministically in every tag (about 1% of restarts reach 5). Caveat: two of three tags hit 6 inside the first minute, and the prototype was run on three tags only; I make no statement about how often 6 occurs, and I did not tune parameters.

## 6. Ledger

- Chain-6 witness W6, infinite-chain witness A_3 (period 60), census on A_2..A_5, Kempe radii, validation table: [computed, exact on the stated graphs].
- Lemma 1, Lemma 2 (step 0 -> 1 crossing condition), Lemma 3: [hand].
- Lead on A_r (ring-wrapping locks), general A_r for all r: [lead]. Conjecture R: [conjecture].
- Not claimed: anything about VH-exists, about targetless components, or about the core (W6 has degree-3 vertices; A_r has no protected face).
- Protocol note: I was told to prototype only; the three 60 s prototype runs happened to contain the kill. I stopped searching after that and did no tuning.
