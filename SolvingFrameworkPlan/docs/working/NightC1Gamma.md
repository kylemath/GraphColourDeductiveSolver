# Night: Conjecture C1Γ at (5,5,5,5,6) holes, exact σ-exit criteria and the obstruction

Night worker, 7 October 2026 (written 02:04 MDT). **Exploratory. Hand arguments plus single-core checks. Unreviewed.**

Builds on:
- `NightFloorAtEasyHoles.md` (F5, Lemma 3);
- `NightF5Review.md` (the exact identity);
- `NightFloorHP.md` (Lemmas A–D);
- `NightFloorHP2.md` (Lemma 2, Γ-cycles, Conjecture C1Γ);
- `NightFloorR53.md` (Lemma 3′);
- Studio Job E (`local-runs/27-studio-positive-config/jobe-summary.txt`, `jobe-gamma-holes.jsonl`), which the coordinator relayed mid-task.

Labels:
- [proved]: a hand argument modulo the cited facts and the standard Kempe/Jordan duality (D below);
- [data]: computed by the scripts in §6;
- [Studio]: taken from the Job E files;
- [conjecture]: not proved.

Frame. These are as in HP:
- link x₀..x₄ = α, μ, α, A, B (relative to the repeat j);
- ring w₀..w₄;
- the degree-6 vertex is p = x_k;
- m is p's extra outer neighbour, adjacent to p, w_{k−1} and w_k;
- R3 = (w₀..w₄) = (B, A, B, μ, A);
- σ swaps K_σ, the {α,μ}-component of x₁.

## Verdict

1. **C1Γ is false** [Studio]. The first failure is at p25 #14805 h5. At orders 25 and 26, 8/60 and 41/290 Γ-cycle R3 states have no lockless σ-exit (per orientation). p25 #5594 h18 itself satisfies C1Γ (10/10).
   - Locally I reach the same conclusion from the other side. The forced ring colouring along an all-DL run gives **no** information about any σ-exit. Each exit is a radius-unbounded Kempe-connectivity statement, and windows of DL states on both sides do not force it (§3).
2. **Exact σ-exit criteria at every position k [proved; data: 0 exceptions at orders 16–22, both orientations]:**
   - **k = 3.** σ(r) is lockless iff w₂ lies in the {μ,B}-component of x₁ (the Lock2 component, which also contains w₀, w₃ and x₄). Otherwise σ(r) has **exactly Lock1**.
   - **k = 4.** σ(r) is lockless iff w₄ lies in the {μ,A}-component of x₁ (the Lock1 component, which also contains x₃). Otherwise σ(r) has **exactly Lock2**.
   - **k = 0, 1, 2.** If w₃ ∉ K_σ, σ(r) is lockless. This is sufficient only: it is exact at orders ≤ 20, and the converse fails 268 times at orders 21–22.
   - **Main k = 0, 1, 2 failure mechanism [data]:** K_σ is the **whole** {α,μ}-subgraph. Then σ(r) = r, a fixed point of the involution, and r is its own (DL) σ-image. This accounts for 550 of the 558 DL σ-images at k = 0, 1, 2 at orders 16–21; the other 8 are R3 states on a DL run.
   - This matches the Studio "same cycle, odd count" failures, e.g. a single k = 1 failure on a cycle. The Studio should confirm it (S2).
3. **The redirected target (σ-joined group) cannot be paid locally [data].** At R3 states with DL neighbours on both sides:
   - A lockless exit lands on a u = 1 excursion worth 1 − 3f. Here f = 1, worth exactly −2, in 180 of 236 cases at k = 0, 1, 2 (orders 16–21).
   - Single-lock exits land on excursions with f = 1 (one case has f = 3). At k = 3, 4 these have u ∈ {3, 4}, worth 0 or +1; at k = 0, 1, 2, u ∈ {2, 3, ≥5}. So they bring at most 1 and usually **no** local credit.
   - So the "the excursion behind a one-lock exit pays ≥ 2" step of the relayed plan is false as stated. The credit must come from the whole target cycle.
   - Over all R3 states (orders 16–21), 391 of 1,762 excursions hit by a non-DL σ-image cannot pay 2.
