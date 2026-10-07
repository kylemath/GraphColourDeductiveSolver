# Night: the quarter floor at holes with three consecutive degree-5 link vertices (F5-3 attempt)

Night worker, 7 October 2026 (written 01:43 MDT). **Exploratory. Hand proofs plus single-core checks. Unreviewed.**

Cited notes:
- **F5** = `NightFloorAtEasyHoles.md`, reviewed PASS in `NightF5Review.md`. The review gives the exact per-class identity Σλ = |DD| − 2N₀ − E₂ − 3·#τ.
- **R5³** = `MathRstar55566.md` (Theorem R5³), reviewed CORRECT in `MathReviewRstar55566.md`.
- **QRP** = `QuarterRotationPlanar.lean`: R₊₃ is defined exactly on Lock2 states, its image has Lock1, and x_j ∉ K_F (Jordan).
- **HP6** = `NightFloorHP.md`, the parallel (5,5,5,5,6) note. I read it at 01:40 and did not duplicate its Lemmas A–D.

Labels: [proved] means a complete argument modulo the cited reviewed or formal facts; [sketch] means the gap is named; [conjecture] means not proved; [data] means computed by the scripts in §7.

**Hypothesis (R5³ hole).** v has degree 5, with link y₀..y₄ in rotation order. Three cyclically consecutive link vertices y_p, y_{p+1}, y_{p+2} have degree 5. The graph has no separating triangle (gentri: 4-connected, minimum degree 5).

**Frame.** A state t with repeat j has link x₀..x₄ = α, μ, α, A, B, where x_i = x_{j+i}. w_i is the common outer neighbour of x_i and x_{i+1}. K_F is the {α,A}-component of x₂, and K_B is the {α,B}-component of x₀. σ swaps the {α,μ}-component of x₁. At a hole with exactly three consecutive 5s, write r = j − p (mod 5). The π-step on a DL state moves r to r + 3.

## Verdict

1. **Theorem F5-3 is not proved.** The class floor Σλ ≤ 0 holds at every R5³ hole tested [data]:
   - orders 12–22, both orientations;
   - 5,327 classes at orders 21–22 and 784 at orders 12–20;
   - 0 failures, and the exact identity holds in every class.
2. **The floor is attained at an R5³ hole, with nothing but N₀ to pay** [data]. At gentri 17 #2, hole 0 (pattern (5,5,5,6,6)):
   - The whole state space is one class: 64 states, Σλ = 0, |DD| = 12, N₀ = 6, E₂ = τ = 0.
   - So any proof must pay these 12 DD steps exactly 2-to-1 with the 6 lockless states.
   - Yet 4 of the 12 DD steps have **both** endpoints at Kempe distance ≥ 3 from every N₀ state.
   - Consequence: **no charging of DD steps into N₀/E₂/τ through exits of ≤ 2 swaps can prove F5-3.** Over all R5³ holes at orders 16–20, the best such assignment within 2 swaps of a DD endpoint is short at 24 holes (19 mirrored).
   - Also, unlike the (5,5,5,5,6) picture of HP6, τ cannot be the general payer: this hole has none.
3. **Which DD steps admit F5's exit (Lemma 3′, [proved], engine-checked).**
   - F5's exit is *radius-2 local* only at an endpoint whose x₀..x₄ all have degree 5. That never happens at a hole with a link vertex of degree ≥ 6.
   - At an exact-three hole, only frame r = 0 has x₀, x₁, x₂ of degree 5. So only the DD types **0→3 (via t)** and **2→0 (via πt)** can use the |K| = 3 form. Even there the exit is equivalent to two cut-vertex conditions on the far side, which are non-local.
   - The types 1→4, 3→1 and 4→2 never have such an endpoint.
   - Table: §3.
