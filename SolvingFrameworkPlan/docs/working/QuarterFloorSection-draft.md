# The quarter floor (draft section for the VH∃ paper)

*Draft by Long Table, 6 October 2026, for later merging. Status labels follow the ledger. Sources are listed at the end.*

## Setting and notation

Let T be a plane triangulation and v a vertex of degree 5, with link x₀x₁x₂x₃x₄ in rotation order (indices mod 5). A *state* is a proper 4-colouring of T − v. A *Kempe class* S is an equivalence class of states under Kempe changes in T − v. A proper colouring of a 5-cycle uses 3 or 4 colours, so every state is of exactly one of two kinds.

- **Filled:** the link uses 3 colours. Exactly one colour appears once (the *singleton*). If it sits at position i, the pairs {i+1, i+3} and {i+2, i+4} are each monochromatic. Let **F_i ⊆ S** be the filled states with singleton at i. A filled state extends uniquely to a 4-colouring of T: v takes the missing colour.
- **Unfilled:** the link uses 4 colours, with exactly one repeated colour α at positions j and j+2. Let **U_j ⊆ S** be the unfilled states with repeat pair {j, j+2}. Write m = x_{j+1}, a = x_{j+3} and b = x_{j+4}, with colours μ, A and B.
  - *Lock 1*: m and a lie in one {μ, A}-component of T − v.
  - *Lock 2*: m and b lie in one {μ, B}-component.
  - **D_j ⊆ U_j** is the set of *doubly locked* states (both locks hold).

  An unfilled state that is not doubly locked becomes filled after one Kempe change (Kempe's step).

Write F = Σ_i |F_i| and U = Σ_j |U_j|. Tilley's D-resolvability conjecture [Tilley 2017], which we call R\*_v, asks that **F > 0 in every class S**.

## The observation [computed]

**Exhaustively, at orders 12–24** (all minimum-degree-5 triangulations, every degree-5 vertex, every Kempe class of T − v; 156,033 holes, 160,979 classes):

> **every class satisfies F ≥ ¼ |S|**, i.e. U ≤ 3F.

- 419 classes sit exactly at ¼: 2 at order 17, 2 at 21, 11 at 22, 129 at 23 and 275 at 24.
- 405 of these split into four equal link-pattern blocks; the other 14 are mixed.
- No class is targetless.
- **No floor holds at degree 6 or 7.** The minima observed there are 1/8 and 2/17.

[local compute, commit 0c0e098, message 1805.] An adversarial search over 95,884 further core graphs found no class below ¼ [local intel, 9c1e03c, message 1848].

Summing over the classes of one hole gives the chromatic-polynomial form **P(T,4) ≥ ¼·P(T − v,4)**, because each filled state extends uniquely.

## A fan-contraction identity [hand, unreviewed]

Let G_i be T − v with x_i and x_{i+2} identified (the fan contraction at x_{i+1}). A filled state has exactly two equal non-adjacent link pairs, and an unfilled state has exactly one. So Σ_i P(G_i,4) = 2F_tot + U_tot, summed over all states, and

$$P(T,4) \;=\; \sum_{i=0}^{4} P(G_i,4) \;-\; P(T-v,4).$$

The chromatic form of the floor is therefore Σ_i P(G_i,4) ≥ (5/4)·P(T − v,4). For a free 5-cycle the filled fraction is 120/240 = ½, so the observed floor is half the value an unconstrained ring would give.

## The non-doubly-locked half [hand, audited]

**Lemma A** [Math; audited, correct per j]. For every class S and every j,

$$|U_j \setminus D_j| \;\le\; |F_{j+3}| + |F_{j+4}|.$$

*Idea of proof.* If lock 1 fails, swap the {μ, A}-component of a. It meets the link only in a, and the result lies in F_{j+4}. Otherwise lock 2 fails: swap the {μ, B}-component of b, and the result lies in F_{j+3}. Each image determines its preimage, so the map is injective for each j.

Each filled state has at most two preimages over all j. So **Σ_j |U_j ∖ D_j| ≤ 2F**: the non-doubly-locked unfilled states of a class are at most twice its filled states. The floor U ≤ 3F therefore reduces to paying for the doubly locked states with one unit per filled state, plus the unused slack.

## A class identity [hand, unreviewed; verified computationally]

Join each unfilled state d ∈ U_j that has lock 2 to its image under the rotation R₊₃ (swap the {α, A}-component of x_{j+2}). This lands in U_{j+3} with lock 1. The resulting graph Γ is a disjoint union of paths and cycles, and Math proves

$$3F - U \;=\; 2N_0 \;+\; \tfrac32 L_F \;+\; \sum_{\text{paths }P}\bigl(1 - d(P)\bigr) \;-\; D_{\mathrm{cyc}},$$

where:
- N₀ counts unfilled states with neither lock;
- L_F counts the "long bits" of filled states;
- d(P) is the number of doubly locked states inside a path P;
- D_cyc is the number of doubly locked states on cycles of Γ.

[Math, message 1818; *MathQuarterFloorBijections.md*.] **[computed]** The identity holds with 0 mismatches on 46,488 classes [local compute, 2163e02]. At the floor, every term on the right vanishes, which gives exactly the four equal blocks observed.

## The open inequality: DD_j [open; holds in every class tested]

For d ∈ D_j with R₊₃(d) not doubly locked, the two-swap map ρ = φ ∘ R₊₃ injects into F_{j+1}, and its image avoids Lemma A's images. It is undefined exactly on

  **DD_j = {d ∈ D_j : R₊₃(d) is doubly locked}**,

the doubly locked states whose rotation stays doubly locked. Math's exact per-j accounting reduces the floor to

$$|DD_j| \;\le\; \mathrm{room}_j \;:=\; L_j + |U_j^{ff}| + |U_{j+3}^{ff}| + |E_j|,$$

with:
- L_j the long bits;
- U^{ff} the states where both locks fail;
- E_j the path starts with no interior doubly locked state.

**[computed]** This held at every j of every class tested, including an adversarial search for long doubly-locked rotation chains. The maximum excess |DD_j| − room_j was **0** (never positive). All-DL rotation cycles of length up to **880** occur in the core class, and all cycle lengths are ≡ 0 mod 5 [local intel, 9c1e03c].

DD_j is non-empty in general. The A_r family has infinite all-doubly-locked rotation orbits, which refuted Conjecture L. So **the inequality is genuinely global**. A targetless class would satisfy every local fact used above, so no local argument can close it.

### Locality [computed]

Can the doubly locked states in DD_j be paid for by a charging rule of fixed radius? The data say no:
- **Compensating units are near.** Every DD state lies within 5 Kempe changes of a compensating unit, at orders up to 23 [707840b].
- **A per-j injection does not stay near.** A per-j injection that charges only within swap radius k needs k_min ≤ 5 up to order 20, 6 at orders 21–23, and 7 at order 24. Radius 7 is first needed at gentri order 24, #1460, hole 19 [534dfb2, 3a346c8].
- **Pooling across j does not stay near either.** Pooled across j, the requirement is 4, 5 and 6 respectively [ba90dfd].

About 98% of cases match within 3 swaps, but the worst case grows by about one every few orders. **So no fixed-radius charging proof exists in this form.** The open inequality is genuinely global, which fits its strength (next section).

## Strength, stated plainly

The DD_j inequality at every j implies the floor F ≥ ¼|S| in every class, which implies F > 0, i.e. R\*_v. So:

- **the DD_j inequality, or the floor, for all triangulations is at least as strong as R\* at every degree-5 vertex**;
- that is Tilley's open D-resolvability conjecture [Tilley 2017], **and so it implies the Four Colour Theorem** (through R\* ⇒ VH∃ ⇒ 4CT, compiled in Lean);
- the converse is not claimed.

The quarter floor is therefore a quantitative strengthening of a published open problem. It is consistent with all data up to order 24, and it is not a route around the difficulty of the Four Colour Theorem. What is new is the exact location of the missing step: chains of rotations that stay doubly locked must be paid for elsewhere in the class.

## Sources

- **Messages** (in `SolvingFrameworkPlan/messages/2026-10-06/`):
  - local compute 1805 (exhaustive census) and 1811 (counting lemma);
  - Math 1813 (Lemma A) and 1818 (bijections, class identity, DD_j);
  - local intel 1848 (adversary).
- **Commits:** 0c0e098, 2163e02, 9c1e03c; locality: 707840b, 534dfb2, 3a346c8, ba90dfd.
- **Working pages:**
  - `docs/working/MathQuarterFloorLemmaA.md`;
  - `docs/working/MathQuarterFloorBijections.md`;
  - `docs/working/QuarterFloorLiterature.md` (no prior statement found).
- **Literature:**
  - J. Tilley, "D-resolvability of vertices in planar graphs", *JGAA* 21(4) (2017) 649–661;
  - G. D. Birkhoff and D. C. Lewis, "Chromatic polynomials", *Trans. AMS* 60 (1946) 355–451.
