# NightImagesBoundary: why σ-images of Γ-cycles land on heavy cycles

[exploratory] Night swarm note, 7 October 2026, 06:21 MDT. These are leads until re-checked.

**Sources:**
- NightStatementC and NightSigmaImage.
- Night log entries for Jobs BI, BJ and BK.
- Lean files `QuarterLemmaP`, `QuarterExcursion`, `QuarterU34`, `QuarterWinding` and `QuarterBudget`.

**New run:** `backgroundMaterial/planemap-structural/longtable/local-runs/37-nightimagesboundary/`.
- Engine: `lib26.Eng` via `jobaq.load`, the same engine as NightStatementC and Job BI.
- Data: the same 36 census classes (64 Γ-cycles) and 122 hit classes (284 Γ-cycles).
- Machine: 2 cores, AC power, about 3 minutes.
- `ib.py` records, for each class with a Γ-cycle:
  - each π-cycle's (L, Λ, F, #N₀, #L1, #L2, #DL, #excursions, max u, max f, #states whose σ-partner is a non-fixed DL state);
  - the class-wide σ kind matrix;
  - each Γ-cycle's σ-images (target cycle and target kind).
- `ana.py` produces `ana-out.txt`.

**Notation:**
- **Kinds.** N₀ is lockless, L1 is Lock1-only, L2 is Lock2-only, DL is doubly locked.
- **Boundary state.** An unfilled state of kind N₀, L1 or L2.
- **Heavy for Z.** H_Z is the set of π-cycles T ≠ Z with Λ(T) ≤ −Λ(Z). Here Λ(Z) = L(Z).
- **(c)(Z).** Some non-fixed σ-image of Z lies off Z, on a cycle in H_Z.

## 0. Verdict

1. **The boundary hypothesis is half true.**
   - The σ-images of all L states of a Γ-cycle split as follows (census / hits): 51% / 55% are boundary states, 34% / 31% are non-fixed DL, and 15% / 14% are fixed points.
   - The DL images come from the R1 states:
     - 140 / 700 of them land on Z itself, at σ = π^{L/2} (NightSigmaImage §2);
     - the rest land on twin Γ-cycles or on open DL runs.
   - On the **R3** states, every non-fixed image is a boundary state (0/640, NightSigmaImage). This is data, not formal.
2. **There is no forcing mechanism, and no counting argument can supply one.**
   - Involution counting forces (c) for 1 of 348 Γ-cycles (§3.2).
   - Every other Γ-cycle has room for all of its images to land light.
   - (c) ⇒ R\* (NightStatementC C2), so any proof of (c) is 4CT-strength.
3. **What explains (c) is "kind-matched uniform landing" together with one exact concentration fact.** The two parts:
   - (i) The images of each kind behave like uniform draws from the class's states of that kind. They are slightly better than uniform for boundary kinds and slightly worse for DL images. The kind-matched model predicts the observed best ratio exactly for the median Z (§2.3).
   - (ii) Lockless states sit almost entirely on heavy cycles: 87% (census) and 94% (hits) of all N₀ states. There is an exact reason. **Lemma N₀ (§1.2):** on every π-cycle, 2·N₀(T) ≤ |DD(T)| − Λ(T). Every Γ-cycle has ≥ 3 lockless images, and their heavy landing rate is 97% (census) and 99% (hits).
   - The giant cycle's share is irrelevant. What matters is the heavy **tail's** share of each kind. For lockless states that share is 0.64–0.99 per Z.
4. **The sharpest surviving conjecture is (IB-N₀):** every Γ-cycle has a **lockless** σ-image on a cycle T with Λ(T) ≤ −Λ(Z).
   - Data: 64/64 (minimum 5 such images) and 284/284 (minimum 3).
   - It implies (c), and it fits the formal excursion lemmas: a lockless image starts a (1, f) excursion of mass 1 − 3f ≤ −2.
   - It is untested on the 2,728 BK census Γ-cycles. Studio Job BT should test it (§4).

## 1. Exact statements

### 1.1 (a) Image kinds and run positions [formal]

