# NightGammaLength — why the Γ-cycle length L is 20, 40 or 60 [exploratory]

2026-10-07. Inputs: NightLog-2026-10-06 (Jobs O, AH, AJ, AN, AO; Lean QuarterGammaPeriod,
QuarterMirror, QuarterWindow), NightPotential §4 "closing permutation", `jobuv/joban.json`,
`jobao-lengths.txt`, `jobuv/jobao-summary.txt`. Ring-table computation:
`faces.py` (scratch; reproduced in §2 below; it only reads the `xTab/wTab/mTab` tables of QuarterWindow).
No new graph runs: the plantri inputs that `uv_lib.load` needs are not in this checkout.

## 0. Facts (formal or settled data)

- **Formal (QuarterGammaPeriod, QuarterWindow).** On an all-DL π-orbit at a `Hole6`, (type,k) has period exactly 10; `period_colour_rotation`: every hole vertex with letter ℓ at `s n` has letter σℓ at `s (n+10)`, σ = `sig` = (μ B A) a 3-cycle **fixing α = c(x_j)** (the repeat colour of the anchoring frame; at an R3k2 anchor, j = q, so this is c(p), which is how Job AN read it). `closing_perm`: an orbit closed **in colouring space** has 30 ∣ L.
- **Formal (QuarterMirror).** The mirror reads each Γ-cycle backwards. This is a map between two different rotation systems, not a symmetry of one cycle.
- **Data (Job AO).** All core triangulations of orders 12–27, both orientations: L ∈ {20, 40, 60} only (2,566 / 136 / 48). The canonical period is exactly L. No orientation-preserving automorphism fixing h relates s(t+d) to s(t): all stabilisers are trivial (L = 20, 40 and 60).
- **Data (NightCycleBound, A7).** The adversarial 37-vertex graph A7 has a Γ-cycle with L = 800. So **"L ≤ 60" is a small-order fact, not a law: killed as a theorem candidate.**

## 1. The reduction: L = 10·m with m the orbit length of a pinned return map [proved]

Lift π to absolute colourings, π̃. Each step swaps one Kempe component, chosen from the canonical state, so π̃ commutes with relabelling: π̃(g·c) = g·π̃(c).

Define **T = σ⁻¹ ∘ π̃¹⁰** on colourings of an anchor's (type,k). By `period_colour_rotation`, T(c) has the **same ring colours as c**.

**Claim.** The canonical period is L = 10m, where m is the T-orbit length of c₀, and the closing permutation is ρ = σ^m.

*Proof.* Suppose s(L) = s(0) canonically, i.e. π̃^L c₀ = g·c₀ for some g ∈ S₄.
1. 10 ∣ L, because (type,k) has period exactly 10. Write L = 10m.
2. π̃^{10m} c₀ = σ^m·T^m c₀ by equivariance. T^m c₀ has c₀'s ring colours.
3. The ring uses all four colours, so g = σ^m and T^m c₀ = c₀.
4. Conversely, T^m c₀ = c₀ gives canonical closure at 10m. ∎

**Consequences.**
- ρ = σ^{L/10}, which is Job AN's observation, now explained.
- The colouring-space orbit has length L·3/gcd(m,3), i.e. 30 ∣ length (`closing_perm`).
- **"20 ∣ L" ⇔ "T has no odd orbit through a Γ-state".**
- The data say m ∈ {2, 4, 6} at orders ≤ 27, and m = 80 at A7.
- ρ = id ⇔ 3 ∣ m. The data match exactly: L = 60 ⇔ ρ = id (48/48), and L = 20, 40 ⇔ 3-cycle.
- L = 10 means m = 1: the colouring at position 10 is exactly σ(colouring at 0). In that case every vertex not coloured α must leave its colour class during the period, and every vertex coloured α must return to α.

## 2. Parity: the Heawood/Tait sign gives a necessary condition, but the ring does not decide it [proved + computed]

**Tait view.** Use colours in F₂², and give each edge uv the colour c(u)+c(v) ≠ 0.
- A swap of {a,b} on a component K cuts edge e when exactly one endpoint of e is in K. On each cut edge it applies the transposition (a+c ↔ a+d), which fixes a+b. Uncut edges keep their Tait colour.
- A relabelling g ∈ S₄ = AGL(2,F₂) acts on Tait colours through its linear part in S₃ = GL(2,F₂). The linear part has the same sign as g.

