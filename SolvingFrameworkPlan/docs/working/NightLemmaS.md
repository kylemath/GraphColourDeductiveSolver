# Night: Lemma S on Γ-cycles at (5,5,5,5,6) holes, block structure and the rotating colour pair

Night worker, 7 October 2026 (written 02:48 MDT). **Exploratory. Hand arguments plus single-core checks. Unreviewed.**

Builds on:
- `NightC1Gamma.md` (exact k = 3, 4 exit criteria; role dynamics);
- `NightF6.md` (§1.1 explicit two-step colours; §2: worth ≥ 5 at k = 3, 4);
- `NightF6Flow.md` §2.1 (one-question lemma: lockless ⇔ pm is a bridge of G[v ∪ {c(p),c(m)}]);
- `NightFloorHP2.md` Lemma 2;
- Studio Jobs L, M and N (`local-runs/27-studio-positive-config/jobl-cycles.json`, `jobm-gamma-sequences.jsonl`, `jobm-summary.txt`, `jobn-summary.txt`). The coordinator relayed M and N mid-task.

Labels:
- [proved]: a hand argument modulo the cited facts;
- [data]: read off the Studio files or computed by the local scripts of §6;
- [sketch]: an incomplete argument;
- [conjecture]: not proved.

Frame. As in `NightF6.md`:
- link x₀..x₄;
- R3@4 colours x = (0,1,0,2,3), ring w = (3,2,3,1,2), so (α, μ, A, B) = (0, 1, 2, 3);
- p = x₄, m its extra outer neighbour (colour 0);
- y = w₃ and z = w₄ flank m.

## Verdict

0. **Main result: period lemma for A₃₄′ (§0) [proved; the rest is a precise obstruction].**
   - In every R-run the y–z join J (equivalently, a lockless exit at k = 3, 4) is forced true at R3k0, R3k1, R3k2, R1k3 and R1k4. Each is witnessed by an explicit 6-vertex two-coloured path around the hole.
   - The pm-swaps cannot change J.
   - Hence J changes only at the four far swaps. A k = 4 failure is exactly a break by the R₊₃ swap at the preceding R3k0, and every break is undone by R3k2.
   - **A₃₄′ is equivalent to "the R3k0 swap never breaks J in two consecutive periods".** I could not prove this.
   - It is **false inside general DL runs**: at order 24 one run of 18 DL states has two consecutive k = 4 failures. So it can only hold through the Γ-closure.
   - The suggested per-period coupling with the k ≤ 2 exits is false. The true coupling is the reverse: failures cluster (§0).
1. **Lemma S cannot be proved from the k = 3, 4 exits alone [data, exact].**
   - With the best possible worth (8 per exit, f = 3), 6 of the 62 records have k = 3, 4 credit 16 < L = 20: p26 #87942 h22, p26 #36087 h15 and p26 #38516 h20, both orientations.
   - Every proof must use k ∈ {0,1,2} exits on those cycles.