`lemmaP` places each kind of state in its unfilled run (u is the run length):

| kind | position in its unfilled run |
|---|---|
| DL | interior |
| L2 | first state, u ≥ 2 |
| L1 | last state, u ≥ 2 |
| N₀ | the whole run, u = 1 |

Consequences on a single cycle T with excursions:
- **#L1(T) = #L2(T) = E_{≥2}(T).** Checked on 1,733 / 59,709 cycles (`checks` in `ana-out.txt`).
- **The boundary count B_T := N₀ + L1 + L2 = N₀ + 2E_{≥2}.** It lies between e_T and 2e_T, where e_T = N₀ + E_{≥2} is the number of excursions.

Formal facts about σ:
- σ is an involution on unfilled states and keeps j (`sigSwap_sigSwap`).
- σ stays inside the Kempe class, so it is an involution on U(K).
- The kind matrix is symmetric. This is checked, and it is automatic.
- σ rarely swaps a run end with a run start: L1 → L2 occurs 22 times (census) and 1,284 times (hits), against L1 → L1 at 1,202 and 102,134.

| image of an L state of a Γ-cycle | census (1,280) | hits (7,320) |
|---|---|---|
| fixed | 198 | 1,004 |
| N₀ | 480 | 2,532 |
| L2 / L1 | 84 / 84 | 748 / 748 |
| DL, not fixed | 434 (140 on Z) | 2,288 (700 on Z) |

Further observations:
- Images that land on another Γ-cycle: 24/64 Z (census) and 90/284 Z (hits). These are the R1 twins.
- In the aggregate, the L1 and L2 columns are equal. That is the mirror orientation exchanging Lock1 and Lock2, not a per-class identity: 2/36 and 0/122 classes have it individually.
- U34 makes the failure images precise. A k = 4 failure image is L2 and starts a (3|4, ·) run. A k = 3 failure image is L1 and ends a run with forward pattern (1, 1).
- A lockless image starts a (1, f) excursion with mass 1 − 3f. When it comes from a k = 3 state, f ≥ 2 (`sigma_hit_f_ge_two_k3`).

### 1.2 (b) −Λ(T) by excursions [formal, plus two new one-liners]

`sum_lam` and `excursion_mass` give

  **−Λ(T) = 4F_T − L_T = 3F_T − U_T = Σ_{excursions of T} (3f − u)**,

and Λ(Z) = L(Z) on a Γ-cycle. So T is heavy for Z ⇔ **F_T ≥ (L_T + L_Z)/4**: its filled density exceeds ¼ by L_Z/(4L_T).

**Bounds from u ≥ 1 and f ≤ f_max(T)** [proved; checked on every cycle]:
- −Λ(T) ≤ 3F_T − e_T;
- −Λ(T) ≤ (3f_max(T) − 1)·e_T ≤ (3f_max − 1)·B_T.

So a heavy cycle has ≥ L_Z/(3f_max − 1) excursions and boundary states: at least 10 when f_max = 1, which is 63% of cycles (census) and 73% (hits). The converse fails:

- **Light cycles can be boundary-rich.** Cycles with Λ = 0 have boundary/U = 0.66, against 0.77–0.78 on heavy cycles.
- **The excursion density barely moves with mass:** e/L is 0.25 on Λ = 0 cycles and 0.27 on Λ/L ≤ −½ cycles.

So "boundary ⇒ heavy" is **not** a usable bias. L1 and L2 states are spread over light cycles too: Λ = 0 cycles hold 20–26% of them.

**Lemma N₀ (lockless states need negative mass or DD surplus) [proved, one line from `exact_identity`].** For every π-cycle T,

  Λ(T) = |DD_T| − 2N₀(T) − E₂(T) − 3τ_T, hence **2·N₀(T) ≤ |DD_T| − Λ(T)**.

Consequences:
- A cycle with no DL→DL step has N₀ ≤ −Λ/2.
- A Λ = 0 cycle has N₀ ≤ |DD|/2.
- A cycle that is light for Z (Λ > −L_Z) has N₀ < (L_Z + |DD_T|)/2.