4. **(5,5,5,5,5) Γ-cycles, counted exactly [data].** At 17 #4 h0/h16 and 22 #649 h0/h21, both orientations:
   - all 10 R3 states of each Γ-cycle (L = 20, Σλ = 20) have lockless exits;
   - **all 10 land on one single π-cycle**;
   - every landing excursion has f = 3, worth −8;
   - the target cycle sums are −80 and −220, so the group sum is −60 and −200.
   - At (5,5,5,5,5) the lockless σ-image of any R3 state with DL neighbours has f = 3 (848/848, orders 17–22). This is far more than F5's 2 per state.

## 1. Rigidity of an all-DL run [proved, mostly cited]

- Along a DL run the types alternate: R3@k → R1@k+2 → R3@k−1 (HP Lemma A, HP2 Lemma 2).
- At every state the 6-vertex ring (w₀..w₄ and m) is forced up to role names.
  - R3: Lemma D.
  - R1 = (A, B, μ, α, μ): m is forced to B, α, A, B, A for k = 0, 1, 2, 3, 4. m sees p, w_{k−1} and w_k, which have three distinct colours.
- **Role dynamics.** One R-step maps the roles (α, μ, A, B) to (α, B, μ, A), a 3-cycle on {μ, A, B}.
- **Kempe memory.** The swap at an R-step is an {α,A}-swap, so it preserves the {μ,B}-components and nothing else among the cross pairs.
  - Hence each Kempe fact about a pair survives exactly one step: r's {μ,B} is πr's Lock1 pair, and the next step swaps the colour μ.
  - Consequently the 2-ball data along a run is **constant up to relabelling**. The plan "the forced ring colouring decides the cut condition" is empty: the ring is the same at every R3@k whether or not the exit exists.

## 2. The exact criteria

**(D) Duality used.** In a triangulation with a proper 4-colouring, take two vertices with colours in a pair P. They lie in different components of the P-subgraph minus a vertex z iff some closed walk through z, of vertices with colours outside P (v allowed, being uncoloured), separates them. This is the standard Kempe/Jordan fact for triangulated discs. It was used in QRP's Jordan step and is not re-proved here.

**k = 3 [proved].** Here p = x₃ and m = α.
- **Lock2′ dies.** x₄ has degree 5, and its neighbours in σ(r) are x₃ (A), x₀ (μ), w₃ (μ) and w₄ (A).
- **Lock1′ reduces to a cut condition.** Lock1′ exists iff w₁ and m are joined in K_F − x₂ (Lemma 3′(c); x₃ ~ m).
- **Cut condition by D.** The rotation at x₂ is x₁, w₁, w₂, x₃, v. A separating walk through x₂ must use w₂ together with x₁ or v. So it continues through {μ,B} vertices from w₂ to x₁ or x₄, which are joined by Lock2.
- **Hence** σ(r) is lockless ⇔ w₂ ∈ K_{μ,B}(x₁).

**k = 4 [proved].** This is the mirror argument at x₀.
- The rotation at x₀ is v, x₁, w₀, w₄, x₄.
- Lock1′ dies at x₃: x₃ has degree 5, and its neighbours in σ(r) are x₂ (μ), x₄ (B), w₂ (B) and w₃ (μ).
- Lock2′ exists iff w₀ and m are joined in K_B − x₀.
- **Hence** σ(r) is lockless ⇔ w₄ ∈ K_{μ,A}(x₁).

**k = 0, 1, 2 [proved, sufficient only].**
- x₃ and x₄ have degree 5, and x₀, x₂ ∈ K_σ.
- If w₃ ∉ K_σ, then after σ neither x₃ nor x₄ has an α_old-neighbour, so both locks die.
- If K_σ is the whole {α,μ}-subgraph, then σ(r) = r is DL.

[data] Orders 16–22, both orientations, all R3 DL states, (criterion, σ(r) lockless):

| k | orders 16–20 | orders 21–22 |
|---|---|---|
| 3 | (T,T) 47, (F,F) 54 | (T,T) 1,125, (F,F) 483 |
| 4 | (T,T) 47, (F,F) 54 | (T,T) 1,125, (F,F) 483 |
| 1 | exact: (T,T) 50, (F,F) 32 | (T,T) 512, (F,F) 472, **(F,T) 88** |
| 0 | (T,T) 138, (F,F) 69, (F,T) 14 | (T,T) 1,078, (F,F) 1,088, (F,T) 90 |
| 2 | (T,T) 138, (F,F) 69, (F,T) 14 | (T,T) 1,078, (F,F) 1,088, (F,T) 90 |

