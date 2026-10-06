# Attack on "some off-phi degree-5 vertex is clean"

Math research worker, 6 October 2026 (the earlier worker died before writing; this file was created fresh). Hand work; one small Python check on random triangulations I built (§3). No census, no declared experiment, no status change. Builds on `MathConfinementAttack.md` (Theorem A, Corollary B) and `MathTraceFourConnAttack.md`.

## Verdict, first

Not proved, not refuted. Two new exact facts about a targetless component C (both [hand], checked [computed] on small examples), and an exact account of why they, and any argument built only from this kind of data, stop short:

- **Theorem C (equidistribution).** For a degree-5 hole v, the states of C at v split into five types (repeat pair {xj,xj+2}), and there are **exactly the same number n_v of each type**. So |C_v| = 5 n_v. The Theorem A rotation is a bijection, not just a surjection.
- **Theorem D (slide balance).** If v, w are adjacent, both of degree 5, both off phi, both in S, then **n_v = n_w**. More generally the number of slide edges between the states at v and the states at an off-phi neighbour w is 3 n_v. So n is constant on every connected cluster of off-phi degree-5 vertices of S.
- **[open] Clean vertex.** Still open. §4 shows the data (Theorems A, C, D, closure under off-phi neighbours, two locks everywhere) is satisfiable abstractly with S = every off-phi vertex, so no counting or discharging on this data alone can give a clean vertex. The contradiction, if there is one, must use the actual colour/path geometry again (Try 1 of the earlier page, still dead).

## 1. Theorem C (the rotation is a bijection)

Notation as in MathConfinementAttack §1. A targetless unfilled state s at degree-5 v, link x0..x4, repeat pair index j (colours c_k on x_k, c_j = c_{j+2}). Define two swaps of s:

- F(s): swap the {c_j, c_{j+3}}-component K of x_{j+2} (it contains x_{j+3}). By Step 2 of Theorem A this component misses x_j, and the result has repeat pair {x_j, x_{j+3}}, index j+3.
- B(s): swap the {c_j, c_{j+4}}-component L of x_j (it contains x_{j+4}). By Step 2 it misses x_{j+2}, and the result has repeat pair {x_{j+2}, x_{j+4}}, index j+2.

(With j=0 these are exactly the K-swap and the αδ-swap of Step 2.) Both results are in C, hence targetless, unfilled and doubly locked; Theorem A applies to them.

**Claim 1 [hand]: B(F(s)) = s.** F(s) has index j' = j+3. Its colours on x_{j+3} and x_{j+3+4} = x_{j+2} are c_j and c_{j+3} (swapped). B(F(s)) swaps the {colour of x_{j'}, colour of x_{j'+4}}-component of x_{j'}, i.e. the {c_j,c_{j+3}}-component of x_{j+3}. Swapping a bichromatic component does not change its vertex set as a {c_j,c_{j+3}}-component, so this is K again; swapping K twice is the identity.

**Claim 2 [hand]: F(B(s)) = s.** Symmetric: B(s) has index j'' = j+2; F(B(s)) swaps the {colour of x_{j''}, colour of x_{j''+3}}-component of x_{j''+2} = x_{j+4}. Those colours are (c_{j+4}, c_j) after the swap, and this is L again.

**Consequence.** Let C_v^j be the states of C at v of index j. F: C_v^j → C_v^{j+3} and B: C_v^{j+3} → C_v^j are mutually inverse bijections. Since 3 generates Z5, |C_v^0| = |C_v^3| = |C_v^1| = |C_v^4| = |C_v^2| =: n_v. In particular F is a permutation of C_v whose orbits have length divisible by 5 (index advances by 3 each step), and every degree-5 vertex of S carries 5 n_v states, n_v ≥ 1.

Counting colourings up to renaming or as raw colourings both work, since colour renaming commutes with F and B.

## 2. Theorem D (slide balance)

A slide from a state at v to a neighbour w = x_i (singleton colour in the link of v, w off phi) gives a state at w in which v is a singleton of w's link, and the reverse slide is always allowed (the other neighbours of w avoid the old colour of w). So slides give a bijection

{states of C at v with x_i singleton} <-> {states of C at w with v singleton}.

