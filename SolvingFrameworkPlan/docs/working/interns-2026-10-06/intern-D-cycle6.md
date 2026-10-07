# Intern D, cycle 6: degree-6 analogue of the class identity, and a correction to my 1/(M+2) heuristic

Hand work only; nothing run. Sources: `MathQuarterFloorBijections.md` (§1-§4), `MathQuarterFloorLemmaA.md`, `pd2_lock_proof.md`. Labels: [hand] derived here, [heur] heuristic, [open] needs the Studio. I could not reach `local-runs/6-quarter-floor/summary.json` for a data check (no program, and not read).

## 0. Correction first
In cycle 5 I compared M = 2 at degree 5 (**slots**, i.e. Lemma A's two moves) with M = 6 at degree 6 (**link vertices**, which counts each slot twice, once per alternative swap). That mixes units: at degree 5 the vertex count is 4, not 2. In slot units, the degree-6 filled (2,2,2) link has only **3** slots (below), so my "1/8 = 1/(6+2)" was a numerical coincidence. Please discard it as an explanation.

## 1. Tait types of the link at degree 6 [hand]
Edge colours e_t = c(x_t)+c(x_{t+1}) in {c1,c2,c3}; counts (n1,n2,n3) have equal parity (so at degree 6 all even, at degree 5 all odd). Sum is 6, so the types are (6,0,0), (4,2,0), (2,2,2). Counting sequences of edge colours (183 in all, times 4 for the start colour = 732 colourings): (6,0,0): 3; (4,2,0): 6 x 15 = 90; (2,2,2): 90. Walking the sequence on the colour square gives filled/unfilled:
- (6,0,0): ABABAB, filled (12 colourings).
- (4,2,0), the two c2-edges adjacent (36 seq): link pattern (3,2,1), filled (144 colourings).
- (4,2,0), c2-edges at distance 2 (36 seq): shape T1 (crossing, `a b a b s t`), unfilled (144).
- (4,2,0), c2-edges at distance 3 (18 seq): shape T4 (`a s a b t b`), unfilled (72).
- (2,2,2): 24 sequences filled, pattern (2,2,2) (96 colourings); 66 sequences unfilled = T2 (144) + T5 (72) + (3,1,1,1) (48) = 264 colourings.
Totals: filled 12+144+96 = 252, unfilled 144+72+264 = 480, as before.
At degree 5, by the same reading, every state has type (3,1,1): filled iff the two minor-colour edges are adjacent, unfilled iff at distance 2. That is why degree 5 has a single unfilled shape.

## 2. Slots and locks [hand]
A move that changes the link is the swap of a P-path of one of the three 2-factors. P has d paths in all (counting ends, 2d = sum over pairs of the pair's edge count / ... = d). A **slot** is a pair (c,c') with 4 edges at P (two non-crossing matchings: "short"/"long", as in M2/M3 and L1/L2); a pair with 2 edges is trivial (renaming); a pair with 6 edges has 5 matchings (a 5-ary slot).
- Degree 5, both filled and unfilled: two 4-edge pairs, so **2 slots** each; for unfilled they are the two locks.
- Degree 6:
  - (2,2,2) types: **3 binary slots** (all three pairs have 4 edges);
  - (4,2,0) types: one 6-edge pair (5-ary, 3 paths) and one 4-edge pair (binary);
  - (6,0,0): two 6-edge pairs.
- Reading off which Kempe pair each slot controls (Kempe pair {p,q} lives in the Tait pair complementary to p+q): in T5 (`a b s a b t`) the slot of Tait pair (c2,c3) governs {s,t} and {a,b}, and its "short" outcome is the fill s~t; the other two slots (pairs (c1,c3) and (c1,c2)) govern {a,s},{b,t} and {a,t},{b,s}, and **both of their outcomes stay unfilled** (checked on T5 by hand: swapping {a,s}-component of x3 gives T2 or T5 again, never a 3-colour link). So T5 and T2 have **1 fill-lock and 2 rotation slots**, and (3,1,1,1) has 3 fill-locks and no rotation slot. T1 and T4 involve the 6-edge pair and I did not finish them [open].
- Rotation analogue: R+3 is the swap of the P-path in a 4-edge pair that is in its "long" matching and keeps the state unfilled. At degree 6, T5 <-> T2 by this swap (R+3 of x3's {a,s}-component when x0 is outside it); there are two such rotation slots per T5/T2 state, so the rotation graph Gamma has **degree up to 2 at T5/T2 states and up to 3 at (3,1,1,1)-type fully locked states**, instead of the path structure (degree <= 2) at degree 5.

## 3. Class identity analogue [hand]
Double counting fill moves gives the exact equation
  sum over unfilled s of (number of failed fill-locks of s) = sum over filled f of (number of slots of f whose short outcome is unfilled),
the analogue of N1 + 2N0 = 2F - L_F. At degree 5 each filled state contributes at most 2, and each unfilled one contributes 0, 1 or 2. At degree 6:
  - filled (2,2,2): at most **3**; filled (3,2,1): at most 1 + (one to three paths of the 6-edge pair); filled ABABAB: up to 6;
  - unfilled: T5, T2: at most 1; (3,1,1,1): at most 3; T1, T4: unknown [open].
The rest of the identity needs Gamma's components. At degree 5 they are paths, with endpoints bearing one fill-edge each, and 3F - U = (sum of (1-d(P)) over paths) + nonnegative terms, so U <= 3F exactly when the average number of interior locked states is <= 1 (the global step of part (b)).

## 4. Predictions
- **Degree 6, local model.** Suppose each filled state has the full 3 slots and every unfilled component is a tree with locked interior nodes of degree 3 (all three slots hold) and leaves bearing one fill-edge. A tree with i interior nodes has i+2 leaves, so U = 2i+2 and fill-edges = i+2 = 3F, giving U/F = 3(2i+2)/(i+2): 4 for i=1, **-> 6 as i grows**. So even with unlimited local structure a degree-3 locked tree gives F/(F+U) >= 1/7 > 1/8. The observed 1/8 (U/F = 7) therefore needs something beyond this model: either filled states with more than 3 slots (the ABABAB link has 6, and (3,2,1) up to 4), or unfilled leaves with 2 fill-locks, or locked nodes of higher degree (T1/T4 with the 5-ary slot: degree up to 5 would give a limit 1/(5+...)). The 5-ary slot is the natural suspect: a locked T1/T4 node with a 6-edge pair can have up to 3 + 1 rotation moves, and the same tree count with interior degree k gives U/F -> k.. up to 7 at k = 4? (tree with interior degree k has (k-2)i+2 leaves; with slots-per-filled 3: U/F -> 3 (k-1)/(k-2) x ... I did not complete this; [open]).
- **Degree 7 (odd).** Types (5,1,1) (pairs 6,6,2: two 5-ary slots) and (3,3,1) (pairs 6,4,4: one 5-ary and two binary). Filled links are (3,2,2) only. By parity the same method applies; I predict the floor is lower than degree 6 since the 5-ary slot is present in every type, but I cannot get a number: the local model cannot supply U/F = 7.5 (2/17) or bound it. So 2/17 is consistent with >= 1/9 but my bound is not derived.

## 5. Requests for the Studio
1. In the 1/8 class (order 24, gentri 71, hole 12): histogram of states by Tait type [(6,0,0), (4,2,0) adjacent/dist-2/dist-3, (2,2,2) filled/T2/T5/(3,1,1,1)], and for each the number of fill-moves and rotation-moves. Check: are the filled states mostly (2,2,2) with all 3 slots short?
2. In the same class: the components of the rotation graph (R+3 analogue = swap of a 4-edge-pair P-path keeping the state unfilled): sizes, number of leaves with a fill-lock, interior degree distribution. Does U/F = 7 arise from trees of locked nodes of degree 3, or do T1/T4 nodes with the 5-ary slot give higher degree?
3. Same table for the 2/17 class (order 23, gentri 189, hole 14).
4. Does any state of either class have a filled ABABAB link (2-colour)? Those have 6 slots and could drive the multiplicity.

## 6. Self-check
Most likely failure: the slot-to-fill-lock reading of T1/T4 is incomplete and the 5-ary pair may add fills I missed; my tree model assumes degree-3 interiors. I have no confirmation of 1/8 or 2/17 from this model, and the earlier 1/(M+2) agreement was an artefact of mixing slots with vertices.
