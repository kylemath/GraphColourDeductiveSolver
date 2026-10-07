# Night: C1 along π at (5,5,5,5,6) holes, an excursion bound (F6, second attempt)

Night worker, 7 October 2026 (written 01:52 MDT). **Exploratory. Hand arguments plus single-core checks. Unreviewed.**

Builds on `NightFloorHP.md` (Lemmas A–D, Conjecture C1), `NightFloorAtEasyHoles.md` (run bookkeeping), `NightF5Review.md` (exact identity), and the coordinator's relay about `NightFloorR53.md` (σ-joined groups, conjecture σC).

Labels: [proved] means a complete argument modulo the cited facts. [data] means computed by the scripts in §6. [conjecture] means not proved.

## Verdict

1. **C1 is not proved.** The planned route, an excursion bound along π, is **refuted** [data]. Widening the unit to the whole π-cycle cannot work in general either [proved, using Studio data at order 25].
2. **The per-excursion bound fails** at 818 of the 1,476 excursions that carry a D₀-step (orders 17–22, both orientations). Even with 2 units of slack it fails at 205 of them.
   - The unit "D₀-steps paid by τ/E₂/N₀ within π-distance d on their own cycle" needs d up to 18 at order 22, and d grows with the order.
3. **The π-locality seen at 17 #3 has a simpler cause** [data]: no π-cycle at any (5,5,5,5,6) hole has positive λ-sum at orders 16–23. This holds on every π-cycle at all 3,441 such holes, in both orientations.
   - By the per-cycle identity (§1), a nonpositive cycle pays all of its DD steps from its own N₀, E₂ and τ.
   - So "paid along its own π-cycle" is per-cycle nonpositivity. It is not extra structure.
4. **Per-cycle nonpositivity is false at order 25** [Studio data, already in the repo]. A Γ-cycle is an all-DL π-cycle; such cycles exist at (5,5,5,5,6) holes. Examples: p25 #5594 hole 18 (L = 20, nDL = 20, w = +4), p25 #14805 hole 5, p25 #16945 hole 3, and p26 #38442, #38516, #43840, #45501.
   - A Γ-cycle has no N₀, E₂ or τ states, so it has no in-cycle credit (Lemma 2).
   - Any proof of C1 that pays D₀-steps inside their own π-cycle (excursion, window or whole cycle) therefore needs every D₀-count on such a Γ-cycle to be 0. That would mean every R3 state on it has a lockless σ-exit.
   - Nothing at gentri orders can test this, because there are no Γ-cycles at (5,5,5,5,6) up to order 23.
