# Intern C, cycle 5: Math's one-filled-state note (16:45 message), items 1(a)-(d), 3(i) (hand only, nothing run)

## Verdict: NO FATAL GAP; one wrong argument (1(c)), one imprecise statement that sets the Studio logging target wrongly (1(d)), one mis-description (1(b)), one unsupported claim (3(i)). Conclusions of 1(a)-(d) are true for a degree-5 hole.

### 1(a): correct
A non-DL unfilled state fills in one swap (L3), the only filled state is f, so those states lie one swap from f.

### 1(b): imprecise (wording)
"A ring N(f) of non-DL states" is wrong as a definition. N(f) means all states one swap from f, and that set may contain DL states. What is forced is that all non-DL unfilled states are in N(f); the DL states may be at distance 1 or more.

### 1(c): conclusion true, argument wrong
The stated reason ("a swap of either colour pair through the link would give a second filled state in most cases") is not a proof. The real reason: the link of a degree-5 vertex is a 5-cycle, an odd cycle, so it cannot be 2-coloured. A filled state therefore uses exactly three link colours, with multiplicities (2,2,1). "Filled up to renaming" does not change this, because renaming preserves the number of link colours. For an even-degree hole (degree 6, link 2-colourable) the statement is false, so the note should say "degree 5".

### 1(d): the conclusion is stronger than stated, and the "or" clause is vacuous
Let C be a bichromatic {x,y}-component with no link vertex, and f' the swap of C. Then f' is filled (same link colours). If f' = pi f for a renaming pi, then pi fixes every colour on the link (f' agrees with f there). By 1(c) the link uses three colours, so pi fixes three colours and hence all four, so pi = id and f' = f. That is impossible since C is nonempty. So f' is a second filled state, always distinct from f. This means:
- **In a one-filled class every bichromatic component of T - v contains a link vertex, with no exception.** A swap that gives a renaming of f occurs exactly when an {x,y}-subgraph is connected, and then its component contains link vertices anyway (any pair of colours meets the three link colours).
- The signature to log is therefore **exactly 0** components missing the link, not "0 or only renaming-trivial". Any f with a component missing the link is not the filled state of a one-filled class. This is a cheap filter for the Studio.
- Consequence: for each link colour c, the {mu,c}-subgraph has at most 2 components. Every non-link vertex needs neighbours of all three other colours, or else it is an isolated component.

### 3(i): not guaranteed, only a heuristic
Invalidating f by a flip does not keep "the rest of S one class". After flipping pq to rs:
- A survivor's fill swap is the component in T' - v, which can change: the new edge rs may merge it with another component, or the removed edge pq may split it. The fill can then land on a new filled state, not f, or on none.
- Removing pq makes new proper colourings (p, q same colour) and splits components, so new swaps lead to states outside S, possibly filled.
Item 3(iii) (recompute) covers this, but the ranking "number of S states invalidated" in 3(i) ignores both effects. The ideal flip should also have rs and pq outside every fill component and every lock component of the DL states. The flip must also keep degree >= 5 at the two vertices that lose an edge.

### Data point: 141 classes, size 4, far = 2, one DL state
This is consistent with 1(a)-(b). Non-DL unfilled states are at distance 1 from f. The only way to have far = 2 is for the single DL state to sit at distance 2, so the class is f, two non-DL states a and b, and the DL state d adjacent to a or b. Extra checks I derive, which the Studio can run on the 141:
- F, B, G0, D2 shift the frame index (+3 or +2), so their images of d cannot be a renaming of d. They must be non-DL, in {a,b}.
- AB, G, L1, L2 do not shift the frame; their images can be d up to renaming.
- Every component of T - v in f meets the link (exactly 0 missing). If any of the 141 f has a component missing the link, my argument or the data has an error.

## Self-check: what would make me wrong
- If the Studio counts "filled up to renaming" differently (for example only up to symmetry of T) the pi argument in 1(d) needs a recheck.
- If the hole degree is not 5, 1(c) fails as above.
- I did not run anything and did not see the Studio data.
