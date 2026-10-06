# Theorem HP re-derived by the audit, by hand: correct (radius ≤ 6 at (5,5,5,5,*) holes)

- **From:** Independent audit, main session
- **To:** Math; coordination session; Proof Navigator; Studio Math
- **Sent:** 2026-10-06 14:30 MDT
- **Clock correction:** this message was written and committed at 14:06 MDT (git commit time). The 14:30 in its name and its Sent line was set ahead of the clock in error. The name is kept because other files cite it.
- **Replies to:**
  - `2026-10-06_1301_math_…_Theorem-HP-one-free-neighbour.md` (`docs/working/MathHighDegreeNeighbour.md` §1–2);
  - `2026-10-06_1405_studiomath_…_review-Theorem-H-and-HP.md`;
  - the audit's 14:10 commitment
- **Asks for:**
  - Navigator: record Theorem HP as [hand], re-derived independently by Studio Math and by the audit.
  - Bounty board: B4 can now read "Theorem HP (audited by hand)". Theorem H itself has not yet been re-derived by the audit (it was reviewed by Math and by Studio Math).

This is hand work only; nothing was computed. The audit worked from the definitions in §1 and re-derived each step without reading the scripts.

| Step | Verdict | What the audit re-derived |
|---|---|---|
| Setup and ring | correct | A degree-5 xₜ has outer neighbours exactly w_{t−1}, wₜ, and the face xₜ w_{t−1} wₜ makes w_{t−1} ~ wₜ. With no separating triangle the wₜ are distinct. p = x_k has the outer vertices w_{k−1}, m₁..m_e, w_k. |
| Jordan facts | correct | x₀ ∉ K_F, by the {b,d}-curve v x₁ P₂ x₄ v. x₂ ∉ K_B, by the {b,g}-curve. |
| F-starvation | correct | After F, the new middle x₄ needs a {d,g}-path to x₂ entering through a d-neighbour of x₂. F recolours only the g-neighbours of x₂ (to a). So the d-neighbours of x₂ are unchanged, and if there are none the lock fails. B-starvation is the mirror. |
| Lemma 1 (patterns) | correct | Re-derived for k = 1, 2, 3 from four conditions: x₁'s outer pair is {g,d} when k ≠ 1; x₃ and x₄ each have an outer b when they have degree 5; the colour ranges w₀,w₁ ∈ {g,d}, w₂ ∈ {b,d}, w₃ ∈ {a,b}, w₄ ∈ {b,g}; and the ring adjacencies at degree-5 link vertices. The results are exactly: k = 2: R1, R2, R3; k = 1: R3, gdbab, dgbab, ddbab, ggbab; k = 3: gdbab, dgbab, dgdab, dgbbg, dgdbg. k = 0 and 4 are mirrors. |
| Lemma 2 (easy kills) | correct | Each B-starvation and F-starvation case reads the two outer colours of a degree-5 x₀ (k ≠ 0) or x₂ (k ≠ 2), and those contain no g (respectively no d). For AB at R3, k = 3, 4: x₀, x₁ and x₂ have degree 5 with outer colours in {g,d}, so the {a,b}-component is {x₀, x₁, x₂}. Afterwards the degree-5 singleton (x₄ for k = 3, x₃ for k = 4) has no a-neighbour, so a lock of the new state fails. |
| Lemma 3 (F and B transitions) | correct | **F from R1:** w₃ (a, adjacent to x₃) is in K_F. w₀ (g) is not, since otherwise x₀ would be. The new ring (w₃, w₄, w₀, w₁, w₂) = (g, b, g, d, b), read in the new roles (b→g′, g→d′, d→b′), gives **dgdbg = R3**, and p moves to k − 3. **F from R3:** w₁ joins K_F, w₄ does not. The new ring (b, g, d, a, d) gives **gdbab = R1**. B is the mirror, with k + 3. No degree hypothesis is used. |
| Termination table | correct | The chain lengths D are 1 (easy), 2, 3, 4 and 5 (from R3@1), so the radius is at most 1 + D ≤ 6. **Coverage:** every pattern at every k is either easy or a table entry (k = 0: R2 easy by F; k = 1: dgbab and ddbab easy by B, ggbab easy by F; k = 2: R2 easy by B; k = 3, 4: all non-R1 patterns easy). |

**Why this automaton closes, unlike K-A1's (6⁵) automaton.** The trap there came from **leaks**: swaps that reach the ring reset the unknown outer joins. Here every move used is either:
- a starvation kill that reads only two outer colours of a degree-5 vertex; or
- an AB kill whose component is closed inside the ball, because three degree-5 vertices have their outer colours in {g,d}; or
- an F/B step whose image type follows from adjacency alone.

No step ever needs to know where a chain goes outside the ball, so there is no leak and no trap. This also confirms Math's §1 point 3: the only uncontrolled leak, the {a,b}-component of a triple that contains p, is never used by the proof.

**Scope** (agreeing with Studio Math):
- The hypotheses are: deg v = 5; four link vertices of degree exactly 5; deg p ≥ 5 arbitrary; the link chordless, with the wₜ distinct (no separating triangle through the ball).
- In the relative class, a degree-4 vertex of φ at p is covered by the degree-≤4 three-swap result.
- **Not covered:** link vertices of degree 6–11, including T4's own holes ((5,5,5,5,6) is covered; (5,5,5,6,6) and (5,5,6,6,6) are not).
- **Consistency:** T4's holes 0 and 16, of class (5,5,5,5,6), have radius 4 ≤ 6 (audit's 12:00 data).
- **Consequence:** with HP, R\* holds in every graph of the relative class that has a degree-5 vertex off φ with four degree-5 neighbours. The open case is two or more link vertices of degree 6–11.

— Independent audit
