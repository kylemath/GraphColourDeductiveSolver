# Review: Theorem F5 (quarter floor at (5,5,5,5,5) holes)

Adversarial review, 7 October 2026 (written 01:19 MDT), of `NightFloorAtEasyHoles.md` §1–§4 (commit 6826897).
Inputs re-read: `QuarterPi.lean` (π table, λ), `QuarterWinding.lean` (`lam_eq`, `sum_lam`, `quarterFloor_iff_lam`), `QuarterRotationPlanar.lean` (Lock2 ⇔ R₊₃ defined, image has Lock1, x_j ∉ K), `MathRadiusGeometry.md` (Theorem H, Steps 1–4).

## Verdict: PASS

The hand proof is correct as written, modulo four cosmetic points (§5). No gap found. The independent recomputation agrees on every checked claim. One reported tally in §4 of the source note does not reproduce: the transition counts.

## 1. Lemma 1: exact form

From the formal table:
- U with Lock2 → R₊₃, λ = +1, and the image has Lock1;
- U without Lock2 → φ_B⁻¹, λ = −1, and the image is filled;
- F with M3 short → φ_A, λ = −1, and the image is U without Lock1;
- F with M3 long → τ, λ = −3, and the image is filled.

**Runs.** In an unfilled run s₁…s_u:
- s₁,…,s_{u−1} have Lock2, and s_u lacks it;
- s₂,…,s_u have Lock1, being R₊₃ images;
- s₁ lacks Lock1 when it follows a filled state (φ_A image).

So the DL states are exactly s₂…s_{u−1}, and the DD steps number max(u−3, 0).

**Neither lock ⇔ u = 1.**
- (⇐) A run of length 1 starts after a filled state, so s₁ lacks Lock1, and it ends, so s₁ lacks Lock2.
- (⇒) A state without Lock1 is not the image of an R₊₃ step, so its predecessor is filled. A state without Lock2 ends its run.

So the N₀ accounting is exact.

**States with Lock1 but not Lock2** are exactly the run ends s_u with u ≥ 2. Each has λ = −1, and it is already included in the run sum.

**Excursion sum.** Writing f for the filled-run length, an excursion has (u − 1) − 1 − 3(f − 1) − 1 = u − 3f.

**All-filled π-cycles** (all τ, sum −3L) are omitted from the source proof. They are harmless.

**Exact identity (per class):**

  Σλ = |DD| − 2N₀ − E₂ − 3·#τ,

where:
- E₂ = the number of excursions with u = 2;
- #τ = the number of filled states with M3 long.

Lemma 1 follows, since E₂ and #τ are both ≥ 0. The identity was checked on every class (§4).

## 2. Lemma 2: does Theorem H apply to the π-step?

Yes. H's "F" swaps the {a,g}-component of x₂. In the role dictionary (a,b,g,d) = (α,μ,A,B), that is the {α,A}-component of x_{j+2}: the same seed and the same component as R₊₃ (`rot3`). The ring patterns match: H's R1, R2, R3 are the note's R1, R2, R3.

I rederived all three steps.

**Step 1 (the ring is forced).**
- x₁ = μ needs an A-neighbour (Lock1) and a B-neighbour (Lock2) among w₀ and w₁.
- The entry vertices of x₃ and x₄ then force R1, R2 or R3.
- This uses w_t ~ w_{t+1} and the degree-5 neighbour lists.

**Step 2 (R2).**
- After the swap, x₂ = A. Its neighbours are x₁ (μ), x₃ (α), w₁ (α, since it is in K) and w₂ (μ).
- The image's Lock2 is a {B,A}-path from x₄ to x₂, so it must enter x₂ through a B-vertex. There is none.
- So the image is not DL.

**Step 4 (R1).**
- K contains x₂, x₃ and w₃.
- K misses w₀, because w₀ ∈ K would put x₀ in K, and x₀ ∉ K is formal in QRP (the Jordan step).
- The image ring, read from w₃, is (A, μ, A, B, μ) = (B′, A′, B′, μ′, A′), which is pattern R3.
- This holds whether or not the image is DL.

So every DD step has an R3 endpoint.

## 3. Lemma 3

