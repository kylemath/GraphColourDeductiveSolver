# Night: the quarter floor at the easy holes

Night worker, 7 October 2026 (written 01:13 MDT). **Exploratory. Hand proof plus single-core checks. Unreviewed.**

Cited notes:
- **QW** = `StudioMathLean/.../PlaneMap/QuarterWinding.lean` (Theorem W, formal);
- **QP** = `QuarterPi.lean` (π and the λ table, formal);
- **QRP** = `QuarterRotationPlanar.lean` (R₊₃ is defined ⇔ Lock2; its image has Lock1);
- **RG** = `MathRadiusGeometry.md` (Theorem H, Steps 1–4; review verdict CORRECT);
- **CL** = `NightConfigurationLead.md`.

Labels: [proved] means a complete argument modulo the cited formal or reviewed facts; [sketch] means the gap is named; [conjecture] means not proved; [data] means computed by the scratchpad scripts in §6.

## Verdict

1. **The per-cycle statement is false at (5,5,5,5,5)** [data, from run 23 and re-checked here]. Gentri 17 #4 (1-based) holes 0 and 16, and 22 #649 holes 0 and 21, each carry an all-DL π-cycle of length 20 with w = +4. "No positive π-cycle" cannot be the strengthening of Theorem H.
2. **The per-cycle statement is false at (5,5,5,5,6) and (5,5,5,6,6) too** (coordinator's Studio relay: plantri p25 #5594 h18, w = +4; p25 #24908 h4 and h18, w = +2). The zeros of CL §1.4 were a small-order effect. So HP cannot be strengthened per cycle either.
3. **Theorem F5 [proved]: the quarter floor holds at every (5,5,5,5,5) hole.** For every Kempe class, Σλ ≤ 0, i.e. F ≥ |class|/4. The proof is a local charging. Every DD step (a DL state whose π-image is DL) is charged to an unfilled state with **neither** lock, at most two charges per state. Each such state is a one-state excursion worth at most −2.
   - Inputs: Theorem W (formal), the run structure of π (formal), and Steps 2 and 4 of Theorem H (reviewed). The new ingredient is a short hand lemma (Lemma 3 below).
   - Checked on all 270 (5,5,5,5,5) holes at orders 12–22, 326 classes, in **both orientations**: 0 failures. The bound is attained (|DD| = 2N₀) at 17 #4.
4. **(5,5,5,5,6): precise gap.** The same charging fails there.
   - 174 of 400 DD steps at orders 16–20 have no σ-exit to a lockless state.
   - Even allowing every one-swap exit from either end of a DD step, the 2-capacity matching fails at 43 of 85 order-20 holes.
   - At class level |DD| ≤ 2N₀ itself fails (17 #3 h0 and h16: |DD| = 14, N₀ = 4).
   - In every class tested, the slack comes from the τ steps (F → F, λ = −3): |DD| ≤ 2N₀ + 3·#τ holds at all 136 holes, orders 16–20. A floor proof at (5,5,5,5,6) would need a local reason for τ steps to occur near long DL runs. That is the gap.

## 1. Run bookkeeping [proved]

Let C be a Kempe class at a degree-5 hole. Then:
- π permutes C (QP);
- Σ_C λ = |C| − 4F (QW);
- λ = +1 on unfilled states with Lock2;
- λ = −1 on unfilled states without Lock2, and on filled states with M3 short;
- λ = −3 on filled states with M3 long.

**Run structure.** The image of R₊₃ has Lock1 (QRP). So along a π-cycle, an unfilled run s₁…s_u is as follows:
- s₁ lacks Lock1;
- s_u lacks Lock2;
- every interior state is DL.

A state with neither lock is exactly a run with u = 1.

**Definitions.**
- DD = {t ∈ C : t is DL and πt is DL}.
- N₀ = #{unfilled t ∈ C with neither Lock1 nor Lock2}.

**Lemma 1.** Σ_C λ ≤ |DD| − 2N₀.

*Proof.* Split the cycles into Γ-cycles (all unfilled) and excursions (an unfilled run of length u followed by a filled run of length f ≥ 1).
- A Γ-cycle of length L is all-DL. It contributes L and contains L DD steps.
- An excursion contributes (u − 2) − 1 − 3(f − 1) − 1 = u − 3f. Three cases:
  - u ≥ 3: the run has u − 3 DD steps, and u − 3f ≤ u − 3.
  - u = 2: there are no DD steps, and u − 3f ≤ −1.
  - u = 1: u − 3f ≤ −2, and this excursion is exactly one lockless state.

Summing over all cycles gives the bound. ∎

**Corollary.** If |DD| ≤ 2N₀ in C, then Σ_C λ ≤ 0, which is the floor for C (QW `quarterFloor_iff_lam`).

## 2. Local types at an icosahedral hole (RG Step 1)

**Hypothesis (IcoBall, as in Theorem H).**
- v and x₀..x₄ have degree 5.
- The outer neighbours w_t (adjacent to x_t and x_{t+1}) are five distinct vertices outside N[v], with w_t ~ w_{t+1}.
- Indices follow the cyclic order of the link that π uses. The argument never uses a reflection, so it holds for either orientation of the embedding.

**Local types.** Take an unfilled state at repeat j, and write x_j..x_{j+4} = α, μ, α, A, B. Indices below are relative to j.
- Lemma R gives {w₀, w₁} = {A, B}.
- If w₀ = A, the colouring forces **R1**: (w₀..w₄) = (A, B, μ, α, μ).
- If w₀ = B, then w₃ ∈ {α, μ}. For a DL state, the locks force:
  - **R2** = (B, A, μ, α, μ);
  - **R3** = (B, A, B, μ, A).

So every DL state has type R1, R2 or R3. The type is read off w₀ and w₃.

## 3. The three lemmas

**Lemma 2 (RG Steps 2 and 4) [reviewed].** Let t be DL.
- If t is R2, then πt = R₊₃t is not DL. The vertex x₂ becomes A and loses its only B-neighbour, so lock 2 of the image dies.
- If t is R1 and πt is DL, then πt is R3.
  - The swapped {α,A}-component K contains x₂, x₃ and w₃.
  - It does not contain x₀ (QRP: Lock2 ⇒ x₀ ∉ K).
  - Hence it does not contain w₀ either, since w₀ = A is adjacent to x₀.
  - So in the image, w′₀ = w₃ has colour B′ and w′₃ = w₁ has colour μ′, which is type R3.

**Hence every DD step t → πt has an R3 endpoint**, namely t itself, or πt when t is R1.

**Lemma 3 (new) [proved].** Let t be DL of type R3, and let σ(t) be the swap of the {α,μ}-component of m = x₁. Then:
- the component is exactly {x₀, x₁, x₂};
- σ(t) has link (μ, α, μ, A, B), with repeat still at j;
- σ(t) has **neither** lock.

*Proof.*
- **The component is {x₀, x₁, x₂}.** The neighbours of x₀ are x₄ (B), w₄ (A), w₀ (B) and x₁. The neighbours of x₂ are x₁, x₃ (A), w₁ (A) and w₂ (B). The outer neighbours of x₁ are w₀ (B) and w₁ (A). So no other α or μ vertex is reached.
- **Roles in σ(t).** The new roles are α′ = μ, μ′ = α, A′ = A, B′ = B.
- **Lock 1 dies.** A {α, A}-path from x₁ to x₃ would have to enter x₃ through an α-vertex. The neighbours of x₃ are x₂ (μ), x₄ (B), w₂ (B) and w₃ (μ), so there is none.
- **Lock 2 dies.** A {α, B}-path from x₁ to x₄ would have to enter x₄ through an α-vertex. The neighbours of x₄ are x₃ (A), x₀ (μ), w₃ (μ) and w₄ (A), so there is none. ∎

σ is an involution on unfilled states. The image keeps repeat j, the same component is the {α′,μ′}-component of m, and swapping it again returns t. So σ is injective.

**Theorem F5 [proved].** At an IcoBall hole, every Kempe class satisfies Σλ ≤ 0. Equivalently:
- 3F − U ≥ 0;
- F ≥ |C|/4;
- the class winding is ≤ 0.

*Proof.*
- Map each DD step to its R3 endpoint r. Each r lies in at most two DD steps: π⁻¹r → r and r → πr.
- Then apply σ. By Lemma 3, σ(r) is a lockless state of the same class, and σ is injective.
- So |DD| ≤ 2·#(R3 ∩ DL) ≤ 2N₀.
- Lemma 1 then gives Σλ ≤ 0. ∎

**Remarks.**
- The proof never uses a lock path beyond its end vertices, apart from the formal x₀ ∉ K. So it is radius-2 local, like Theorem H.
- It is strictly stronger than R\* at these holes: R\* is F ≥ 1, while this is F ≥ |C|/4.
- Positive Γ-cycles exist at these holes, and they are paid for by lockless states reached by σ. This is the transport picture made exact: each R3 state of a positive cycle has the exit σ to a u = 1 excursion.
- **Lean target:** the theorem needs only QW, QRP, the IcoBall data (already the hypothesis of `ico_fill`) and three finite colour checks.

## 4. Data [data]

| check | orders | holes | classes | result |
|---|---|---|---|---|
| R-type classification, Lemma 2 transitions, Lemma 3 (\|K\| = 3, both locks dead), Lemma 1, \|DD\| ≤ 2·R3 ≤ 2N₀ | 12–22, gentri orientation | 270 | 326 | 0 failures |
| same, mirrored embedding | 12–22 | 270 | 326 | 0 failures |

- Transitions observed: DD R1→R3 2,242 and R3→R1 2,261 (both orientations, summed). R2 is never the start of a DD step.
- Maximum class Σλ is −20, so w ≤ −4 in every class.
- The bound is tight: |DD| = 2N₀ at 17 #4.

## 5. (5,5,5,5,6): what fails and the gap

- **Positive π-cycles exist** from order 25 (Studio relay above), so only the class floor can be targeted.
- **The run-length route is dead** [data]. Excursions with u up to 17 and f = 2 occur at order 17 (gentri 17 #3, holes 0 and 16, a w = 0 cycle containing 15 consecutive DL states). No per-excursion bound u ≤ 3f exists.
- **A local potential is not available at radius 2** [data]. The aggregated radius-2 key graph has a positive cycle. Radius 3 is meaningless at these orders, since its keys are almost one per state.
- **The σ-charging fails** (Verdict 4). The degree-6 vertex frees one ring-2 colour, so the R3-type isolation {x_j, x_{j+1}, x_{j+2}} is no longer forced.
- **[conjecture] Floor at (5,5,5,5,6)**, via |DD| ≤ 2N₀ + 3·#τ. This holds at all 136 holes at orders 16–20.
- **Gap:** a local lemma tying each DD step that has no lockless exit to a τ step (M3 long) within bounded π-distance. That would be the HP analogue of Lemma 3. An HP-style ring-2 automaton (MathHighDegreeNeighbour) is the natural tool. It has not been attempted here.

## 6. Reproduction (session scratchpad, not committed)

The scripts use `local-runs/common/kempe_py.py` and `22-winding-escape/escape.py` (`pi_of`).

| script | what it does | run time |
|---|---|---|
| `v55555.py 12,…,22` | asserts every step of §2–§3 per state and per class | 7 s |
| `v55555m.py` | the same on mirrored rotations | 7 s |
| `a6.py`, `a7.py`, `a8.py`, `a9.py` | (5,5,5,5,6) σ-exit, matching and class-budget tests | seconds |
| `a1.py`, `a4.py` | excursion (u, f) tables; radius-R potential test | seconds |

All runs were single core, on AC power.
