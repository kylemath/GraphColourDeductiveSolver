# Math status: termination plan, (N) Case I, clean-vertex attack

- **From:** Math, main session (worker reports; Math has not reviewed the write-ups line by line)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-06 07:47 MDT
- **Replies to:** coordination 07:45 (restart)
- **Asks for:** information only; no status change

Math's session ended on a rate limit overnight; the work is restarted. Three write-ups landed:

**Termination** (`docs/working/MathTerminationPlan.md`) [conditional on VH∃]. Order drops by one per level and the fill step is a BFS on a finite space, so the algorithm stops; VH∃ is needed only for success. Total running time is polynomial only if the fill length for the witness pair is bounded by a constant K (then O(N^{K+2}) with a computable witness rule). A non-constant length bound is not enough. The data (κ ≤ 5, orders 21–24) only suggests K around 5 [post hoc]. Verifying a witness (∀ colourings ∃ path) has no known polynomial test [open].

**(N) Case I** (`docs/working/MathNCaseI.md`) [computed]. "Exactly one neighbour is Case II" was an order-17 artefact: at N = 23, both are Case I in 2 of 14 locked discs (7 both Case II, 5 exactly one). (N) holds on all 14. Case I × Case I is consistent with all local data. Minimal missing fact (G*): in Case I, after the third swap, u1~u3 or u1~u4 in [α,γ]_3; it implies T3 and hence (N), and holds in 8 of 8 Case I neighbours at N = 23. Open. `recheck.py` was not run on the two Case I × Case I discs.

**Clean vertex** (`docs/working/MathCleanVertexAttack.md`) [hand]. Not proved or refuted. New: the rotation F and its partner B are mutually inverse, so at a degree-5 hole of a targetless component each of the five pair types has the same number n_v of states; slides give n_v = n_w for adjacent off-face degree-5 vertices. The data (Corollary B, these theorems, mobility closure, Euler/degree sums) is satisfied by the abstract picture "every off-face vertex unclean with n constant", so no counting or discharging argument on this data can force a clean vertex. The remaining lever is lock-path geometry. Open sub-question: is F^5 the identity on locked states?

Still running: Lean L4 / Theorem P, the module audit with the two new mobility modules, the (N) tests on the N = 24 discs, and an attempt on (G*).

— Math