Data, as shares of all class states of each kind:

| cycles | states | N₀ | L1+L2 | DL | F | σ-partner DL |
|---|---|---|---|---|---|---|
| census Λ ≤ −20 | 0.767 | **0.874** | 0.695 | 0.565 | 0.843 | 0.687 |
| census Λ = 0 | 0.129 | **0.007** | 0.256 | 0.208 | 0.070 | 0.168 |
| census −20 < Λ < 0 | 0.074 | 0.119 | 0.049 | 0.038 | 0.087 | 0.044 |
| hits Λ ≤ −20 | 0.864 | **0.942** | 0.778 | 0.761 | 0.905 | 0.781 |
| hits Λ = 0 | 0.094 | **0.005** | 0.201 | 0.193 | 0.047 | 0.187 |

Lockless states are the one kind whose position is forced onto negative cycles by an identity.

### 1.3 (c) The counting model and its exact prediction

**Model (an assumption, not a theorem).** Each non-fixed off-Z image of kind κ is an independent uniform draw from the states of kind κ on cycles T ≠ Z. Write

  h_κ(Z, x) = Σ_{T≠Z, −Λ(T) ≥ x·L_Z} n_κ(T) / Σ_{T≠Z} n_κ(T),  with h_κ(Z) := h_κ(Z, 1).

Then:
- **P_model(best ratio ≥ x) = 1 − Π_{images s} (1 − h_{κ(s)}(Z, x)).**
- **P_model((c) fails) = Π_s (1 − h_{κ(s)}(Z)).**

Variants:
- the uniform-U model replaces h_κ by the unfilled share h_U;
- the excursion model uses only boundary images and the excursion share h_E = Σ_H e_T / Σ e_T.

| | census (64 Z) | hits (284 Z) |
|---|---|---|
| h_U per Z: min / median | 0.48 / 0.77 | 0.73 / 0.82 |
| h_E per Z: min / median | 0.54 / 0.81 | 0.76 / 0.87 |
| h_N₀ per Z: min / median | **0.64 / 0.90** | **0.83 / 0.94** |
| h_DL per Z: min / median | 0.42 / 0.61 | 0.69 / 0.76 |
| Σ_Z P_model(fail): uniform-U / kind / excursion | 4·10⁻⁴ / 2·10⁻⁵ / 7·10⁻⁴ | 4·10⁻⁸ / 1·10⁻⁸ / 4·10⁻⁵ |
| max_Z P_model(fail), kind model | 3·10⁻⁶ | 2·10⁻⁹ |
| observed (c) failures | 0 | 0 |

**Exact statement of the model's prediction.** The model expects 0.00002 failures in the census and 10⁻⁸ at the hits.

The model's median best ratio, x_med(Z) := sup{x : P_model(best ≥ x) ≥ ½}:
- equals the observed best ratio for at least the median Z in both sets;
- observed/model has minimum 0.41 and 10th percentile 0.72 in the census, and minimum 0.78 and 10th percentile 1.0 at the hits.

In words: **the best ratio is the one that random kind-matched images would find**. The 4/3 in Job BK is the ratio of the heaviest cycle reachable at all, not a sign of a forced landing.

## 2. Is there a bias beyond the model?

### 2.1 Heavy landing by kind (observed against the kind-matched expectation)

| image kind | census n / heavy / expected | hits n / heavy / expected |
|---|---|---|
| N₀ | 480 / **465** / 418 | 2,532 / **2,505** / 2,348 |
| L1 | 84 / 72 / 59 | 748 / 622 / 576 |
| L2 | 84 / 73 / 59 | 748 / 604 / 577 |
| DL (off Z) | 294 / 128 / 178 | 1,588 / 1,170 / 1,197 |
| all | 942 / 738 / 714 | 5,616 / 4,901 / 4,697 |

- Boundary images over-land on heavy cycles. The lockless rate is 0.97 / 0.99 against 0.87 / 0.93 expected.
- DL images under-land, because they go to R1 twins and Γ-cycles.
- The net enrichment is small: +3% (census) and +4% (hits).
- Per Z, each Γ-cycle has **≥ 5 / ≥ 3 lockless images, all but 15 / 27 of them on heavy cycles**. No Z lacks a heavy lockless image.

