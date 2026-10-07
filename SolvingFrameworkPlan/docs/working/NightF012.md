# Night: F₀₁₂′ and the k ≤ 2 exits on Γ-cycles at (5,5,5,5,6) holes

Night worker, 7 October 2026 (written 03:02 MDT). **Exploratory. Hand arguments plus single-core reads of Studio files (Jobs M, O, P, Q; Job R at order 27). Unreviewed.**

This note builds on:
- `NightF6Flow.md` §2.2, for Lemma S_Γ, F₀₁₂′ and A₃₄′;
- `NightC1Gamma.md` §2, for the frame and duality (D);
- `NightF6.md`;
- the night-log entries for Jobs M–R.

The scope is (5,5,5,5,6) only. At (5,5,5,6,6) the period has R2 states (coordinator, Job R).

Labels:
- [proved] means proved by hand, modulo (D) where that is said;
- [data] means read from the files by the scripts in §6;
- [conjecture] means not proved;
- [killed] means refuted by the data.

## Frame and notation

The frame at an R3 state is the one used in C1Gamma:
- link x₀..x₄ = α, μ, α, A, B;
- ring w₀..w₄ = B, A, B, μ, A;
- p = x_k is the degree-6 link vertex, with y = w_{k−1}, z = w_k and m its third outer neighbour;
- σ swaps K_σ, the {α,μ}-component of x₁.

The credit of a lockless exit is 3f − 1. A **fixed point** is a state with σ(r) = r, i.e. K_σ is the whole {α,μ}-subgraph of T − v; Job Q's flag means exactly this.

## Verdict

1. **[proved] The k ≤ 2 fixed point is a forest condition (§1).** At R3@k with k ≤ 2:
   - {c(p), c(m)} = {α, μ}, so σ swaps the {c(p),c(m)}-component of p itself;
   - the complementary pair is {c(y), c(z)} = {A, B};
   - y and z are always joined in {A,B} by a fixed 6-vertex path P around the far side of the hole (P = y … x₄x₃ … z);
   - **σ(r) = r ⇔ the {A,B}-subgraph of T − v is acyclic** (direction ⇐ is elementary; direction ⇒ uses (D)).

   So at every k the exit is a question about the complementary pair {c(y),c(z)}:
   - at k = 3, 4 it asks whether y ∼ z (one edge, NightF6Flow);
   - at k ≤ 2, y ∼ z is automatic through P, and the question is whether any {A,B}-cycle exists anywhere.

   That is why no one-edge rule exists at k ≤ 2 (Job P).
2. **[data] F₀₁₂′ is not a period statement, and 7L/20 is not forced by the period structure.**
   - The k ≤ 2 credit of a period can be as low as 2, with pattern (k2, k1, k0) = (L1, X, X). This happens in 3/140 periods at orders 25–26 and 8/412 at order 27.
   - It falls below 7 in 13/140 and 11/412 periods, for every choice of period phase.
   - The per-cycle bound is tight at exactly two cycles, p25m #16945 h3 and p27 #273919 h26, by **the same mechanism**: in both periods k1 and k0 are fixed points, and k2 is lockless with f = 1 in one period and f = 2 in the other, giving 2 + 5 = 7.
   - A cycle with (L1, X, X) in every period would have k ≤ 2 credit L/5 < 7L/20. Nothing local excludes it.
3. **[killed] The coordinator's joint lemma.** "A fixed point at k ≤ 2 forces lockless f = 3 at k = 3, 4 of the same period" fails in:
   - 22/50 periods with a fixed point at orders 25–26, and 46/94 at order 27;
   - the same counts for "the next period";
   - 18/50 and 34/94 for "the same or the next period".

   The usual counterexample is k3 lockless with f = 2 next to (X, X): (L3, L2, X, X, L3) occurs ×11.
