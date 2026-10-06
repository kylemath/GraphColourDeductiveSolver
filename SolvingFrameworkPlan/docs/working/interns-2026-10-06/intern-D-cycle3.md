# Intern D, cycle 3: the order-20 no-merge instance (plantri 64, hole 0)

Hand reading of `longtable/studio-explore/kempe-census/multiclass-smallest3.json`, third instance. Adjacency was read from `rotation_clockwise` with vertex 0 deleted; colour classes and components were traced by eye. Nothing was run. Labels: [hand-read].

## Data
- Link of v=0 in rotation: 1,2,3,4,5 with degrees 8,5,5,5,6. File: kappa(T-v)=2, kappa(T)=2, new_classes 0, both T-v classes "hit_by_T" and each receives exactly one T-class.
- Rep of the 56-class: colours 0:{1,3,13,15}, 1:{2,5,7,17,18}, 2:{6,8,10,12,19}, 3:{4,9,11,14,16}.
- Rep of the 138-class: 0:{1,3,14,16,18}, 1:{2,5,7,9,12,19}, 2:{6,8,10,13}, 3:{4,11,15,17}.
- **Both reps have the same link colouring (0,1,0,3,1)** (vertices 1..5). Colour 2 is absent, so **both reps are filled** (v takes 2). The link does not tell the classes apart; the difference is in the interior.

## Connectivity of the six bichromatic subgraphs (components in T-v)

| pair | 56-class rep | 138-class rep |
|---|---|---|
| {0,1} | connected | connected |
| {0,2} | connected | 2 components ({3} isolated) |
| {0,3} | connected | 3 components ({1} isolated) |
| {1,2} | 2 components ({2,10,18,12} / {5,6,7,8,17,19}) | connected |
| {1,3} | 2 components ({5,4,14} / rest) | 2 components ({2,11,12,4,5} / {7,15,19,17,9}) |
| {2,3} | connected | 3 components |

So the 56-rep has 4 connected pairs, the 138-rep has 2. The two-line lemma (a DL state has at most 4 of 6 connected) does not constrain either rep, because both are filled, not DL; the 56-rep sits at the lemma's bound, the 138-rep well below it. A connected pair is a trivial move (the swap only renames two colours); the 56-rep has 4 non-trivial chain moves, the 138-rep has 10.

## What separates them, and why each class has a filled state
- I did **not** find a hand invariant. Connectivity profile and class sizes ((4,5,5,5) vs (5,6,4,4)) are not Kempe invariants: swaps change both. The number of odd-size colour classes is odd in both, so parity does not separate. The honest statement is: the classes are distinguished by the census (194 T-v states, 56+138), not by a quantity I can prove invariant.
- Each class contains a filled state because every T-colouring restricts to a filled T-v state ("hit_by_T" true for both, new_classes 0), and both reps themselves are filled. The census says kappa(T-v)=kappa(T): deleting v adds no unfilled-only class.
- Why no merge, heuristic: a T-v move differs from a T move only for a chain of colours {m,q} (m = fill colour) through the link, where in T the chain also contains v and cannot be split. Here the filled states of the two classes share one link colouring, so the extra T-v freedom would have to come from splitting such a chain; for both reps, splitting never reaches a state of the other class (census).

## Conjecture (testable)
**M.** If deletion of v merges two T-classes C1, C2, then they are already joined by a path of length 2 in the T-v Kempe graph: filled s1 in C1 -> a single unfilled state u -> filled s2 in C2 (u: the chain swap splits a {m,q}-chain at v). Equivalently, no merge needs two consecutive unfilled states. Test: over all multi-class instances in the census, for each merged pair compute the shortest T-v Kempe path between the classes and record the number of unfilled states on it. Prediction: always exactly 1. Kill: a merge whose shortest path needs 2 or more unfilled states. No-merge instances (like this one) are predicted to have no such length-2 bridge, which the Studio can check directly for plantri 64.

## Self-check
It may fail because merging bridges can need longer paths; the conjecture is untested and I proved no invariant. The reps may have been chosen by the census as the lowest-index states, so their profile may be unrepresentative of the whole class.
