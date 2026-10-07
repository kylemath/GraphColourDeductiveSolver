# NightW2Euler: W2 as three forests, and the six-pair identity

Night worker, 7 October 2026 (written 04:48 MDT). **[exploratory] Unreviewed.** MacBook on AC (pmset: AC power, 100%, charged). Python on 1 core, about 1 minute in total.

Scripts and outputs: `backgroundMaterial/planemap-structural/longtable/local-runs/33-nightw2euler/`. The engine is `uv_lib.Hole` (Jobs U and V).

**Data.**
- The 34 hole-orientations of `jobak-66dump.json` (orders 25–27). This gives 124 Γ periods plus 100 open DL windows.
- The p25 #668 h18 counterexample.
- gentri orders 20–23 as an open-run control: 404 windows, none of them on a Γ-cycle.

**Window.** Positions 3–9 around R3k2 = position 4. Colours are the absolute ones of NightW2 §1: α = 1, and at R3k2 μ = 2, A = 3, B = 4. Every window's colourings were mapped to absolute names through the link, and every step was checked to be one swap of the tabulated pair (225 + 404 windows, 0 exceptions).

Labels: **[proved]** by hand; **[data]** with counts; **[killed]**.

## Verdict

1. **[proved] The six-pair identity splits into three exact pair dualities (§1).** At any state with link pattern α μ α A B:
   - rank(AB) = C(αμ) − 1 and rank(αμ) = C(AB) − 1;
   - rank(μA) = C(αB) − 1 − [Lock1] and rank(αB) = C(μA) − 1 − [¬Lock1];
   - rank(μB) = C(αA) − 1 − [Lock2] and rank(αA) = C(μB) − 1 − [¬Lock2].

   Summing the six gives `six_pair_rank_identity` (Σrank = ΣC − 8). Checked on all 4,403 window states (DL or not): 0 violations.

   **Consequence [killed as an obstruction]:** the identity carries no information beyond the three pairings separately.
   - "ΣC − 8 ≥ 0 at DL", and "the lock pairs {α,A}, {α,B} have ≥ 2 components", are literally rank(μB) ≥ 0 and rank(μA) ≥ 0.
   - "{3,4} is a forest at R3k2" (F₄) is exactly C(12) = 1. It forces nothing on the other five ranks. At F₄ states those five take 7 or more different vectors on Γ, for example (0,0,0,0,0) ×20 and (0,0,0,0,1) ×10.
2. **[proved] A colour-free recursion on a DL run (§3).** Let (f, g, h)ᵢ be the component counts of the {α,μ}-, {α,B}- and {α,A}-graphs at state i.
   - σ is fixed ⇔ fᵢ = 1. Checked on all windows.
   - DL ⇒ gᵢ, hᵢ ≥ 2.
   - Exactly: g_{i+1} = hᵢ, f_{i+1} = (gᵢ after the step), h_{i+1} = (fᵢ after the step).

   Each α-pair graph cycles through three roles: free, then A (its own component gets swapped, so it is frozen), then B. **W2 failure in the interior of a DL run is six forced events.** Step 3 merges G₁₂ to connected and step 4 splits it; steps 5 and 6 do the same to G₁₃; steps 7 and 8 do the same to G₁₄.
