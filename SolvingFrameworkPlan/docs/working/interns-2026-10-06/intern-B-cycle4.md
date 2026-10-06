# Intern B, cycle 4: anatomy of the K3 counterexample (order 26, plantri 5401, hole 13)

Hand only, nothing run. Inputs: the plantri line and the first_k_ge4 colouring in `studio-explore/conjecture-K3/`. I parsed the adjacency by hand (letters a..z = 0..25) and checked the degree sum (144 = 6*26-12). Labels [hand]. Hole 13 = n; the colouring has 25 entries, hole absent.

## 1. Graph and state
Degrees: 5 for {0,2,3,4,6,7,12,13,15,16,18,19,21,22,23,24}, 6 for {1,5,8,10,17,20,25}, 7 for {9,11}, 8 for {14}.
Link of 13 in order: g(6), m(12), u(20), o(14), h(7); degrees 5,5,6,8,5, colours 0,3,1,2,3. So the class is NOT (5,5,6,5,6): two free vertices u (deg 6) and o (deg 8), adjacent.
Frame (HP letters): repeated colour 3 at h and m, middle g (colour mu = 0), x3 = u (A = 1), x4 = o (B = 2). Free positions 3,4, adjacent singletons.
Colour classes: 0 = {0,6,8,11,17,22}, 1 = {1,4,9,20,23,25}, 2 = {2,5,10,14,16,19}, 3 = {3,7,12,15,18,21,24} (6,6,6,7).

## 2. The two lock chains
- {0,1}-chain of g: BFS gives 6,1,0,8,4,9,11,17,20,25,22,23. It is **all 12** vertices of colours 0 and 1. It contains u. Forced path 6-1-0-4-11-20, length 5.
- {0,2}-chain of g: 6,5,0,11,2,8,10,19,14,17,22,16. Again **all 12** vertices of colours 0 and 2; contains o. Forced path 6-5-0-2-8-14, length 5.
- lock_size = 24, lock_dist = 10, Phi = (24,10). The {1,2} subgraph is also connected (all 12 vertices).

## 3. All one-swap moves (complete table) [hand]
Because {0,1}, {0,2}, {1,2} are each a single connected component, swapping any of them is a global renaming of two colours: the same state up to renaming. So the only non-trivial swaps are the components of {3,0}, {3,1}, {3,2}, and each pair has exactly two components. All six, with the Phi of the image (recomputed frame, chains, BFS):
| swap | component | image Phi |
|---|---|---|
| {3,1} of u (= F) | {12,20,21,25,24,18,23,15,9,3,4} | (25,14) |
| {3,1} of h (= G0) | {7,1} | (25,14) |
| {3,2} of o (= B) | {7,14,21,15,19,18,10,3,2,16,24} | (25,16) |
| {3,2} of m (= D2) | {12,5} | (25,16) |
| {3,0} of g (= AB) | {6,12,7,11,18,17,24,22,21,8,15} | (24,14) |
| {3,0} silent | {0,3} | (24,14) |
All six are strictly worse than (24,10); none fills (link still four colours in every image). So k=1 fails, by exhaustion.

## 4. Mechanism (one sentence)
Colours 0,1,2 are pairwise one single spanning component, so lock_size is pinned at the plateau 24 (25 when the 7-class lies in a chain) and every non-trivial swap must go through colour 3, which re-routes the chains through the swapped vertices and **lengthens** the forced path (5,5 -> 7,7, 9, 11) while lock_size does not drop. Shrinking either chain first requires lengthening a path; the size cannot fall because the chains already equal the whole colour pair.
Concrete example of "shrink first grows the other": the silent {0,3} swap removes the shortcut vertex 0 (adjacent to 1 and 4 in chain 1, to 2 and 5 in chain 2), so both paths grow from 5 to 7, Phi = (24,14).

## 5. Depth 2 and 3: what I did not do
I did not enumerate sequences of 2 or 3 swaps; that needs about 6 images, each with about 6 further components, then 6 more levels, too long by hand. The data say least k = 4 here. My evidence is only the exact level-1 table plus the plateau structure (the F, G0, B, D2 images keep three spanning pairs, checked for F: {0,2} unchanged, {1,2} spanning with 13 vertices). Ask the Studio for: the sets of reachable Phi values at depth 2 and 3, and whether lock_size is ever < 24 within 3 swaps of this state.

## 6. Birkhoff diamond
Yes, several, one containing the hole. Hole 13 and its link vertices g(6), m(12), h(7) are all degree 5: triangles 13-6-12 and 13-6-7 share edge 13-6, so {12,13,6,7} is a Birkhoff diamond. Others: {0,2,3,4} (triangles 0-2-3 and 0-3-4, shared edge 0-3, all degree 5; 0 is at distance 3 from the hole, adjacent to ring vertices 1 and 5 via 1 and 5), {22,23,24,16} and {15,16,23,24} (near o). So this graph is reducible and the counterexample is a descent failure of K3, not a diamond-free case.

## 7. Self-check, two weakest points
1. Each image Phi was computed by one BFS in a recoloured graph by hand; one adjacency slip could change a path length by 2, but the qualitative conclusion (no image below (24,10)) needs only that sizes are >= 24, since 24 is the full-pair maximum of 12+12 with all classes of size 6, and dist 5 is the minimum possible.
2. The mechanism sentence is proved only for depth 1; the claim that depth 2 and 3 also cannot shrink is the data's claim (K3 failure) and is not explained by my table.