## 3. Why no window argument proves C1Γ [data]

For each R3 DL state I recorded the status of π⁻²r, π⁻¹r, πr and π²r.
- At orders 16–22, k = 3 has 7 states with **all four DL and a lockless exit**, and 51 with all four DL and no lockless exit.
- At 17 #3, 21 #40 and 22 #353, R3@3 and R3@4 states with ≥ 5 DL states on both sides are D₀.
- So no window of radius ≤ 2 (and, at k = 3, 4, none of radius 5) decides the exit. A proof would have to use the closing of the cycle, and Job E shows that closing does not force it either.

## 4. What the σ-group proof must count [proved bookkeeping; conjecture]

Let c be a Γ-cycle, with L = 10n and Σ_c λ = L = 5w. It has L/2 R3 states, L/10 at each k. Split them by exit:
- a lockless exits;
- b single-lock exits (only at k = 1, 3, 4 in the Studio data);
- d DL exits (fixed points or same-cycle).

Proved facts:
- σ is an involution on unfilled states, so the a + b exit images are distinct states.
- A lockless image is a whole u = 1 excursion, worth 1 − 3f ≤ −2. Distinct images give distinct excursions.
- A Lock1-only image is the end s_u of its run, and a Lock2-only image is the start s₁. So any excursion receives at most 2 single-lock charges. Locally it never receives 2.

Sufficient local inequality (**Conjecture G**):

  L ≤ Σ over the lockless exits s of (3f(s) − 1),

with the excursions of distinct Γ-cycles disjoint. If G holds, then the group of c restricted to these excursions is nonpositive without using b or d.
- It holds at (5,5,5,5,5), with slack: 80 against 20.
- At (5,5,5,5,6) it needs, for example, a ≥ 5 with mean f ≥ 5/3. The Studio minimum is a = 5 (p25 #16945 h3, p26 #87942 h22). Locally f = 1 is common at k = 0, 1, 2.
- If G fails, the payment must use the rest of the target cycles. That is π-global on the target, and I see no local proof.

## 5. Studio checks (orders 25–26, both orientations, every Γ-cycle)

- **S1.** Assert the k = 3 and k = 4 criteria of §2 at every Γ-cycle R3 state:
  - k = 3: lockless ⇔ w₂ ∈ K_{μ,B}(x₁), and otherwise exactly Lock1;
  - k = 4: lockless ⇔ w₄ ∈ K_{μ,A}(x₁), and otherwise exactly Lock2.
  This confirms or refutes §2 at order 25.
- **S2.** For each DL-exit failure at k ∈ {0,1,2}, report whether σ(r) = r (K_σ is the whole {α,μ}-subgraph) or σ(r) is another state, and of which type. This confirms or refutes the fixed-point mechanism.
- **S3.** For each Γ-cycle report a, b and d, and for each lockless exit its f and its target cycle's w. Then test Conjecture G and whether two positive cycles ever share a target cycle.
- **S4.** For single-lock exits, report the landing excursion's (u, f). The local prediction is f = 1 and u ≥ 3 at k = 3, 4, i.e. no local credit.
- **S5.** Report the f of every lockless exit on Γ-cycles at (5,5,5,5,5) holes of orders 25–26. The local prediction is f = 3 always. Is it a lemma?

## 6. Reproduction (session scratchpad `c1g/`, not committed; single core, AC power)

| script | content | time |
|---|---|---|
| `probe.py ORD` | §2 criteria per k; DL-window context | 3 s (16–20), 40 s (21–22) |
| `probe2.py`, `probe3.py` | DL-run context and neighbour lock status (§3) | 10 s, 42 s |
| `gam5.py ORD 5\|6` | (5,5,5,5,5) Γ-cycle targets; k = 0, 1, 2 σ-image kinds (fixed points) | seconds |
| `conj.py`, `fdist.py`, `exits.py` | σ-intertwining test (negative), landing (u, f), per-excursion credit (§1, §4) | ≤ 15 s each |

All scripts import the F6 `base.py`, which in turn uses `kempe_py.py` and the QuarterPi table re-implemented in `rev_f5.py`.
