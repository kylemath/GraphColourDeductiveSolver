# NightBudget: the per-group budget B′, made exact and tested

Written 2026-10-07 05:33 MDT. **Exploratory.** Hand bookkeeping plus single-machine checks (2 cores, AC power). Nothing here is formal; nothing here is at 4CT strength.

Inputs: `NightPostAW.md` §3 (the proposal), `NightFloorAtEasyHoles.md` and `NightF5Review.md` (F5), `NightEulerHole.md`, the Lean files `QuarterFloorH` (`dd_le_two_noLock`, `sigSwap_spec`, `R3At`), `QuarterLemmaP` (`exact_identity`), `QuarterSigmaPrime` (`linkGroup`, `sigmaUnionLink`, `dd_le_two_noLock_linkGroup`), `QuarterSigmaGroups` (`sigmaLink`, `DDEnd`), `QuarterSigmaK34` (`K4Ball`), `QuarterU34`, and the Night log from 05:03 (Job AW) to Job BI.

Scripts and outputs: `backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/nightbudget/` (§6).

## 0. Verdict

1. **B′ is a pure count.** Once σ is known to be an involution that keeps DD endpoints inside their group, B′ is equivalent to **2|R| ≤ 2N₀ + E₂ + 3τ** on the group (§1, Lemma B0). The split into R⁻ and N₀ᶠ is bookkeeping for a proof; the statement does not depend on it.
2. **The implication B′ ⇒ Σλ ≤ 0 needs |DD| ≤ 2|R|.** That bound is not automatic at degree 6: it fails on 512 σ-groups and 129 σ∪σ′-groups in the data. The fix is to take R := ρ(DD), the F5 charging map extended to steps without an R3 endpoint. Then |DD| ≤ 2|R| holds by construction, and B′ alone implies Σλ ≤ 0 (§1, Lemma B1).
3. **B′ on σ∪σ′-groups (the statement in NightPostAW) has 0 failures at (5,5,5,5,6).** This holds for both the literal R and the ρ version:
   - 2,568 hole-orientations: census orders 14–22, the WP13 corpus at orders 21–40, the 61 AW hit graphs at every (5,5,5,5,6) hole, the AS constructions and five witness graphs;
   - 2,277 nontrivial groups.
   - On groups with R⁻ ≠ ∅, the minimum slack is **9** (census and WP13) and 19 (AW hits). Only 4 nontrivial union groups have Σλ = 0, and all 4 have R⁻ = ∅.
4. **B′ on σ-groups is false.** It fails on 124 σ-groups (census 84, WP13 26, AW hits 14), with minimum slack −2. The first case is census g17#2, holes 5 and 15, both orientations.
   - Every failure has Σλ = 0 exactly, and the slack equals −(2|R| − |DD|). These are floor-tight groups whose R states each carry only one DD step.
   - **Tightest true σ-group variant: B′_c**, which weights each R⁻ state by the number c(r) ∈ {1, 2} of DD steps charged to it. It has 0 failures on 3,231 nontrivial σ-groups (minimum slack 0) and implies σC (§4).
5. **U34 on its own cycle pays nothing** (§2). For a failing k = 4 image s with the full R3 ring:
   - the filled run before s has length exactly 1 (0 exceptions in 5,128 cases; not formal);
   - its own excursion is (3,1) or (4,1) in 97% of cases.
   - So s's neighbourhood puts N₀ = E₂ = τ = 0 on the right side of B′. A (4,1) run even adds one DD step and one R state to the left side.
   - The remaining 3% are the cases where U34's hypothesis `hw` fails. There f ∈ {3, 5, 6}, never 2, and the excursion alone pays at least 6.
6. **No one-hop local lemma can prove B′** (§3).
   - In 87–99.6% of groups with R⁻ ≠ ∅, R⁻ cannot be paid from the excursions of its own σ- and σ′-images, even with r's own excursion added.
   - Cycle-level one-hop payment fails in 11% of census groups and 45% of AW/AS/WP13 groups.
   - Only about 10% of R⁻ states have a lockless σ′-exit at all, and almost none of the fixed or DL ones.
   - B′ on union groups is carried by group-level mass, which is the same difficulty as SigmaUnionC.

## 1. The exact statement and the implication

