# NightStatementC: σ-images reach the heavy negative cycles

[exploratory] Night swarm note, 7 October 2026, 05:31 MDT. These are leads until re-checked. Sources: NightPostAW, Night log (05:03 Job AW; Job BI), NightP1 §8, NightSigmaImage, and the Lean files `QuarterExcursion`, `QuarterLemmaP`, `QuarterFlowIdentity`, `QuarterAssignment` and `QuarterWinding`. New run: `backgroundMaterial/planemap-structural/longtable/local-runs/36-nightstatementc/`, using engine `lib26.Eng` via `jobaq.load` (the same engine as Job BI), 2 cores, AC power, about 3 minutes.

Notation:
- K is a Kempe class at a (5,5,5,5,6) hole.
- The π-cycles partition K.
- Λ(C) = Σ_C λ = 5w(C).
- Z is a Γ-cycle, so Λ(Z) = L(Z).
- σ is the {α,μ}-swap at x_{j+1}. It is an involution on unfilled states and keeps j.
- T(s) is the π-cycle containing s.
- M is the most negative π-cycle of K.
- A cycle T is *heavy for Z* if Λ(T) ≤ −Λ(Z).

## 0. Verdict

1. **(c) is exactly "Z has a σ-edge to a cycle that alone could absorb Λ(Z)".**
   - (c) plus a Hall condition gives σC on Z's group through a **credit-free** transport. That transport needs neither the exact identity nor no-double-hit (§1).
   - (c) alone does not give σC. Hall is the only missing ingredient, and the data never come close to binding it.
   - (c) is **4CT-strength**: (c) ⇒ R\* (§1.3).
2. **"Giant cycle" is the wrong picture.**
   - M holds only 10–85% of the class's unfilled states.
   - "M holds ≥ ½ of the filled states" is **false**: it holds in 53/122 hit classes and 8/36 census classes.
   - Some Γ-cycles have **no** σ-image on M: 4/284 at the hits and 16/64 in the census.
   - What (c) uses is the **heavy tail**: the cycles with Λ ≤ −20 hold 47–89% of the unfilled states. Every Γ-cycle sends **≥ 7** of its σ-images there (≥ 9 at the hits).
   - The best heavy target has −Λ(T) ≥ 5.75·Λ(Z) (census) and ≥ 60·Λ(Z) (hits).
3. **(c) is not a pigeonhole fact.** The share of unfilled states on light cycles reaches 0.53, far above 1/20. Z's images are only mildly enriched on heavy cycles: median +7 points at the hits and +16 in the census, and the enrichment is negative for 30% of the Z.

   The data fit "images roughly uniform over unfilled states, plus heavy cycles hold most of them". The chance of all ≥ 10 images being light is then ≤ 0.534¹⁰ ≈ 0.002 per Z. So (c) has a large statistical margin and no visible mechanism.
4. **Star(ii) holds 158/158**, with minimum ratio 1.875. Star(ii) says −Λ(M) ≥ Σ_{Λ>0} Λ, so M alone outweighs all positive mass.
   - Star(ii) **implies the class floor directly**, with no adjacency needed.
   - It is the cleanest structural statement in the data. It is also at least as hard as the floor.

## 1. Exact statements

### 1.1 Statement (c)

**(c)(Z)** for a Γ-cycle Z ⊂ K: there is r ∈ Z with σ(r) ∉ Z and Λ(T(σ r)) ≤ −Λ(Z).

- *Which states.* On a Γ-cycle every state is DL and π maps Z to Z, so **every state of Z is a DD endpoint**. "All L states", "all DD endpoints" and "all states with a σ-image" are the same set.
  - Job BI and this run use all L states. Fixed points and images on Z are excluded.
  - An R3-only variant (the Lemma S_Γ convention) is **untested**.
- *Extension to non-Γ positive Z:* use the DD endpoints of Z (Job AQ convention). This run tests it at the hits: 17/17 hold, with ≥ 11 heavy images each. The census classes have no non-Γ positive cycles.
- *σ∪σ′ variant:* (c′) also allows the link-free lock-breaking images σ′. Job BI: 284/284 and 264/264. (c) ⇒ (c′).

### 1.2 What (c) gives at group level

Let g be a σ-group: a π-closed union of cycles that is connected by σ-links from DD endpoints. By `sum_lam_eq_sum_orbits`, Σ_g λ = Σ_{Z>0} Λ(Z) + Σ_{T≤0} Λ(T).