4. **R5³'s moves, in the identity's terms [proved / data].**
   - R5³'s F is exactly π on Lock2 states. Its forced chain F1–F3 from S = 01 is a forced stretch of a DL run (r = 3 → 1 → 4 → 2).
   - Its kills (G then F- or B-starvation) are 2-swap exits to non-DL states.
   - They produce short fills, but by Verdict 2 they cannot pay DD steps locally.
5. **Residual (Conjecture σC, the σ-cluster floor).**
   - Join two π-cycles when σ maps an endpoint of a DD step on one to a state on the other. Then every cluster has Σλ ≤ 0.
   - [data] This holds at all R5³ holes, orders 16–22, both orientations: 5,801 holes per orientation, 0 failures.
   - Every positive π-cycle found (orders 21–23, both orientations) is paid by its direct σ-neighbours.
   - σC implies F5-3. It is π-global but Kempe-local in one hop (§5).

## 1. Identity and run facts (cited)

- Σλ = |DD| − 2N₀ − E₂ − 3·#τ holds per class and also per π-cycle, since every term is attached to an excursion.
- DL states are the interior states of unfilled runs. A run of DL length ℓ contributes ℓ − 1 DD steps.
- So the floor is automatic for every π-cycle with Σλ ≤ 0. All the content lies in positive cycles.

## 2. Lemma 3′: the exact σ-exit criterion [proved]

**Lemma 3′.** Let t be unfilled, and let x₀, x₁, x₂ have degree 5. Then:

(a) {w₀, w₁} = {A, B}, w₄ ∈ {μ, A} and w₂ ∈ {μ, B}. If w₀ = A, then w₄ = w₂ = μ.

(b) σ's component is exactly {x₀, x₁, x₂} if and only if (w₀, w₁, w₂, w₄) = (B, A, B, A).

(c) In that case:
- σ(t) has Lock1 if and only if w₁ and x₃ lie in one component of K_F − x₂;
- σ(t) has Lock2 if and only if w₀ and x₄ lie in one component of K_B − x₀.

(d) If deg x₃ = 5 and w₃ ≠ α, then Lock1 of σ(t) is dead. If deg x₄ = 5 and w₃ ≠ α, then Lock2 of σ(t) is dead.

(e) If t is DL and x₂ has no B-neighbour (that is, w₁ ≠ B and w₂ ≠ B), then πt is not DL (F-starvation).

*Proof.*

(a)
- w₀ and w₁ are adjacent to x₁ (μ) and to an α vertex, and w₀ ~ w₁. Hence {w₀, w₁} = {A, B}.
- w₄ is adjacent to x₀ (α) and x₄ (B), so w₄ ∈ {μ, A}. Likewise w₂ is adjacent to x₂ (α) and x₃ (A), so w₂ ∈ {μ, B}.
- Since deg x₀ = 5, w₄ ~ w₀. Since deg x₂ = 5, w₁ ~ w₂. So w₀ = A forces w₄ ≠ A and w₁ = B forces w₂ ≠ B, giving w₄ = w₂ = μ.

(b) The outer neighbours of x₀, x₁ and x₂ are w₄, w₀, w₁ and w₂. By (a), w₀ and w₁ are never coloured α or μ, so the component closes exactly when w₄ ≠ μ and w₂ ≠ μ.

(c)
- In σ(t), x₁ is α and x₀, x₂ are μ, and every other vertex keeps its colour.
- A {α,A}-path from x₁ must leave x₁ through its A-neighbour w₁. After that it uses only t-coloured α/A vertices other than x₀ and x₂.
- So Lock1 of σ(t) holds exactly when w₁ reaches x₃ in the {α,A}-graph of t minus x₀ and x₂. Both w₁ and x₃ are in K_F (each is adjacent to x₂), and x₀ ∉ K_F by Jordan (QRP), so this is the stated condition.
- Lock2 is the same argument with {α,B} and w₀, using x₂ ∉ K_B.

(d) If deg x₃ = 5, the neighbours of x₃ other than v are x₂, x₄ (B), w₂ (B) and w₃. So when w₃ ≠ α, x₃ is a leaf of K_F hanging off x₂. The same argument works for x₄, whose neighbours are x₃ (A), x₀, w₃ and w₄ (A).