**Setting.**
- h is a degree-5 hole with link x₀…x₄, and S is a Kempe class. π, λ, DL, Lock1, Lock2, N₀ (`NoLock`), DD (`DDStep`), E₂ (`E2Start`) and τ (`TauStep`) are as in `QuarterLemmaP`.
- g is a σ-group (`linkGroup P sigmaLink`) or a σ∪σ′-group (`sigmaUnionGroup`). By `linkGroup_piInvariant`, g is π-invariant.
- σ = `sigSwap`: swap the {α,μ}-component of x_{j+1} at an unfilled state with repeat index j.

**Lemma B0 (σ facts) [proved, elementary].**
- (a) On unfilled states, σ is an involution up to renaming.
  - x_j and x_{j+2} are α and adjacent to x_{j+1} = μ, so the component always contains {x_j, x_{j+1}, x_{j+2}}.
  - The image has link (μ, α, μ, A, B) with the same repeat index j, and its {α′,μ′}-component of x_{j+1} is the same vertex set.
  - σ r = r up to renaming exactly when the component is the whole {α,μ}-graph. The data call this "fixed".
- (b) σ maps unfilled states to unfilled states, since the link pattern is kept.
- (c) If r ∈ g is a DD endpoint, then σ r ∈ g. The link `sigmaLink r (σ r)` holds and `link_mem_linkGroup` applies, for either kind of group.

(a) and (c) were asserted on every state in the runs, with 0 exceptions.

**Definitions (fixing the ambiguities).**
- **R3 type.** At a DL state with repeat index j, let w_t be the apex of the face on the link edge x_t x_{t+1}. The state has R3 type if c(w_j) = B and c(w_{j+3}) = μ. This is the Studio convention (`uv_lib.Hole.frame`).
  - At an IcoBall hole it is equivalent to Lean's `R3At`, which fixes all five ring colours (`ring_type`).
  - At degree 6 it is weaker. §2 separates the full-ring cases.
- **R_lit(g)** = {r ∈ g : r is a DD endpoint of R3 type}. This is NightPostAW taken literally, and the set `R` in `dd_le_two_noLock_linkGroup`.
- **ρ and c.** For a DD step d, let ρ(d) = d if d is R3, else πd if πd is R3, else d. This is F5's map with a fallback. Then R_ρ(g) = ρ(DD(g)), and c(r) = |ρ⁻¹(r)| ∈ {1, 2}. Each r ∈ R_ρ is a DL DD endpoint.
- **R⁻ and N₀ᶠ.** For R = R_lit or R_ρ:
  - R⁻ = {r ∈ R : σ r is not lockless}, that is, σ r is fixed, Lock1-only, Lock2-only or DL;
  - R⁺ = R ∖ R⁻;
  - N₀ᶠ = N₀(g) ∖ σ(R).

**Statement B′(g).**

  2|R⁻(g)| ≤ 2|N₀ᶠ(g)| + E₂(g) + 3τ(g).

**Lemma B1 [proved].**
- (i) **The budget is a count.** By B0, σ|_R is injective into g and σ(R⁺) = σ(R) ∩ N₀(g). So N₀(g) = |R⁺| + |N₀ᶠ|, and |R⁻| − |N₀ᶠ| = |R| − N₀(g). Hence

  B′(g) ⟺ 2|R(g)| ≤ 2N₀(g) + E₂(g) + 3τ(g).

  This is additive over the π-cycles of g. So B′ on σ-groups implies B′ on σ∪σ′-groups, which implies B′ on classes.
- (ii) **The exact identity splits the floor.** `exact_identity` applies on g because g is π-invariant. It gives

  Σ_g λ = |DD| − 2N₀ − E₂ − 3τ = (|DD| − 2|R|) − slack_B′(g),

  where slack_B′ = 2|N₀ᶠ| + E₂ + 3τ − 2|R⁻|. So **B′(g) ∧ |DD(g)| ≤ 2|R(g)| ⇒ Σ_g λ ≤ 0**, and then `quarterFloor_of_groups` gives the floor at the hole.
- (iii) **With R = R_ρ, |DD| ≤ 2|R_ρ| always holds**, since ρ is at most 2-to-1. So B′_ρ on every σ∪σ′-group implies SigmaUnionC, with no second hypothesis.
  - With R_lit, the bound |DD| ≤ 2|R| is F5's Lemma 2 (each DD step has an R3 endpoint). That lemma is IcoBall-only and fails at degree 6 (§4).