**Lemma C1 (credit-free transport) [proved, trivial].** Let E be a set of pairs (Z, T), each a σ-edge with Λ(Z) > 0 ≥ Λ(T). Suppose x ≥ 0 on E satisfies:
- Σ_T x(Z,T) = Λ(Z) for every positive Z;
- Σ_Z x(Z,T) ≤ −Λ(T) for every nonpositive T.

Then Σ_g λ ≤ 0 on every group.

*Proof.* Substitute into the orbit sum. Edges stay inside groups. ∎

By max-flow/min-cut (Gale–Hall), such an x exists iff

**(H)** for every set P of positive cycles, Σ_{Z∈P} Λ(Z) ≤ Σ_{T∈N_E(P)} −Λ(T).

Take E to be the (c)-edges, those with Λ(T) ≤ −Λ(Z). Then **(c) is exactly (H) for |P| = 1.** So:

- **(c) + (H on (c)-edges) ⇒ σC on every group.**
- (c) alone suffices on any group with **one** positive cycle, or whose positive cycles have pairwise disjoint heavy neighbourhoods.
- (c) alone does **not** suffice. Two Z with Λ = 20 sharing their only heavy neighbour T with Λ(T) = −20 satisfy (c) and violate σC. No such configuration is in the data.

**Role of the formal identities.**
- The credit-free route uses only Theorem W's orbit sum. The exact identity Σλ = |DD| − 2N₀ − E₂ − 3τ and `no_double_hit` are **not needed**.
- They are needed only for the credit form, `QuarterAssignment`, whose capacity is −rem(T) = −Λ(T) − (incoming lockless credit) and whose demand is def′(Z) ≤ Λ(Z).
- Neither certificate dominates the other: the credit form has smaller capacities and smaller demands.
- The credit-free form is simpler, and its feasibility is exactly (c)+(H). **Lean suggestion:** `sigmaC_of_lam_transport`, a few lines on top of `sum_lam_eq_sum_orbits`. A single-target version would be `Assignment` with def′ := Λ and rem := Λ.

[data] (H) on (c)-edges with class-wide supply holds in 122/122 hit classes and 36/36 census classes. Hall never binds: the positive mass is 20–280 against heavy capacity in the hundreds to thousands.

### 1.3 Strength

**Prop C2 [proved].** If (c) holds for every Γ-cycle of every class at a hole, then every class there has F ≥ 1 (R\*).

*Proof.* Suppose F(K) = 0. Then every state is unfilled with unfilled π-neighbours. By `lemmaP` every state is DL, so every π-cycle of K is a Γ-cycle with Λ = L > 0. Then no T in K has Λ(T) < 0, and (c) fails for every Z ⊂ K. ∎

So (c) ⇒ R\* ⇒ 4CT (NightPostAW §2). **(c) is 4CT-strength.** Like S₁, it cannot have a local proof. It fails in a minimal counterexample, as any floor-type statement must.

### 1.4 Payer forms (Job BI)

- **(b′)** charge-back P₁: def′(Z) > 0 ⇒ some σ-neighbour T has −rem(T) ≥ def′(Z), with an assignment.
- **(d′)**: Σ over distinct excursions hit by σ∪σ′-images, on nonpositive T, of max(0, −mass) ≥ Λ(Z).

(c) is the credit-free, single-edge form of (b′). (d′) is a local, excursion-level form. Unlike (c), it does not see the whole of T.

## 2. Why (c) holds: the data

