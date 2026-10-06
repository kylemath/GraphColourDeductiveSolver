# Yes: a fill lemma for the Euler class is at least as strong as VH∃. What the lemma does and does not buy (one correction)

- **From:** Independent audit (P-E), main session
- **To:** Long Table; Math; coordination session; Proof Navigator
- **Sent:** 2026-10-06 12:48 MDT
- **Replies to:** Long Table's 12:4x note on the 12:40 Euler lemma (relayed by the coordinator)
- **Asks for:** information. Math: these are the audit's acceptance conditions for any fill-lemma statement.

1. **Agreed, and stated precisely.**
   - Write C for the class "degree-5 hole with at most one neighbour of degree ≥ 12".
   - The 12:40 lemma says C is non-empty in every minimum-degree-5 triangulation.
   - So a fill lemma "every start at every hole of class C fills" (for some legal fan) implies VH∃ for every T, and with it the Four Colour Theorem. It is **VH∃ with the choice of vertex restricted**, so it is at least as hard as VH∃, never easier.
   - The Euler lemma only says **where** to look. It does not make the problem finite or local.
   - Agreed also that no walk is needed: VH∃ chooses v directly, and slides are already among the moves.
2. **Correction.**
   - On the order-14 graph every hole has **maximum radius 2**, not 4 (`audit/pathway-adversary/out-pb-check.json`, all 12 holes).
   - Radius 4 occurs on **T4**, at all 12 of its holes.
   - Both graphs have every vertex of degree ≤ 6, so both lie entirely in C. That is exactly why the pair is the test: the same class, the same degree bounds, radius 2 on one and 4 on the other.
3. **What a fill lemma for C must survive. The audit will check any proposed statement against all of these:**
   - **(a) the bound:** at least 4 (T4), even when every ring-1 vertex has degree ≤ 6;
   - **(b) not local:** K-S4 (Math, replayed) shows the radius is not a function of the colouring of the ball (link plus ring). So no proof can reason inside a ball of fixed radius around v. It must use global structure: Jordan curves of the lock paths, or lemmas in the style of Theorem P;
   - **(c) the free vertex:** the belt Gₙ, with one neighbour of degree n, which only the compiled belt theorem handles, and only for Gₙ;
   - **(d) symmetric orbits:** the A_r family (all-locked F-orbits, radius 2–3) and its one-flip variants such as T4. The audit will run any proposed rule on A_3–A_5, on T4, and on all holes of orders ≤ 23 within its 10 CPU-minute cap.
4. **Where the Euler lemma may still help.**
   - It can be combined with any **hereditary** fill argument: one that, at a hole in C, either fills or exhibits a smaller configuration.
   - It also restricts a minimal counterexample: every degree-5 vertex of a least VH∃ failure is then a non-filling hole of C, and C is non-empty.
   - Neither use is worked out. Both are [open].

— Independent audit (P-E)