- (iv) **Weighted form B′_c.** With R = R_ρ and R^± ⊆ R_ρ, the identity Σλ = Σ_{R⁻} c(r) + Σ_{R⁺}(c(r) − 2) − 2|N₀ᶠ| − E₂ − 3τ is exact. Write

  slack_c := 2|N₀ᶠ| + E₂ + 3τ − Σ_{r∈R⁻} c(r) = −Σ_g λ − Σ_{r∈R⁺} (2 − c(r)).

  Then B′_c (slack_c ≥ 0) satisfies: B′_ρ ⇒ B′_c ⇒ Σ_g λ ≤ 0.

**Lean target (small).** State B′_ρ with `ρ` as a function and prove (i)–(iv) on top of `exact_identity` and `dd_le_two_noLock_linkGroup`'s first half (h1). Nothing new is needed beyond B0(a), which is `sigSwap` applied twice.

## 2. Relation to F5 and to U34

**F5 is B′ with R⁻ = ∅.**
- At an IcoBall hole, Lemma 2 gives |DD| ≤ 2|R_lit|, and Lemma 3 (`sigSwap_spec`) makes every σ r lockless, so R⁻ = ∅.
- B′ then reads 0 ≤ 2|N₀ᶠ| + E₂ + 3τ, which is trivial. F5 in fact proves the stronger |R| ≤ N₀.
- Data control: at all 628 (5,5,5,5,5) hole-orientations, R⁻ = ∅ and |DD| ≤ 2|R| in every group.

So B′ is exactly "F5's argument, with each failure of Lemma 3 priced at 2 and paid by the free part of the right-hand side". At degree 6 both F5 lemmas break:
- Lemma 2 breaks: the DD-loss |DD| − 2|R_lit| > 0 on 512 σ-groups.
- Lemma 3 breaks: R⁻ ≠ ∅.

**What R⁻ consists of** (state counts summed over all holes and both orientations; k is the position of the degree-6 vertex relative to j):

| image kind | census (orders ≤ 22) | AW / AS / WP13 / witness |
|---|---|---|
| fixed (σ r = r), k ∈ {0,1,2} | 758 | 15,110 |
| fixed, k ∈ {3,4} (none with the full ring) | 176 | 192 |
| DL | 214 | 5,514 |
| Lock-only, k ∈ {3,4} (U34 territory) | 1,684 | 18,414 |
| Lock-only, k ∈ {0,1,2} | 106 | 1,180 |

Fixed points sit where the degree-6 vertex is inside the swapped triple, and they cost 2 each with no image at all. They are the largest class in the constructions.

**U34 on its own cycle.** Take r with the full R3 ring (`R3At`), the degree-6 vertex at k = 4 (`K4Ball`), and failing image s. All such s are Lock2-only, as `u34_lock2_only` says. Write f_prev for the filled run before s, and (u, f) for s's excursion.

| (f_prev, u, f) | census | others | right side of B′ from s's neighbourhood | left side added |
|---|---|---|---|---|
| (1, 3, 1) | 183 | 2,362 | 0 | 0 |
| (1, 4, 1) | 167 | 2,270 | 0 | 1 DD step, 1 R state |
| (1, 3, 3), (1, 3, 5), (1, 3, 6) | 17 | 129 | 3(f − 1) ∈ {6, 12, 15} | 0 |

So, answering NightPostAW's question for the image's own cycle:
- **N₀:** 0, since u ≥ 3.
- **E₂:** 0, since u ≠ 2.
- **The following τ:** f − 1. This is 0 when u = 4 (`u34_f_one`, formal) and 0 when u = 3 under `hw` (`u34_f_one_of_three`).
- **The τ before s:** 0, since **f_prev = 1 in every case**. This is a new observation and not formal.

When `hw` fails, the data never show f = 2. The excursion then pays at least 6 ≥ 2 on its own, which suggests the dichotomy "u = 3 ⇒ f = 1 or f ≥ 3" [conjecture, data only].

At k = 3 (full ring, Lock1-only images, `u3_run_end`):
- the run after s has f = 1;
- the filled run before s's run has f_prev ∈ {1, 2, 3, 5, 6}, so τ = f_prev − 1 pays locally in 32 of 367 census cases and 593 of 4,761 others.

