# Night: the quarter floor at (5,5,5,5,6) holes (Theorem F6 attempt)

Night worker, 7 October 2026 (written 01:36 MDT). **Exploratory. Hand proofs plus single-core checks. Unreviewed.**

Cited notes:
- **F5** = `NightFloorAtEasyHoles.md`, reviewed PASS in `NightF5Review.md`. That review gives the exact per-class identity Σλ = |DD| − 2N₀ − E₂ − 3·#τ.
- **HP** = `MathHighDegreeNeighbour.md` §1–§2, reviewed CORRECT in `MathReviewTheoremHP.md`. It provides the pattern table (Lemma 1), F/B-starvation, and the F/B transitions (Lemma 3).
- **QRP** = `QuarterRotationPlanar.lean`. It provides R₊₃ as a bijection from {repeat j, Lock2} to {repeat j+3, Lock1}, the fact x_j ∉ K, and `kempe_hex`.

Labels: [proved] means a complete argument modulo the cited reviewed or formal facts; [conjecture] means not proved; [data] means computed by the scripts in §6.

Frame: as in HP. The link is (a,b,a,g,d) = (α,μ,α,A,B) on x₀..x₄ (relative to the repeat j). The ring w₀..w₄ is written as a pattern in these letters, and @k gives the position of the degree-6 vertex p = x_k. F = R₊₃ is the π-step on Lock2 states, and σ is the {α,μ}-swap at x₁ (as in F5).

## Verdict

1. **Theorem F6 is not proved.** It is reduced to one counting statement about a single kind of DD step (Conjecture C1, §4). C1 holds with 0 failures on 1,086 holes at orders 16–22 (2,172 hole-orientations).
2. **Every DD step falls into one of three kinds [proved]:**
   - **T-steps:** four "terminal" types. These are paid **injectively by E₂ excursions** via a new one-vertex recolouring ψ (Lemma B). This is a new payer that F5 did not need.
   - **X-steps:** R1↔R3 steps whose R3 endpoint has a σ-exit. These are paid by N₀ exactly as in F5, at most 2 per state.
   - **D₀-steps:** R1↔R3 steps with no σ-exit. These are what remains, and C1 is about them.
3. **Answer to plan step 1: no.** The σ-exit does not fail exactly when p ∈ {x_j, x_{j+1}, x_{j+2}}. Exit failures occur at **every** position k of p relative to the R3 endpoint, and for a forced local reason (Lemma D):
   - At degree 6, the single extra neighbour m of p has a **forced colour** at an R3 state.
   - At k = 0, 1, 2, m joins σ's component (|K| ≥ 4).
   - At k = 3, 4, |K| = 3, but m is an α-neighbour of p, so the lock ending at p survives σ.
   - A degree-7 vertex has two extra neighbours, and these are not forced. This is the 2-ball contrast with (5,5,5,5,7) that the coordinator asked about.
4. **Plan step 2 is refuted [data]:**
   - A τ state is never one swap away from either endpoint of a DD step: 0 of 648 D₀-steps have one, orders 16–21. Both endpoints of a DD step are DL, and the data shows this one-swap gap; I have no general proof.
   - The best capacity-3 assignment of D₀-steps to τ states within 2 swaps leaves steps uncovered at 120 of the 174 hole-orientations that have D₀-steps. Within 3 swaps it still fails at 14.
   - The first failure is gentri **17 #3, hole 0**. It has 14 D₀-steps; at most 3 can be covered within 2 swaps and at most 10 within 3.
   - So no ≤2-swap τ charging exists.

## 1. Classification of DD steps [proved]

**Lemma A.** At a (5,5,5,5,6) hole (no separating triangle), every DD step t → πt = F(t) is one of the following:
- **R-steps:** R1@k → R3@k+2, or R3@k → R1@k+2, for any k.
- **T-steps:**
  - T1: ddbab@1 → dgbbg@3;
  - T2: dgbab@2 → dgbag@4;
  - T3: dgdab@3 → dgbab@0;
  - T4: dgdbb@4 → ggbab@1.

The image of a T-step is F-starved, so a T-step is the last DD step of its run.

*Proof.*
- HP Lemma 1 lists every DL pattern.
- F-starvation (HP §1, any degrees) needs x₂ ≠ p and w₁, w₂ ≠ d. It kills dgbab@0,1,3,4, ggbab@1, dgbbg@3 and dgbag@4 as DD starts.
- HP Lemma 3 handles R1 and R3.
- That leaves ddbab@1, dgbab@2, dgdab@3 and dgdbb@4. For these, K_F contains x₂ and x₃, plus:
  - w₃ when w₃ = a (it is adjacent to x₃);
  - w₁ when w₁ = g (it is adjacent to x₂).
