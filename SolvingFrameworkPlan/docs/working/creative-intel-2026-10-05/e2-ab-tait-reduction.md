# E2 after AB: exactly when each new lock holds (Long Table, 6 Oct 2026, about 14:45 MDT)

[hand]: written by Long Table on the MacBook, nothing computed (user's 13:01 rule). Not yet reviewed. Notation from `rstar-tait-angle.md` (§1–2) and `explore-vhphi/pathways/pd2_lock_proof.md`. The setup is Intern A cycle 3 (`docs/working/interns-2026-10-06/intern-A-cycle3.md`).

## Setup

E2: link x0..x4 = (a,b,a,g,d); ring w0..w4 = (d,g,d,a,g), where w_i is the outer apex on x_i x_{i+1}; m3 = m4 = b. x0, x1 and x2 have degree 5, and x3, x4 have degree 6. The state s is doubly locked (DL).

In Z2×Z2 put β = a+b = g+d, γ = a+g = b+d, δ = a+d = b+g. The P-edges (e_t dual to x_t x_{t+1}) are e0 = e1 = e3 = β, e2 = γ, e4 = δ, so j = 0 and the middle edge is e3.

**AB is the W-swap.** The cut of {x0,x1,x2} consists of the eight edges e2, x2w2, x2w1, x1w1, x1w0, x0w0, x0w4, e4, all coloured γ or δ, alternating. That is exactly the (γ,δ) P-path W of the normal form, here the short one. AB swaps γ and δ along it. Call the result s′.

**Hooks.** Each of W's seven nodes has one β-edge:
- b1 = x3w2, b2 = w1w2, b4 = w0w1, b6 = w0w4 and b7 = x4w4 point away from P;
- e1 and e0 point to P.

Together with the free P-edge e3, the outward hooks in cyclic order around the outer region are (e3, b1, b2, b4, b6, b7). The outer region is a disc, because W ∪ P bounds the disc containing x0, x1, x2.

## Lemma (exact criterion) [hand]

Let s be DL in E2. Then:
- **lock_ag holds after AB** (an {a,g}-path from x1 to x3 in s′) **iff the (β,δ) P-path Y2 of s does not use the edge dual to x2w2**. Equivalently, the (β,δ)-component of s through x2w2 is a closed cycle.
- **lock_ad holds after AB** (an {a,d}-path from x1 to x4 in s′) **iff the (β,γ) P-path Y1 of s does not use the edge dual to x0w4**. Equivalently, the (β,γ)-component of s through x0w4 is a closed cycle.

*Proof.* Inside W the (β,δ)-edges of s pair the hooks as b1–b2 (via x2w2), e1–b4 (via x1w1), e0–b6 (via x0w0) and e4–b7. Outside W the (β,δ)-subgraph is a non-crossing perfect matching M of the hooks (e3, b1, b2, b4, b6, b7). Of the five such matchings, exactly two make Z2 return by e0 and Y2 return by e1, which s needs because it is DL:
- M1 = {e3b1, b2b4, b6b7}: here Y2 = e3 ~ b1 − x2w2 − b2 ~ b4 − e1;
- M3 = {e3b4, b1b2, b6b7}: here Y2 = e3 ~ b4 − e1, and b1 − x2w2 − b2 closes into a cycle.

In s′ the colour a+d is carried by the δ-edges of s off W and the γ-edges of s on W. So inside W the (β, a+d) pairing becomes e2–b1, b2–e1, b4–e0 and b6–b7, and outside nothing changes. By the lock criterion applied to s′ (repeat colour b, middle x1, odd edges e2 and e4), lock_ag of s′ holds iff the (β, a+d)-path from e2 returns by e1:
- under M1 it runs e2 − b1 ~ e3, and returns by the middle edge, so the lock fails;
- under M3 it runs e2 − b1 ~ b2 − e1, so the lock holds.

The (β,γ) case is the mirror image. Inside W the (β,γ) pairing of s is e2–b1, b2–e1, b4–e0 and b6–b7. DL leaves N3 = {e3b4, b1b2, b6b7} or N4 = {e3b7, b1b2, b4b6}. Under N4, Y1 = e3 ~ b7 − x0w4 − b6 ~ b4 − e0. In s′ the pairing becomes b1–b2, b4–e1, b6–e0 and b7–e4. So the path from e4 runs e4 − b7 ~ b6 − e0 under N3 (lock holds) and e4 − b7 ~ e3 under N4 (lock fails). ∎

No degree beyond those of the setup is used. (The degree-5 hypothesis on x0, x1, x2 fixes W's shape.)

## Consequences

1. **AB fails to kill E2 iff M3 and N3 both hold.** In that case Y1 and Y2 both run from e3 to the *same* hook b4 = w0w1 without touching W: Y1 enters P by e0 and Y2 by e1. Leaving T(x3x4w3), Y1 crosses x3w3 and then w3m3, and Y2 crosses x4w3 and then w3m4. Their next steps depend on w3's other neighbours. **When deg w3 = 6, with Intern A's rotation (x3, x4, m4, y2, y1, m3) where y1 is g and y2 is d, follow the colours.**
- Y1 crosses w3y1 (γ), and Y2 crosses w3y2 (δ).
- Both reach the node T(w3y1y2), and both leave it by the β-edge y1y2.
- So together they wrap around the single vertex w3.

(This is not a new proof of Intern A's Proposition, which concerns the vertex paths of s′. It is the picture of the same configuration in s.) By the same argument at the other end, they share b4 and wrap around the apex r of the outer triangle on w0w1.
2. **A prediction the Studio's records can check in about a second:** in all 500 deg-6 records, Y2 uses x2w2 and Y1 uses x0w4 (M1 and N4). In the 24 records where lock_ag holds, Y2 avoids x2w2; in the 24 where lock_ad holds, Y1 avoids x0w4. If any record disagrees, this page has an error.
3. **The remaining gap, stated exactly.** Prove that a DL state in E2 cannot have both Y1 and Y2 run from e3 to w0w1 while avoiding W. The data say that x1's new components never reach N(w3). In this language that means: in each record Y2 runs *through* x2w2 and Y1 *through* x0w4, so after AB the new paths are short-circuited back into W at once, far from w3.
   - What I tried and did not finish: a parity count on the lens bounded by Y1 and Y2 between y1y2 and b4. Every cut has n_β ≡ n_γ ≡ n_δ (mod 2), and the pentagon node respects this because its counts (3,1,1) are all odd. The count gives only that the inward γ- and δ-edges along the lens are even in number, not a contradiction.
   - Studio intel's suggested barrier (old locks L1 and L2) appears here as Z1 and Z2. Z1 = e2 − b1 ~ b2 − e1 runs alongside the (β,δ) cycle through x2w2 when M3 holds; Z2 runs alongside the (β,γ) cycle through x0w4 when N3 holds. Under M3 ∧ N3 the hooks b1, b2 and b6, b7 each carry two outside paths of different colour pairs. Either a crossing argument there will close the gap, or a counterexample will be built from it.

**Not claimed:** E2 has radius ≤ 2 in general. What is proved is the equivalence above, which reduces the sub-case to one exact statement about two P-paths.
