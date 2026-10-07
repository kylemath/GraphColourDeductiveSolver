# Night: Lemma P₁ (charge-back form) — one-hop assignment of deficits

Night worker, 7 October 2026 (written 03:25 MDT). **Exploratory. Hand arguments plus short single/two-core runs (AC power). Unreviewed.**

Builds on `NightF6Flow.md` (identity §1.2, P₁ §1.4), `NightLemmaR.md` (landing excursion, exact rem formula, charge-back), `NightLockBreaking.md` (Prop 2.4), `NightCycleBound.md` (Transport T), Studio Jobs S, Y, Z and charge-back P₁ (`27-studio-positive-config/`). New run: `longtable/local-runs/29-P1/` (§6).

Labels: [proved] hand argument modulo the cited facts; [data]; [killed] counterexample in the data; [conjecture].

## Verdict

1. **[proved] P₁ is credit-free: def′(Z) ≤ Λ(Z) = 5w(Z)** (§1). So P₁ follows from **P₁^str**: every positive Z has a σ-neighbour T with −rem(T) ≥ Λ(Z), plus a Hall condition for shared T. [data] P₁^str holds on **every non-Γ positive cycle**: 246/246 at (5,5,5,5,6)/(5,5,5,6,6), orders 25–27, Studio's directed neighbours; 209/209 at orders 17–24, all patterns, undirected neighbours. The minimum ratio is **1.25** in both ranges (p27m #167230 h23; tri24 #3633 h0).
2. **[proved; data] The paying neighbour is not the target of an exit.** The task's route (lockless exit ⇒ u = 1 landing ⇒ rem(T) ≤ −c·hits) is the wrong mechanism.
   - The landing lemma is true and extends to every lock type (§2).
   - Any bound of the form rem(T) ≤ −c·#hits is **killed**: rem = +6 at p27 #68456 h19, and rem = +2 at the w = 0 targets.
   - The best neighbour T* is **unhit** in 73/101 deficit cycles at orders 25–27 and in 123/149 at orders ≤ 24. It is reached by a lock1-only, lock2-only or DL image as often as by a lockless one.
   - T* is the most negative cycle of the σ-group in 132/149 (≤ 24), and the most negative listed target in 101/101 (25–27).
   - The real phenomenon is a **star** (§4): in 227/227 σ-groups with a positive cycle (orders ≤ 24), the group's most negative cycle M alone outweighs all positive Λ. In 210/227, M is one σ-hop from every positive cycle; the version with −rem(M) as capacity holds in 206/227.
3. **[data] Hall / sharing is never what binds** (§3). At orders 25–27:
   - only 7 holes have two or more deficit cycles;
   - their minimum residual slack is 85;
   - the tight cases are all single-deficit holes.

   Tightest: **p27m #167230 h23**, where Z (non-Γ, L = 28, Λ = 20, *no lockless credit*) has best neighbour Λ = rem = −25, unhit. That gives slack 5 and Hall ratio 2.5. Next is p27m #204626 h4 (L = 28, Λ = 20, −40, slack 20).