**Lemma (proved).** On a closed canonical cycle, every edge is cut an **even** number of times in total. Equivalently, every triangular face meets an even number of the swapped components (Heawood face signs).

*Proof.* The net action on each edge's Tait colour is the linear part of ρ = σ^m. That is a 3-cycle or the identity, so it is even, and a product of transpositions is even only when there are an even number of them. ∎

So a cycle with L = 10 needs **every edge cut an even number of times within one period**.

**The ring does not obstruct this.** I computed from the formal tables (`xTab`, `wTab`, `mTab`, with row 10 = σ(row 0)). A vertex lies in the step's K iff its colour changes. Over one period:
- every ring edge (x–x, x–w, w–w, y–m, m–z, p–m: 22 edges) is cut exactly **4** times;
- every ring face (11 faces) meets **6** components.

All of these are even. **Killed:** "a ring-local parity forbids L = 10". Any obstruction to m = 1, and any reason for 20 ∣ L, must use the far edges.

**Studio test (not run here; inputs absent).** For each Γ-cycle, record the set D_b of far edges cut an odd number of times in period b.
- m = 1 would need D₀ = ∅.
- 20 ∣ L would follow from "the D_b-sum over any odd number of consecutive periods is never ∅", which is strictly stronger than what is needed.
- Hypothesis H_D: D_b ≠ ∅ for every period of every Γ-cycle. This would kill L = 10, but not L = 30.

## 3. Involution hypotheses [killed / no evidence]

- **Mirror.** It reverses the cycle in the mirror rotation system. It is not an orientation-preserving involution of the cycle and gives no relation between s(t) and s(t+L/2).
- **Graph symmetry.** "π^{L/2} = a graph automorphism ∘ relabelling" is killed by Job AO: stabilisers are trivial, and no shift d ∈ {10, 20, 30} is induced by an automorphism.
- **Colour swap.** "π^{L/2} = colour swap" is impossible as a canonical statement, because canonical states are already taken modulo S₄. With the ring pinned, the only candidate is T^{m/2}. That is just "m is even", restated.

## 4. What distinguishes L = 20, 40, 60 [data, from joban.json / jobao]

- **By pattern** (Job AN):
  - L = 60 (ρ = id) occurs at (5,5,5,5,5) 28, (5,5,5,5,7) 10, (5,5,5,5,6) 4, (5,5,5,6,8) 4, (5,5,5,5,8) 2.
  - L = 40 is spread over patterns.
  - Most patterns show only L = 20.
- **Rank vectors** (A/B, μ/B, μ/A at positions 4/6/8). The period map v_b → v_{b+1} is the identity in 294/552 transitions at degree 6, with no fixed structure separating L classes (Job AN).
- **Fusion.** "L = 60 is three L = 20 cycles fused" is not supported: the stabiliser is trivial (Job AO), and m = 6 is a single T-orbit, not three.

## 5. Status

| statement | status |
|---|---|
| 10 ∣ L; ρ = σ^{L/10}; L = 10m with m the pinned return-map orbit length; 30 ∣ colouring-orbit length | **proved** (§1, `closing_perm`) |
| every edge cut an even number of times over a closed Γ-cycle | **proved** (§2) |
| ring edges cut 4×, ring faces met 6× per period (universal) | **proved** (table computation) |
| L ≤ 60 | **killed** (A7, L = 800) |
| ring-local parity forbids L = 10 | **killed** (all ring counts even) |
| automorphism/involution relating s(t), s(t+L/2) | **killed** (Job AO, trivial stabilisers) |
| **20 ∣ L** (m even) | **conjecture**: 2,750 Γ-cycles at orders 12–27 + A7 (m = 80), 0 exceptions; no proof |
| L = 60 ⇔ ρ = id ⇔ 3 ∣ m | **proved** as ρ = σ^m; the data only confirm that m ∈ {2,4,6} |
| H_D: every period cuts some far edge an odd number of times (would forbid L = 10) | **open**, Studio test in §2 |