(e) This is the F-starvation margin of R5³ §2. ∎

F5's Lemma 3 is the special case of (b) and (d) with all five degrees equal to 5. With E2, deg x₃ = 5 forces w₃ = μ there.

**Consequence.** At an exact-three hole, frame r = 0 is the only frame with x₀, x₁, x₂ of degree 5. There x₃ = y_{p+3} and x₄ = y_{p+4} have degree ≥ 6. So (d) is unavailable, and the exit is decided by the far-field cut conditions in (c).

[data] (a), (b), (c), (d) and (e) were asserted at every unfilled state, in every frame with x₀, x₁, x₂ of degree 5, at all R5³ holes of orders 16–20, both orientations:
- 19,298 frames per orientation, 0 failures;
- 6,216 frames with |K| = 3; of these, 432 DL states have a lockless σ-image and 160 do not.

## 3. Which DD steps have F5's exit [data, exact-three holes only]

Orders 16–21, gentri orientation.

| DD type (r → r+3) | steps | some endpoint has a lockless σ-image | with \|K\| = 3 |
|---|---|---|---|
| 0→3 | 931 | 475 | 245 |
| 1→4 | 614 | 315 | 24 |
| 2→0 | 1,003 | 534 | 263 |
| 3→1 | 508 | 312 | 59 |
| 4→2 | 575 | 353 | 62 |

- The mirror swaps 0→3 with 2→0 and 3→1 with 4→2, and it fixes 1→4.
- About 45% of DD steps of every type have no σ-exit.
- At DD endpoints, σ is most often a pure renaming (σ(t) = t, the {α,μ}-subgraph being connected): 2,580 of 5,058 endpoints.
- Neither the Klein orbit {t, σt, Gt, σGt} nor any one-swap neighbourhood suffices:
  - the 2-capacity matching of DD steps into lockless states fails at 232 classes (Klein) and 142 holes (radius 1);
  - adding the E₂ and τ payers at radius 2 still fails at 24 holes.

## 4. R5³ translated [proved, from the reviewed R5³]

- **F is π.** π on a Lock2 state is R₊₃ = F. So R5³'s Proposition S01 in case W3 = b (r = 3, with w₃ = μ, w₂ = B, w₄ = A, w₁ = A) says that F1, F2 and F3 are forced. A DL run through such a state continues deterministically r = 3 → 1 → 4 → 2 for as long as it stays DL.
- **The case W3 = α at r = 3.**
  - If w₁ = A, then πt is not DL (Lemma 3′(e)). So no DD step starts there.
  - If w₁ = B, then G confines to {x₃, x₄}, and G-F follows.
- **Kills.** R5³'s kills G·B and G·F are injective-looking 2-swap exits to non-DL states. They are not exits to N₀, E₂ or τ, and by Verdict 2 no ≤ 2-swap payer assignment exists.
- **Verdict on the translation.** The radius-7 bound and the floor are logically unrelated at this resolution. A short fill does not give an excursion credit.

## 5. Residual: the σ-cluster floor

**Conjecture σC.** At an R5³ hole, let 𝒢 be the graph whose vertices are the π-cycles of a class. Put an edge Z–Z′ whenever t ∈ Z is an endpoint of a DD step and σ(t) ∈ Z′. Then Σλ ≤ 0 on every connected component of 𝒢.

σC implies F5-3, since a class is a union of components. At all-5 holes it follows from F5's proof: each DD step is charged via σ from its own endpoint.