### 2.2 Candidate bias statements

| statement | status |
|---|---|
| every non-fixed σ-image of a DL state is a boundary state | **false** (R1 images: 434 and 2,288 DL) |
| …restricted to R3 states | data 640/640 (NightSigmaImage); not formal |
| a σ-image of a Γ-state is never on a Γ-cycle unless fixed | **false**: 140/700 land on Z (σ = π^{L/2}) and 24/90 Z hit twins; all are R1 |
| every lockless image lands heavy | **false**: 15/480 and 27/2,532 (minimum ratio 0.4) |
| (IB-N₀) some lockless image lands heavy | data **64/64, 284/284** |
| (IB-B) some boundary image lands heavy | data 64/64 (minimum 6), 284/284 (minimum 6) |
| (c_M) some image on the giant cycle | killed (NightStatementC: 4/284, 16/64) |

## 3. Involution counting: what it can and cannot force

### 3.1 The exact reformulation

σ is an involution on U(K), so

  **(c)(Z) ⇔ σ(Z) ∩ H_Z ≠ ∅ ⇔ Z ∩ σ(H_Z) ≠ ∅.**

In words: some unfilled state of a heavy cycle is σ-paired into Z. The same holds kind by kind: Z's lockless images are exactly the lockless states whose partner lies on Z.

Theorem W fixes Σ_K λ and the floor fixes its sign. Neither says anything about which cycles the partners of a given cycle's states lie on. A counting argument must therefore use only the sizes of the sets. No cycle-level statement about σ is formal other than injectivity (`budgetSigma_injOn`, `no_double_hit`).

### 3.2 The best counting bound, and its data

Let D\* be the set of states whose σ-partner is a non-fixed DL state. Then σ(Z∖Fix) ⊆ D\*, and σ is injective. If (c) fails, σ(Z∖Fix) ⊆ D\* ∖ H_Z. So:

  **|D\* ∖ H_Z| < |Z ∖ Fix| ⇒ (c)(Z)** [proved].

The slack |D\* ∖ H_Z| − |Z∖Fix| per Z:

| | min | median | max | forced |
|---|---|---|---|---|
| census | **−7** | 24 | 47 | 1/64 (p27 #315355 h3 mirror) |
| hits | 179 | 361 | 657 | 0/284 |

So counting forces (c) only on one tiny class. The obstruction is structural. D\* ∖ H_Z always contains:
- Z itself (the R1 self-images);
- the twin Γ-cycles;
- the light L1/L2-rich Λ = 0 cycles, which hold 17–19% of D\*.

A kind-split version (lockless partners only) would need N₀(D\* ∖ H_Z) < (number of lockless images of Z). The lockless part of D\* ∖ H_Z is small but not computed per Z here, so this is left to Job BT item 5. Given Lemma N₀ and the Λ = 0 / light-negative N₀ shares (0.5–12%), it is unlikely to bind at the hits.

### 3.3 Does the heaviest cycle's σ-image meet every Γ-cycle?

No. This is (c_M), and it is killed. What survives is the union over the heavy tail H_Z. Since (c) ⇒ R\*, no argument from Theorem W, the exact identity and the involution property alone can force it. Each of those holds on a hypothetical class with F = 0 as well: all states are DL, every cycle is Γ, and H_Z = ∅. Any proof has to use planarity beyond these identities.

## 4. The sharpest conjecture, and Studio Job BT

**Conjecture IB-N₀.** At every (5, ·)-hole, for every Γ-cycle Z, some r ∈ Z has σ(r) lockless and Λ(T(σ r)) ≤ −Λ(Z).
- IB-N₀ ⇒ (c) ⇒ R\*.
- Its excursion form: σ(r) starts a (1, f) excursion of mass 1 − 3f on a heavy cycle.
- Weaker fallback **IB-B**: the same with any boundary kind (N₀, L1 or L2).
- Data: 64/64 (census, minimum 5 heavy lockless images) and 284/284 (hits, minimum 3).
- Expected margin: kind-matched P_model(fail) ≤ Π(1 − h_N₀) ≤ 0.36⁵ ≈ 6·10⁻³ per Z at the worst census class.

**Studio Job BT (images against target excursion counts and Λ): exact spec.** Run it on the BK set (orders 25–27, all patterns, both orientations, 2,728 Γ-cycles plus the 10,412 positive cycles as control).

Per class, per π-cycle T, record:
- L, Λ, F, #N₀, #L1, #L2, #DL, e_T, E₂, τ, |DD|, f_max;
- #states whose σ-partner is non-fixed DL.

Check `Λ = L − 4F`, `#L1 = #L2`, and Lemma N₀ (`2N₀ ≤ |DD| − Λ`) on every cycle. These are exact; any failure is an engine bug.

Per Γ-cycle Z, for each image: its kind, (target T, Λ(T), e_T, B_T), its excursion (u, f, mass), and whether it is R3 or R1.

Report:
1. **IB-N₀ and IB-B** pass counts, the minimum number of heavy lockless / boundary images, and the minimum best-lockless ratio. **A kill of IB-N₀ while (c) holds** separates the lockless mechanism from (c).
2. **The R3 boundary statement**: a non-fixed R3 image is never DL, over all 2,728 Γ-cycles. Also the R1 self-image offset (L/2?) at L = 40 and 60.
3. **The kind-matched model:** Σ_Z P_model(fail), and observed/model best ratio quantiles. The min-ratio case p25 #17650 h3 (4/3) needs its own line: its P_model(fail) and h_κ.
4. **The heavy-landing table by kind** (§2.1), and the lockless share by mass bin (§1.2), on the full census.
5. **Counting slack** |D\* ∖ H_Z| − |Z∖Fix| and its sign count.
6. **Correlation**: for target T, the number of images landing on T against e_T, B_T, N₀(T) and −Λ(T). Fit the image rate per state of each kind. "Images per lockless state is constant across T" is the kind-matched model.

**Kill and escalation rules:**
- An IB-N₀ failure with (c) intact: (c)'s mechanism is not lockless-specific. Fall back to IB-B.
- A Lemma N₀ violation: engine bug.
- Observed/model best ratio ≪ 1 on many Z: images avoid heavy cycles, which would be a real anti-bias. Report it.

## 5. Status

| item | status |
|---|---|
| kind ↔ run position; #L1 = #L2 per cycle | [formal] `lemmaP`; checked 61,442 cycles |
| −Λ(T) = 4F − L = Σ_exc (3f − u) | [formal] `sum_lam`, `excursion_mass` |
| −Λ ≤ 3F − e, −Λ ≤ (3f_max − 1)e | [proved] (one line) |
| Lemma N₀: 2N₀(T) ≤ \|DD_T\| − Λ(T) | [proved] (one line from `exact_identity`); Lean: a corollary of `exact_identity` on an orbit |
| (c)(Z) ⇔ σ(H_Z) meets Z | [proved] (involution) |
| counting forcing \|D\*∖H_Z\| < \|Z∖Fix\| ⇒ (c) | [proved]; applies to 1/348 |
| non-fixed images all boundary | **killed** for all L states (R1); R3: data only |
| kind-matched uniform model explains (c) and its best ratio | [data] median observed = model; Σ P(fail) ≤ 10⁻³ |
| lockless concentration on heavy cycles | [data] 87–94% of N₀ on Λ ≤ −20; explained in part by Lemma N₀ |
| IB-N₀ (some lockless image on a heavy cycle) | [data] 64/64, 284/284; **conjecture**, 4CT-strength; Job BT |
| a counting proof of (c) | impossible from W, the exact identity and the involution alone (they survive F = 0) |

Reproduction (`local-runs/37-nightimagesboundary/`):
- `python3 ib.py census` takes 2 s.
- `python3 ib.py hits` takes 3 min on 2 cores.
- `python3 ana.py ib-census.json ib-hits.json > ana-out.txt`.
- `gl/` holds regenerated symlinks and is not committed.
