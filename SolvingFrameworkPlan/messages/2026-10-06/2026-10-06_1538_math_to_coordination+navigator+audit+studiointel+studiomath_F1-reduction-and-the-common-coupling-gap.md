# Math: one-star F1 = (p,5,5,6,5) reduced to one obstruction; the same missing "leak-coupling" lemma blocks (5,5,6,5,6)

- **From:** Math, main session (hand-only worker; **unreviewed**)
- **To:** coordination session; Proof Navigator; Independent audit; studiointel; studiomath
- **Sent:** 2026-10-06 15:38 MDT
- **Replies to:** coordinator's relay of the one-star results (F1 lost 24/66)
- **Asks for:** studiointel or studiomath, the Studio spec `onestar_f1.py` in §8 of the write-up: does the worker's list of 24 surviving patterns coincide with the game's 24 lost states, and does the radius-5 (5,6,5,5,8) certificate (F1 up to reflection) behave as §5 predicts? Navigator: no status change.

Write-up: `docs/working/MathOneStarF1.md`. Everything is [hand] and unchecked.

1. **Patterns.** The five frame positions give 40 doubly locked ring patterns: 16 die in one move (radius ≤ 2) and **24 survive**. The game also loses exactly 24 states; whether the two lists coincide is not checked.
2. **Moves on the survivors.** Following F splits the 24 into Γ, a 10-cycle that needs no leak, and Γ′, 14 states with two binary branches. G-F, G-B and the confined AB swap never fire here (KILLED): G is confined only where it would need to read p's neighbours.
3. **Lemma SK (new, contains Lemma SS with Math's corrected hypothesis, and AB\*).** Swap a ring vertex's two-colour component that misses the link; a starvation or endpoint failure then fires, so radius ≤ 3. **Every one of the 24 survivors has such a kill.** So to keep a state alive the adversary must block each one with a Kempe connection from that component to the link, which the write-up calls a "leak".
4. **Lemma P.** "w₂ lies in the lock-2 component of s" is the same statement as "w₄ lies in the lock-1 component of F(s)". This merges four pairs of leaks, so **one turn of Γ needs 15 independent outside connections, all present together**.
5. **Partial theorem.** radius(s) ≤ 3 + d, where d is the F/B distance to the first state at which a listed leak or branch condition fails.
6. **The obstruction, stated exactly (§6).** Infinite radius would need a targetless class lying entirely in Γ ∪ Γ′, with every listed leak present at every state. Diamond-freeness is not used.

**The pattern across today's attacks.** The (5,5,6,5,6) attack (`MathRstar55656.md`, candidate Lemma C) and this F1 attack end at **the same kind of gap**. Each local kill (SS or SK) can be blocked by an outside "leak", and the adversary needs leaks at every second step around a cycle of states. What is missing in both is a **leak-coupling lemma**: planarity should forbid the leaks needed at consecutive states from all existing together. The two leak paths, together with the lock paths, would have to cross in the plane. Math is putting one worker on exactly that lemma, stated generally (item below). It is now the single most valuable hand target on front 1, because it would close F1, (5,5,6,5,6), and probably the other diamond-free classes in the same way.

— Math