- Every other ring vertex is coloured b or d. x₀ ∉ K_F by QRP.
- The new frame is j' = 3 with a→a, d→b, b→g, g→d. Reading (w₃, w₄, w₀, w₁, w₂) gives the four images listed, at k − 3.
- Each image has x_{j'+2} ≠ p and (w₁, w₂) = (g, b), so it is F-starved: its π-image lacks Lock2. ∎

## 2. T-steps are paid by E₂ [proved]

Every T-start is **B-starved**: (w₄, w₀) = (b, d) and k ≠ 0. So x_j has neighbours coloured μ, B, μ, B, and its {α,A}-component is {x_j}.

Every T-image u has (w₁, w₂) = (g, b) and k ≠ 2. So x_{j_u+2} has no α- or B-neighbour, and its {α,B}-component is a singleton. This vertex is the same vertex as x_{j_t}.

**Lemma B.** Let t → u be a T-step. Define:
- ψ(u) = u with x_{j_u+2} recoloured α → B;
- ρ(t) = t with x_{j_t} recoloured α → A.

Then:
- ψ(u) lacks Lock1 and has Lock2;
- π(ψ(u)) = ρ(t), which has Lock1 and lacks Lock2.

So {ψ(u), ρ(t)} is an unfilled run of length exactly 2, that is, an E₂ excursion. The map t ↦ ψ(u) is injective.

*Proof.* Work in u's frame (j = 0, link a,b,a,g,d). u is DL with lock paths P₁ ({b,g}, from x₁ to x₃) and P₂ ({b,d}, from x₁ to x₄). Neither path uses x₂.

1. **ψ(u).** Its link is (a,b,d,g,d), with frame j' = 2 and roles (α′, μ′, A′, B′) = (d, g, a, b).
   - Lock1′ would be a {g,a}-path from x₃ to x₀. The curve v x₁ P₂ x₄ v separates x₀ from x₃, and its colours are disjoint from {g,a}, so there is no such path.
   - Lock2′ is a {g,b}-path from x₃ to x₁, and P₁ is one.
2. **π(ψ(u)).** π(ψ(u)) = R₊₃ swaps the {d,a}-component of x₄. That component is K′ = K_B(u), the B-move component of u, because x₂ is {a,d}-isolated.
   - K_B(u) is K_F(t): the {a,g} (= {α_t, A_t}) component of x_{j_t+3} in u. So swapping it gives back t, since B = F⁻¹.
   - Hence π(ψ(u)) = t with x_{j_t} recoloured, which is ρ(t).
3. **ρ(t).** In t's frame, ρ(t) has repeat j + 3, with Lock2″ an {α,B}-path from x₂ to x₄ that avoids x₀.
   - t's Lock1 path ({μ,A}, from x₁ to x₃) separates x₂ from x₄, so ρ(t) has no Lock2″.
   - Its Lock1″ is t's Lock2 path.
4. **Injectivity.** u is recovered from ψ(u) by recolouring x_{j'} back to the colour of x_{j'+3}, and t = π⁻¹u. ∎

[data] Lemma B, including the identity π(ψ(u)) = ρ(t), checked on all 1,838 T-steps at orders 16–22, both orientations: 0 failures. It also holds at (5,5,5,5,7) holes: 700 T-steps at orders 17–22, 0 failures.

## 3. R-steps: σ and the forced sixth neighbour [proved]

**Lemma C (F5, unchanged).** σ is an involution on unfilled states, and each R3 state lies on at most 2 DD steps. So the X-steps (σ(r) lockless, where r is the R3 endpoint) satisfy #X ≤ 2N₀. This needs no |K| = 3 hypothesis.

**Lemma D (forced m).** Let r be DL of type R3 = dgdbg with p = x_k of degree 6, and let m be p's outer neighbour other than w_{k−1} and w_k. Then m is adjacent to p, w_{k−1} and w_k (the two faces at m), and those three are coloured with three distinct colours. So the colour of m is forced:

| k | m | consequence for σ at r |
|---|---|---|
| 0, 2 | μ | m ∈ K, so |K| ≥ 4 (leak) |
| 1 | α | m ∈ K, so |K| ≥ 4 (leak) |
| 3 | α | K = {x₀,x₁,x₂}; Lock2′ dies at x₄ (HP Lemma 2), but Lock1′ can enter p through m |
| 4 | α | K = {x₀,x₁,x₂}; Lock1′ dies at x₃, but Lock2′ can enter p through m |

**Contrast with degree 7.** At degree 7, p has two extra neighbours m₁ ~ m₂. Colourings exist with no leak and no α-neighbour, for example m₁ = A, m₂ = B at k = 1, or m₁ = μ, m₂ = B at k = 3. So nothing in the 2-ball forces the exit to fail. This is the 2-ball reason why (5,5,5,5,7) is F5-type at order 17. It is **not** a proof for degree 7, because D₀-steps also occur at (5,5,5,5,7) from order 19 on (1,100 at orders 19–22).

[data] D₀-steps by the k of their R3 endpoint, orders 16–22 (both orientations, summed), with the lock status of σ(r):

| k | D₀-steps | σ(r) lock status |
|---|---|---|
| 3 | 563 | always Lock1 only |
| 4 | 563 | always Lock2 only |
| 0 | 407 | mostly DL |
| 1 | 412 | mostly DL |
| 2 | 407 | mostly DL |

In the k = 0, 1, 2 rows σ(r) is mostly DL, often inside the same long run.

## 4. Reduction of F6 [proved] and the missing lemma [conjecture]

From the exact identity together with Lemmas A, B and C, the floor Σλ ≤ 0 for a class follows from:

**Conjecture C1.** #D₀ ≤ (2N₀ − #X) + (E₂ − #T) + 3·#τ per class.

Two stronger forms also hold on the data.

| form | result, orders 16–22 (2,172 hole-orientations, 1,086 holes, 1 class each) |
|---|---|
| **C1′:** #D₀ ≤ 3·#τ | 0 failures |
| **C1″:** #D₀ ≤ 2N₀ − #X (spare N₀ capacity alone) | fails only at **gentri 17 #3, holes 0 and 16** (both orientations) |

At 17 #3 hole 0:
- DD = D₀ = 14, N₀ = 4, τ = 8, E₂ = 2, Σλ = −20.
- The 15 DL states form a single run of length 17 inside a π-cycle of sum 0.
- In that cycle the run is paid exactly by its own 4 τ and 2 E₂ (14 = 12 + 2). This is π-local, not Kempe-local.
- The π-distance from a D₀-step to its nearest τ reaches 21 or more on the data.
- 27 D₀-steps (orders 16–21) lie on π-cycles that contain no τ at all.

**The local lemma still needed:** an injection, with capacity 3, from D₀-steps into τ states (or into the spare N₀ and E₂ capacity), built from Kempe paths of bounded length. By the radius tests above, those paths would need at least 3 swaps, possibly 4.

Charging multiplicities found (orders 16–22, summed):

| order | T → E₂ (multiplicity 1) | X → N₀ | N₀ load 1 / 2 | D₀ |
|---|---|---|---|---|
| 16 | 8 | 8 | 8 / 0 | 0 |
| 17 | 0 | 0 | 0 / 0 | 56 |
| 18 | 0 | 4 | 4 / 0 | 4 |
| 19 | 12 | 58 | 30 / 14 | 10 |
| 20 | 176 | 362 | 126 / 118 | 102 |
| 21 | 300 | 824 | 332 / 246 | 476 |
| 22 | 1,342 | 3,976 | 1,496 / 1,240 | 1,704 |

Every class at every order passes the identity check and Σλ ≤ 0. The first hole where the naive charging (σ plus ψ) fails is **gentri 17 #3, hole 0**.

## 5. Next step

Try to prove C1′ along π instead of Kempe distance. A long R-run cycles the position of p with period 10 (R3 positions k, k−1, …). Lemma D says which R3 states leak. The candidate is an excursion-level statement: a maximal block of consecutive D₀-steps in one run is bounded by 3 × the number of τ in the adjacent filled runs plus E₂. This is the "long M3" link the coordinator suggested. Untested.

## 6. Reproduction (session scratchpad `f6/`, not committed)

| script | what it checks | run time |
|---|---|---|
| `verify2.py 16,…,22` | Lemma A, Lemma B (ψ, ρ, E₂, injectivity), Lemma C, Lemma D sizes and locks, C1/C1′/C1″ | 45 s |
| `DEGS=55557 verify3.py` | the same checks at (5,5,5,5,7) holes | 37 s |
| `d0tau.py` | radius-R matchings of D₀-steps into τ, and π-distances | about 10 s |
| `match.py` | matchings into all payers, radius 1–4 | seconds |

All runs used one core on AC power.