4. **[killed] P₁ in the directed σ-form is false outside the two patterns.**
   - Studio Job Z finds 22 failing holes at other patterns, orders 25–27.
   - My run finds tri24 #2976 h15 (5,6,6,5,8+): Z (Λ = 5, L = 21) has σ-images only on itself and on two Λ = 0 cycles.
   - [data] Repair: count σ-links from DD endpoints of **either** cycle (the σ-group's own edges). Then P₁ holds at all 227 holes of orders ≤ 24, min best-neighbour ratio 3.0.
   - No σ-form can hold everywhere: p26 #70869 h11 (a Job Z failure) is the σC counterexample, a σ-island of Σw = +1. The general statement must use σ ∪ σ′. [data] P₁ on σ + Transport-T edges holds at all holes ≤ 24.
5. **[proved] Relation to Transport T** (§5): P₁ is **not** the σ-restriction of T.
   - The σ-swap (the {α,μ}-component through m) always meets the link, while T's swaps are link-free. So the edge sets are disjoint.
   - The capacities differ: −rem against |w|.
   - What links them is σ′ = T's lock-breaking edges at DD endpoints: "P₁ on σ ∪ σ′" is the common refinement.
   - T has no proof idea to transfer: it is 4CT-strength.
   - **P₁ restricted to non-Γ cycles is vacuous in a minimal counterexample and on the torus** (§5). So, unlike Lemma S_Γ and T, it fails the Prop 2.4 test for being 4CT-strength. It is the "easy" half of the F6 flow, though no proof is in hand.

## 1. Charge-back makes P₁ credit-free [proved]

Notation is as in NightF6Flow §1.1 and NightLemmaR §3a. For T ∈ N hit by exits e with credits c(e) > 0, set hit(T) = −Σc(e), and recall rem(T) = Λ(T) − hit(T). Charge-back sends rem⁺(T) to the sources in proportion to their credit: ch(Z,T) = rem⁺(T)·c(Z→T)/Σ_e c(e).

**Lemma 1.1.** ch(Z,T) ≤ c(Z→T). Hence def′(Z) = Λ(Z) − Σ_T (c(Z→T) − ch(Z,T)) ≤ Λ(Z).
*Proof.* Λ(T) ≤ 0 gives rem(T) ≤ −hit(T) = Σ_e c(e). So rem⁺(T)/Σc ≤ 1. ∎

**Corollary 1.2.** Charge-back P₁ on a group follows from:
- **P₁^str(g):** there is a map Z ↦ T(Z) from the positive cycles with def′ > 0 to σ-neighbours with rem < 0, such that Σ_{Z↦T} Λ(Z) ≤ −rem(T).

The credit-free version loses nothing in the data: for non-Γ cycles the best neighbour already covers Λ(Z), with min ratio 1.25 (§3). On Γ-cycles P₁^str fails 48 times at orders 25–27, because their neighbours are fully hit, but Γ-cycles have def′ ≤ 0 by Lemma S_Γ (Job Z: all DD-endpoint R-types, both patterns). So:

> **F6 flow at (5,5,5,5,6)/(5,5,5,6,6) = identity + Lemma S_Γ (credit side) + P₁^str on non-Γ cycles (debit side).** The non-Γ part never needs the exits it emits.

[data] 60/101 deficit cycles at orders 25–27 have def′ = Λ(Z): no lockless credit survives at all.

## 2. Where σ-images land [proved modulo the π table]

Let s be unfilled. By the π table (Theorem W; `QuarterPi.lean` `piMove`/`piInv`), π s is unfilled ⇔ Lock2(s), since π s = R₊₃ s. Also π⁻¹s is unfilled ⇔ Lock1(s), since s is then an R₊₃ image. Otherwise the predecessor is filled (φ_A) and the successor is filled (φ_B⁻¹). NightF5Review §1's "neither lock ⇔ u = 1" is the conjunction of these.

**Lemma 2.1 (landing by lock type).** Let r be a DD endpoint and s = σ(r) ≠ r unfilled, in the excursion E of its cycle T:

| image s | position in E | u(E) |
|---|---|---|
| lockless | the only unfilled state | 1 (NightLemmaR §1) |
| Lock2 only | first unfilled state | ≥ 2 |
| Lock1 only | last unfilled state | ≥ 2 |
| DL | interior unfilled state | ≥ 3 |

σ is an involution preserving j (NightLemmaR §1a), so distinct DD endpoints have distinct images. ∎

[data, orders ≤ 24, links from deficit cycles into T*] Landing excursions (u, f):
- (1,1) 74, (1,2) 22, (1,≥3) 20;
- (3,1) 48, (4,1) 42, (6,1) 25, (2,1) 18, …;
- up to (14,1).

Only the lockless landings carry credit. T* is reached by 116 lockless, 90 lock1-only, 97 lock2-only and 87 DL images.

**What is killed.** Bounds rem(T) ≤ −c·#hits, or rem(T) ≤ 5w(T) − (credits):
- p27 #68456 h19 has rem = +6, with two (1,3) hits plus an unhit (17,2) run;
- the w = 0 targets ((1,1) hit + (5,1) free) have rem = +2.

rem(T) is exactly Σ_{free E}(u − 3f) (NightLemmaR §2), and nothing better holds per target. **The positive cycle does not pay through the cycle it hits.** It pays through a large, usually unhit, neighbour.

## 3. Slack and the tight cases [data]

**Orders 25–27** (`p1_slack.py` on Job S records plus the Studio charge-back sources; (5,5,5,5,6)/(5,5,5,6,6), 544 positive cycles, 94 holes and 101 deficit cycles with def′ > 0):

| run | deficits | min ρ = −rem(T*)/def′ | min Hall ratio | min residual slack |
|---|---|---|---|---|
| p25 | 1 | 48 | 57 | 470 |
| p25m | 2 | 57 | 83 | 195 |
| p26 | 11 | 4.0 | 10.5 | 60 |
| p26m | 13 | 9.5 | 17 | 85 |
| p27 | 25 | 13.9 | 18.5 | 130 |
| p27m | 49 | **1.25** | **2.5** | **5** |

The tight cases:
1. **p27m #167230 h23:** Z29 non-Γ, L 28, Λ 20, CrN 0, two σ-neighbours with rem < 0. Best is T21, Λ = rem = −25, unhit. Slack 5.
2. **p27m #204626 h4:** Z12 L 28, Λ 20, CrN 0; T4 = −40. Slack 20.
3. **p26 #68224 h23** and **p26 #83426 h18:** L 28, Λ 20, CrN 0; −80 and −95.
4. The rest are mostly L = 14, Λ = 10, CrN = 0 cycles against −95 … −145.

All the tight cycles have **CrN = 0** and L = 7Λ/5 (w = L/7), consistent with one long DL excursion per 14 states. At orders ≤ 24 these are (13,1) excursions, mass +10. The p27 #68456 h19 Γ-cycle is not tight: its def′ is −35 + 6 = −29.

**Sharing.**
- Holes with ≥ 2 deficit cycles: 7. The optimal assignment shares a target in 5 of them. Minimum slack 85 (p26m #74500 h20 and p27m #166940 h23, two L = 14 cycles each, on targets −95/−95).
- Hall is never the binding constraint. Single targets are.
- Max deficits on one target: 2.

**Orders ≤ 24, all patterns** (`p1_struct.py` on `picyc.p1` output; 227 holes, 231 positive cycles, 149 deficit cycles with R3 exits):
- directed P₁ min ρ = 2.0, at tri20 #59 h18 and tri24 #5777 h22: Λ = 5, L = 21 against T* Λ = −10, L = 18, hit by Z's only lockless exit;
- min slack 5;
- deficit Λ ∈ {5, 10, 20}; positive excursions mostly (13,1), (7,2), (7,1), (8,1), (12,1).

## 4. The star form [conjecture; data]

**Star(g):** the most negative cycle M of a σ-group g with a positive cycle (i) is σ-adjacent (one hop, either direction) to every positive cycle of g, and (ii) has −Λ(M) ≥ Σ_{Z∈P_g} Λ(Z).

- **Star_rem** is the same statement with −rem(M) in place of −Λ(M). Star_rem ⇒ P₁^str ⇒ P₁, with every deficit sent to M [proved, trivial]. Star with Λ(M) alone is not enough, because hits on M lower its capacity.
- [data, `star_check.py`, orders ≤ 24, all patterns, both orientations]
  - (ii) with Λ(M) holds in **227/227** groups; with rem(M), in 223/227.
  - (i) holds in 210/227, and Star_rem in 206/227.
  - The positive cycles not adjacent to M are at σ-distance 2 (14) or 3 (3), and all are paid by a nearer neighbour.

So the data say more than P₁: σ-groups are dominated by one cycle whose negative mass exceeds the whole positive supply. That is a statement about where the class's filled states sit (M carries most τ-steps). I have no argument for it.

## 5. P₁ versus Transport T [proved comparisons; data]

| | Transport T (NightCycleBound) | P₁ (charge-back) |
|---|---|---|
| edges | link-free swaps from DL states of Z (variant d: lock-breaking) | σ = {α,μ}-swap of the component through m, from DD endpoints |
| supply | w(Z) | def′(Z) ≤ 5w(Z) (§1) |
| capacity | \|w(N)\| | −rem(T) = −Λ(T) − incoming credit |
| scope | Kempe class, flow (splittable) | σ-group, single target, one hop |
| min ratio | Hall 3.0 (p25 #12342 h24) | ρ 1.25 (p27m #167230 h23); undirected ≤ 24: 3.0 |
| implies | floor | σC on g (identity) |

1. **Not a restriction [proved].** K_σ contains m, x_j and x_{j+2}, so it meets the link. T's swaps miss the link. The edge sets are disjoint, and neither statement implies the other.
   - The σ′ edges of Job H (link-free lock-breaking swaps from DD endpoints) are T's variant (d) restricted to DD endpoints.
   - The natural common statement is **P₁ on σ ∪ σ′**. [data] It holds at all holes ≤ 24. σ′C holds at all 22 Job Z P₁ failures, so it is the candidate at orders 25–27.
   - p25 #12342 h24 is both T's tightest hole and a Job Z P₁ failure.
2. **Zero relays.** T never needs them. Directed P₁ does: at tri24 #2976 h15, Z's own σ-images reach only Λ = 0 cycles. The undirected form removes the need: cycle 2 (Λ = −110) has a DD endpoint whose σ-image lies on Z. ≤ 24: undirected P₁ fails 0 times, and P₁ through zero relays fails 0 times.
3. **No proof idea to transfer.** T is open and 4CT-strength (NightCycleBound §4). NightLockBreaking Prop 2.4 shows even "one breaking exit per Γ-cycle" ⇒ 4CT.
4. **Vacuity test [proved].** In a minimal counterexample every Kempe class of T − v is targetless, hence all-DL (NightClosedSets C1), hence every π-cycle is a Γ-cycle. So:
   - **P₁ and P₁^str restricted to non-Γ cycles hold vacuously there.**
   - The same happens on the torus at a frozen state, which is a one-state Γ-cycle.
   - So P₁(non-Γ) is not 4CT-strength by the Prop 2.4 argument. Lemma S_Γ and T are.
   - The whole 4CT content of the F6 flow at (5,5,5,5,6) sits in Lemma S_Γ (A₃₄′ / Lemma W on closed runs). P₁(non-Γ) is the part that can, in principle, be local.
   - This is not a proof of P₁: non-Γ cycles live in classes with filled states, and what has to be shown is that such a class has a big negative cycle next to each of them.

## 6. Status

| item | status | support |
|---|---|---|
| def′ ≤ Λ(Z); P₁ ⇐ P₁^str + Hall | [proved] | — |
| landing position by lock type | [proved] mod π table | landing histogram ≤ 24 |
| rem(T) ≤ −c·hits / ≤ 5w − credit | [killed] | p27 #68456 h19; w = 0 targets |
| P₁ (directed σ), (5,5,5,5,6)/(5,5,5,6,6) | [data] | 25–27: 0 failures, min ρ 1.25, min slack 5 |
| P₁ (directed σ), all patterns | [killed] | tri24 #2976 h15; Job Z: 22 holes |
| P₁ (undirected σ), all patterns ≤ 24 | [data] | 227/227, min ratio 3.0 |
| any σ-only P₁, all patterns | [killed] | p26 #70869 h11 (σC island) |
| P₁ on σ ∪ σ′ / σ ∪ T-edges | [conjecture] | ≤ 24: 0 failures |
| P₁^str on non-Γ | [conjecture] | 246/246 (25–27), 209/209 (≤ 24, undirected); min 1.25 |
| Star (M dominates all positive Λ) | [conjecture]; Star_rem is false as a universal | (ii) 227/227 (223 with rem), (i) 210/227 |
| Hall ever binding | no | max 2 deficits per target; multi-deficit slack ≥ 85 |
| P₁(non-Γ) vacuous in a counterexample and on the torus | [proved] | — |

**Studio requests.**
1. On Job Z's 22 failing holes, test undirected σ-P₁ and σ ∪ σ′ P₁. Expected: undirected σ fails at least at p26 #70869 h11, and σ ∪ σ′ passes.
2. At orders 25–27, both patterns, test P₁^str with undirected neighbours and the Star test (needs the group's cycle list and edges, which `--p1` in `29-P1/build_p1.py` prints).
3. At p27m #167230 h23, give the excursions of Z29 and T21 and the link types between them. This is the ρ = 1.25 case.

## 7. Reproduction (`backgroundMaterial/planemap-structural/longtable/local-runs/29-P1/`)

- `build_p1.py` copies `27-studio-positive-config/picyc.cpp` (untouched) to `picyc_p1.cpp`, adds `--p1`, and builds `picyc.p1`.
  - Per hole with a positive cycle, `--p1` prints the σ-groups, every group cycle's Λ, L, Γ-flag and excursions, and every DD-endpoint σ-link of each positive cycle (R-type, image kind, locks, f, landing excursion).
  - It also prints all σ-edges of the groups and Transport-T edges.
- Inputs: `../28-lemmaR/in{17,20..24}.txt` (gentri), both orientations. 2 cores, about 30 s on AC power. The `out*.jsonl` files (≈150 MB) are not committed and can be regenerated.
- `p1_struct.py` → `p1-struct.txt` (§2–§5, orders ≤ 24). `star_check.py` → `star-check.txt` (§4). `p1_slack.py` → `p1-slack.txt` (§3, orders 25–27, from Studio files).

## 8. Addendum (03:27): the coordinator's reframing, using Studio Job AD

**Reframed target.** A positive non-Γ cycle Z has a DD endpoint whose σ-image lies on a cycle T with rem(T) ≤ −1.25·def′(Z). Why is the σ-image of a DD state of a short positive cycle on a long negative cycle?

### 8.1 Data profile of the paying neighbour T*

Sources:
- Job AD, `jobad-records.json`: 75 deficit cycles, (5,5,5,5,6)/(5,5,5,6,6), orders 25–27, both orientations, exits from all R-types;
- my orders ≤ 24 run.

**Z.** All 75 are non-Γ. The (L, w) counts are:
- (14,2) ×30, (22,2) ×12, (18,2) ×7, (26,2) ×7, (28,4) ×7, (30,2) ×6;
- single cases (21,1), (36,4), (41,1), (48,4), (50,2), (89,1).

**T*** (the neighbour with the most negative rem):

| quantity | min | median | max |
|---|---|---|---|
| L(T*) | 77 | 379 | 911 |
| w(T*) | −193 | −64 | −5 |
| L/\|w\| | 3.6 | 5.4 | 22.2 |

- L(T*) ≥ 3·L(Z) in 74/75.
- T* is **unhit** in 53/75 (orders ≤ 24: 123/149).
- At orders ≤ 24, L(T*)/L(Z) has median 8.8 and minimum 0.86.

**The tight case p27m #167230 h23** is *long but light*:
- T* has L = 111, w = −5 (rem = −25, unhit), against Z with L = 28, w = 4, def′ = 20, CrN = 0.
- Its twin cycle 22 is identical, and the other six σ-neighbours have w = 0.
- So "long" does not imply "heavy". The 1.25 comes from a long cycle with only one negative unit per 22 states.

The next three tight cases have the same shape, (L 28, w 4) against (128, −8), (172, −16) and (77, −19).

**Link types into T*** (orders ≤ 24, DD endpoints): lockless 116, lock1-only 90, lock2-only 97, DL 87. Job AD agrees: 39/75 deficit cycles have no lockless exit into any nonpositive cycle.

### 8.2 What can be proved

**Lemma 8.1 [proved, modulo the π table as in §2].** Let r be a DD endpoint and suppose s = σ(r) is not DL (lockless or single-lock). Then the π-cycle T of s contains a filled state adjacent to s:
- πs is filled if s lacks Lock2;
- π⁻¹s is filled if s lacks Lock1.

So T is not a Γ-cycle, and s is an excursion endpoint (Lemma 2.1). If s is lockless, T carries the excursion mass 1 − 3f ≤ −2 next to s. ∎

This is the only local sign information I can prove. It shows that the non-DL σ-images of Z sit at the **boundary of filled runs** of their cycles. These are exactly the places where λ < 0 (φ_A, φ_B⁻¹, τ, by `lam_eq`).

It does not show that T is negative overall, let alone by 1.25·def′. Negativity of T is a global property of T's whole orbit, Σ over T's excursions of (u − 3f). The σ-link sees one or two states of T.

**What is false or unsupported.**
1. *σ carries runs coherently* (σ∘π = π∘σ along a DL run, which would make Z's run shadow a run of T). **[data: no]**
   - Among 469 consecutive pairs of DD endpoints of non-Γ positive cycles whose images both leave Z (orders ≤ 24), only 88 land on the same T.
   - σ is not π-equivariant. This contrasts with the link-free swaps of Transport T, which commute with R₊₃ for one step (NightLockBreaking Lemma 2.2).
   - So "Transport T's reasoning" (ladder rungs) **does not transfer**. σ's component K_σ ∋ m changes with every R₊₃ step, because the swap at x_{j+2} recolours the α-vertices that K_σ uses.
2. *A one-state certificate.* Even Lemma 8.1's local mass is ≤ −2 per lockless image and 0 per single-lock image. That is far below the def′ of 5–20 that must be paid.
   - The payment comes from T's *other* filled runs, which σ does not see.
   - A proof must therefore be global in T, for instance a count of T's filled states.

### 8.3 Heuristic [not a proof]: why the image is on a long cycle

In every σ-group with a positive cycle at orders ≤ 24, the most negative cycle M alone outweighs the whole positive supply (227/227, §4). M is also long, so it holds most of the group's states.

Z's σ-images are 4–28 states spread across the group, with no π-coherence (§8.2.1). So some image landing on M is the generic outcome: the event is "some image hits the cycle that holds most of the states".

The data fit this:
- T* is the group's most negative cycle in 132/149 cases;
- the exceptions are at σ-distance 2–3 (§4).

The tight case fits too. At p27m #167230 h23 the large cycles are light (w = −5 on L = 111). The ratio 1.25 is a ratio of *weights*, not lengths.

A provable version would be a counting statement:

> "In a class with filled states, the σ-images of the DD endpoints of a non-Γ positive cycle Z cannot all avoid the cycles carrying at least |Λ(Z)| of negative mass."

This is σC-flavoured and global. I do not see it following from Jordan/Euler at single states.

### 8.4 Updated status lines

| item | status |
|---|---|
| non-DL σ-image sits next to a filled state of its cycle (T not Γ) | [proved] mod π table |
| σ commutes with π along runs / ladder argument of T | [killed] (88/469 coherent pairs) |
| reframed P₁ (σ-image on T with rem ≤ −1.25 def′) | [data] 75/75 (Job AD), tight 1.25; no proof |
| T* profile | L 77–911 (median 379), w −5…−193 (median −64), L ≥ 3L(Z) in 74/75, unhit 53/75 |