[data] Results for σC:
- **σC itself:** 0 failures, orders 16–22, both orientations; about 74,000 components per orientation.
- **Per-cycle floor:** holds at every exact-three hole up to order 20 (2,793 cycles, maximum Σλ = 0, attained at 17 #2 h0).
- **Positive π-cycles at R5³ holes** (they appear from order 21 on). The table lists every one found:

| order | gentri, hole (pattern) | length | w | DD | N₀ | σ-neighbour cycle sums |
|---|---|---|---|---|---|---|
| 21 | #97 h2 (5,5,6,7,5) | 14 | +2 | 10 | 0 | −195, 0 |
| 21 | #135 h0 (5,5,5,5,7) | 14 | +2 | 10 | 0 | −60, 0 |
| 22 | #516 h16 (6,5,5,5,7) | 14 | +2 | 10 | 0 | −130, −10, 0 |
| 22 | #596 h0 / h2 (5,5,5,6,7) | 14 | +2 | 10 | 0 | −115, −35, 0, 0 |
| 23 | #1491 h2 / h20, #1543 h2 (5,5,6,7,5) etc. | 14 | +2 | 10 | 0 | −285 / −275 |
| 23 | #1495 h0 / h22, #1544 h0 (5,5,5,5,7) | 14 | +2 | 10 | 0 | −220, −105, −10 / −145 |
| 23 | #1768 h11 / h15 (7,6,5,5,5) | 18 | +2 | 12 | 1 | −200, −20, −20 |
| 22 (mirror) | #569 h2 (5,6,7,5,5) | 18 | +2 | 12 | 1 | −150, 0, 0 |

- The length-14 positive cycles are all one excursion with u = 13 and f = 1: a DL run of 11 states, closed by a single φ_A step.
- In every case a 1-hop flow along σ-edges, from positive cycles into negative σ-neighbours, covers the whole surplus. That is 8/8 holes at order 23 and 3/3 at order 23 mirrored; orders 21–22 pass in both orientations.
- This also verifies the class floor at those order-23 holes.

**What a proof of σC needs [sketch].**
- (i) A π-local argument that a cycle whose DL runs are not long, u − 2 ≤ 3f + (credits), pays itself. HP6 §5 proposes the same "along π" route at (5,5,5,5,6).
- (ii) A structure lemma for the long-run cycles: the u = 13, f = 1 type, and Γ-cycles at all-5 holes. It must show that a DD endpoint on them has a σ-image on a cycle with matching slack.
- Neither (i) nor (ii) is proved. The 17 #2 h0 example shows that (i) must be exact: each of its two cycles has Σλ = 0, with |DD| = 2N₀ inside the cycle and the N₀ states ≥ 3 swaps from 4 DD steps.

## 6. Relation to HP6

- (5,5,5,5,6) is a sub-case here. HP6's Lemmas A and B (T-steps paid by E₂ via ψ) and its Lemma D are finer than Lemma 3′ for that pattern.
- HP6's C1′ (#D₀ ≤ 3·#τ) cannot extend to all R5³ holes: 17 #2 h0 has τ = 0 and |DD| = 12.
- Both notes find the payment π-local, not Kempe-local.

## 7. Reproduction (session scratchpad `r53/`, not committed)

The scripts use `local-runs/common/kempe_py.py` and `22-winding-escape/escape.py` (`pi_of`).

| script | what it does | run time |
|---|---|---|
| `survey.py ORDERS [m]` | identity and class floor at all R5³ holes | 8 s (12–20); a few min (21–22) |
| `lem3p.py ORDERS o\|m` | Lemma 3′ (a)–(e) assertions | 10 s |
| `ddtab.py`, `dd.py`, `dlr.py`, `sigimg.py` | §3 tables | seconds |
| `match.py ORDERS o\|m sig\|R1\|R2` | payer matchings within radius 0/1/2 | about 1 min |
| `dist.py 17 2 0` | Kempe distances of DD endpoints to N₀ at the tight hole | 1 s |
| `cyc.py ORDERS o\|m c\|s\|d\|D` | per-cycle and σ-cluster floors | 45 s per order 22 |
| `pos.py ORDERS o\|m` | positive cycles and the 1-hop σ flow | 3 min (order 23) |

All runs used one core on AC power, with the battery at 100%.
