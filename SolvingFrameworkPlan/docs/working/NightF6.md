# Night: Theorem F6 (σC at (5,5,5,5,6) holes), Γ-cycle exits and the honest remainder

Night worker, 7 October 2026 (written 02:30 MDT). **Exploratory. Hand arguments plus single-core reads of the Studio files. Unreviewed.**

Builds on:
- `NightFloorAtEasyHoles.md` (F5, run bookkeeping);
- `NightF5Review.md` (Σλ = |DD| − 2N₀ − E₂ − 3#τ);
- `NightFloorHP.md` (Lemmas A–D);
- `NightFloorHP2.md` (Lemma 2: Γ-cycles);
- `NightC1Gamma.md` (exact σ-exit criteria at k = 3, 4; Conjecture G);
- the formal files `QuarterPi.lean` (π table), `QuarterRotationPlanar.lean` (x_j ∉ K for R₊₃), `QuarterSigmaGroups.lean` (`sigmaCConj_imp_floor_on_family`);
- Studio Jobs G and I (`local-runs/27-studio-positive-config/jobg-gamma.jsonl`, `jobi-cycles.jsonl`, `jobi-summary.txt`).

Labels:
- [proved]: a hand argument modulo the cited facts and the Kempe/Jordan duality (D) of `NightC1Gamma.md` §2;
- [data]: read off the Studio files (the script is the inline Python of §6);
- [conjecture]: not proved.

Frame. These are as in C1Gamma:
- link x₀..x₄ = α, μ, α, A, B;
- R3 ring (w₀..w₄) = (B, A, B, μ, A);
- p = x_k has degree 6, and m is its extra outer neighbour (m = α at k = 3, 4, Lemma D);
- K_σ = {x₀, x₁, x₂} at k = 3, 4 (Lemma D).

Colours are named by r's roles throughout a computation: 0 = α, 1 = μ, 2 = A, 3 = B.

## Verdict

1. **F6 is not proved.** Three new local facts are proved (§1, §2). The counting route through Conjecture G **cannot** close from local f-bounds alone (§3). Non-Γ positive cycles at (5,5,5,5,6) are paid only through multi-hop σ-groups (§4).

2. **[proved] A common form of the k = 3 and k = 4 exits along a Γ-cycle.**
   - Let r be R3@4. Then π²r = t is R3@3, two R-steps later.
   - The exit at r is lockless ⇔ w₃ and w₄ (p's two ring neighbours, flanking m) lie in one {1,2}-component **in r**.
   - The exit at t is lockless ⇔ the **same** two vertices lie in one {1,2}-component **in t**.
   - So both exits are one Kempe question about the same pair of vertices, asked before and after the two swaps K₁ ({0,2}) and K₂ ({0,1}). I could not prove that the answer survives the swaps; it does not always (§1.3).

3. **[proved] At k = 3 and k = 4 a σ-exit is never DL, and a lockless exit lands on an excursion with f ≥ 2.** So each such exit is worth 3f − 1 ≥ 5.
   - [data] Actually f = 3 at k = 4 (133/133) and f ∈ {2, 3} at k = 3 (97 + 36).
   - f = 1 occurs only at k = 0, 1, 2 (43 cases).
   - So the minimum f at (5,5,5,5,6) is 1, as Job I says, and the k = 3, 4 exits are exactly where f ≥ 2 is forced.

4. **Correction to the relayed count (units).**
   - The credit 3f − 1 and the Γ-cycle's debt are both in λ-units: Σ_c λ = L (= 5w), and Job G's `G_credit` is 77 against L = 20 at p25 #5594 h18.
   - So a ≥ L/4 exits worth ≥ 2 each give ≥ L/2, **not** ≥ L. One exit per 10 steps gives L/5, which is short by a factor of 5. The winding w = L/5 is the debt in units of 5λ, so it cannot be compared with 3f − 1.
   - With the proved bounds (5 per k = 3, 4 lockless exit, 2 per k = 0, 1, 2 lockless exit), the Job G exit counts give 5a₃₄ + 2a₀₁₂ − L ≥ −4. This is negative at p26 #87942 h22 (both orientations, −4) and p25 #16945 h3 (−1).
   - Even adding f = 3 at k = 4 leaves −1 at p26 #87942.
   - So G at (5,5,5,5,6) needs f = 3 at most k = 0, 1, 2 exits. That f is a radius-unbounded fact, as at k = 3, 4.

5. **Non-Γ positive cycles at (5,5,5,5,6)** (Job I, orders 25–26; 37 cycle records).
   - 17 records have lockless-exit credit Σ(3f − 1) < 5w. In 10 of them a = 0.
   - In 7 of these 10 every single-lock exit lands on a **w = 0** cycle, at a u = 3, f = 1 excursion worth 0. Examples: p26 #68224 h23, p26 #83426 h18, p26m #71953 h6. All DL exits there are σ-fixed points.
   - So the payment is neither "own non-DL steps" (the cycle is positive), nor direct lockless exits, nor the direct single-lock targets.
   - **σ alone still suffices in the data**: Job F found 0 failing σ-groups at every (5,5,5,5,6) hole, orders 24–26, both orientations. Paying needs σ-chains of length ≥ 2 through w = 0 cycles, or σ-links from other cycles into the positive one.
   - **F6 does not need σ′ up to order 26.** It does need a group-global argument for non-Γ cycles, and none is available.
   - (p26 #7490 h3, the relayed example, has pattern (5,5,5,6,6), not (5,5,5,5,6).)

## 1. Two R-steps from R3@4 to R3@3 [proved]

### 1.1 Explicit colours

Let r be R3@4:
- x = (0,1,0,2,3), w = (3,2,3,1,2);
- p = x₄, m = 0, ring order w₃, m, w₄.

**Step 1 (R₊₃: swap K₁, the {0,2}-component of x₂).**
- K₁ ∋ x₂, x₃, w₁.
- K₁ ∌ x₀ (QRP). Hence K₁ ∌ w₄ and m: x₀ (0) – w₄ (2) – m (0) is a {0,2}-path.
- The ring vertices w₀, w₂ (3) and w₃ (1) are not in K₁.
- Image s₁ = R1@1 in the frame j′ = j + 3, with roles α′ = 0, μ′ = 3, A′ = 1, B′ = 2. So old μ → A′, A → B′, B → μ′.

**Step 2 (R₊₃: swap K₂, the {0,1}-component of x′₂ = x₀ in s₁).**
- K₂ ∋ x₀, x₁, w₁ (w₁ = 0 in s₁).
- K₂ ∌ x₃ (QRP, x′₀ = x₃). Hence K₂ ∌ w₃ and m: x₃ (0) – w₃ (1) – m (0) is a {0,1}-path.
- Image t = R3@3 in the frame j″ = j + 1, with x″ᵢ = x_{i+1}, w″ᵢ = w_{i+1}, and roles α″ = 0, μ″ = 2, A″ = 3, B″ = 1.
- Check:
  - t link = (1,0,2,0,3), i.e. (x″₀..x″₄) = (0,2,0,3,1);
  - ring (w″₀..w″₄) = (w₁, w₂, w₃, w₄, w₀) = (1,3,1,2,3) = (B″, A″, B″, μ″, A″);
  - p = x₄ = x″₃, and m = 0 = α″.

### 1.2 The common form

**In r.** The {1,2} link vertices are leaves on the ring:
- x₁ (1) has the single {1,2}-neighbour w₁;
- x₃ (2) has the single {1,2}-neighbour w₃.

So any {1,2}-path between ring vertices can be taken off the link. Then:
- Lock1(r) ⇔ w₁ ∼₁₂ w₃;
- the exit criterion at k = 4 (w₄ ∈ K_{μ,A}(x₁)) ⇔ w₁ ∼₁₂ w₄;
- given Lock1, this is **w₃ ∼₁₂ w₄ in r**.

**In t.** The {1,2} link vertices are again leaves:
- x₂ (2) has the single {1,2}-neighbour w₁;
- x₀ (1) has the single {1,2}-neighbour w₄.

Then:
- Lock2(t) (the {μ″,B″} = {2,1} path from x₂ to x₀) ⇔ w₁ ∼₁₂ w₄;
- the k = 3 criterion at t (w″₂ ∈ K_{μ″,B″}(x″₁)) ⇔ w₁ ∼₁₂ w₃;
- given Lock2, this is **w₃ ∼₁₂ w₄ in t**.

The colours of w₃ (1) and w₄ (2) are unchanged from r to t. ∎

### 1.3 What the swaps can do [sketch]

By (D), w₃ ≁₁₂ w₄ iff a closed {0,3}-walk separates them. Such a walk passes through m (0, adjacent to both).
- Between r and t, the {1,2}-graph changes only on K₁ ∪ K₂. A {0,3} separating walk of r survives to t iff it meets no 0-vertex of K₁ ∪ K₂.
- So the two failures are correlated but not equivalent. [data] Per L = 20 Γ-cycle, (#k=3 failures, #k=4 failures) is:
  - (0,0) in 50 cycle records;
  - (1,1) in 6;
  - (1,0) in 1 and (0,1) in 1 (p25 #16945 h3, the two orientations);
  - (2, ·) or (·, 2) in **none**.
  - The L = 60 cycles have no failures.

**Conjecture A₃₄.** On a Γ-cycle at a (5,5,5,5,6) hole, for each k ∈ {3, 4}, the L/10 R3@k states do not all fail. [data: 62/62 cycle records]

## 2. Exits at k = 3, 4: never DL, and f ≥ 2 [proved]

**Never DL.** This is C1Gamma §2: at k = 3 Lock2′ dies at x₄, and at k = 4 Lock1′ dies at x₃. So d-exits occur only at k = 0, 1, 2, which agrees with Job G (no `DL_k8`/`DL_k16`).

**The first two steps after a lockless exit.**
- Let s = σ(r) = (1,0,1,2,3) on the link, with the ring unchanged (K_σ = {x₀,x₁,x₂}). s has repeat 0 with α_s = 1, μ_s = 0, A_s = 2, B_s = 3.
- If s is lockless, π(s) = φ_B⁻¹ swaps the {0,3}-component K_φ of x₄. K_φ ∌ x₁, because s lacks Lock2.
- So t₁ = π(s) has link (1,0,1,2,0). This is F₃ with W = 2, X = 0, Y = 1, Z = 3.
- Since π(t₁) is τ iff M3 is long at t₁, **f ≥ 2 ⇔ x₀ ∼₁₃ x₂ in t₁**.
- By (D) applied at v, x₀ ≁₁₃ x₂ iff x₁ (0) is {0,2}-joined in t₁ to x₃ (2) or to x₄ (0); here x₃ ∼ x₄ are adjacent.

**k = 3.**
- x₄ has degree 5, with neighbours x₃ (2), x₀ (1), w₃ (1), w₄ (2). So K_φ = {x₄}, and off the link t₁ has r's colours.
- In r, x₁ and x₄ are {1,3}-leaves (on w₀ and on w₃), and the other link vertices are 0 or 2.
- So the criterion w₂ ∈ K_{1,3}(x₁) gives an off-link {1,3}-path from w₀ to w₂. It persists in t₁.
- x₀ (1) ∼ w₀ (3) and x₂ (1) ∼ w₂ (3), so x₀ ∼₁₃ x₂. ∎

**k = 4.**
- The criterion gives an off-link {1,2}-path R from w₄ to w₁ in r (§1.2). Neither σ nor φ_B⁻¹ changes an off-link 1 or 2, so R persists in t₁.
- In t₁, x₀ = x₂ = 1. Hence v x₀ w₄ R w₁ x₂ v is a closed {1,2}-walk.
  - At x₀ (rotation v, x₁, w₀, w₄, x₄) it puts x₁ and x₄ on opposite sides.
  - At x₂ (rotation v, x₁, w₁, w₂, x₃) it puts x₁ and x₃ on opposite sides.
- So x₁ ≁₀₂ x₃, x₄ in t₁, and f ≥ 2. ∎

**A partial step towards f = 3 at k = 4 [proved]: w₂ ∉ K_φ.**
- In s, the walk v x₂ w₁ P w₃ x₃ v separates w₂ from x₄. Here P is r's Lock1 path, off-link {1,2}, which σ does not change.
- So w₂ keeps colour 3 in t₁, and x₃'s only {2,3}-neighbour after τ is w₂.

f = 3 then needs w₀ ∼₂₃ w₂ in t₂ = τ(t₁), where τ has recoloured w₁ from 2 to 0. I did not finish this.

**Conjecture F₄.** At k = 4 every lockless exit has f = 3. [data 133/133]

## 3. Counting: Conjecture G at (5,5,5,5,6) [proved bookkeeping; conjecture]

**Proved.**
- Σ_c λ = L on a Γ-cycle c (HP2 Lemma 2).
- A lockless exit is a whole u = 1 excursion, worth 1 − 3f.
- σ is an involution, so distinct R3 states, even on different Γ-cycles, have distinct targets.
- §2 gives worth ≤ −5 at k = 3, 4; F5's Lemma 1 gives ≤ −2 at k = 0, 1, 2.

**Why this is not enough [data].** Write a₃₄ for the lockless exits at k = 3, 4 and a₀₁₂ for those at k = 0, 1, 2.

| bound used | min over 62 (5,5,5,5,6) Γ-cycle records of (bound − L) |
|---|---|
| 5a₃₄ + 2a₀₁₂ (proved worths) | −4 (p26 #87942 h22) |
| 8a₄ + 5a₃ + 2a₀₁₂ (with F₄) | −1 (p26 #87942 h22) |
| actual Σ(3f − 1) (Conjecture G) | +11 (p25m #16945 h3: 31 vs 20) |

Even if A₃₄ held with a₃₄ = L/5, it would give only L from the k = 3, 4 exits with f ≥ 2. Γ-cycles with one k = 3 failure and one k = 4 failure (a₃₄ = L/10) need about 2.5 more f = 3 exits from k = 0, 1, 2. Those exits can be fixed points (d) or land at f = 1.

**Sufficient form [conjecture].** G holds if:
- **A₃₄** holds;
- **F₄** holds;
- and **F₀₁₂**: at least L/10 + 1 lockless exits at k = 0, 1, 2 with f = 3 whenever a₃₄ < L/5.

Data for F₀₁₂: the f = 3 counts at k = 0, 1, 2 are 98 + 81 + 86, against f = 1 counts of 14 + 10 + 19. I see no local mechanism for F₀₁₂: at k = 0, 1, 2 the σ-component leaks (|K_σ| ≥ 4) and the image link is not forced.

**G ⇒ σC on Γ-groups needs one more lemma.**
- **Lemma R.** On each σ-target cycle T, the λ-sum of T outside the hit excursions is ≤ 0. The rest of the group must also be ≤ 0.
- This is not testable from the Job G files, which identify target cycles only by their w. It needs a Studio check.

## 4. Non-Γ positive cycles (coordinator item 2) [data]

From `jobi-cycles.jsonl`, (5,5,5,5,6) only, orders 25–26, both orientations:

| | records |
|---|---|
| positive non-Γ cycles | 37 |
| lockless credit ≥ 5w (directly paid, in the G sense) | 20 |
| lockless credit < 5w | 17 |
| ... with a = 0 | 10 |
| ... with a = 0 and every single-lock exit landing on a w = 0 cycle | 7 |

- The single-lock exits of these cycles land at u = 3 or 4, f = 1 excursions. These are worth 0 or +1, so they give no local credit (S4 again).
- **Precise answer.** These cycles are paid neither by their own non-DL steps (their sum is +5w > 0) nor by the excursions their single-lock images land on. They are paid only inside the full σ-group, which Job F found nonpositive at every (5,5,5,5,6) hole through order 26: either through further σ-links of the w = 0 targets, or through σ-links from other cycles into them.
- **σ′ is not needed at (5,5,5,5,6) up to order 26.** Whether that persists is Job J's question at order 27.

## 5. What remains for F6

F6 ⇐ σC on (5,5,5,5,6) holes, since these holes have three consecutive 5s (`sigmaCConj_imp_floor_on_family`).

| # | statement | status | support |
|---|---|---|---|
| 1 | k = 3, 4 exit criteria; exits there never DL | [proved] C1Gamma §2 | Job G S1: 0/464 violations |
| 2 | common form w₃ ∼₁₂ w₄ (§1.2) | [proved] | — |
| 3 | f ≥ 2 at k = 3, 4 (§2) | [proved] | 266/266 |
| 4 | A₃₄: per k ∈ {3,4}, not all L/10 states fail | [conjecture] | 62/62 |
| 5 | F₄: f = 3 at k = 4 | [conjecture], partial step proved | 133/133 |
| 6 | F₀₁₂ (or directly G) | [conjecture], no local mechanism | G: 62/62, min slack 11 |
| 7 | Lemma R: target remainders ≤ 0 | [conjecture] | untested (needs cycle ids) |
| 8 | σC on groups with positive non-Γ cycles (multi-hop) | [conjecture], no mechanism | Job F 0 failures at (5,5,5,5,6), ≤ 26 |
| 9 | everything at order ≥ 27 | open | Job J running |

Items 6 and 8 are the real gaps. Both are radius-unbounded Kempe statements: 6 about the f of an exit at k = 0, 1, 2, and 8 about σ-chains through w = 0 cycles. Items 4 and 5 look provable with the same Jordan bookkeeping as §1–§2.

**Studio requests.**
1. Lemma R with true cycle ids.
2. For the 10 a = 0 non-Γ positive cycles: the σ-distance in the group to the paying cycles, and whether incoming σ-links (from other cycles' DD endpoints) suffice.
3. The f distribution at k = 0, 1, 2 split by K_σ size.

## 6. Reproduction

All numbers in §§1.3, 3 and 4 come from short Python passes over `jobg-gamma.jsonl` and `jobi-cycles.jsonl`. These parse the `exits` keys (`kind_k<mask>_u<u>_f<f>_wT<w>`; kmask 8 ↔ k = 3, 16 ↔ k = 4). They took under 1 s on one core, on AC power. No new enumeration was run (plantri is absent on the MacBook).

> **Correction (07 Oct, 03:05).** The §2 claim that a lockless σ-exit at k = 4 lands on f ≥ 2 is FALSE: Studio Job R found p27 #133619 h21 with a k = 4 lockless exit of f = 1 (both orientations; 2 of 400 at order 27). The Lean attempt (QuarterJordanDual.lean) located the gap: the closed {μ,A}-walk separates x₁ from x₃, x₄ only in {α,B}, and the argument needs {α,A}. Use credit ≥ 2 at k = 4; f ≥ 2 at k = 3 is formal (`sigma_exit_f_ge_two_k3'`).