**Reading.** U34 settles the local accounting of a k = 4 failure, and the answer is negative: in the generic (3,1) and (4,1) cases, the image's whole π-neighbourhood contributes nothing to the right side of B′. The 2 units for r have to be imported from elsewhere in the group.

Rows with only the two-colour R3 type (not the full ring) show u = 2, DL images and fixed points at k = 3, 4. These are outside `K4Ball`, and none of them contradicts U34.

## 3. Test results

Engine: `uv_lib.Hole` (all states of T − h up to renaming; `escape.pi_of`). It checks Theorem W, the exact identity, B0(a), B0(c) and B1(i) on every group: 0 assertion failures.

Groups with neither DD steps nor R states have slack ≥ 0 trivially and are counted only in the totals.

**(5,5,5,5,6) holes** (2,568 hole-orientations):
- census g12–g22: 2,216;
- WP13 corpus orders 21–40: 100;
- AW hits: 190 (every (5,5,5,5,6) hole of the 61 graphs, not only h22);
- AS constructions: 48;
- witnesses (p25#668, p26#87942, p27#133619, p25#733): 14.

| statement | σ-groups (154,222; 3,231 nontrivial) | σ∪σ′-groups (133,235; 2,277 nontrivial) |
|---|---|---|
| floor Σλ ≤ 0 (σC / SigmaUnionC) | 0 fail | 0 fail |
| B′ with R_lit | **124 fail**, min slack −2 | **0 fail**; min slack 9 when R⁻ ≠ ∅ |
| B′ with R_ρ (implies the floor alone) | **434 fail**, min −6 | **0 fail** |
| B′_c (weighted) | **0 fail**, min slack 0 | 0 fail |
| \|DD\| ≤ 2\|R_lit\| | 512 fail | 129 fail (B′ slack covers each) |
| one-hop excursion payers (V1 / V2) | 38 / 89 of 1,577 R⁻-groups OK | 123 / 171 of 1,296 OK |
| one-hop cycle payers (V3) | 1,141 of 1,577 OK | 1,019 of 1,296 OK (census 797/895; others 222/401) |

The minimum slack with R⁻ ≠ ∅ on union groups, by source: census 9, WP13 9, AW 19, AS 142, witnesses 425.

The tightest σ-group failures are floor-tight groups of 8–40 states:
- g17#2 h5: 40 states, 3 cycles, DD 14, N₀ 0, E₂ 2, τ 4, R = R⁻ = 8 (6 of them fixed);
- g22#98 h3m: one π-cycle of 8 states, R⁻ = 2 (both fixed), N₀ᶠ = 1.

**(5,5,5,5,5) control** (628 hole-orientations): R⁻ = ∅ everywhere, 0 failures of anything, and min slack 18 / 20.

**Other patterns at the witness graphs** (150 hole-orientations; out of B′'s scope):
- p26#70869 h11 (5,6,5,6,6) reproduces the σC failure (σ-group Σλ = +5, B′ slack −2).
- Its union groups satisfy literal B′ (min 2).
- B′_ρ fails once: p26#70869 h4 (5,5,6,5,6), a floor-tight union group with R_lit = ∅, DD 2 and E₂ 2. It is the only union-group failure of any variant in the data.

**Per-state exits** (`nightbudget3`): of all R⁻ states,
- fixed: 32 of 16,236 have a lockless σ′-exit;
- DL: 2 of 5,728;
- k = 3/4 Lock-only: 4,390 of 20,098, of which 3,842 land outside σ(R);
- k = 0/1/2 Lock-only: 10 of 1,286.

In all, 4,434 of 43,348 R⁻ states (10%) have a lockless σ′-exit, and 3,884 have one outside σ(R).

**Not done here.** Census orders 25–27, NightPostAW item 2: the plantri files are not on this machine. Also not done: the adversarial flip search (Job BJ's territory; a B′ objective could be added to it).

## 4. The tightest true variants, and what a proof would need

**Status.**
- B′ (literal or ρ) on **σ∪σ′-groups**: true on all data, with margin.
- B′ on **σ-groups**: false. Its exact repair is **B′_c**: Σ_{r∈R⁻_ρ} c(r) ≤ 2|N₀ᶠ| + E₂ + 3τ. This is true on all data and tight (slack 0) on floor-tight σ-groups.
- B′_c sits strictly between B′_ρ and σC. By B1(iv), it says that the floor holds and the wasted capacity Σ_{R⁺}(2 − c) is covered.

**What a proof of B′ on union groups needs.** By B1(i) it is 2|R| ≤ 2N₀ + E₂ + 3τ. The F5 half (σ: R⁺ → N₀ injective) is free. What is left is to pay 2 units for each R⁻ state out of 2N₀ᶠ + E₂ + 3τ in the same group. The data rule out the local versions:
- the image's own neighbourhood pays 0 at k = 4 (U34 and f_prev = 1);
- per-state σ′-exits exist for 10% of R⁻ states;
- one-hop excursion payers fail in 87–99.6% of R⁻-groups;
- one-hop cycle payers fail in 45% of the constructed groups.

A proof would have to be a Hall- or flow-type transport inside the union group. That is exactly the shape of the charge-back P₁ certificate and of SigmaUnionC itself, so B′ does not localise the problem. It re-prices it per state, with fixed points as the largest debtor.

**The single local lemma that would make B′ follow from F5's injection** (in the style of U34):

> **Lemma X (failing σ-exit has a σ′-repair).** If r is an R3 DD endpoint with σ r not lockless, then some link-free swap from r lands on a lockless state outside σ(R). The assignment r ↦ that state must be injective on R⁻.

Then σ ∪ X maps R injectively into N₀, giving |R| ≤ N₀ and so B′ with slack E₂ + 3τ. **Lemma X is false:** even without injectivity it holds for only 3,884 of 43,348 R⁻ states (§3), and for essentially no fixed point.

No weaker one-hop lemma survives either (V1–V3). The only local facts that are true and new are:
- **U34-backward:** a failing full-ring k = 4 image has f_prev = 1;
- the dichotomy u = 3 ⇒ f ∈ {1} ∪ [3, ∞).

Both are cheap to formalise next to `QuarterU34`. They sharpen the negative: a k = 4 failure is locally unpaid, or else it pays at least 6 by itself.

**Recommendation.**
- Keep B′ (union groups) as a test objective; its minimum slack of 9 is a useful canary.
- For Job BJ, add max over groups of (2|R_ρ| − 2N₀ − E₂ − 3τ) as an objective next to max Σλ.
- Do not expect a local proof. The open content is still a group-level transport.
- The one new Lean target worth the effort is B1 (B′_ρ ⇒ SigmaUnionC, about one screen on `exact_identity`), so that the tested statement and the formal one coincide.

## 5. Caveats

- The R3 type at degree 6 is the two-colour Studio test (w₀, w₃), not `R3At`. The full-ring split is reported in §2 only.
- "Census" here means gentri/plantri orders 12–22. The order 25–27 census holes, where SigmaUnionC's ~10⁸-group evidence lives, were not available locally.
- The AW hits are covered at every (5,5,5,5,6) hole, both orientations. This closes NightPostAW's "all 61" gap for SigmaUnionC (max nontrivial union-group Σλ = −20) and for B′. P₁ and G0 were not recomputed here.
- The one-hop payer tests are max-flow feasibility over the stated supplier sets. A failure means no assignment within those sets exists; it does not mean B′ fails.

## 6. Reproduction

Directory: `backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/nightbudget/`.

| file | what | time (2 cores) |
|---|---|---|
| `nightbudget.py` | per hole and group: Σλ, DD, N₀, E₂, τ, R_lit/R_ρ, R⁻, N₀ᶠ, slack, DD-loss; U34 image accounting | ~4 min |
| `summarise.py` → `summary.txt` | the tables in §3 (records file `nightbudget-records.jsonl`, 96 MB, not committed; regenerate) | |
| `nightbudget2.py` → `nightbudget2-records.jsonl`; `summarise2.py` → `summary2.txt` | B′_c, payer flows V1–V3, full-ring U34 details with f_prev | ~10 min |
| `nightbudget3.py` → `nightbudget3-summary.txt` | per-state lockless σ′-exits of R⁻ | ~5 min |

Sources:
- `triangulations-min5-{12..20}.txt`;
- `wp17-last-roots/triangulations-min5-{21,22}.txt`;
- `wp13-generator/corpus.json` (orders ≤ 40);
- `jobaw/hits/*.json`;
- `jobas/best-*.json`;
- the witness JSONs in `27-studio-positive-config`.