3. **[data] Parity.** The total rank changes by an odd amount on every DL→DL step (3,214/3,214, of which 744 are Γ steps). It changes by an even amount on every step that touches a non-DL state (560/560). So on any DL run R ≡ R(4) + (i − 4) (mod 2). Any linear potential still cancels on closed orbits (NightPotential's obstruction).
4. **[data] What the closure adds, quantitatively (§4).** Of the 75 open W2-failure windows (17 in the dump, including p25 #668; 58 in gentri):
   - **71 skip one of the two outer events.** Either G₁₂ is already connected at position 3 (no merge at step 3), so Lock1 dies at position 3; or G₁₄ is still connected at position 9 (no split at step 8), so Lock2 dies at position 9.
   - 27 skip both. p25 #668 is one of these: a(12) = 1 at positions 3 and 4, and a(14) = 1 at positions 8 and 9.
   - 2 have a lock die although the graph has ≥ 2 components.
   - 2 are DL on both sides (gentri; they die at distance 2 and 3).

   On a Γ-cycle all six events must occur, and they never do: 0/124 periods. There is also no spacing-2 triple of fixed points at **any** period position on Γ (0 over 10 × 124 windows), against 16 open ones, all starting at R3k2.
5. **Not proved.** I have no argument that the six events cannot all occur on a closed orbit. The sharp target is in §5.

## 1. Exact pair duality [proved]

**Lemma D (full triangulation).** Let T be a triangulated sphere with a proper 4-colouring, {a,b} ⊔ {c,d} a pairing of the colours. Then rank(G_ab) = C(G_cd) − 1.

*Proof.*
- Every triangle has exactly one "pure" edge (in G_ab or G_cd) and two mixed edges. Gluing triangles along mixed edges gives disjoint cyclic strips (annuli). One side of each strip is a closed walk in a single ab-component, the other side a closed walk in a single cd-component.
- For a component K of G_ab and a face f of K, all triangles inside f along ∂f are strip triangles. Around a boundary vertex u inside f, all neighbours are c/d, because an a/b neighbour would give a further edge of K. So they form one strip. Hence #strips at K = #faces(K) = rank(K) + 1.
- The bipartite graph {components} – {strips} is connected (the sphere is connected) and acyclic (each annulus separates the sphere). So it is a tree.
- Therefore #strips = C_ab + C_cd − 1 = rank_ab + C_ab, which gives rank_ab = C_cd − 1. ∎

(Forest ⇔ the complementary pair is connected is the leaf case; this is Lemma Fix's duality.)

**Hole version.** Triangulate the pentagon x_j..x_{j+4} = α μ α A B by the chords x_{j+1}x_{j+3} (μA) and x_{j+1}x_{j+4} (μB). Both are properly coloured, so this gives a 4-coloured triangulation T*.
- Assumption: neither chord is an edge of T − h. Otherwise there is a separating triangle through h, which does not happen in core graphs.
- The chord μA adds 1 to rank(μA) if Lock1 holds; otherwise it merges two μA-components.
- Likewise the chord μB, with Lock2.
- Apply Lemma D in T* and subtract. This gives the six formulas of Verdict 1. Their sum is −6 − 2 = −8, which is `six_pair_rank_identity`. Lean: these are `QuarterEuler` plus a strip lemma (not formalised).

At a DL state this reads:
- rank(AB) = a_μ − 1 and rank(μA) = a_B − 2;
- rank(μB) = a_A − 2;
- rank(αc) = C(complement) − 1 for each c.

Here a_c = C(G_{1c}) and b_c = C(complement of {1,c}). So **R = Σ_c (a_c + b_c) − 8** is a sum of three independent pairing terms. The "≥ 2 lock components" are the two α-pairs that are not free.

## 2. Bookkeeping at positions 3–9 [proved; table checked on 629 windows]

μᵢ, Aᵢ, Bᵢ are absolute colours (α = 1 throughout). Step i swaps {1, Aᵢ}. **The pattern is 3-periodic:** μ_{i+1} = Bᵢ and A_{i+1} = μᵢ.

| pos | state | μ (free α-pair) | A (swapped at step i) | B | locks force (≥ 2 comps) | W2 failure needs |
|---|---|---|---|---|---|---|
| 3 | R1k0 | 3 | 4 | 2 | a₂, a₄ | |
| 4 | R3k2 | 2 | 3 | 4 | a₃, a₄ | a₂ = 1 (F₄ ⇔ r₃₄ = 0) |
| 5 | R1k4 | 4 | 2 | 3 | a₂, a₃ | |
| 6 | R3k1 | 3 | 4 | 2 | a₂, a₄ | a₃ = 1 (F₆ ⇔ r₂₄ = 0) |
| 7 | R1k3 | 2 | 3 | 4 | a₃, a₄ | |
| 8 | R3k0 | 4 | 2 | 3 | a₂, a₃ | a₄ = 1 (F₈ ⇔ r₂₃ = 0) |
| 9 | R1k2 | 3 | 4 | 2 | a₂, a₄ | |

**Per-step rank change.** A {1,c} swap leaves pairing c ({1c | de}) untouched: both rank(1c) and rank(de) are unchanged. Only the other two pairings move.

At each DL state, the six ranks are, with the duality corrections:
- r(1μ) = b_μ − 1, r(1A) = b_A − 1, r(1B) = b_B − 1;
- r(AB) = a_μ − 1, r(μB) = a_A − 2, r(μA) = a_B − 2.

What each fixed point forces on the other five ranks at its state:

| | forces | other five ranks |
|---|---|---|
| F₄ | a₂ = 1 | r₁₂ = b₂ − 1, r₁₃ = b₃ − 1, r₁₄ = b₄ − 1, r₂₄ = a₃ − 2, r₂₃ = a₄ − 2 |
| F₆, F₈ | the same with the roles rotated | |

These are all free; the identity holds automatically. Time reversal maps i ↔ 12 − i, so F₄ ↔ F₈ and g ↔ h.

## 3. The recursion and the six events [proved]

Since step i swaps a component of G_{1Aᵢ}, that graph is unchanged: g_{i+1} = a_{μ_{i+2}}(i+1) = a_{Aᵢ}(i) = hᵢ. The other two α-graphs are rewritten.

Suppose a W2 failure sits inside a DL run covering positions 3–9. DL at positions 3, 5, 7, 9 gives a_B, a_A ≥ 2, so:

| step | swap | event (forced) |
|---|---|---|
| 3 | {1,4} | G₁₂: ≥ 2 → 1 (merge) |
| 4 | {1,3} | G₁₂: 1 → ≥ 2 (split) |
| 5 | {1,2} | G₁₃: ≥ 2 → 1 (merge) |
| 6 | {1,4} | G₁₃: 1 → ≥ 2 (split) |
| 7 | {1,3} | G₁₄: ≥ 2 → 1 (merge) |
| 8 | {1,2} | G₁₄: 1 → ≥ 2 (split) |

Every step 3–8 is an event. The three graphs take turns being connected, at the three R3 k ≤ 2 states.

On Γ data, at most two of the three pairs occur in one window: patterns (F,F,–) ×38, (–,F,F) ×38, (F,–,–) ×10, (–,–,F) ×10, (–,F,–) ×6, (–,–,–) ×22; (F,–,F) and (F,F,F) ×0.

## 4. p25 #668 and what closure adds [data]

p25 #668 (the "a" columns are a₂, a₃, a₄; the "b" columns are C₃₄, C₂₄, C₂₃):

| pos | a₂ a₃ a₄ | b | locks | R |
|---|---|---|---|---|
| 3 | **1** 2 2 | 2 2 1 | L1 dead | 3 |
| 4 | 1 2 2 | 1 1 1 | DL | 0 |
| 5 | 2 2 1 | 2 1 1 | DL | 1 |
| 6 | 2 1 2 | 2 1 2 | DL | 2 |
| 7 | 2 3 2 | 1 1 2 | DL | 3 |
| 8 | 3 3 1 | 2 1 2 | DL | 4 |
| 9 | 3 2 **1** | 2 2 4 | L2 dead | 6 |

The window has only four of the six events:
- G₁₂ is connected before step 3, so there is no merge and Lock1@3 fails;
- G₁₄ stays connected after step 8, so there is no split and Lock2@9 fails.

Across all 75 open W2-failure windows, (a₂(3), locks@3, a₄(9), locks@9):

| pattern | count |
|---|---|
| (1, L1 dead, 1, L2 dead): both outer events missing | 27 |
| (1, L1 dead, ≥ 2, DL): merge at step 3 missing | 21 + 2 |
| (≥ 2, DL, 1, L2 dead): split at step 8 missing | 21 + 2 |
| (≥ 2, DL, ≥ 2, DL): all six events | 2 (gentri; run dies at distance 2 and 3) |

So **closure adds exactly the two outer events (merge at step 3, split at step 8), plus DL beyond them.**
- Open runs avoid W2 mostly (71/75) by missing one of them.
- Job AL's 106/10,813 order-27 windows with DL on both sides are the cases with all six events. In them the run dies later: one side reaches up to 21–29 steps (Job AL). So no fixed-distance version is true, and the remaining statement is global.

**Other quantities [data].**
- R(4) + R(8) ≥ 2 on Γ (124/124). It is 0 in 14 open failures, and those are exactly the states where all six pairs are forests at both ends.
- R(4) = 0 itself is allowed on Γ (20/124), so low total rank is not the obstruction.

## 5. Sharp target and next steps

**Six-event lemma (target, ⇔ W2 at degree 6 on Γ).** On an all-DL orbit at a Hole6, the six events of §3 never all occur in one period.

Equivalent single-graph form: G₁₂, G₁₃ and G₁₄ cannot be connected at R3k2, R3k1 and R3k0 respectively.

Leads:
- (a) Each merge is a {1,c}-swap whose component K joins all components of G_{1d}. Each split is the next swap cutting G_{1d}, through the link arc (K₄ ∋ p, y, x₃; K₆ ∋ x₃, x₄, m, z; K₈ ∋ x₄, x₀). A strip-tree version of Lemma D tracks how one Kempe swap moves the ab/cd strip tree, and might bound consecutive merge/split alternations.
- (b) Mirror symmetry pairs steps 3 ↔ 8, 4 ↔ 7 and 5 ↔ 6, so it is enough to exclude "merge at 3 ∧ split at 8" given the middle four.
- (c) The 2 gentri windows with all six events and DL on both sides (`gentri.jsonl`, back/fwd = (2,3) and (3,2)) are the smallest open witnesses to study by hand.

## Reproduction

In `local-runs/33-nightw2euler/`:
- `python3 w2e.py dump dump.jsonl` and `python3 w2e.py 20,21,22,23 gentri.jsonl` write the window records (6 ranks and components at positions 3–9, locks, run extent).
- `summ1.py` runs the duality check.
- `summ2.py` writes the component vectors.
- `steps.py` gives the per-step changes.
- `python3 fx.py dump > fx-dump.txt` gives the fixed-point patterns.
