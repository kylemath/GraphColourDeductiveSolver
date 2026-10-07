# Intern D, cycle 5: where the quarter floor comes from, and why it is a degree-5 count

Hand work only; nothing run. Source read: `docs/working/MathQuarterFloorLemmaA.md`. Labels: [hand] derived, [heur] heuristic, [open] needs the Studio. Counts are labelled link colourings (4 colours, proper, link a cycle).

## 1. Degree 5: where 1/4 comes from [hand]
- Filled link = 3 colours, pattern (2,2,1): 5 singleton positions i x 4 x 3 x 2 = **120** colourings, 24 per position. Unfilled = (2,1,1,1) with repeat positions j, j+2: 5 x 4 x 3 x 2 = **120**, 24 per j. So the raw local ratio is 1:1, not 1:3. The 1/4 is not a raw count; it comes from the inequality U_j <= F_{j+1} + F_{j+3} + F_{j+4}.
- **3 = 2 + 1.** Two F-positions are paid by one-swap moves (Lemma A: swap the component of a or b, which makes it the twin of m; the images lie at singleton positions j+4 and j+3). One position, F_{j+1}, is reserved for the doubly locked states (part (b), the open global step).
- Why only two one-swap moves: the unfilled link has three singletons m,a,b. a and b each have exactly one legal target colour (mu), since their two link neighbours use the other colours. m has two targets (A or B), but these are the same two lock relations m~a and m~b read from the other end. So the relation graph on the singletons is a path with **2 locks**; one failing lock gives one swap; both holding is "doubly locked".
- Why each F_i is hit at most 2+1 times: F_i occurs in the sums for j=i-1, i-3, i-4 (three of five j), by symmetry of the same count. Hence sum U <= 3 sum F, i.e. F/(F+U) >= 1/(3+1) = 1/4.

## 2. Degree 6: filled and unfilled patterns [hand]
- Link C6, 4 colours: 732 proper colourings. 2 colours (ABABAB): 12. Exactly 3 colours: 240, patterns (2,2,2) and (3,2,1). So **filled = 252, unfilled = 480**. Unfilled: (3,1,1,1): 48; (2,2,1,1): 432, in four cyclic shapes (letters = colours, s,t singletons):
  - T1 `a b a b s t` (144), T2 `a b a s b t` (144), T4 `a s a b t b` (72), T5 `a b s a b t` (72, the two repeats antipodal).
- A one-swap fill must swap a component K of some {Y,t} with every Y-vertex of the link inside K and no t-vertex (then Y leaves the link), or the symmetric case. Reading off which swaps are legal gives the **locks**:
  - (3,1,1,1) `a s1 a s2 a s3`: the three singletons pairwise: **3 locks** (s1~s2, s2~s3, s3~s1), a triangle. Locked iff all three hold.
  - T5 and T2: only the two singletons: **1 lock** (s~t in {s,t}); every other move drags a neighbour of the wrong colour into K.
  - T1 and T4: the legal moves also include conjunctive ones ("the two a-vertices lie in one {a,t}-component and the t-vertex does not"); about 2-3 conditions. I did not fully list them [open].
- So at degree 6 there is no single shape and no path of two locks. A state with one failing relation does have a one-swap filled neighbour, and **a one-swap injection exists per (state, chosen move)**, but the rule must now choose among up to three relations.

## 3. Multiplicity: why the count breaks [heur]
- The multiplicity of a filled f is the number of (colour t, component K) giving an unfilled preimage. A preimage needs a colour t on the link with >= 2 vertices, with K containing a proper nonempty part of them. At degree 5 the naive count is 4 (the four vertices of the two doubled colours); Lemma A's rule uses only 2 of them (the m-position and the other swaps are never chosen). At degree 6 the pattern (2,2,2) offers up to **6** (each vertex), (3,2,1) up to 5; at degree 7 (3,2,2) offers 7. I see no rule that cuts this to 2, since m-type vertices (between two repeats) now appear in more shapes.
- With multiplicity M plus one slot for the fully locked states, U <= (M+1) F, so F/(F+U) >= 1/(M+2):
  - degree 5: M=2 -> 1/4 (proved up to part (b));
  - degree 6: M=6 -> 1/8, equal to the observed minimum (order 24, hole 12);
  - degree 7: M=7 -> 1/9, below the observed 2/17 = 1/8.5, consistent.
  The match at degree 6 is suggestive, not a proof (M=6 is only an upper bound, and the locked slot is assumed to cost 1).

## 4. One-line answer
**1/4 is 1/(2+1+1): at degree 5 the link has a single unfilled shape with only two lock relations, so one-swap fills pay for two positions, the doubly locked states for one, and each filled state is used 3 times; at degree 6 there are five unfilled shapes, up to three locks, and a filled state can be an image 5-6 times, so the same count gives 1/8.**

## Requests for the Studio
1. At degree 6, for every class: tabulate unfilled states by shape (T1, T2, T4, T5, (3,1,1,1)) and by number of failing relations, and the number of one-swap preimages of every filled state (max, mean).
2. Check M: is the maximum number of one-swap unfilled preimages of a filled state 6 for (2,2,2) links, and is it attained in the extremal class (order 24, gentri 71, hole 12, F = 1/8)?
3. In that class, how many unfilled states are fully locked (no one-swap fill) per filled state? The 1/8 needs this to be about 1 per filled state if the heuristic holds.
4. Test the degree-7 analogue (M<=7) against 2/17.

## Self-check
Most likely failure: M is only an upper bound; real extremal classes may have lower multiplicity and a different share of locked states, so the 1/8 match could be a coincidence. The T1/T4 lock lists are incomplete.