2. **No per-block statement is local [data].** On full 10-step DL blocks (R3@4 … R3@0 all DL) at orders 17–22, all five exits fail in 11 of 18 blocks (first: 17 #3 h0, both orientations, pattern O O D D D).
   - Across consecutive blocks, the k = 3 exit of one block and the k = 4 exit of the next both fail inside a 9-state DL window at 20 #20 h0 (gentri numbering), both orientations.
   - So A₃₄′ and any "≤ 1 failing block" statement need the Γ-closure, not a window.
3. **On the 62 Γ-cycle records the true per-block facts are [data, Job M]:**
   - (i) e₄ and e₃ of one block fail together or not at all, except in one cycle pair (p25 #16945 h3, one orientation each): 132 TT, 6 FF, 1 TF, 1 FT;
   - (ii) at most one block per cycle has a k = 3 or k = 4 failure;
   - (iii) block credit ≥ 10 in 139 of 140 blocks. The exception is p26 #87942 h22 (plantri orientation), pattern 10000, credit 8, and its partner block has 32.
   - So "every block pays its own 10" is **false**. The per-cycle statement holds with min slack +11 (31 vs 20).
4. **New structural fact [proved]: the colour pair rotates.** Track the actual colouring c_i after i R-swaps, without renaming colours.
   - The k = 4 question in block b asks whether pm is a bridge in the pair {0, c(p)}, where c(p) = 3, 2, 1 for b ≡ 0, 1, 2 (mod 3).
   - So consecutive blocks ask about **different** perfect matchings of the four colours: {03|12}, then {02|13}, then {01|23}.
   - Within a block, the k = 4 and k = 3 visits ask about the same matching. The two swaps between them are exactly the two swaps **outside** that matching.
   - Consequence: "the y–z connection can be cut at most once per two visits" cannot be a persistence statement about one 2-colour graph. Consecutive blocks look at different 2-colour graphs (§2).
5. Lemma S therefore stays [conjecture] at the level of the whole cycle. The sufficient pair A₃₄′ + F₀₁₂′ of `NightF6Flow.md` §2.2 is reformulated in §3 in matching language.

## 0. A₃₄′: the period lemma, and where the proof stops

The coordinator narrowed the brief to A₃₄′: at most one failure in any two consecutive k = 4 visits. This section is the main result of the note.

**Notation.**
- One period of 10 R-steps visits the states in the order
  R3k4, R1k1, R3k3, R1k0, R3k2, R1k4, R3k1, R1k3, R3k0, R1k2
  (Job O; HP2 Lemma 2). Positions are 0..9, and step i goes from position i to i + 1.
- Write J(s) for "y ∼ z in {c(y), c(z)} in state s", with the current colours.
- By `NightF6Flow.md` §2.1, the σ-exit at R3k4 / R3k3 is lockless ⇔ J holds there.

**Lemma P1 (five forced joins) [proved, radius 2].** J holds at every R3 state with k ∈ {0,1,2} and every R1 state with k ∈ {3,4}. No lock or DL hypothesis is needed beyond the ring pattern.

Recall the colours:
- R3: link (α, μ, α, A, B), ring (B, A, B, μ, A);
- R1: ring (A, B, μ, α, μ).

Around the hole the ring is the cycle w₀ w₁ w₂ w₃ w₄, with m inserted between w_{k−1} and w_k. So every other ring edge w_t w_{t+1} is present, and x_t is adjacent to w_{t−1} and w_t. In each case below, the path is two-coloured in {c(y), c(z)} and avoids m:

| state | y, z | path from y to z |
|---|---|---|
| R3k0 | w₄ (A), w₀ (B) | w₄ x₄ x₃ w₂ w₁ w₀ (A B A B A B) |
| R3k1 | w₀ (B), w₁ (A) | w₁ w₂ x₃ x₄ w₄ w₀ (A B A B A B) |
| R3k2 | w₁ (A), w₂ (B) | w₂ x₃ x₄ w₄ w₀ w₁ (B A B A B A) |
| R1k3 | w₂ (μ), w₃ (α) | w₂ x₂ x₁ x₀ w₄ w₃ (μ α μ α μ α) |
| R1k4 | w₃ (α), w₄ (μ) | w₃ w₂ x₂ x₁ x₀ w₄ (α μ α μ α μ) |

∎ [data: 0 exceptions among all 5,000+ such DL states, orders 16–22, both orientations (`ls/l1.py`)]

**Lemma P2 (pm-swaps are invisible) [proved].**
- Steps 2 (R3k3 → R1k0) and 9 (R1k2 → R3k4) swap the pair {c(p), c(m)}. This holds from the explicit colours: at R3k3, p = x₃ = A and m = α; at R1k2, p = x₂ = α and m = A.
- y and z are adjacent to both p and m and have distinct colours. So {c(y), c(z)} is the complementary pair, and a Kempe swap in a pair preserves the vertex sets of both halves of its matching.
- Hence J(position 2) = J(position 3) and J(position 9) = J(position 0). ∎

**Corollary P3 [proved].**
- J is true at positions 4–8 (P1).
- J can change only at steps 0, 1, 3 and 8. The near swaps at steps 4–7 go from true to true.
- J(R3k4) = J(R1k2), and J(R3k3) = J(R1k0).
- The off-interval of J in any period lies inside positions 9, 0, 1, 2, 3, and it is always closed by position 4 (R3k2).
- In particular:
  - **a k = 4 failure in period n ⇔ the step-8 swap of period n − 1 breaks J**. This is the R₊₃ swap at R3k0: the {α,A}-component K of x₂, with pair {c(p), c(y)}.
  - **J cannot stay false from one k = 4 visit to the next.**

This proves the mechanism of Job O (only steps 8, 0, 1, 3 change J; break at 8 → 9; restore by 3 → 4) for every R-run, not only on Γ-cycles. [data] The local windows of `ls/trace.py` (orders 17–22) show exactly this pattern in every run.

**Why the step-8 swap breaks J [proved].**
- At R3k0 the explicit join of P1 is w₄ x₄ x₃ w₂ w₁ w₀. Its A-vertices x₃ and w₁ are adjacent to x₂ (α), so they lie in K and become α.
- So the swap always destroys the local path. J after step 8 holds iff a far {A,B}-path from y to z survives in the new colouring, i.e. it uses no A-vertex of K. Any new A-vertices are former α-vertices of K.
- This matches Job P: K meets every y–z path in the {c(y), c(z)}-graph.

**Precise obstruction to A₃₄′.**
- By P3, A₃₄′ is **equivalent** to: the R₊₃ swap at R3k0 does not break J in two consecutive periods.
- P3 rules out persistence, so the coordinator's form ("the break is restored by step 0 or 3 before the next R3k4") is proved. But it does **not** imply A₃₄′: each period's break is a fresh event. A failure at the k = 4 visit of period n + 1 needs a new break at step 8 of period n.
- What remains is a statement about two R₊₃ swaps ten steps apart, at R3k0 states c₁₀ₙ₊₈ and c₁₀ₙ₊₁₈. By §2 they ask about different colour matchings: the first breaks a {1,2}-type join, the second a {1,3}-type join.
- I found no argument. The local windows cannot test it: no (5,5,5,5,6) DL window at orders ≤ 23 contains two R3k0 → R1k2 steps followed by R3k4 (§5).
- [data, Job O] 0/140 consecutive double breaks on Γ-cycles.
- **[data, order 24] Two consecutive breaks do occur inside one DL run** (24 #3611 h0, a DL run of 18 states; §5). So A₃₄′ is not run-local. Any proof must use the closure of the Γ-cycle, e.g. the relation c₂₀ = ρ(c₀) at L = 20 (§2).

**Coupling test (coordinator, Job Q) [data, jobm-gamma-sequences.jsonl].**
- *"In a period with a k = 4 failure, the k ≤ 2 visits of that period and the next are all lockless with f ≥ 2"* is **false**: it holds for this period in 3/7 cases and for the next period in 0/7.
- The sharpest true coupling found is an **anti-coupling**: every k = 4 failure (7/7) is preceded by an R3k0 exit (the state whose R₊₃ swap breaks J) that is **not** lockless with f ≥ 2. It is lockless with f = 1 in 4 cases, DL in 2, and Lock2-only in 1.
  - The converse fails: 27 of 133 k = 4 successes also follow such an R3k0.
  - So failures cluster: a k = 4 failure costs its own 8 and usually ≥ 6 at the preceding k = 0.
- Hence Lemma S_Γ on such cycles is paid by the other period(s): p26 #87942 has 8 + 32, p26 #36087 18 + 34.
- A per-period coupling lemma of the suggested kind is not available.

**k = 3 [proved from P1–P3].**
- J(R3k3) = J(R1k0) is decided by steps 0 and 1 (from R3k4 and R1k1, the "far" (m,z) and (m,y) swaps) applied to J(R3k4).
- So a k = 3 failure needs either J(R3k4) false and not restored by steps 0–1, or a break at step 0 or 1. [data] The latter happens once in 140 (p25 #16945).

Lean: P1 is a finite adjacency-and-colour check on the 11-vertex hole neighbourhood (v, x₀..x₄, w₀..w₄, m). It needs only the face structure x_t ~ w_{t−1}, w_t, w_t ~ w_{t+1} (t + 1 ≠ k). I did not write it this session. It would be a `decide` over the explicit path list, once the repo's hole-neighbourhood structure from `QuarterRotationPlanar.lean` is imported.

### 0.1 Scope and the order-27 data

**Scope.** §0 is for (5,5,5,5,6) holes only. The degree-6 position enters exactly once, in P1. With a single degree-6 link vertex p, the ring is w₀..w₄ with **only** m inserted (between w_{k−1} and w_k). So the four other ring edges w_t w_{t+1} exist, and these are what the five P1 paths use.
- At (5,5,5,6,6) a second extra ring vertex breaks one of these edges.
- The period also differs there: Jobs J/R report R2 states on Γ-cycles at order 27, and a Lemma S failure at p27 #316043 h18 (C = 18 < D = 20, one orientation).
- P2 uses only that p, m, y, z carry four distinct colours and that the R-swap at R3k3 and at R1k2 is in the pair {c(p), c(m)}. Both come from the (5,5,5,5,6) colour tables (Lemma D; the R1 m-colours of `NightC1Gamma.md` §1).

**Order 27 [Studio, Jobs J/R; `jobr27/`].** On 202 (5,5,5,5,6) Γ-cycle records:
- the one-edge rule, the universal period, P3's break-at-8 / restore pattern and A₃₄′ (230/230) all hold;
- Lemma S has minimum ratio 1.95.

**F₄ fails**, however (p27 #133619 h21, both orientations: one of the two k = 4 lockless exits has f = 1).
- This **contradicts the k = 4 half of `NightF6.md` §2** ("a lockless exit at k = 4 lands on f ≥ 2", marked [proved]). That proof has a gap, which I could not locate without the state: there is no plantri on this machine, and the jobr27 files carry no rotation system.
- Candidate weak points are in that proof's own steps: the claim that the off-link {1,2}-path R from w₄ to w₁ survives σ and φ_B⁻¹ (φ_B⁻¹ swaps the {0,3}-component K_φ, which could contain a 0-vertex adjacent to R; this does not recolour R, but the closed-walk argument then needs x₁ ∉ K_φ only); and the identification "f ≥ 2 ⇔ x₀ ∼₁₃ x₂ in t₁".
- **Studio request:** dump the R3@4 state of p27 #133619 h21, its σ-image s, t₁ = π(s) and t₂, with the rotation system.
- §0 does not use f anywhere. It concerns only lockless versus not.

## 1. What mix suffices [proved arithmetic]

Debt per block of 10 R-steps is 10 (Σλ = L, L/10 blocks). Each block has one R3 state at each k = 4, 3, 2, 1, 0, in this order, two steps apart (HP2 Lemma 2; Job M confirms on all 140 blocks).

Worths of a lockless exit, 3f − 1:
- 8 at k = 4 under F₄ (133/133 at orders 25–26). **F₄ is false at order 27**: p27 #133619 h21 has a k = 4 lockless exit with f = 1, worth 2 (both orientations; Jobs J/R). The safe value is ≥ 2;
- ≥ 5 at k = 3 (proved);
- ≥ 2 at k ≤ 2 (proved);
- 8 whenever f = 3.

| block has lockless | k = 3, 4 credit | needed from k ≤ 2 |
|---|---|---|
| e₄ and e₃ | ≥ 13 | 0 |
| e₄ only | 8 | ≥ 2: one lockless k ≤ 2 exit |
| e₃ only | 5 or 8 | ≤ 5: three exits at worth 2, or one with f ≥ 2 |
| neither | 0 | 10: needs f = 3 at two of k = 0, 1, 2 (or 8 + 2) |

Per cycle at L = 20, the k = 3, 4 exits alone suffice iff (s₄, s₃) ∈ {(2,1), (2,2)}, or s₃ = 2 with both k = 3 exits at f = 3. A uniform k = 3, 4 success fraction suffices alone iff it is ≥ 10/13.

## 2. The rotating colour pair [proved]

**Role dynamics on actual colours [proved; checked].** An R-step from a state with roles (α, μ, A, B) and repeat j swaps the {α,A}-component of x_{j+2}. In the **actual** (un-renamed) colouring the new roles are (α, B, μ, A), with repeat j + 3 (`NightC1Gamma.md` §1; `NightF6.md` §1.1).
- [data] All 2,400 DD R-steps at (5,5,5,5,6) holes, orders 16–21, both orientations, satisfy this on actual colours (`ls/roles.py`).
- So α = 0 throughout, and (μ, A, B) has period 3:

| i mod 3 | μ | A | B | swap at step i → i+1 |
|---|---|---|---|---|
| 0 | 1 | 2 | 3 | {0,2} |
| 1 | 3 | 1 | 2 | {0,1} |
| 2 | 2 | 3 | 1 | {0,3} |

**Visits.** Let r = c₀ be R3@4. The k = 4 visits are at i = 10b, with frame j unchanged, since 30 ≡ 0 mod 5. The k = 3 visits are at i = 10b + 2. p, m, y and z are fixed vertices (`NightF6Flow.md` §2.1(c); Job N 280/280).
- At i = 10b (k = 4): c(p) = B_i and c(m) = 0. The question is "pm is a bridge of G[v ∪ {0, B_i}]", equivalently "y ∼ z in {μ_i, A_i}".
- At i = 10b + 2 (k = 3): c(p) = A_i = B_{10b}, and the question is in the same pair.
- Since 10b ≡ b mod 3, block b's question lives in the matching M_b:

| b mod 3 | pair of p, m | pair of y, z |
|---|---|---|
| 0 | {0,3} | {1,2} |
| 1 | {0,2} | {1,3} |
| 2 | {0,1} | {2,3} |

**Invariance lemma [proved].** A Kempe swap in a pair Q preserves, as vertex sets, the colour classes Q and Q^c. Hence it preserves G[v ∪ P] for P ∈ {Q, Q^c}, and it preserves the question of every visit whose matching contains Q.

The swaps between visits are as follows (b ≡ 0 shown; the others follow by the 3-cycle (1 2 3)):
- steps 1, 2 (r → t, inside block 0): {0,2} and {0,1}. **Both lie outside M₀ = {03|12}.** These are the only swaps that can change the in-block answer, and they do so only on K₁ ∪ K₂ (`NightF6.md` §1.1: K₁ ∌ x₀, w₄, m, y; K₂ ∌ x₃, y, m).
- steps 3 … 10 (t → r′): {0,3}, {0,2}, {0,1}, {0,3}, {0,2}, {0,1}, {0,3}, {0,2}.
  - The question changes from M₀ in c₂ to M₁ in c₁₀.
  - The {0,3}-swaps preserve block 0's graph, and the last swap ({0,2}, step 10) preserves block 1's graph.
- For L = 20 the closure gives c₂₀ = ρ(c₀) with ρ = (1 2 3) on colours. The question of "block 2" (M₂ in c₂₀) is block 0's question relabelled. **An L = 20 Γ-cycle asks exactly two questions: M₀ in c₀ and M₁ in c₁₀.**

**Consequences.**
- (a) The in-block "one event" [Job M: 132 + 6 of 140] is persistence of one 2-colour graph question across two swaps outside the matching. A change needs the cut cycle (or the y–z path) to meet a recoloured vertex of K₁ ∪ K₂.
  - [sketch] By (D), a {0,B}-cycle C through pm survives unless a 0-vertex of C lies in K₁ ({0,2}) or K₂ ({0,1}).
  - A y–z {μ,A}-path P survives unless one of its A-vertices lies in K₁ or one of its μ-vertices lies in K₂.
  - Neither m nor y lies in either component, but the rest of C or P can. This happens once in 140 blocks (p25 #16945).
- (b) **A₃₄′ is a statement about two different matchings.**
  - For L = 20 it reads: pm is not a non-bridge both in G[v ∪ {0,3}] of c₀ and in G[v ∪ {0,2}] of c₁₀, where c₁₀ is reached from c₀ by the ten swaps above.
  - No single 2-colour graph is preserved across a block boundary. So a "cut at most once per two visits" proof cannot track one y–z connection. It must say why a {0,3}-cycle through pm in c₀ forces a {1,3}-path y ∼ z in c₁₀ (equivalently, no {0,2}-cycle through pm).
- (c) **Where the cut cycle goes [proved].** At a k = 4 visit, p's neighbours in G[v ∪ {0,B}] are only v, x₀ and m (p has degree 6: v, x₃ (A), x₀ (0), y (μ), m (0), z (A)). Also v's neighbours there are only the two 0-coloured link vertices x₀ and x₂.
  - So a failure means m is {0,B}-joined, avoiding p, to x₀ or x₂, hence (off the link) to w₀ or w₂ (the B-coloured ring vertices next to x₀ and x₂).
  - Job N's sizes fit this: |K_{0,B}(p)| = 9–11 at failures against 5–10 at successes. The cycle closes through the hole side.

[data] The local windows show that the closure is essential. At 20 #20 h0, a DL window t → r′ (9 states) has both the M₀ question at t and the M₁ question at r′ failing. So "M₀ fails in c₂ ⇒ M₁ holds in c₁₀" is **false** as a statement about 8 swaps. Any proof must use that the run continues around a full Γ-cycle. For L = 20 this is the relation c₂₀ = ρ(c₀).

## 3. Lemma S in matching language [conjecture]

**Conjecture A₃₄″.** On a Γ-cycle at a (5,5,5,5,6) hole, no two consecutive blocks both have their (matching-M_b) pm-question failing. For L = 20 this is A₃₄ (≤ 1 failing block). For L = 60 the data have 0 failures.
- [data] 62/62 records.
- With (i) it gives ≥ 2 + 5 = 7 credit per two blocks from k = 3, 4. With F₄, where it holds, it gives ≥ 13.

**Conjecture F₀₁₂″.** A block whose e₄ or e₃ fails has k ≤ 2 credit ≥ 10 − (its own k = 3, 4 credit), with one allowed exception per cycle. This is paid by a neighbouring block's surplus of ≥ 3, since a block with e₄, e₃ lockless has ≥ 13.
- [data] The failing blocks have patterns 11100 (credit 18, 24, 30), 00110 (13), 10001 (16), 11000 (16) and 10000 (8, the one exception; the partner block has 32).

A₃₄″ + F₀₁₂″ ⇒ Lemma S_Γ (bookkeeping as in §1).

## 4. Per-block data table [data, Job M, (5,5,5,5,6), orders 25–26]

Bits are k = 0..4, with 1 = lockless; credit is Σ(3f − 1). Blocks start at R3@4. L = 20 unless stated. Duplicate rows are distinct Γ-cycles at the same hole.

| run | graph | hole | block 0 | block 1 | cycle credit |
|---|---|---|---|---|---|
| m25m | p25#16945 | 3 | 00111 (18) | 00110 (13) | 31 |
| m25 | p25#16945 | 3 | 10001 (16) | 10011 (21) | 37 |
| m26 | p26#87942 | 22 | **10000 (8)** | 01111 (32) | 40 |
| m26m | p26#87942 | 22 | 00111 (24) | 11000 (16) | 40 |
| m26 | p26#75311 | 19 | 00111 (21) | 00111 (21) | 42 (×2) |
| m26 | p26#88643 | 24 | 00111 (21) | 00111 (21) | 42 (×2) |
| m26m | p26#75311 | 19 | 10011 (21) | 10011 (21) | 42 (×2) |
| m26m | p26#88643 | 24 | 10011 (21) | 10011 (21) | 42 (×2) |
| m26m | p26#71592 | 3 | 01111 (26) | 00111 (18) | 44 (×2) |
| m26 | p26#41859 | 3 | 11111 (22) | 10111 (26) | 48 |
| m26m | p26#41859 | 3 | 10111 (23) | 11111 (25) | 48 |
| m26 | p26#71592 | 3 | 10011 (21) | 11011 (29) | 50 (×2) |
| m25 | p25#14805 | 5 | 11111 (25) | 10111 (26) | 51 |
| m25 | p25#17710 | 19 | 10111 (23) | 11111 (28) | 51 |
| m25m | p25#17710 | 19 | 11111 (25) | 10111 (26) | 51 |
| m26m | p26#36087 | 15 | 11111 (34) | 11100 (18) | 52 |
| m25m | p25#14805 | 5 | 11111 (31) | 10111 (23) | 54 |
| m26 | p26#41724 | 4 | 11111 (31) | 10111 (23) | 54 |
| m25m | p25#14805 | 5 | 11111 (31) | 10111 (26) | 57 |
| m26m | p26#41724 | 4 | 10111 (23) | 11111 (34) | 57 |
| m26 | p26#36087 | 15 | 11100 (24) | 11111 (34) | 58 |
| m26 | p26#38516 | 20 | 11111 (34) | 11100 (24) | 58 |
| m26m | p26#45501 | 19 | 10111 (26) | 01111 (32) | 58 |
| m25 | p25#14805 | 5 | 11111 (34) | 10111 (26) | 60 |
| m26 | p26#41724 | 4 | 11111 (37) | 10111 (23) | 60 |
| m26m | p26#41724 | 4 | 10111 (23) | 11111 (37) | 60 |
| m26 | p26#45501 | 19 | 10111 (32) | 11011 (29) | 61 |
| m26 | p26#38442 | 18 | 00111 (24) | 11111 (40) | 64 (×2) |
| m26m | p26#38442 | 18 | 10011 (24) | 11111 (40) | 64 (×2) |
| m26m | p26#38516 | 20 | 11100 (30) | 11111 (34) | 64 |
| m25, m25m | p25#17710 | 19 | 11111 (37) | 11111 (28) | 65 |
| m26m | p26#72507 | 18 | 01111 (26) | 11111 (40) | 66 |
| m26m | p26#55419 | 21 | 11111 (34) | 11111 (34) | 68 (×2) |
| m26 | p26#72507 | 18 | 11111 (40) | 11011 (32) | 72 |
| m26 | p26#55419, p26#72505 | 21, 16 | 11111 (37) | 11111 (37) | 74 (×2 each) |
| m25, m25m, m26m | p25#5594, p26#43840 (m), p26#87914 (m, ×2) | | 11111 (37/40) | 11111 (40/37) | 77 |
| m26, m26m | p26#43840, p26#87914 (×2), p26#72505 (m, ×2) | | 11111 (40) | 11111 (40) | 80 |
| m26, m26m | p26#87887 (L = 60, ×2 each) | 21 | 6 × 11111 (40) | | 240 |

Summary:
- in-block (e₄, e₃): TT 132, FF 6, TF 1, FT 1;
- (e₃ of block b, e₄ of block b + 1): TT 126, FT 7, TF 7, **FF 0**;
- blocks with credit < 10: 1 of 140.

## 5. Local-window checks [data; `ls/blk.py`, `blk2.py`, `blk3.py`]

(5,5,5,5,6) holes, gentri lists, both orientations, all R3@4 DL states.

| check | orders | result |
|---|---|---|
| (e₄, e₃) on R3@4 → R3@3 DL windows | 17–22 | TT 26, TO 11, OT 11, OO 66: correlated, not equal |
| full DL blocks, all five exits fail | 17–22 | 11 of 18 full blocks (17 #3 h0, h16; 22 #134, #152, #177, #413, #476, #568) |
| e₃(t) and e₄(π⁸t), 9 DL states | 16–22 | OO 2 (20 #20 h0, both orientations), OT 3, TO 3 |
| DL windows ≥ 11 from R3@4 | 16–24 | none at ≤ 22; 2 at 23 (no double failure); 15 at 24, **one with consecutive k = 4 failures** (24 #3611 h0) |

**Order 24 (`blk2.py 24`, 12 min, one core, AC power).**
- DL windows from R3@4 of length ≥ 11: 15. In these, (e₄, e₃, e₄ next) =
  - TTT 5;
  - FFT 4;
  - TFT 1;
  - TFF 1;
  - **TFF with e₃ next T: 2**;
  - **FTF: 1**.
- **Consecutive k = 4 failures inside one DL run do occur**: 24 #3611 h0 (gentri numbering, unmirrored), a maximal DL run of 18 states (`ls/one.py`).
- The J trace is
  `R3k1:1 R1k3:1 R3k0:1 R1k2:0 R3k4:0/X R1k1:1 R3k3:1/L R1k0:1 R3k2:1 R1k4:1 R3k1:1 R1k3:1 R3k0:1 R1k2:0 R3k4:0/X R1k1:1 R3k3:1/L R1k0:1`.
  Each failure is a fresh break at R3k0 → R1k2, restored at step 0, exactly as P3 says. Other windows have e₄ next false after e₄ true.
- So A₃₄′ (no two consecutive k = 4 failures) is **not a property of R-runs**. It can only come from the Γ-closure (the run closes up after L/10 periods), or it is false on larger Γ-cycles.
- This sharpens §0: the double break at R3k0 in consecutive periods is possible in a run, so no window argument proves A₃₄′.

## 6. Reproduction

Session scratchpad `ls/`, not committed; single core, AC power.

| script | content | time |
|---|---|---|
| `roles.py` | role map on actual colours | 5 s |
| `blk.py ORD` | block patterns on DL windows | 3 s (16–20), 40 s (21–22) |
| `l1.py ORD` | J at every DL R1/R3 state by (type, k): Lemma P1 check | 60 s (16–22) |
| `near2.py ORD` | J before and after each R-step between R1/R3 states, by swapped pair and component contents: Corollary P3 check (near swaps T→T only) | 60 s |
| `near.py ORD` | the same over **all** Kempe swaps of all states: near swaps alone do not preserve J (e.g. (p,y)-swaps with K ∋ p, y: T→F 196 times at orders 16–18), so P3 needs P1 | 20 s |
| `trace.py ORD` | J along maximal DL runs | 60 s |
| `blk2.py`, `blk3.py` | 11-state windows; consecutive-block pairs | 40 s (16–22), 150 s (23) |

These use the F6 `base.py` (`kempe_py.py`, `rev_f5.py`). §4 is a 1 s pass over `jobm-gamma-sequences.jsonl`, rotated to start at kmask 16 and cut into blocks of 10.