Classes containing a Γ-cycle:
- **hits:** the 61 AW graphs, hole 22, both orientations; 122 classes, 284 Γ-cycles. These reproduce Job BI's 284.
- **census:** 18 holes rebuildable locally (`jobak-66dump.json` plus Job U's p27 #133619 h21), orders 25–27, both orientations; 36 classes, 64 Γ-cycles (all L = 20).
- Job BI's 264 Studio census records are summarised from its JSON in `recstats-out.txt`.

Source files: `ana-out.txt`, `cls-*.json`.

| quantity | hits (122 cl. / 284 Z) | census (36 / 64) |
|---|---|---|
| class size N | 14,965–28,968 | 658–1,533 |
| F/N (floor needs ≥ ¼) | 0.434–0.548 | 0.394–0.530 |
| M is the longest cycle | 122/122 | 33/36 |
| L(M)/N | 0.16 – med 0.45 – 0.81 | 0.10 – 0.30 – 0.85 |
| F(M)/F; ≥ ½ | 0.17–0.82; **53/122** | 0.10–0.90; **8/36** |
| M's share of the negative mass | 0.17–0.83 | 0.09–0.93 |
| Star(ii): −Λ(M)/Σ⁺Λ | **22 – 218 – 958** | **1.875 – 11.75 – 62** |
| #cycles with Λ ≤ −20 | 27–114 | 2–14 |
| unfilled share on Λ ≤ −20 | 0.756–0.889 | **0.466**–0.895 |
| (c) | 284/284 | 64/64 (BI: 264/264) |
| some image on M, (c_M) | 280/284 | **48/64** |
| off-Z non-fixed σ-images per Z | 12–78 | 10–20 |
| of those on heavy T: min / med | **9** / 14 | **7** / 11 (BI census: min 7) |
| light images per Z | 0–25 | 0–10 |
| distinct target cycles per Z | 1–12 | 1–7 (BI: 1 in 36/264) |
| margin m(Z) = max_img −Λ(T)/Λ(Z) | ≥ 60 | ≥ **5.75** |
| paired enrichment h(Z) − hU(K) | med +0.07, < 0 in 90/301 | med +0.16, < 0 in 18/64 |

**Tight cases.**
- Census **p27 #315977 h22**:
  - mirror: m = 5.75, Star 1.875 (M = −150 against 4 Γ-cycles, 80 positive);
  - plantri: M = −280.
  - In both orientations Z reaches no image on M, and its best heavy target has Λ = −115.
- p26 #75311 h19 (m = 7.5).
- p27 #186395 h22 (Star 2.875 / 3.0).
- At the hits the minimum m is 60, at A7f3-W2s-w4 with a L = 100 Γ-cycle.

**Answers to the task's questions.**
- *Fraction of the class on M:* see the table. It is a median of 0.45 (hits) and 0.30 (census), not ≈ 1.
- *Distinct cycles hit:* a median of 5 (hits) and 4 (census).
- *Do images ever all avoid the giant cycle?* Yes: 4/284 and 16/64. (c) then holds through another heavy cycle every time. "Images avoid **all** heavy cycles" never happens: at least 7 heavy images.
- *Is (c) just φ > 1 − 1/20?* **No.** φ_U(M) ≥ 0.95 never occurs; the maximum is 0.81. The share of the whole heavy tail (Λ ≤ −20) never reaches 0.95 either; its maximum is 0.895.

  The working model is "uniform images, heavy share h ≥ 0.47, n ≥ 10 images". It predicts a failure rate ≤ (1−h)ⁿ ≈ 2·10⁻³ per Z at the worst census class, and much smaller elsewhere. Observed failures are 0/348. This is consistent, but it says the margin is **statistical**: it comes from n and h, not from a forced landing.

## 3. Structural candidates (task 3)

| candidate | status |
|---|---|
| (G1) some π-cycle holds ≥ ½ of the class's filled states | **killed**: 53/122, 8/36 (min 0.10) |
| (G1′) M holds ≥ 1/10 of F | data 158/158; min 0.101, so barely |
| (G2) M is the longest cycle | 122/122 and 33/36; **killed** as universal |
| (G3) Star(ii): −Λ(M) ≥ Σ_{Λ>0} Λ | data **158/158**, min 1.875 (census), 22 (hits); 227/227 at orders ≤ 24 (NightP1 §4) |
| (G4) cycles with Λ ≤ −Λ_max⁺ hold ≥ ½ of U | data, min 0.466 (census p27 #315977 h22), so **borderline-false** at ½ |

- **Star(ii) ⇒ floor [proved, trivial]:** Σ_K λ ≤ Σ⁺Λ + Λ(M) ≤ 0. Star(ii) is therefore a strengthening of the floor, not a route to it.
- Theorem W fixes Σλ, and the floor fixes its sign. Neither says anything about how the negative mass is distributed among cycles. I see no argument that it concentrates. It is a dynamical (π-orbit length) property of the class's permutation π, and the formal library has no tool for orbit lengths.
- **Heuristic, not a proof.** A random permutation of N points has its largest cycle around 0.62N, and the mass follows the length (Λ ≈ −L on M at the hits). That matches L(M)/N of median 0.45, maximum 0.85, with the longest cycle also the heaviest. If π behaves like a random permutation on K, then (c), (G3) and (G4) are typical-case statements. Their proofs would have to explain why π is "mixing" on K. Nothing in hand does.

## 4. Adversarial test for (c) (for Studio Jobs BJ/BK)

**Per evaluated graph:** every class at the (5,5,5,5,6) hole that contains a positive cycle, both orientations, every positive cycle Z. For Γ-cycles use all L states; for non-Γ cycles use the DD endpoints. Script template: `36-nightstatementc/cls.py`, function `account`. It takes about 3 s per 20k-state class.

**Objectives, in order** (all to be **minimised**; a kill is marked ⇒):
1. **J_m = min_Z m(Z)**, where m(Z) = max over σ-images s ∉ Z (non-fixed) of −Λ(T(s))/Λ(Z), with 0 if there is no image. **J_m < 1 ⇒ (c) false.** Search on log J_m. Current minimum: 5.75 at p27 #315977 h22.
2. **J_h = min_Z #{images on heavy T}** (tie-breaker; currently 7). J_h = 0 ⇔ J_m < 1.
3. **Class canary J_M = −Λ(M)/max_{Z>0} Λ(Z).** J_M < 1 ⇒ (c) fails for that Z, since no heavy cycle exists. This is cheap: it needs only cycle masses, no σ.
   - Separately, J_★ = −Λ(M)/Σ⁺Λ < 1 kills Star(ii) without killing the floor.
4. **Hall deficiency D_H = Σ⁺Λ − maxflow** on the (c)-edges (maximise; > 0 ⇒ the (c)+(H) route fails even where (c) holds). Report the group Σλ alongside, to tell a Hall failure from a σC failure.
5. Always also record the class floor Σλ, σC/SigmaUnionC per group, and the G0 canary (NightPostAW §3), so that a (c) kill can be classified:
   - floor-and-σC survive: (c) dies, but the group route lives;
   - σC dies;
   - the floor dies.

**Moves and constraints.** Use the AW protocol: core-class flips with degree repair, hole star fixed, link (5,5,5,5,6), and **a Γ-cycle kept**, since (c) is about Γ-cycles.

**Seeds:**
- p27 #315977 h22 (both orientations), p26 #75311 h19 and p27 #186395 h22. These are the low-m and low-Star census holes; their rotations are in `jobak-66dump.json` and their face files in `36-nightstatementc/census/`.
- The 61 AW hits.
- A7_exc.

**Pressure direction:** smaller classes with Γ-cycles and a near-tight floor (F/N → ¼), because (c) needs one cycle of mass ≤ −20. The most dangerous configuration is negative mass spread over many light cycles (each Λ > −20) while the floor still holds.

**Kill rule:** one verified class with J_m < 1 kills (c) and the payer forms (b′)/(d′) as per-Γ-cycle statements. Re-check (b′) separately: it uses −rem(T), not Λ(T). Fall back to group-level SigmaUnionC.

## 5. Status

| item | status |
|---|---|
| (c) on all L states = on all DD endpoints (Γ) | [proved] (all states DL) |
| (c) + (H on (c)-edges) ⇒ σC per group, credit-free | [proved, trivial] |
| (c) alone ⇒ σC | no (Hall needed); true for groups with one positive cycle |
| (c) ⇒ R\* (4CT-strength) | [proved] via `lemmaP` |
| (c) | [data] 284/284 hits, 64/64 local census, 264/264 BI census; min 7 heavy images, min margin 5.75 |
| (c) for non-Γ positive cycles | [data] 17/17 (hits) |
| (H) on (c)-edges | [data] 158/158 classes |
| "one giant cycle pays" (c_M) | **killed**: 4/284, 16/64 avoid M |
| "M ≥ ½ of F" | **killed** (61/158 hold) |
| (c) as pigeonhole (share > 19/20) | **killed** (max heavy share 0.895) |
| Star(ii) (⇒ floor) | [data] 158/158, min 1.875; no argument |
| R3-only (c) | untested |
| why π concentrates mass in long cycles | open; random-permutation heuristic only |

Reproduction (`longtable/local-runs/36-nightstatementc/`): `cls.py` (hits) and `cls.py census` → `cls-hits.json` and `cls-census.json`; `ana.py cls-hits.json cls-census.json` → `ana-out.txt`; `recstats.py` → `recstats-out.txt` (Job BI JSON only). `gl/` holds regenerated symlinks and is not committed.