**Component.** The full neighbour lists are known because x₀, x₁ and x₂ have degree 5:
- x₀: v, x₄ (B), x₁, w₄ (A), w₀ (B);
- x₁: v, x₀, x₂, w₀ (B), w₁ (A);
- x₂: v, x₁, x₃ (A), w₁ (A), w₂ (B).

The outer neighbours of x₀, x₁ and x₂ are w₄, w₀, w₁ and w₂. In R3 these are coloured A, B, A, B, none of them α or μ. So K = {x₀, x₁, x₂} exactly.

**Locks after the swap.**
- Lock1′ is an {α,A}-path from x₁ to x₃. The neighbours of x₃ are μ, B, B, μ, so it has no α-neighbour, and Lock1′ dies.
- Lock2′ is an {α,B}-path to x₄. The neighbours of x₄ are A, μ, μ, A, so it has no α-neighbour, and Lock2′ dies.
- This uses deg x₃ = deg x₄ = 5.

**Charging.**
- σ keeps the repeat index j, and swapping the same vertex set again returns t. So σ is injective.
- Each R3 state lies on at most two DD steps (π⁻¹r → r and r → πr), so the map from DD steps to R3 states is at most 2-to-1.
- σ(r) is a single Kempe swap, so it stays in the same class.
- Hence |DD| ≤ 2·#R3DL ≤ 2N₀.

## 4. Hidden assumptions

- **Planarity and orientation.** These enter only through the formal QRP facts. No reflection is used, and the mirrored run also passes.
- **Separating triangles.** These are not needed.
  - Degree 5 in a simple triangulation already forces w_t ∉ N[v], w_t ≠ w_{t+1} and w_t ~ w_{t+1}.
  - A coincidence w_t = w_{t+2} needs a separating triangle. It only adds colour equalities, and every step above is a check on neighbour colours, so the steps survive.
  - However, the statement in §3 says "IcoBall" while Verdict 3 says "every (5,5,5,5,5) hole". The data (gentri: 4-connected, minimum degree 5) cannot test the coincidence case.
- **Icosahedral cap.** This is not forced, since ring-2 degrees are free from order 17 on, and it is not used. Only ring-1 neighbour lists and ring-2 colours enter.

### Recomputation

Method: an independent script (`rev_f5.py`, session scratchpad).
- It reimplements π, the locks and λ from the QuarterPi table. It agrees with `escape.pi_of` on all 4,858 states at orders 17 and 20.
- Per class it checks: pointwise W, π preserving the class, the full ring pattern (all five w), Lemma 2 transitions, Lemma 3 (K equals the exact vertex set, lockless, same class, σ injective), the exact identity above, the chain |DD| ≤ 2·R3 ≤ 2N₀, and Σλ ≤ 0.
- It ran on orders 12–20 (42 holes) and then on 21–22, both orientations: 270 holes and 326 classes per orientation.

Results:
- 0 failures.
- The maximum class Σλ is −20.
- The bound is tight at 17 (both holes, both orientations).

| order | holes | DD | N₀ | R3 DL |
|---|---|---|---|---|
| 12 | 12 | 0 | 240 | 0 |
| 17 | 2 | 80 | 40 | 40 |
| 18 | 2 | 16 | 64 | 16 |
| 19 | 5 | 40 | 260 | 46 |
| 20 | 21 | 316 | 1748 | 272 |
| 21 | 50 | 764 | 4376 | 878 |
| 22 | 178 | 3490 | 22246 | 4176 |

Orders 14 and 16 have no (5,5,5,5,5) holes.

## 5. Cosmetic points

1. **Transition tally.** §4 of the source reports DD R1→R3 = 2,242 and R3→R1 = 2,261. I get 2,353 each (orders 12–22, both orientations). The author's script classifies type from w₀ and w₃ only, which may explain the difference. The proof does not depend on this tally.
2. **Lemma 2 wording.** The R2 case says x₂ "loses its only B-neighbour". x₂ never had a B-neighbour. The point is that it has none after the swap.
3. **Lemma 1 proof.** It omits all-filled π-cycles. Use the exact identity of §1.
4. **Scope of the statement.** It should name its hypothesis: a triangulated spherical map, with v and x₀..x₄ of degree 5. IcoBall distinctness is not needed.
