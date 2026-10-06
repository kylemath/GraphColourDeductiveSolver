# Intern D, cycle 2: what the four radius-5 core states have in common

Read by hand from `studiointel/run-C-2026-10-06/cert/` (graph faces + state dicts). No program was run to analyse them; I used text search to list faces and counted by eye. Labels: [hand-read] unless stated. The files record no swap witness path (state JSON is only vertex->colour; meta has phi/rho), so I cannot describe the length-5 swap sequence.

Notation: link in rotation, repeat colour alpha at x_j, x_{j+2}; m = x_{j+1} (colour mu); a = x_{j+3}; b = x_{j+4}. w = third vertex of the face across the link edge ab (not v).

## Data (three of the four read in full; 62661... has the same hole-23 face list and state as 8a23...)

| Cert, hole | link degrees (x_j, m, x_{j+2}, a, b) | colours | w, c(w) |
|---|---|---|---|
| 91a3, 22 | 5, 6, 5, 5, 6 | 2,0,2,3,1 | 3, colour 0 = mu |
| 8a23 (and 62661), 23 | 5, 6, 6, 6, 5 | 0,3,0,1,2 | 9, colour 3 = mu |
| 80b9, 23 | 5, 6, 5, 6, 7 | 2,0,2,1,3 | 18, colour 0 = mu |

## Common features

1. **m has degree 6 in all four**, and in the two I checked (91a3: neighbours of m outside the link have colours 3,2,1; 8a23: 0,2,1) the three outer neighbours of m carry exactly alpha, c(a), c(b): m is frozen, cannot be recoloured. (Not checked for 80b9.)
2. **c(w) = mu in all four.** So w is a same-colour twin of m, and w is adjacent to both a and b (a face w,a,b). In 91a3 and 8a23, a and b have no other neighbour in their lock colour pair (91a3: 11's only {0,3}-neighbour is w=3; 14's only {0,1}-neighbour is w), so each lock is "m to w by a mu/c(a) chain, then the edge w-a", and likewise for b.
3. **Lock paths (hand-traced).** 91a3: {0,3}-chain 20-23-26-10-6-0-3-11 (7 edges), {0,1}-chain 20-15-5-1-6-2-3-14 (7 edges). 8a23: {3,1}-chain 22-20-21-15-8-1-6-2-9-26 (9 edges), {3,2}-chain 22-11-4-13-21-17-24-10-9-12 (9 edges). Each chain leaves m through a different outer neighbour of m and reaches the hole's second ring only at the two ends (at m and at w); the middle runs through the third ring and beyond (order 28: they cover about a third of the graph).
4. **The two chains share an internal mu-vertex** (u != m, w): 6 in 91a3 (and w), 21 in 8a23. So the {mu,c(a)}- and {mu,c(b)}-components are pinched at one mu-vertex.
5. Degree of w: 7 (91a3), 5 (8a23), 6 (80b9). The hole's second degree-5 pair (x_j, x_{j+2}) has at least one degree-5 vertex in all four; no other regularity in the link degrees.

## Conjecture (testable by the Studio from its tables)

**C5.** Let s be a doubly locked state at a core-class degree-5 hole with m of degree 6. Then r(s) >= 5 only if (i) c(w) = mu, (ii) all three outer neighbours of m carry alpha, c(a), c(b), and (iii) the {mu,c(a)}-chain and {mu,c(b)}-chain from m to w have a common internal vertex.
Reason (heuristic): any swap of the chain K1 = {mu,c(a)} component or K2 keeps m, w, a (resp. b) together, so the lock can only be cut by first swapping a third chain through the common vertex u; with m frozen and w a twin of m, that needs several steps.

Test: for every doubly locked state in the Phase C tables (T4, A_3, the 1,226-state hole-22 table, the order-32 table), compute (i)-(iii) and tabulate against radius. Prediction: 4/4 at radius 5; radius-2 states mostly fail (i) or (iii). Kill: a radius-5 state failing any of (i)-(iii), or radius-2 states satisfying all with equal frequency (then C5 is a tautology of double locking).

## Self-check
Four states from related tabu runs (three share one parent graph): common features may be search artefacts. Item 2 may hold for every doubly locked state (a and b adjacent, w across the edge); I did not test that on radius-2 states, and that is the first thing the table should show. Item 3's chain lengths are not an invariant; I traced only 91a3 and 8a23. 80b9 was only partly read.
