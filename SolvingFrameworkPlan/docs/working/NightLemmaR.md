# Night: Lemma R (remainder of nonpositive σ-targets) — KILLED as a per-target lemma; what survives

Night worker, 7 October 2026 (written 03:02 MDT). **Exploratory. Hand arguments plus single-core reads/runs. Unreviewed.**

Builds on `NightF6Flow.md` §1, `NightF5Review.md` §1 (exact identity), `NightEulerHole.md` (Theorem W), `QuarterWinding.lean` (`lam_eq`), the Job K records (orders 25–26) and the Studio's order-27 Job K records (`27-studio-positive-config/jobr27/jobk-records.jsonl`, coordinator's message). New run: `longtable/local-runs/28-lemmaR/` (§5).

Labels: [proved] hand argument modulo the cited facts; [data]; [killed] a counterexample is in the data.

## Verdict

1. **[killed] Lemma R is false, in the Job K form AND in the NightF6Flow DD-endpoint form.**
   - Order 27 (Studio, coordinator): p27 #68456 h19, (5,5,5,5,6), both orientations: target w = −2, L = 38, 2 hits with f = 3, rem = −10 + 16 = **+6**. The hole's only positive cycle is a **Γ-cycle**. On a Γ-cycle every state is DL, so every state is a DD endpoint: the two forms coincide there, and the DD-endpoint form fails too.
   - Orders 20–24 (gentri, both orientations, my run §5): the DD-endpoint form (hits from R3 DD endpoints of positive cycles, target ≠ source) fails on **11** nonpositive targets, all with **w = 0**, rem = +2. Typical target: L = 8, excursions (u, f) = (1, 1) hit + (5, 1) free. Sources: mixed positive cycles (w = 1, L = 17 or 21). Patterns (5,5,5,6,6), (5,5,6,6,7), (5,5,5,7,7), (5,5,6,6,6), (5,5,5,6,8); none at (5,5,5,5,6) at orders ≤ 24.
   - The 210/210 at orders 25–26 is reproduced (`jobk-lemmaR-check.txt`), but it is not a theorem.
   - Studio Job S (`jobs-records.jsonl`, DD-endpoint form) confirms this: 0 failures at orders 25–26, and 12/732 at order 27. These are p27 #68456 h19 (both orientations) and 10 targets with Λ = 0, L = 8, hit once at f = 1 (rem +2). Job S also finds #exits = #distinct hit excursions everywhere.
2. **[proved] There is no double counting.** Two exits never hit one excursion, and the credit 3f − 1 is *exactly* the λ-mass of the hit excursion (§1). So restricting sources to DD endpoints can only delete hits; it cannot remove an over-count, because there is none. The failures are a genuine overflow: the target has its own positive DL runs, and its hit excursions were the only thing paying for them.
   - **Answer to "where does the rest of the claimed credit come from".** It comes from nowhere: the credit is confined to the hit excursions. At p27 #68456 h19 the target T (L = 38, Λ = −10) contains two hit excursions (u, f) = (1, 3). Each has 4 states and λ-mass −8, so together they have 8 states and mass −16, exactly the credit claimed.
   - The other 30 states of T have Σλ = +6. They are DL runs with u > 3f, net positive, and they are **not** hit. Λ(T) = −16 + 6 = −10.
   - So the claim 16 exceeds the sink capacity 10 because T's unhit part is positive, not because anything is counted twice.
   - p27m #166916 h19 is the same at size 8: Λ = 0, with one hit (1, 1) of mass −2 and an unhit part of +2, which at orders ≤ 24 is always a single (5, 1) run.
3. **[proved] Exact form and reduction (§2).**
   - rem(T) = Σ over the free (non-hit) excursions of (u − 3f) = |DD_T| − 2N₀^free − E₂(T) − 3τ^free.
   - Lemma R holds automatically for any target with no free excursion with u > 3f. Every failure needs a DL run with u ≥ 3f + 1 in T.
   - Such runs are common: 118 of 203 nonpositive targets at orders ≤ 24 have one, typically (4,1) or (5,1). So the 25–26 success was not structural.