4. **[conjecture; data, sharp] The right unit is the shifted window.** Let W(r) = (r, π²r, π⁴r, π⁶r, π⁸r) for r an R3@3 state, i.e. the exits at k = 3, 2, 1, 0 and then the **next** k = 4.

   **Lemma W.** On every Γ-cycle at a (5,5,5,5,6) hole, the lockless-exit credit of every W(r) is ≥ 10.
   - Min 10 at orders 25–26 (attained once: p25m #16945 h3, labels L3 L1 X X S2). 0 failures in 140 windows.
   - Min 16 at order 27; 0 failures in 412 windows.
   - The W(r) partition the R3 states of the cycle into L/10 windows of debt 10, so **Lemma W ⇒ Lemma S_Γ** with no further input. It replaces the pair A₃₄′ + F₀₁₂′.
   - Of the five R3 phases, this is the only one where the per-window bound survives. The Job M blocks (from R3@4) fail once with credit 8, and the other phases fail with credit down to 0.
5. **[conjecture; data] Lemma W splits into three 0-failure statements (§3), each with an explicit Kempe reading:**
   - **W1.** k3 or k4′ is lockless.
   - **W2.** Some k ≤ 2 exit in W is lockless; in particular no period has three fixed points.
   - **W4.** If k4′ fails, then k3 is lockless with f = 3.

   With F₄ (f = 3 at k = 4), W1 + W2 + W4 ⇒ Lemma W:
   - k4′ fails: 8 + 2 = 10;
   - k3 fails: 8 + 2 = 10;
   - neither fails: 5 + 8 + 2 ≥ 10.

   F₄ fails once at order 27 (p27 #133619 h21). That window still has credit 17, so at order 27 Lemma W itself is the safe statement.

## 1. The k ≤ 2 fixed-point condition

### 1.1 Roles [proved; data-checked]

Here p = x_k has neighbours (in rotation) x_{k−1}, w_{k−1} = y, m, w_k = z, x_{k+1}, v. Every other link vertex has degree 5, so w_t ∼ w_{t+1} whenever x_{t+1} ≠ p.

| k | p | y | z | m (adjacent to p, y, z) | {c(p),c(m)} | {c(y),c(z)} |
|---|---|---|---|---|---|---|
| 0 | x₀ = α | w₄ = A | w₀ = B | μ | {α,μ} | {A,B} |
| 1 | x₁ = μ | w₀ = B | w₁ = A | α | {α,μ} | {A,B} |
| 2 | x₂ = α | w₁ = A | w₂ = B | μ | {α,μ} | {A,B} |
| 3 | x₃ = A | w₂ = B | w₃ = μ | α | {α,A} | {μ,B} |
| 4 | x₄ = B | w₃ = μ | w₄ = A | α | {α,B} | {μ,A} |

At k ≤ 2, p ∈ {x₀, x₁, x₂}, which lies in K_σ, and m is p's neighbour of the other colour in {α,μ}. So K_σ = K_{c(p),c(m)}(p) ∋ p, m.

The R₊₃ step swaps {α,A}. That gives the predicted swapped pairs at R3k4, k3, k2, k1, k0: (m,z), (p,m), (p,y), (m,z), (p,y). This is exactly Job O's universal pattern at period positions 0, 2, 4, 6, 8 (140/140 periods at orders 25–26), which checks the table against the data.

### 1.2 The local {A,B}-path [proved; data]

At k ≤ 2 the path

  P: y … x₄ x₃ … z

is an alternating A/B path. Explicitly:
- k = 0: w₄ x₄ x₃ w₂ w₁ w₀;
- k = 1: w₁ w₂ x₃ x₄ w₄ w₀ (reversed);
- k = 2: w₂ x₃ x₄ w₄ w₀ w₁ (reversed).

The adjacencies used are the link edge x₃x₄, the faces x₂x₃w₂ and x₄x₀w₄, and the ring edges at degree-5 link vertices.

Hence **y ∼ z in {c(y),c(z)} at every R3@k, k ≤ 2**. [data] Job O: 140/140 per k at orders 25–26 and 412/412 at order 27, against 7/140 and 12/412 failures at k = 3, 4.

### 1.3 Lemma Fix [proved; ⇒ mod (D)]

At R3@k with k ≤ 2: σ(r) = r ⇔ the {A,B}-subgraph of T − v has no cycle.

*Proof (⇐ fails, i.e. a cycle C kills the fixed point).*
- C ⊂ T − v bounds two discs, and v lies inside one of them, D_v.
- x₀, x₁, x₂ are coloured α/μ, so they are not on C. They are adjacent to v, so they lie inside D_v.
- Take an edge e of C and the face on the other side. Its third vertex u is not on C, since a properly coloured triangle needs three colours. Also u ≠ v, and u is coloured α or μ, since it is adjacent to an A-vertex and a B-vertex.
- Every {α,μ}-path from x₁ to u would have to meet C, which is impossible. So K_σ is not the whole {α,μ}-subgraph, and σ(r) ≠ r. ∎

*Proof (⇒: not fixed gives a cycle).*
- If the {α,μ}-subgraph is disconnected, (D) gives a closed walk in colours A, B (v allowed) separating two α/μ vertices.
- v's only non-{α,μ} neighbours are x₃ and x₄. So each passage x₃ v x₄ can be replaced by the edge x₃x₄, across the face v x₃ x₄, which contains no vertex. Separation is preserved.
- The resulting closed {A,B}-walk in T − v separates two vertices, so it contains a cycle. ∎

**Reading.** At k ≤ 2 the {A,B}-graph already contains P from y to z around the hole.
- A fixed point means P is the only y–z connection and there is no other {A,B}-cycle anywhere: the {A,B}-graph is a forest.
- The exit exists as soon as one {A,B}-cycle appears anywhere, for example a second y–z route, which closes a cycle with P.

This is the k ≤ 2 counterpart of the k = 3, 4 criterion "y ∼ z in {c(y),c(z)}". It is global (any cycle counts), which explains Job P's "no edge works at k ≤ 2". It is also consistent with Job Q, where the steps that create a fixed point merge the rest of the {α,μ}-graph: merging {α,μ} components is the same as destroying the last {A,B}-cycle.

### 1.4 Colour bookkeeping across the three k ≤ 2 questions [proved]

Name the colours at R3k2 (position 4) as p = 1, m = 2, y = 3, z = 4. The universal period (Job O: pairs and swapped-component contents) gives:
- position 4, R3k2: fixed ⇔ the {3,4}-graph is acyclic;
- step 4 swaps {1,3} ∋ p, y, then step 5 swaps {1,2} ∋ m, y;
- position 6, R3k1: (p, m, y, z) = (3, 1, 2, 4), and fixed ⇔ the {2,4}-graph is acyclic;
- step 6 swaps {1,4} ∋ m, z, then step 7 swaps {1,3} ∋ p, z;
- position 8, R3k0: (p, m, y, z) = (1, 4, 2, 3), and fixed ⇔ the {2,3}-graph is acyclic.

Over one full period (p, m, y, z) goes from (1, 2, 3, 4) to (1, 4, 2, 3): a 3-cycle on the colours of m, y and z, of order 3 in periods.

Since a swap of {a,b} preserves the {a,b}- and {c,d}-subgraphs:
- the {2,4}-graph at position 6 is the position-4 {2,4}-graph changed only on step 5's component;
- the {2,3}-graph at position 8 is the position-6 {2,3}-graph changed only on steps 6 and 7.

So the three fixed-point questions of a period ask about the three pairs avoiding p's position-4 colour, each perturbed by one or two swaps through m or p. W2 (§3) says they are never all answered "acyclic". I have no proof of that.

## 2. f at k ≤ 2

- **f ≥ 1 always** [proved, cited]. A lockless σ(r) is a whole u = 1 excursion. Its π-image is filled (F5 Lemma 1), so the credit is ≥ 2.
- Distribution [data]:
  - orders 25–26: f = 1/2/3/5 = 43/27/265/1;
  - order 27: f = 1/2/3/4/5/8 = 93/127/829/4/2/1.
- **When f ≤ 2** [data, correlation only]. At k = 2, a lockless exit with f ≤ 2 is often followed (two π-steps later) by a fixed point at k = 1:

  | order | f = 1 | f = 2 | f = 3 |
  |---|---|---|---|
  | 25–26 | 9/19 | 12/14 | 4/86 |
  | 27 | 10/19 | 6/41 | 19/293 |

  At k = 0, f = 2 follows a k = 1 fixed point in 4/8 cases (orders 25–26).
- So low f and fixed points cluster in the same half-period (R3k2 → R3k1 → R3k0), which is where the {α,μ}-graph is nearly connected. I have no proof of any f-level at k ≤ 2. The f ≥ 2 / f = 3 arguments of NightF6 §2 use K_σ = {x₀, x₁, x₂}, which fails at k ≤ 2.

## 3. Windows: what is true per period [data]

Each test was run over all phases of the period (`f012.py` [2]). "Total" means all five R3 exits; "k ≤ 2" means the k ≤ 2 exits only.

| window (10 states) | min total, 25–26 | min total, 27 | min k ≤ 2 |
|---|---|---|---|
| from R3k4 (Job M blocks) | 8 | 8 | 2 |
| from R3k3 (= W) or R1k1 | **10** | **16** | 2 |
| from R1k0 / R3k2 / R1k2 | 8 | 8 | 2 |
| from R1k4 / R3k1 / R1k3 / R3k0 | 0 | 0 | 0 |

On W (140 + 412 windows) the sub-statements are:

| statement | failures, 25–26 | failures, 27 |
|---|---|---|
| W1: k3 or k4′ lockless | 0 | 0 |
| W2: a k ≤ 2 exit lockless | 0 | 0 |
| W2′: no period has fixed points at all of k = 2, 1, 0 | 0 | 0 |
| W4: k4′ fails ⇒ k3 is L with f = 3 | 0 (7 cases) | 0 (12 cases) |
| k3 fails ⇒ k4′ is L with f = 3 | 0 (7 cases) | 0 (12 cases) |

- The number of lockless exits in a window is ≥ 2 always. It is exactly 2 in 4 + 8 windows.
- **Why W and not the Job M block.** Job O's failure event is "k4 fails, then k3 fails two steps later" (a break by the step-8 far (p,y)-swap). The Job M block puts both failures in one block. W separates them: the k4 failure ends one window and the k3 failure starts the next, so each window loses at most one k ≥ 3 exit (W1).
- The two tight cases:
  - **p25m #16945 h3.** Windows (L3 L1 X X S2) = 10 and (L3 L2 X X L3) = 21. The single unpaired k4 failure sits in the window whose k ≤ 2 part is (L1, X, X), and k3 = L3 pays exactly 8.
  - **p27 #273919 h26.** Windows 21 and 18. Tight for F₀₁₂′ but not for W.
- The p26 #87942 h22 short block (8) of Job M becomes windows of ≥ 16.

## 4. Status

| item | statement | status | support |
|---|---|---|---|
| §1.1 roles | {c(p),c(m)} = {α,μ} and K_σ ∋ p, m at k ≤ 2 | [proved] | Job O pattern 140/140 |
| §1.2 | y ∼ z in {A,B} through P at k ≤ 2 | [proved] | 552/552 |
| Lemma Fix | fixed ⇔ the {A,B}-graph of T − v is acyclic | [proved], ⇒ mod (D) | consistent with Jobs P, Q |
| f ≥ 1 | credit ≥ 2 | [proved] (F5 Lemma 1) | — |
| F₀₁₂′ per period / any phase | k ≤ 2 credit ≥ 7 per period | [killed] | 13/140, 11/412 periods < 7 |
| "fixed point ⇒ f = 3 at k = 3, 4 of the same / next period" | | [killed] | 22/50, 46/94 |
| F₀₁₂′ per cycle | ≥ 7L/20 | [conjecture], tight twice, same mechanism | 62/62, 202/202 |
| **Lemma W** | credit(W(r)) ≥ 10 for every R3@3 state r | [conjecture], tight once | 140/140, 412/412 |
| W1, W2, W4 | §3 | [conjecture] | 0 failures |
| Lemma W ⇒ Lemma S_Γ | | [proved] (W partitions the R3 states) | — |

**Recommendation.** Replace "A₃₄′ + F₀₁₂′" in NightF6Flow §2.2 by Lemma W (or W1 + W2 + W4 + F₄ at orders ≤ 26).
- W1 is the A₃₄′ mechanism localised. It needs Job O's "never two consecutive k = 4 failures" in the sharper form "a k = 3 failure and the following k = 4 failure never share a window".
- W2 is a statement about three {·,·}-forests in one period (§1.4).
- W4 is the only new coupling between the k ≤ 2 and k ≥ 3 sides. Its support is 19 cases.

**Studio requests.**
1. Run Lemma W, W1, W2 and W4 at order 28, or on the bigsample (5,5,5,5,6) Γ-cycles.
2. At every R3@k, k ≤ 2, record the number of independent {A,B}-cycles (the cycle rank of that graph), to watch Lemma Fix's quantity along the period.
3. Find the f-mechanism at k = 2: is f ≤ 2 ⇔ some condition on π²σ(r) versus σ(π²r)?

## 5. Proved versus conjectured, in one line

The fixed-point condition is now exact and geometric: the {A,B}-forest of Lemma Fix. F₀₁₂′ is a true but non-local average, and its 7L/20 bound is not forced. The local truth is Lemma W, a per-window bound of 10 that is tight once and that alone implies Lemma S_Γ.

## 6. Reproduction

Scripts are in `backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/nightf012/`. Each is a single core and runs in under 2 s, on AC power.
- `python3 f012.py` (orders 25–26) and `python3 f012.py ../jobr27/` (order 27) give sections [1]–[11] in `out2526.txt` and `out27.txt`. These read `jobm-gamma-sequences.jsonl` and `jobo-steps.jsonl`.
- `xcheck.py [DIR]` aligns `jobq-steps.jsonl` with `jobm-gamma-sequences.jsonl`: Job Q's fixed flag equals Job M's 'X' label at every R3 state (0 disagreements, 62 + 202 cycles).
