# Intern B: link class (5,5,6,5,6), where Theorem HP breaks

Intern B, 6 October 2026. Hand reasoning only, nothing run. Sources: MathHighDegreeNeighbour.md §1-§2 (HP), its two reviews.

## 1. Claim
**[hand] negative/partial.** HP's proof does not extend to (5,5,6,5,6): the ring-2 colour automaton (the method of HP) has a closed set of 20 "admissible, no one-move kill" states, 4 at each of the 5 free-pair positions, closed under F and B. So no finite bound follows from the HP method, and AB (HP's terminal kill) is never available in this class. No bound on the radius is proved. Radius >= 4 (T4) is untouched; nothing here says the radius is infinite.

## 2. Setup
Frame (a,b,a,g,d), free (degree-6) pair at {k,k+2}; the five positions P_k = {k,k+2}. Degree-5 vertices are the other three. Allowed ring colours: w0,w1 in {g,d}; w2 in {b,d}; w3 in {a,b}; w4 in {b,g}.
Necessary DL conditions (degree-5 vertices only): ring edge w_{t-1} != w_t for deg-5 x_t; x1 deg 5 gives {w0,w1}={g,d}; x3 deg 5 gives b in {w2,w3}; x4 deg 5 gives b in {w3,w4}. "Admissible" = these hold.
Key fact re-derived (colour-only, any degree): F changes only w1 (g->a) and w3 (a->g); B only w0 (d->a) and w3 (a->d). Reason: w0=g or w4=g in K_F would put x0 in K_F (Jordan fact); w1=d, w2=d in K_B would put x2 in K_B. New ring and roles are as in Lemma 3: F reads (w3,w4,w0,w1,w2) with d->b, b->g, g->d, shift k-3; B reads (w2,w3,w4,w0,w1) with g->b, d->g, b->d, shift k+3. So the image ring is determined by the ring alone; an inadmissible image is NL (distance 1).

Admissible counts: P0 4 (gdbab, dgbab, gddbg, dgdbg); P1 9; P2 6; P3 6; P4 9; 34 in all. (P0 differs from HP: new pattern gddbg.)

## 3. HP step table
| HP step | Verdict |
|---|---|
| Setup, Jordan facts, F/B colour-only description | survives (degree-free) |
| Lemma 1 pattern lists | patched: recomputed above for the 5 pairs (34 patterns) |
| F-starvation (needs x2 deg 5, w1,w2 != d) | survives only when x2 is deg 5: P1, P3, P4 |
| B-starvation (needs x0 deg 5, w0,w4 != g) | survives only when x0 is deg 5: P1, P2, P4 |
| Lemma 2 AB kill for R3 (needs x0,x1,x2 all deg 5) | **fails always**: the complement of {k,k+2} in Z5 contains no 3 consecutive vertices, so the triple {x0,x1,x2} always holds a degree-6 vertex |
| Lemma 3 transitions R1<->R3 | survives, but the image can also be a non-HP pattern |
| Termination table | **fails**: no cycle-free chain to a kill |

One-move kills found (state@position, move): P1: ggbab F, dgbab F, dgdab B, ddbab B, dgbbg F. P2: dgbab B, dgdbb B. P3: dgbab F, dgbbg F. P4: ggbab F, dgbab F, ddbab B, dgbag F, dgdbb B. P0: none.
Closed set (all F,B images stay inside, checked state by state):
- P0: gdbab, dgbab, gddbg, dgdbg
- P1: ggdab, gdbab, dgdbg, ddbbg
- P2: gdbab, gddbb, dgbag, dgdbg
- P3: gdbab, gdbbg, dgdab, dgdbg
- P4: gdbab, ddbag, ggdbb, dgdbg

Answer to the key question: both free vertices can block. Each non-adjacent pair removes the F kill or the B kill at some frame positions, and removes AB at all positions; no side is uniformly HP-controlled. The degree-5 vertex between the two degree-6 ones does not help, because F/B starvation read x0/x2, and AB reads the whole triple.

## 4. Gap and repair
Gap: the 20 closed states need a move that reads beyond ring 2. The natural one is AB: the {a,b}-component C of x1 contains x0,x1,x2 plus any a/b-coloured m of a free vertex in the triple; the swap kills iff C does not reach the ring neighbours of the degree-5 singleton (x3 or x4; at least one is deg 5 in every position). Extra hypothesis that would repair it: for each degree-6 vertex in the triple, its outside neighbour m is not coloured a or b, or its {a,b}-component avoids w_{j+3}. Colours alone cannot force this when x1 is free (a is never among its ring colours), so it is a ring-3 / m-colour condition. Alternatively add m-colours to the automaton state and rerun the enumeration (finite, needs a program, so not done here).

## 5. Self-check, two weakest points
1. Admissibility uses only necessary conditions, so the closed set may contain no genuine DL state (m-colour constraints or planarity could empty it). My claim is only that the HP method cannot close, not that the radius is unbounded.
2. About 70 hand image computations over 34 patterns; one slip could move a state in or out of the closed set. The pattern lists for P1 and P4 (9 each) are the likeliest place for an error.