4. **[proved] The group-level form (§3a).** Split rem = rem⁺ − rem⁻. The identity of NightF6Flow §1.2 makes
   **P⁺(g): Σ_{Z∈P_g} def(Z) + Σ_{T∈N_g} rem⁺(T) ≤ Σ_{T∈N_g} rem⁻(T)**
   necessary and sufficient for σC on g.
   - The natural local certificate, **P₁⁺**, has two steps. First, return each overflow rem⁺(T) to the sources that hit T, giving capped deficits. Second, assign every capped deficit > 0 to one nonpositive σ-neighbour with slack rem⁻.
   - That is, the right pair is "P₁ + positive rems charged back to their own sources", **not** "positive rems covered by other targets". The overflow is credit that never existed in T, so it belongs to the source's deficit.
   - [data, Job S] P₁⁺ holds at every hole of orders 25–27. The check is conservative: each overflow is charged in full to every neighbouring source, assignment is greedy to a single target, 0 failures (`jobs-Pplus-check.txt`).
5. **[proved] What replaces it (§3):** the flow of NightF6Flow §1.3 with **binding sinks**. σC on g follows from **Lemma S^cap** (a transport/Hall condition): the positive cycles' supplies Λ(Z) can be routed with edge capacities c(e) and sink capacities −Λ(T).
   - Single-source data: capping never turns a passing hole into a failing one (0 cases at orders 25–27).
   - At p27 #68456 h19 the capped credit is 49 against a debt of 20.
   - So F6's Γ part is **Lemma S^cap**. Lemma R should be dropped.

## 1. The landing excursion [proved]

Let r be a DL state of a positive cycle Z with repeat index j. Let s = σ(r) be the swap of the {α,μ}-component K of m = x_{j+1}, and suppose s is lockless (unfilled, neither lock).

**(a) σ is an involution that preserves j.**
- x_j and x_{j+2} are α and adjacent to m (link cycle), so both lie in K.
- So s has link (μ, α, μ, A, B) from x_j: the repeat is still at j, m is still x_{j+1}, and α_s = μ, μ_s = α.
- K is the {α,μ}-component of m in s as well. Swapping it again returns r.
- Hence r ↦ σ(r) is injective. Distinct exits have distinct images s.

**(b) The landing excursion has exactly one unfilled state.** By `NightF5Review.md` §1, "neither lock ⇔ u = 1":
- s lacks Lock1, so it is not an R₊₃ image, and π⁻¹s is filled;
- s lacks Lock2, so π(s) = φ_B⁻¹(s) is filled.

So s is the unique unfilled state of its excursion E(s) = {s, πs, …, π^f s}. By (a), **two exits never land in one excursion**, from the same source cycle or from different ones.
- [data] Over all forms at orders 17–24 (346 targets), 0 excursions carry two hit codes, and 0 hit excursions have u ≠ 1.

**(c) λ around the landing state.** Use `lam_eq`, λ(c) = 1 − 2[F c] − 2[F πc]:
- λ(π⁻¹s) = −1 (filled, followed by unfilled: φ_A, M3 short). This state belongs to the *previous* excursion.
- λ(s) = −1 (φ_B⁻¹).
- λ(π^i s) = −3 for 1 ≤ i < f (τ, M3 long), and λ(π^f s) = −1 (φ_A).

So Σ_{E(s)} λ = −1 − 3(f − 1) − 1 = 1 − 3f, and the credit 3f − 1 equals −Σ_{E(s)} λ exactly. E(s) has f + 1 states: f ≥ 2 at k = 3 and f = 3 at k = 4 (F₄; NightF6 §2) give 3 resp. 4 states, worth 5 resp. 8. **The credit counted at the source is exactly the λ-mass present in the target's excursion, no more.**

[data] For each hit excursion, the excursion just before it in T (DD-endpoint form, orders ≤ 24) has:
- u = 3 in 411 cases;
- u = 1 in 96, of which 32 are themselves hit (consecutive hits);
- u = 2 in 25;
- u ≥ 4 in 29.

## 2. Exact form of rem(T) [proved]

