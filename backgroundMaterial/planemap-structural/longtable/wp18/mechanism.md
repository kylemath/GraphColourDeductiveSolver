# How degree-5 fan starts get filled: mechanism note

Long Table, 4 October 2026. This is exploratory work, done after the fact on the WP18 graphs (orders 12–22, the 961 graphs already recorded in `wp18-P1.json` … `wp18-P4.json`). No new order was run. Nothing here is a declared test.

"Proved" means a complete argument is written below. "Observed" means a count over the existing data, made after the run.

## Summary

1. **Slides are almost never needed.** Kempe swaps alone are the mechanism.
   - Every one of the 380,253 starts with fill length ℓ = 2 has a pure Kempe shortest fill, KK.
   - At ℓ = 3, 6,392 of 6,531 starts have KKK.
   - At ℓ = 4, 131 of 132 starts have KKKK.
   - Slides shorten the fill in exactly 140 starts, and always by exactly one move.
   - The first move is therefore *not* always a slide. A slide comes first in every shortest fill only for those 140 starts.
2. **Proved:**
   - ℓ ≤ 1 exactly when the start is not in the gap case. In the gap case, no single move fills, slides included (Lemma A).
   - A fill that ends with a slide can always be rewritten to end with a one-vertex Kempe swap (Lemma B).
   - A slide commutes with a swap whose colour pair avoids the colour that was slid (Lemma C).
   - Kempe's classical pair of swaps fills in two moves unless the configuration X ("Heawood interlock") occurs (Lemma E).
   - Each Kempe swap in the cascade inherits one of the two chains and moves the middle of the link two places around the 5-cycle (Lemma F).
3. **The starts with ℓ = 4** are 132 distinct colourings, which is 396 per fan. They come from 36 graphs, 26 of them in 17:0 and 17:1 together.
   - All are in configuration X in both orders, which Lemma E makes necessary.
   - In 114 of the 132 the middle link vertex b has degree 6. Among ℓ = 2 gap starts the share is 27%.
   - In 82 of the 132, every bichromatic subgraph is connected except the two splits the gap forces.
   - The optimal first move is Kempe's swap in 131 of 132, or a slide.