5. **σ-joined groups (coordinator's request):**
   - At orders 16–22 the test is **vacuous**: every cycle is already nonpositive, so every union of cycles passes. I checked three variants (σ over all DD steps, σ plus ψ, σ over D₀ only): 0 failures, maximum group size 9 cycles.
   - The non-vacuous version asks whether σ-neighbour cycles alone, excluding the D₀-step's own cycle, could pay. It is false at 463 of 838 D₀-carrying cycles.
   - For D₀-steps, σ(r) lands in the **same** π-cycle in 1,316 of 2,352 cases at orders 17–22. This is the k = 0, 1, 2 "σ(r) is DL in the same run" effect.
   - So σ-joining is not what pays at small orders. Whether it pays at order-25 Γ-cycles is the real question and needs the Studio (§5).

## 1. Per-cycle identity [proved]

The run bookkeeping of F5 applies to each π-cycle separately (each excursion contributes u − 3f, and a Γ-cycle contributes L). So, for every π-cycle c:

  Σ_c λ = DD(c) − 2N₀(c) − E₂(c) − 3τ(c),

where each count is taken over the states of c. (An E₂ excursion is counted at its run start, and DD steps at their start state.) Summing over the cycles of a class gives the class identity of `NightF5Review.md` §1.

**Consequence.** Write DD = T + X + D₀ (Lemmas A–C of `NightFloorHP.md`). The class inequality C1 is equivalent to the class floor Σλ ≤ 0; C1 only restates it in charging form. A per-cycle charging that pays every DD step of c from the credit of c (capacity 2 per N₀, 1 per E₂, 3 per τ) exists if and only if Σ_c λ ≤ 0.

## 2. Γ-cycles at (5,5,5,5,6) holes [proved]

**Lemma 2.** Let c be an all-DL π-cycle of length L at a (5,5,5,5,6) hole with no separating triangle. Then:
1. every step of c is an R-step;
2. 10 divides L, and along c the R3 states run through positions k = 4, 3, 2, 1, 0 (relative to p), each exactly L/10 times;
3. c contains no N₀, E₂ or τ state, and Σ_c λ = L > 0;
4. every R3 state of c is the endpoint of exactly two DD steps of c.

*Proof.*
1. Every state of c is DL, so every step of c is DD. By Lemma A, the image of a T-step is F-starved, so its π-image is not DL. That is impossible on c. Hence all steps are R-steps.
2. Lemma A gives R1@k → R3@k+2 and R3@k → R1@k+2. So the types alternate, and two steps take R3@k to R3@k+4 = R3@k−1. The sequence of (type, k) along c is therefore periodic with exact period 10. Because c is a cycle, its length is a multiple of that period.
3. Every state of c is unfilled and has both locks.
4. Each R3 state r of c is the endpoint of π⁻¹r → r and r → πr. ∎

**Corollary.** On a Γ-cycle, the per-cycle form of C1 (D₀(c) ≤ spare credit of c) holds only if D₀(c) = 0. That requires all L/2 R3 states of c, including those at k = 3, 4, to have a lockless σ-exit.

[data] At k = 3, 4 a lockless σ-exit does occur: X-steps with an R3 endpoint at k = 3 number 3,677 at order 23, against 1,336 D₀-steps there. So Lemma D does not rule it out. The F6 note's table "k = 3: always Lock1 only" describes the D₀-steps only.

The status of the k = 3 exit has a sharp local form. Let K be r's {α,A}-component containing x₂ (the component that R₊₃ swaps).
- x₂ has exactly two {α,A}-neighbours, w₁ and x₃.
- So σ(r) lacks Lock1′ **iff** x₂ is a cut vertex of K that separates w₁ from x₃.
- *Proof:* in σ(r), x₁ is α. Its only A-neighbour is w₁. The only α- or A-neighbour of x₃ is the forced vertex m (Lemma D). So Lock1′ exists iff w₁ and m are joined in K − x₂.

This is radius-unbounded, which is why no ring-2 automaton decides it.

## 3. The excursion route [data, refuted]

An excursion here is a maximal unfilled run (length u) together with the filled runs before and after it (lengths f_b and f_a), whose τ counts are f_b − 1 and f_a − 1.

| order | excursions with D₀ | D₀ ≤ 3(τ_b + τ_a) fails | fails even with +2 slack |
|---|---|---|---|
| 17 | 4 | 4 | 4 |
| 18 | 8 | 4 | 4 |
| 19 | 16 | 7 | 4 |
| 20 | 74 | 30 | 10 |
| 21 | 294 | 162 | 49 |
| 22 | 1,080 | 611 | 134 |

The first failure is 17 #3 holes 0 and 16 (u = 17, D₀ = 14, f_b = f_a = 2). The shortest failing excursion is u = 4 with one D₀-step and f_b = f_a = 1, so there is no τ at either end (20 #23 hole 3).

**Pairs, windows, the cycle.** For each π-cycle carrying D₀-steps, I computed the least d such that a capacity matching exists from its D₀-steps into its own spare credit within cyclic π-distance d (the spare credit is 3 per τ, 2 − load per N₀, 1 − ψ-use per E₂).

| d | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11–18 |
|---|---|---|---|---|---|---|---|---|---|
| cycles | 224 | 333 | 101 | 60 | 42 | 26 | 19 | 14 | 19 |

No bounded window suffices. The whole cycle always works up to order 22 (0 failures for D₀(c) ≤ spare(c)), but by §1 and Verdict 3 this is per-cycle nonpositivity, which holds at orders 16–23 and fails at order 25.

**Other run statistics** (orders 16–22, both orientations):
- unfilled run lengths go up to u = 19;
- maximal blocks of consecutive D₀-steps reach 14 (17 #3);
- every all-D₀ block of length ≥ 8 has even length (8, 10, 14).

## 4. What a proof of C1 must look like [conjecture]

Combining §1, Lemma 2 and the order-25 Γ-cycles: a Γ-cycle's DD steps (20 at p25 #5594) must be paid by credit on **other** π-cycles of the class.
- σ-exits do that for X-steps (Lemma C).
- For D₀-steps on a Γ-cycle, the only candidates left are cross-cycle maps: σ, when σ(r) leaves the cycle, or some other Kempe exit.

**Conjecture C1Γ.** On every Γ-cycle at a (5,5,5,5,6) hole, every R3 state has a lockless σ-exit (D₀(c) = 0).
- If true, then on Γ-cycles F5's argument works verbatim, and the remaining D₀-steps live on cycles with filled states.
- If false, C1 needs a genuinely cross-cycle D₀ payment, and σC (with σ over all DD steps) is the natural candidate.

Both are decidable at p25 #5594 h18 and the other order-25/26 Γ-holes listed above.

## 5. Requests (Studio, plantri orders 25–26)

At each (5,5,5,5,6) hole that has a Γ-cycle, both orientations:
1. classify the Γ-cycle's DD steps into X and D₀ (by σ at the R3 endpoint), recording k;
2. evaluate σC (Σλ ≤ 0 on σ-joined groups, σ over all DD steps, with and without ψ) on the hole's class;
3. check C1′ (#D₀ ≤ 3#τ per class).

Items 1 and 2 decide between the two branches of §4. Nothing on the MacBook (gentri ≤ 24, plantri absent) can reach them.

## 6. Reproduction (session scratchpad `hp2/`, not committed; single core, AC power)

| script | content | time |
|---|---|---|
| `common.py` | T/X/D₀ classification, loads, ψ-uses, π-cycles, runs (imports the F6 `base.py`) | n/a |
| `exc.py 16,…,22` | per-cycle tests: D₀ ≤ 3τ, ≤ 3τ + E₂, ≤ spare(c) | 47 s |
| `exc2.py 16,…,22` | per-excursion table (§3), D₀ block lengths, π-radius matching | 47 s |
| `grp.py 16,…,22` | σ-joined groups, three variants | 44 s |
| `sj.py 17,…,22` | σ(r) same or other cycle; σ-neighbour-only payment | 44 s |
| `mx.py 16,…,23` | maximum cycle λ, Γ-cycle count, X/D₀ by k | 194 s |