If deg v = 5, the states at v with x_i singleton are those with index not in {i, i-2} (the two pairs containing x_i), three types, so there are 3 n_v of them (Theorem C). If also deg w = 5, there are 3 n_w states at w with v singleton by the same count. Hence n_v = n_w. [hand]

Corollary. n is constant on each connected component of the subgraph of S induced on off-phi degree-5 vertices. For a degree-5 vertex v and any off-phi neighbour w of larger degree, the number of states at w with v singleton is exactly 3 n_v. Each state at v has exactly 3 slide neighbours, one in each of three consecutive-ish directions (all neighbours except the repeat pair), minus those neighbours lying on phi.

## 3. Check [computed, small]

Script in the session scratchpad (`fb.py`, not committed): random planar triangulations on 10 to 15 vertices (stacking then edge flips, degrees kept at least 4), degree-5 vertices, random proper 4-colourings of G minus v, kept the 433 doubly locked ones. Tested: F shifts the repeat index by exactly 3 in all 433; B(F(s)) = s whenever F(s) is again doubly locked; F(B(s)) = s whenever B(s) is doubly locked. 0 failures. This tests Claims 1, 2 and the index shift on locked states, which is all the proof uses. It is not evidence about targetless components.

## 4. Why this does not close the gap, exactly

Let U be the set of off-phi vertices with a targetless state at them. Known: if v is in U and has degree 5, every off-phi neighbour is in U (mobility). Corollary B: v in U with degree 5 carries all five pairs. Theorems C and D add: n_v = n_w on adjacent degree-5 vertices and 3 n_v slide edges to each neighbour.

All of these constraints are satisfied by the abstract data "S = all off-phi vertices, n_v = 1 constant, every degree-5 state has exactly three slide neighbours, one state per index". Counting the slide edges at a degree-6 vertex w with all neighbours of degree 5 and equal n gives N_w between 6n and 9n, which is consistent. Euler and degree-sum identities only see degrees, not colours, so they cannot distinguish this abstract picture from a real one. Therefore:

- **[hand] Meta-obstruction.** No argument that uses only (a) Corollary B, (b) Theorems C and D, (c) mobility and closure under off-phi neighbours, (d) degree sum / Euler on the core, can prove a clean degree-5 vertex exists. A proof must reintroduce the geometry of the lock paths (Try 1 of the earlier page) or phi.

Idea (i), discharging on states, fails for the same reason: every weight I can assign (per state, per type, per slide edge) is balanced by Theorems C and D, so the total charge is conservative with no forced deficit. Idea (ii) (adjacent degree-5 vertices not both unclean): Theorem D shows adjacent unclean degree-5 vertices are exactly *consistent*, with equal n; no configuration appears. Idea (iii) (Euler with the protected triangle): the only place phi enters is that slides to phi vertices are forbidden. A degree-5 vertex v adjacent to phi has 3 n_v states with a phi vertex singleton, which just lose one slide edge each. This gives no equation at the missing slide (no partner state), so no contradiction. I checked the case of the three vertices on the far side of the edges of phi: they are adjacent to two phi vertices; the loss is at most 2 slides per state, still no equation.

## 5. What would still help (not claimed)

[open] A statement tying the lock paths P1, P2 of s to those of F(s) and B(s) (Try 1) is the only remaining lever. Theorem C says that after five forward steps the index returns, so the closed orbit s, F(s), ..., F^5(s) is a loop in the colouring space with a specific monodromy (colour permutation and component swaps); one could ask whether F^5(s) = s always. If F^5 = id on locked states, each orbit would have length exactly 5 and then the whole local picture at v is a pentagon of states; if F^5 is not the identity, orbits of length 5m, m ≥ 2, exist. I did not decide this; the Python harness above could test F^5 on locked states of small triangulations, but that is a statement about locked states (not targetless ones), so I have not run it.

## 6. Claim ledger

- Theorem C, Theorem D, meta-obstruction §4: [hand]; Theorem C's Claims 1 and 2 and index shift spot-checked [computed, 433 locked states, 0 failures].
- Clean vertex existence, F^5 = id question: [open].
- No other file edited; no status word changed; nothing committed.