4. **Link colours and degrees do not determine the exact length** *[narrowed 5 October at the audit chat's request]*. At one and the same (v, τ), with an identical link colouring and identical degrees, there are gap starts with ℓ = 2, 3 and 4 (17:1, v = 0, τ₀). This shows only that the *exact* value of ℓ is not a function of the link pattern and degrees. It does **not** rule out a common bound: lengths 2, 3 and 4 are consistent with ℓ ≤ 4. It says nothing about coloured neighbourhoods of larger radius, which were not compared. In these examples the length differences coincide with how the chains P, Q, C₀ and D₂ run, but no causal claim is made.

## Setting

A start has hole h of degree 5 and a link 0, 1, 2, 3, 4 in rotation order.

- If the link uses three colours, ℓ = 0.
- Otherwise the link is coloured (α, β, α, γ, δ) up to symmetry (`swarm/fan-link.md`). The **roles** are a0 = 0, b = 1 (the *middle*, between the two α's), a2 = 2, g = 3 (adjacent to a2) and d = 4 (adjacent to a0).

Two chains matter:

- P is a βγ-path from b to g in T − h.
- Q is a βδ-path from b to d.

**Gap** means both P and Q exist. Two components matter as well:

- C₀ is the αγ-component of a0.
- D₂ is the αδ-component of a2.

**Kempe's pair** is one of two orders:

- KP_g: swap C₀, then swap the αδ-component of a2.
- KP_d: swap D₂, then swap the αγ-component of a0.

A fact used throughout: for a 4-colour start the three fans based at b, g and d are proper. So a 4-colour start is a start for every one of those fans that is legal. Per-fan totals are 3× the distinct-start counts below. The apex role carries no information, as the identical columns in `mechanism-raw.json`, key `l_perfan`, show.

## Lemmas proved by hand

**Lemma A (length ≤ 1).** For a start with a 4-colour link, ℓ = 1 if and only if it is not in the gap case. In the gap case, after any singleton slide the new hole's link again uses four colours.

*Proof.* `swarm/fan-link.md` proves that a single Kempe swap frees a colour exactly when P or Q is missing. So it remains to show that no slide fills a gap start. The singletons are b, g and d.

- *Slide to b.* Now h has colour β. Link(b) contains h (β), a0 and a2 (α), the vertex after b on P (γ, a neighbour of b other than h, since P ⊂ T − h), and the vertex after b on Q (δ). That is four colours.
- *Slide to g.* Now h has colour γ. Link(g) contains h (γ), a2 (α, the link edge 2–3), d (δ, the link edge 3–4), and the vertex before g on P (β, possibly b itself if the chord 1–3 is present). That is four colours.
- *Slide to d.* The same argument with Q gives four colours. ∎

In the gap case, therefore, the slide does not open a free colour. P and Q each deliver the missing colour to the new hole's link. This is the Jordan content of task 2: whichever singleton the hole moves to, one of the two chains ends next to it.

**Lemma B (a terminal slide equals a one-vertex swap).** Suppose (w, c) slides to u, and (u, c′) is filled. Then the Kempe swap of the singleton component {u}, in colours {c(u), x}, also fills (w, c). Here x is any colour missing from link(u) under c′.

*Proof.* Let σ = c(u). Since c′(w) = σ and w ∈ link(u), x ≠ σ. The neighbours of u other than w have the same colour under c and c′.

- None of them is x, because x is missing from link(u).
- None of them is σ, because c is proper.

So {u} is a whole {σ, x}-component of T − w. Swapping it recolours u to x. Since σ occurred only at u on link(w), link(w) loses σ. ∎

So every shortest-fill word ending in S has a twin of equal length ending in K. In the data, KS always comes with KK and SS always with SK (`mechanism-classify.txt`).

**Lemma C (commutation).** Suppose (w, c) slides to u, with σ = c(u), and is then swapped on a {p, q}-component K of T − u with σ ∉ {p, q}. The same state is reached by swapping K first, at hole w, and then sliding to u.

*Proof.*

1. w ∉ K, since its colour after the slide is σ.
2. u carries σ under c. Every other vertex has the same colour under c and under the slid colouring. So K is a {p, q}-component of T − w under c.
3. Swapping K creates no σ. Hence u is still the unique σ on link(w), and the slide to u is legal.
4. The two orders change the same vertices to the same colours. ∎

**Corollary (two moves).** Suppose a start has a 2-move fill of the form KS, SS, or SK where the swap avoids the slid colour. Then it has a KK fill.

*Proof.*

- KS becomes KK by Lemma B.
- SS becomes SK by Lemma B.
- An SK whose swap avoids the slid colour becomes KS by Lemma C, and then KK by Lemma B.

The remaining case is SK with the slid colour σ in the swap pair. Two sub-cases are open:

- the swapped component contains the old hole; or
- u has a q-neighbour inside the swapped component.

Where neither holds, the same argument as Lemma B goes through. The swap is a component of T − w, and then {u} is swapped alone. This case is proved too. The two open sub-cases are not proved. In the data every ℓ = 2 start that has SK also has KS, so KK follows there. ∎ (for the cases named)

**Lemma E (Kempe's pair and the Heawood interlock).** In the gap case:

- If some βγ-path P from b to g contains no vertex of C₀, then KP_g fills, and ℓ = 2.
- Symmetrically, if some βδ-path Q from b to d avoids D₂, then KP_d fills.

Hence ℓ ≥ 3 implies **configuration X**:

- C₀ meets every b–g βγ-path, necessarily in a γ-vertex; and
- D₂ meets every b–d βδ-path, in a δ-vertex.

*Proof.* The closed curve h–b–P–g–h is simple. At h the rotation is a0, b, a2, g, d. So the edge h–a2 leaves h on one side of the curve, and h–d and h–a0 leave on the other. The curve therefore separates a2 from {a0, d}.

By the same argument with Q, C₀ contains neither a2 nor g, so swapping C₀ recolours a0 alone on the link. The link becomes (γ, β, α, γ, δ). Assume P ∩ C₀ = ∅.

1. After the swap, every vertex of P keeps its colour, β or γ.
2. An αδ-path from a2 to d in T − h would have to cross the curve at a vertex of P. That is impossible.
3. So the αδ-component of a2 avoids d. It also avoids a0, which is now γ, and the only α on the link is a2.
4. Swapping that component sends the link to (γ, β, δ, γ, δ), which uses three colours. ∎

The converse fails. Observed: X holds in both orders at 25,141 gap starts with ℓ = 2, which are filled by some other KK. Lemma E was also checked mechanically on all 386,916 gap starts (`mechanism-slides.txt`, part 1), with no violation.

**Lemma F (the cascade rotates the middle and inherits one chain).** In the gap case:

- After swapping C₀, the link is (γ, β, α, γ, δ). Its middle is d, and the chain Q (βδ, untouched by an αγ-swap) is still a d–b chain of the new gap pattern. The new state has ℓ = 1 if and only if no αδ-path joins a2 to d.
- Symmetrically, swapping D₂ moves the middle to g, and P survives.

*Proof.* The repeated colour of the new link is γ, on g and a0. The singleton between them is d. The two chains of the new gap test are δβ from d to b, which is Q and unchanged, and δα from d to a2. Then apply `fan-link.md` to the new link. ∎

So the "pure Kempe" fill is a *cascade*. Each swap rotates the middle by ±2 around the 5-cycle and keeps one of the two old chains. It fails to finish only when the recoloured component C₀ or D₂ manufactures the opposite chain, which happens exactly in configuration X. This is Heawood's objection to Kempe, met one step at a time. Iterating only the four α-swaps (ag and ad at a0 and at a2) reaches the optimum in the following share of starts (`mechanism-iter.txt`):

| ℓ | Starts where the α-cascade reaches the optimum |
|---|---:|
| 2 | 358,081 of 380,253 |
| 3 | 4,314 of 6,531 |
| 4 | 95 of 132 |

The rest need an *interior* swap: a component touching no link vertex, which cuts P or Q at an interior vertex.

## Observations (observed after the fact; distinct starts per degree-5 vertex)

**Length classes** (`mechanism-classify.txt`):

| Length | Starts | Condition |
|---|---:|---|
| ℓ = 0 | 1,839,670 | three-colour link |
| ℓ = 1 | 1,539,249 | 4-colour link, not gap (Lemma A) |
| ℓ = 2 | 380,253 | gap |
| ℓ = 3 | 6,531 | gap |
| ℓ = 4 | 132 | gap |

Per-fan totals (×3 for 4-colour starts, plus the three-colour starts once per fan) reproduce WP18's ℓ = 1…4 columns, for example 396 at ℓ = 4.

**Move words.** "Starts admitting each word" counts starts for which that word is among the shortest fills.

| ℓ | Starts admitting each word | Starts with no all-K shortest fill |
|---|---|---:|
| 2 | KK 380,253, KS 300,469, SK 218,362, SS 64,877 | 0 |
| 3 | KKK 6,392, SKK 5,917, KKS 4,616, KSK 4,595, SKS 2,232, SSK 2,222, SSS 1,202, KSS 511 | 139 |
| 4 | SKKK 132, KKKK 131, KSKK 122, SSKK 116, and all other 4-letter words occur | 1 |

So the needed words are K^ℓ, except for 140 starts that need S K^(ℓ−1):

- 139 at ℓ = 3. Their word sets are {SKK}, {SKK, SKS, SSK} or {SKK, SKS, SSK, SSS}.
- 1 at ℓ = 4, at 22:93, v = 17. Its pure-Kempe length κ is 5.

Over all ℓ ≥ 3 starts, κ ≤ ℓ + 1 (`mechanism-kempe.txt`).

**Slide-needed starts** (`mechanism-slides.txt`):

- In 110 of the 140, the only optimal first move is a slide to a *side* singleton (g or d) of degree 6.
- In 19, a slide to the middle b is among the optimal first moves. In 18 of those, b has degree 7 or 8.

**First moves** (`mechanism-first.txt`). Kempe's swap (ag@a0 or its mirror ad@a2) is an optimal first move in:

| ℓ | Starts with Kempe's swap optimal |
|---|---:|
| 2 | 355,112 of 380,253 |
| 3 | 6,315 of 6,531 |
| 4 | 131 of 132 |

Slides to a side vertex are optimal in 52% of ℓ = 2 starts and 87% of ℓ = 3 starts, but they are almost never *necessary*.

**Hole degrees.**

- At ℓ = 2 and ℓ = 4, every start has a shortest fill ending back at the original degree-5 hole.
- At ℓ = 3, 82 starts have every shortest fill ending at a vertex of degree 6 to 8. In 70 of them, every shortest fill ends at degree 6.
- The intermediate hole is degree 5 or 6 in the most common sequences. The typical link-pattern chain for a slide route is 5:2111 → 6:2211 → 6:2211 → 6:222, a degree-6 hole with link counts 2, 2, 1, 1, filled by reaching three pairs.

**ℓ = 4 configuration** (`mechanism-features.txt`, `mechanism-iter-long.json`):

| Feature | ℓ = 4 | ℓ = 2 |
|---|---:|---:|
| Configuration X in both orders | 132 of 132 (necessary by Lemma E) | — |
| deg(b) = 6 | 114 of 132 (86%) | 27% |
| deg(b) ≥ 6 | 124 of 132 | — |
| Both chain subgraphs connected (the whole βγ and βδ subgraphs are single chains) | 113 of 132 | 42% |
| Minimal component signature: αβ, βγ, βδ, γδ each connected; αγ and αδ each exactly 2 components (the forced minimum) | 82 of 132 (62%) | 3% |

Colour populations among the ℓ = 4 starts are 5,5,5,6 in 74, 5,5,5,5 in 30, and 4,4,4,4 in 26. All 26 of the 4,4,4,4 starts are at order 17.

**Link pattern and degrees do not determine the exact ℓ.** At 17:1, v = 0, fan τ₀, the histogram is ℓ = 0: 6, 1: 16, 2: 7, 3: 2, 4: 2. Every gap start there has the same link pattern and the same degrees. This does not exclude a uniform bound such as ℓ ≤ 4. Larger-radius coloured neighbourhoods were not compared.

## Worked example (order 14, `fan-link.md` start)

The dipyramid start is h = U₀ with link (U₁, N, U₅, L₀, L₁) coloured (0, 1, 0, 2, 3). It is in the gap case, with P = N U₄ L₅ L₀ and Q = N U₂ L₂ L₁.

- C₀, the {0, 2}-component of U₁, is {U₁} alone: its neighbours are N, U₂, L₁ and L₂, coloured 1, 3, 3, 1.
- P ∩ C₀ = ∅, so Lemma E applies. Recolour U₁ to 2.
- The {0, 3}-component of U₅ is then {U₅}: its neighbours N, U₄, L₅, L₀ are coloured 1, 2, 1, 2. Recolour U₅ to 3.
- The link becomes (2, 1, 3, 2, 3). Colour 0 is free, and ℓ = 2 by KK.

## What would be needed for a bound, and the obstruction

A lemma of the form "gap ⇒ ℓ ≤ k" for every T is exactly a bounded form of VH∃ at degree 5. It would make the degree-5 step of `swarm/hole-induction.md` unconditional, so it cannot be expected from link-local reasoning.

Lemma E reduces ℓ ≤ 2 to the absence of configuration X, and X is a statement about global chains. Configuration X is necessary for ℓ ≥ 3 but not sufficient: 25,141 starts with ℓ = 2 have it. Lemma F shows that each swap re-creates the same type of question (one chain inherited, one possibly manufactured).

The data suggest that the cascade terminates fast, because each manufactured chain must pass through the previously swapped component. No proof of a bound on the cascade is offered.

The literature on Kempe cycling, Gethner–Springer on iterating Kempe's argument, is recalled here only as context. It is not checked here.

## Conjecture for a later declared test (do not run before review)

**Conjecture M.** Let T be a spherical triangulation of minimum degree 5, v a degree-5 vertex, τ a legal fan at v, and s ∈ S(v, τ) a start. Write ℓ(s) for the mixed fill length (WP18 moves) and κ(s) for the fill length using Kempe swaps only, with the hole fixed.

- **(M1)** ℓ(s) ≤ 4.
- **(M2)** κ(s) ≤ ℓ(s) + 1. Slides save at most one move.
- **(M3)** If ℓ(s) = 2, then κ(s) = 2. Slides never shorten a two-move fill.

*Kill condition:* any start with ℓ ≥ 5, or with κ ≥ ℓ + 2, or with ℓ = 2 < κ, found within a breadth-first cap of 6 mixed moves and 7 Kempe moves. A start beyond either cap is inconclusive.

*Suggested scope:* every graph of `plantri -m5 -a 23`, all v, all legal τ. The input hash is to be recorded before the run.

*Status:* observed on orders 12–22 only, after the fact: the maximum ℓ is 4, the maximum κ − ℓ is 1 (in 140 starts), and M3 holds in all 380,253 ℓ = 2 starts. M3 is partly proved (Corollary above). M1 and M2 are not proved.

## Files (all in `wp18/`)

| Script | Output |
|---|---|
| `mechanism_classify.py` | `mechanism-raw.json`; tables via `mechanism_report.py` → `mechanism-classify.txt` |
| `mechanism_kempe.py` | `mechanism-kempe.txt`, `mechanism-kempe-long.json` (Kempe's pair, κ, all ℓ ≥ 3 starts) |
| `mechanism_first.py` | `mechanism-first.txt` (optimal first moves with touched link roles) |
| `mechanism_iter.py` | `mechanism-iter.txt`, `mechanism-iter-long.json` (α-cascade depth, ℓ ≥ 3 features) |
| `mechanism_features.py` | `mechanism-features.txt` (degree of b, component signatures, populations) |
| `mechanism_slides.py` | `mechanism-slides.txt` (Lemma E mechanical check; the 140 slide-needed starts) |

Inputs: the graphs in `wp18-P1.json` … `wp18-P4.json` only. The scripts reuse `wp18_core.py` (`deletion_states`, `legal_fans`, `moves`, `shortest_fill`).
