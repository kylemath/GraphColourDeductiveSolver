# Candidate: the 66666 wheel is C-reducible (14 Oct 2026) [CANDIDATE, not a result]

Claim (Studio Job 15 interim, `../studio15/crosscheck_neg.out`): the wheel w66666 (degree-5 centre I0, neighbours
I1..I5 of degree 6, ring R0..R9; I1 sees R9,R0,R1, I2 sees R1,R2,R3, …, I5 sees R7,R8,R9) is C-reducible with
X = {R0-I1, I2-I3, I3-I4, I4-I5} (and its rotations).

## Argument (coordinator, to be checked)
Let G be a minimal counterexample (internally 6-connected triangulation) containing w66666.
1. G/X has no loop: the components of X are {R0, I1} and {I2, I3, I4, I5}; the only G-edges inside them are the
   contracted ones (I2I4, I2I5, I3I5 are not edges; interior vertices have no neighbours outside S). G/X has
   |V(G)| − 4 vertices, so by minimality it has a 4-colouring c'.
2. Give every vertex of G − {I0..I5} its c' colour (R0 takes the colour of the merged {R0, I1}). This is proper on
   G − interior. The merged M = {I2..I5} is adjacent to R1..R9 and to I1, hence to R0's colour class too, so the
   ring colouring uses at most 3 colours.
3. Every 3-colouring of the 10-ring is in the Kempe (D-)closure of w66666, so the outside colouring can be Kempe-
   switched until it extends into the interior. Contradiction.

## Independent check of step 3 (`kempe66666.py`, `kempe66666.out`)
A separate Python implementation (Birkhoff vertex-Kempe closure; all non-crossing partitions of the ring, both
colour-pair types jointly non-crossing, consecutive same-type ring vertices in one chain, any subset of chains
switched): 2,461 classes, 530 directly extendable, closure 1,241 at depth 15, **all 171 3-colourings reached**.
These numbers equal dfast's exactly (`ext=530 reached=1241 depth=15`).

## Open before it counts
- Lean certificate of step 3 (DCheck reached-set contains all 3-colourings) and a written proof of steps 1–2.
- Literature check: RSST's 633 do not include w66666. Their contract may not allow ring–interior edges (every
  working X here has exactly one), which would explain the absence without contradicting this argument.
- Consequence if it holds: every degree-5 vertex whose neighbours all have degree 6 is reducible, so every
  "66666 hole" sender in B8/B8b (hemi8, hemi9, the 66666 2-ball families) disappears.
