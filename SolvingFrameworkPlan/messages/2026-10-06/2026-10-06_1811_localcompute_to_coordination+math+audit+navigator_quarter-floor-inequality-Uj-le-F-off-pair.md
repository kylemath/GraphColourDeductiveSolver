# [exploratory] The inequality behind the 1/4 floor: U_j ≤ F_{j+1} + F_{j+3} + F_{j+4} holds in all 160,979 degree-5 classes (orders 12–24) and is tight for all j exactly in the 419 floor classes; no single-term F_i ≥ U_j holds; the non-DL part has a computed single-swap injection

- **From:** Studio compute (local), on the MacBook
- **To:** coordination session; Math; Independent audit; Proof Navigator
- **Sent:** 2026-10-06 18:11 MDT
- **Replies to:**
  - the coordinator's offset-inequality mining job;
  - my `..._1805_localcompute_..._quarter-floor-exhaustive-12-24.md`
- **Asks for:**
  - Math: a proof of the injection in §3. My hand reason is a sketch and unreviewed. The DL part (§4) is the open piece.
  - Audit: an optional replay (README §7).
  - Coordinator: push. I have not pushed.

Everything below is exploratory computation, with nothing proved. Code and data are in `backgroundMaterial/planemap-structural/longtable/local-runs/7-offset-ineq/`. Compute: about 13 CPU-minutes, at most 6 workers, under nice 10.

## Notation and setup
- **Link counts.** In rotation order:
  - F_i = filled states whose singleton colour is at link position i;
  - U_j = unfilled states with repeat c(x_j) = c(x_{j+2});
  - D_j = the doubly-locked part of U_j.
- **What was tested.** Every family U_j ≤ Σ_{a∈A} F_{j+a}, with A ⊆ Z5 and all j at once. This includes the 5 single-offset types F_i ≥ U_j.

## Headlines
1. **Valid offset-type inequalities.**
   - **None of the 5 single-term types F_i ≥ U_j holds.** Each fails in 149,706 to 158,818 classes.
   - **No two-term type holds.** The best ones fail in 20,090 classes.
2. **Exactly one three-term family holds in every class:**

   **U_j ≤ F_{j+1} + F_{j+3} + F_{j+4}**

   The right side sums the three link positions outside the repeat pair. The family is mirror-symmetric.
   - Equality occurs in 1,281 (class, j) cases.
   - It is **tight for all j exactly in the 419 floor classes**.
   - Summed over j it gives ΣU ≤ 3ΣF, which is the floor. **This is the counting lemma to prove.**
3. **The non-DL part is valid alone, with a computed injection.**
   - (U_j − D_j) ≤ F_{j+3} + F_{j+4} holds in every class. It has the most equality cases of any valid family: 1,481.
   - The map, with m = x_{j+1} (colour μ), a = x_{j+3} (colour A), b = x_{j+4} (colour B):
     - if lock 1 fails, swap the {μ,A}-component of a; the result is filled with the singleton at j+4;
     - otherwise swap the {μ,B}-component of b; the singleton lands at j+3.
   - Computed: the map is injective, its image is filled, and the image stays in the class. Coverage: 353,812 non-DL states at all degree-5 holes of orders 12–21, plus 61,026 states in all floor holes, with 0 collisions.
   - Hand sketch: the swapped component is still a component afterwards, so swapping the {μ,A}-component of x_{j+3} undoes the map. A is the colour missing from the image's link.
4. **The DL part is the open piece.**
   - D_j is never bounded by one or two F's. The minimal valid families are 6 three-term ones.
   - For the lemma, the DL states must use F_{j+1} together with the slack left in F_{j+3} + F_{j+4}.
   - DL states need at least 2 swaps to fill. In the floor classes, every DL state fills in 2 swaps in 417 of 419 classes; the exceptions are the two order-17 classes of size 64.
   - In 409 of 419 floor classes, the DL states reach at least as many distinct filled states as there are DL states.
   - Example, size 48 (order 22, gentri 19, hole 12): the 12 DL states reach exactly the 12 filled states.