Fix T ∈ N with filled states. (A Γ-cycle has Λ > 0. An all-filled cycle has no unfilled state, so it is never hit.) T is a cyclic sequence of excursions (u_E unfilled, then f_E filled), and Σ_E λ = u_E − 3f_E (`NightF5Review.md`). By §1 the hit excursions are distinct u = 1 excursions, so

  rem(T) = Λ(T) − hit(T) = Σ_{E free} (u_E − 3f_E).

Per excursion, u − 3f = [u ≥ 3](u − 3) − 2[u = 1] − [u = 2] − 3(f − 1). Hence, with h = #hits:

  rem(T) = |DD_T| − 2(N₀(T) − h) − E₂(T) − 3(τ(T) − Σ_hits (f_e − 1)).

Consequences:
- **Lemma R(T) ⇔ |DD_T| ≤ 2N₀^free + E₂ + 3τ^free.** The target's own DD steps must be paid by its non-hit excursions. Equivalently, the incoming credit is at most the sink capacity, −hit(T) ≤ −Λ(T).
- **Lemma R holds for every target with no free positive excursion** (all free E have u ≤ 3f), in particular for every target with no DL run of length ≥ 4.
- At the tight record p26 #87887 h21, every excursion of the w = −48 target is hit (30 × (1 − 9) = −240). The free part is empty.

**The counterexamples, read through this formula.**
- *w = 0, L = 8:* T = (1,1)_hit + (5,1)_free, with sum −2 + 2 = 0. T has sink capacity 0, so any hit overflows. The (5,1) run has one DD step and nothing free to pay it.
- *p27 #68456 h19:* w = −2, L = 38, hits 2 × (1,3) = −16, free part +6 over 22 states.

Neither is a counting artefact.

## 3a. The group-level form [proved; data]

Write rem⁺ = max(rem, 0) and rem⁻ = max(−rem, 0). NightF6Flow §1.2 reads

  Σ_g Λ = Σ_{Z∈P_g} def(Z) + Σ_{T∈N_g} rem⁺(T) − Σ_{T∈N_g} rem⁻(T),

so σC(g) ⇔ **P⁺(g)**: Σ_Z def(Z) + Σ_T rem⁺(T) ≤ Σ_T rem⁻(T). Without Lemma R this is just σC restated, so the content lies in a certificate.

**Charge-back.** rem⁺(T) ≤ −hit(T) (because Λ(T) ≤ 0), so the overflow can be split among the exits into T, reducing their allocations a(e) ≤ c(e). That raises the sources' deficits to def^cap(Z) = Λ(Z) − Σ_{e from Z} a(e), and leaves every target at rem^cap(T) = min(rem(T), 0) ≤ 0. This is §3's capped flow with the greedy allocation. With it:

  Σ_g Λ = Σ_Z def^cap(Z) − Σ_T rem⁻(T),

and **P₁⁺**: assign each def^cap(Z) > 0 to one-hop nonpositive σ-neighbours within their slack rem⁻.

- p27 #68456 h19: def = −35, and the overflow 6 is charged back, giving def^cap = −29 ≤ 0. Nothing is left to assign.
- p27m #166916 h19: the non-Γ source has Λ = 10 and its only lockless credit is 2, into the Λ = 0 target, so def = 8. Charging back the overflow 2 gives def^cap = 10 = Λ(Z): its lockless credit was worthless. It is paid by neighbour 0 (Λ = −535).
- [data] Over the Job S records (`check_jobs_Pplus.py`), with every overflow charged in full to every neighbouring source and a greedy largest-first single-target assignment: **0 failures** at orders 25, 26 and 27, both orientations. 10 holes have an overflowing target, all at order 27.

## 3. What survives: the capped flow [proved]

Let A be any allocation a(e) ∈ [0, c(e)] on the exits into N_g with Σ_{e→T} a(e) ≤ −Λ(T) for each T ∈ N_g. Then

  Σ_g Λ = Σ_{Z∈P_g} Λ(Z) + Σ_{T∈N_g} Λ(T) ≤ Σ_{Z∈P_g} (Λ(Z) − Σ_{e from Z} a(e)).

So σC on g ⇐ **Lemma S^cap(g)**: the network of NightF6Flow §1.3 (source → Z with capacity Λ(Z), Z → T with capacity Σ c(e), T → sink with capacity −Λ(T)) has a flow saturating every Λ(Z). By max-flow/min-cut this is the Hall condition

  for every set X of positive cycles of g:  Σ_X Λ(Z) ≤ Σ_{T∈N_g} min(c(X→T), −Λ(T)).

- Lemma R was exactly the hypothesis that makes the min always pick c(X→T) (NightF6Flow §1.3). Without it the min is genuinely needed.
- Positive-to-positive exits still drop out. Lemma P (non-Γ deficits against slack) is unchanged, with −rem replaced by the leftover sink capacity.

[data, Job K records, holes with one positive cycle] The minimum of capped credit / 5w:

| pattern | source | orders 25–26 | order 27 |
|---|---|---|---|
| (5,5,5,5,6) | Γ | 1.55 (p25m #16945 h3) | 2.2 |
| (5,5,5,6,6) | Γ | 1.8 | **0.9** (p27 #316043 h18) |

- Capping never turns raw ≥ debt into capped < debt (0 holes).
- The order-27 (5,5,5,6,6) value of 0.9 is the Studio's Lemma S failure: it is below 1 even raw, so it is not caused by capping.
- Holes with several positive cycles need the per-source split, which the records do not carry. That is a Studio check (§4).

**F6 bookkeeping after this note.** The Γ part is Lemma S^cap_Γ (A₃₄′ + F₀₁₂′ + F₄ feed the edge capacities). Proofs of A₃₄′/F₀₁₂′ must now also respect the sink caps; one way is to prove credit ≥ L counting only targets with −Λ(T) ≥ their incoming credit. Lemma R is not a lemma to prove.

## 4. Status and requests

| item | status | support |
|---|---|---|
| no double counting; credit = excursion mass (§1) | [proved] | 0 multi-hit excursions, orders 17–24 |
| rem formula; R ⇔ own DD paid by free excursions (§2) | [proved] | identity 0 failures |
| Lemma R, Job K form | [killed] | 12 at order 27 (Studio); 11 at orders 20–24 |
| Lemma R, DD-endpoint form | [killed] | p27 #68456 h19 (Γ source: forms coincide); 11 at orders 20–24 (w = 0) |
| Lemma R for targets with no free u > 3f excursion | [proved] | — |
| σC ⇐ Lemma S^cap (Hall with sink caps) | [proved] | single-source: capping harmless, 25–27 |
| σC ⇔ P⁺(g); certificate P₁⁺ (charge-back + one-hop) | [proved] ⇔; P₁⁺ [conjecture] | Job S 25–27: 0 failures (conservative) |

Studio request: per hole, the exact P₁⁺/max flow of §3 with the per-(source, target) credit split, so that overflows are charged only to the sources that actually hit the target. Run it at (5,5,5,5,6), orders 25–27.

## 5. Reproduction (`backgroundMaterial/planemap-structural/longtable/local-runs/28-lemmaR/`)

- `build_lemr.py` copies `27-studio-positive-config/picyc.cpp` (untouched) to `picyc_lemr.cpp`, adds a `--lemr` block, and builds `picyc.lemr`.
  - Per hole with a positive cycle (all patterns), the block prints every hit target's excursions [u, f, hit codes].
  - Each hit code records the source R-type, whether the source is a DD endpoint, and whether the target is the source cycle.
- Inputs: `convert.py gentri` on `studiointel/gentri/tri{17,20..24}.txt`, both orientations. The runs used 2 cores and took about 30 s in total, on AC power. The `out*.jsonl` files are not committed (158 MB) and can be regenerated.
- `lemr_check.py` → `lemr-summary.txt` (forms K, D, A; consistency; violations; excursion statistics).
- `check_jobs_Pplus.py` → `jobs-Pplus-check.txt` (Studio Job S records: P₁⁺ with charge-back, orders 25–27).
- `check_jobk_lemmaR.py` → `jobk-lemmaR-check.txt` (Job K records at orders 25–26 and 27: violations, Γ-source flag, capped single-source credit).
