# Night: A₃₄′ as a lock statement: a double step-8 break and Lock2

Night worker, 7 October 2026 (written 03:46 MDT). **Exploratory. Hand arguments plus single-core checks on gentri orders 20–24. Unreviewed.**

Builds on:
- `NightLemmaS.md` (§0 period lemma P1–P3; §5.1 lock-membership form of J);
- `NightF6Flow.md` §2.1;
- the Lean files `QuarterGammaPeriod` (`Hole6`, `pair_own`, `gamma_period_ten`), `QuarterPeriodJ` (`JoinYZ`, `k4_failure_iff_break`), `QuarterJordanDual`, `QuarterSigmaK34` (`K4Ball`, Lock1/Lock2 from `QuarterFloor`);
- Studio Jobs O, P, X, AA, AC and AE, plus the coordinator's two cautions (the R1k1 ring identity, and QuarterMirror/QuarterLockJ).

Labels:
- [proved]: a hand argument from the type tables, properness and planarity;
- [proved mod (D)]: uses the Kempe/Jordan duality in the boundary-parity form of `QuarterJordanDual.hex_core`, not re-formalised here;
- [data]: local scripts, §7;
- [killed]: a counterexample or a data contradiction is given.

## Verdict

**A₃₄′ is not proved. The target as stated in the brief is false in its window. The reduction is sharpened to fixed vertices.**

1. **[killed] The brief's target window.** The brief's target is: "breaks at step 8 of periods b and b+1 force some state of periods b+1, b+2 to lose Lock2".
   - It is false on open runs. Job X has p26m #21951 h22: the second failing R3k4 is at position 0 of period b+2, and the run stays DL for 15 more states. The first non-DL state is position 5 of period b+3.
   - The data support only the weaker form: the run leaves DL within 16 states of the second failing R3k4.
   - For A₃₄′ on Γ-cycles any finite window is enough, since a Γ-cycle never leaves DL. So the correct target is "a double break ⇒ the run is not closed".
2. **[proved] Fixed-vertex bookkeeping (§1).** At every one of the ten positions, Lock1, Lock2 and J reduce to joins between fixed ring vertices in an explicit colour pair (table §1.2). This answers the coordinator's request to make j explicit.
3. **[proved] Far-ness from Lock2 (§2.1).** The step-8 component K avoids p, m, y and z because of Lock2 at R3k0. Job O recorded this as data; here it is a proof.
4. **[proved mod (D)] Pocket lemma (§2.2).** At R1k2, J is false ⇔ m reaches w⁺ = w_{q+1} in the {c(p), c(m)}-graph minus p and x⁺ = x_{q+1}. So a break is a closed {c(p), c(m)}-curve p x⁺ w⁺ ⋯ m p around z. The step-9 swap swaps this whole curve, so it survives to R3k4.
5. **[proved] Window lemma (§3).** On positions 9, 0, 1, 2, 3, 4 (from R1k2 to the next R3k2), the J pair {c(y), c(z)} is one fixed colour pair. In that one 2-colour graph G_J, DL forces:
   - y ~ w₂ at positions 9 and 0;
   - z ~ w₂ at positions 2 and 3;
   - y ~ w₂ ~ z at position 4 (P1).

   So J at positions 9 and 0 is "z joins {y, w₂}", and J at positions 2 and 3 is "y joins {z, w₂}". A k = 4 failure is "z split off" and a k = 3 failure is "y split off".
   - [data] 0 exceptions on all DL states at orders 20–23, both orientations.
6. **[killed] Three proposed crossing mechanisms.** Each fails for an explicit reason (§4):
   - (a) "K′ meets the Lock2 witness at R3k0^{b+1}" is impossible, because the two colour classes are disjoint (QuarterLockJ).
   - (b) "the Lock2 witness at R3k0^{b+1} must cross the second pocket and cannot". It can: it leaves the pocket through m along the edge z–m, which is a Lock2 edge.
   - (c) Every intersection count between K, K′, Π_b and the Lock components is forced ≥ 1 by the fixed local vertices x_{q+2}, x_{q+3} and w⁺. So the "meets" statistics carry no information unless the local vertices are removed.
7. **[conjecture] The isolated sub-statement is Σ in §5**, with a precise Studio test in §6. It is about one swap only: the step-0 and step-1 far swaps of period b+2 against fixed vertex sets of period b. I could not test it locally. The gentri orders ≤ 24 contain only 4 double breaks, all on short open runs with |Z_b| ≤ 3.

## 1. Bookkeeping

### 1.1 Frame and fixed names

- The hole is h. The link is x₀..x₄ in rotation order. The degree-6 vertex is p = x_q; below q = 0.
- w_t is the common outer neighbour of x_t and x_{t+1} (`Hole6`). So y = w_{q−1}, z = w_q, and m is p's extra neighbour between y and z.
- Fixed names (q = 0):
  - p = x₀;
  - x⁺ = x₁, x₂, x₃, x⁻ = x₄;
  - z = w₀, w⁺ = w₁, w₂, w₃, y = w₄;
  - m.
- Cyclic order around p: h, x⁺, z, m, y, x⁻.
- The ring is the cycle z w⁺ w₂ w₃ y m (the edge y–z is replaced by y–m–z).

The colours are actual colours (α = 0 fixed), and the roles (μ, A, B) rotate as in NightLemmaS §2. The table is produced by `table.py`. It is derived from the R1/R3 type tables, the frame j = q − k, and c(m) = the fourth colour (p, y and z have distinct colours and are all adjacent to m).

| pos | (type,k) | j | x₀..x₄ | w₀..w₄ | c(m) | swap pair, anchor | hole vertices recoloured by the swap |
|---|---|---|---|---|---|---|---|
| 0 | R3k4 | 1 | 3 0 1 0 2 | 2 3 2 3 1 | 0 | {0,2} of x₃ | x₃ x⁻ w₂ |
| 1 | R1k1 | 4 | 3 0 1 2 0 | 2 3 0 3 1 | 0 | {0,1} of x⁺ | x⁺ x₂ w₂ |
| 2 | R3k3 | 2 | 3 1 0 2 0 | 2 3 1 3 1 | 0 | {0,3} of x⁻ | p x⁻ w₃ m |
| 3 | R1k0 | 0 | 0 1 0 2 3 | 2 3 1 0 1 | 3 | {0,2} of x₂ | x₂ x₃ w₃ |
| 4 | R3k2 | 3 | 0 1 2 0 3 | 2 3 1 2 1 | 3 | {0,1} of p | p x⁺ y |
| 5 | R1k4 | 1 | 1 0 2 0 3 | 2 3 1 2 0 | 3 | {0,3} of x₃ | x₃ x⁻ y m |
| 6 | R3k1 | 4 | 1 0 2 3 0 | 2 3 1 2 3 | 0 | {0,2} of x⁺ | x⁺ x₂ z m |
| 7 | R1k3 | 2 | 1 2 0 3 0 | 0 3 1 2 3 | 2 | {0,1} of x⁻ | p x⁻ z |
| 8 | R3k0 | 0 | 0 2 0 3 1 | 1 3 1 2 3 | 2 | {0,3} of x₂ | x₂ x₃ w⁺ |
| 9 | R1k2 | 3 | 0 2 3 0 1 | 1 0 1 2 3 | 2 | {0,2} of p | p x⁺ w⁺ m |

This is period b ≡ 0 (mod 3). Period b+1 is the same table with colours relabelled by 2→1, 3→2, 1→3.

The last column is consistent with Job O at every step: steps 0, 1, 3 and 8 avoid p, m, y and z; the other steps contain exactly the pair of `pair_own`.

### 1.2 Locks and J between fixed vertices [proved]

At every position, each lock end x_{j+i} is a link vertex of degree 5. Its only neighbour in the lock pair other than h and other link vertices is one ring vertex. So each lock is a join between two fixed ring vertices in G − h. This is `witness.py`, reducing through link vertices.

| pos | Lock1 ({μ,A}) | Lock2 ({μ,B}) | J ({c(y),c(z)}) |
|---|---|---|---|
| 0 R3k4 | w₂ ~ y | w⁺ ~ y | y ~ z |
| 1 R1k1 | y ~ w⁺ | **z ~ w₃** | y ~ z |
| 2 R3k3 | w₃ ~ z | **w₂ ~ z** (pair = J pair) | y ~ z |
| 3 R1k0 | **z ~ w₂** (pair = J pair) | w⁺ ~ y | y ~ z |
| 4 R3k2 | y ~ w⁺ | w₃ ~ w⁺ (pair {c(m),c(z)}) | forced (P1) |
| 5 R1k4 | w⁺ ~ w₃ | w₂ ~ z | forced |
| 6 R3k1 | z ~ w₂ | y ~ w₂ | forced |
| 7 R1k3 | w₂ ~ y | w₃ ~ w⁺ | forced |
| 8 R3k0 | w⁺ ~ w₃ | **z ~ w₃** (via the only edge x⁺–z) | forced |
| 9 R1k2 | w₃ ~ z | **y ~ w₂** (pair = J pair) | y ~ z |

Remarks:
- *R1k1.* x_{j+1} = p there, and p's only Lock2-coloured neighbour is z. So "z ∈ Lock2-component" at R1k1 is a ring identity, as the coordinator's QuarterRestore probe says. It carries no information about breaks.
- *R3k0.* Lock2 ⇔ z ⇝ x⁻ in G_{μB} − x⁺, since x⁺'s only {μ,B}-neighbour off h is z. [data: T2, 44,109/44,109 R3k0 DL states, orders 20–24, both orientations.]

## 2. Two proved lemmas at a break

### 2.1 Far-ness of the step-8 component [proved]

At R3k0 (j = q), Lock2 is a {μ,B}-chain Λ from x⁺ to x⁻. Together with h it closes into the curve h x⁺ Λ x⁻ h.
- In the rotation at h (p, x⁺, x₂, x₃, x⁻) this curve separates p from x₂ and x₃.
- The step-8 component K is the {α,A}-component of x₂. It is connected and has no colour in common with Λ, so it cannot reach p.
- y is A-coloured and adjacent to p (α). If y were in K, p would be too.
- m (μ) and z (B) are not in the pair.

Hence K ∌ p, m, y, z. ∎ [data F1: 44,109/44,109.] The same argument at the step-0, step-1 and step-3 anchors would give the other far swaps; I did not write those out.

### 2.2 Pocket lemma at R1k2 [⇐ proved; ⇒ proved mod (D)]

At R1k2 (position 9) the colours are c(p) = α, c(m) = A′, and J's pair {c(y), c(z)} is the complementary pair, which is also the Lock2 pair (QuarterLockJ). x⁺ and w⁺ carry c(m) and α (w⁺ ∈ K was recoloured by step 8).

**Claim.** J false ⇔ m ⇝ w⁺ in G_{c(p),c(m)} − {h, p, x⁺}.

*⇐.* A path Q from w⁺ to m closes into the cycle C = p x⁺ w⁺ Q m p.
- At p, C uses the edges to x⁺ and to m. These separate z (between x⁺ and m in p's rotation) from y and x⁻.
- No vertex of C has y's or z's colour, so no G_J-path joins z to y. ∎

*⇒.* By (D) there is a closed walk in G_{c(p),c(m)} ∪ {h} separating z from y. It must pass through p and m, and at p it uses m and one of h, x⁺ (p's only other neighbours in the pair).
- If it uses h, it leaves h through x⁺ or x₃.
- Through x₃, it would separate x₂ from x⁻. But Lock2 at R1k2 joins x⁻ to x₂ in the colour-disjoint graph G_J. So the walk leaves h through x⁺, and shortcutting along the edge p x⁺ gives a walk through m, p and x⁺.
- From x⁺ the only remaining exit in the pair is w⁺. ∎

[data T1: 39,093/39,093 DL R1k2 states (orders 20–24), and 19,132/19,132 in-run R3k4 states (orders 22–24).]

**Corollary (pocket survives step 9) [proved].** The step-9 swap is the {c(p),c(m)}-component Π_b of p, and Π_b contains every such curve C. So the whole curve is recoloured and stays a pocket at R3k4. This is P2 for J, seen as a set statement.

## 3. Window lemma [proved]

By the table, y and z keep their colours from position 9 of one period to position 4 of the next. Steps 9 and 2 are pm-swaps, and steps 0, 1 and 3 are far swaps. So the J pair is one colour pair throughout the window. Write G_J for its graph.

From §1.2, in that one graph:

| pos | forced by DL | J means |
|---|---|---|
| 9 R1k2 | y ~ w₂ (Lock2) | z joins {y, w₂} |
| 0 R3k4 | y ~ w₂ (Lock1, given z = A, i.e. the predecessor is R1k2) | z joins {y, w₂} |
| 2 R3k3 | z ~ w₂ (Lock2) | y joins {z, w₂} |
| 3 R1k0 | z ~ w₂ (Lock1) | y joins {z, w₂} |
| 4 R3k2 | y ~ w₂ ~ z (P1, local) | true |

So along a DL run, the partition of {y, w₂, z} by G_J-components is:
- {y w₂ | z} (break) or {y w₂ z} at positions 9 and 0;
- {y | w₂ z} (k = 3 failure) or {y w₂ z} at positions 2 and 3;
- {y w₂ z} at position 4.

[data `window.py`, orders 20–23, both orientations, all DL states at these positions: 0 exceptions. At order 23 alone: 6,260 states at position 9, 5,447 at 0, 5,447 at 2, 6,260 at 3, 7,369 at 4.]

Consequences:
- **The leaving mechanism of Job AA (36/73: last DL state R1k1, the step-1 (m,y) far swap kills Lock2) is exactly "z fails to re-join w₂ in G_J by position 2".** By the window lemma, Lock2 at R3k3 is z ~ w₂ in the J pair. So the commonest Lock2 death is the window lemma's position-2 constraint failing after a z-split.
- **A₃₄′ in window language.** In period b+1's window (pair J_{b+1}), z is split off at position 9. In period b's window (pair J_b, a different matching), z was also split off. On a Γ-cycle both splits must heal by position 2 of the following period, since both states are DL.
- Under the mirror (QuarterMirror: type preserved, k ↦ 2 − k, π ↦ π⁻¹) the window maps to itself:
  - positions 9, 0 ↔ positions 3, 2;
  - "z split off" ↔ "y split off";
  - a step-8 break ↔ a step-3 restoration.

  So any invariant must be symmetric under (y, positions 2–3) ↔ (z, positions 9–0). The Σ below is chosen with that in mind.

## 4. What does not work

**(a) [killed] K′ ∩ Lock2 witness at R3k0^{b+1}.**
- At R3k0 the step-8 pair is {α, A} and Lock2 is {μ, B}. They are disjoint, so the vertex sets are disjoint at that state.
- So the coordinator's "y–z paths through the ring near m force K′ ∩ (Lock2 witness) ≠ ∅" can never be proved at a single state. It would have to compare K′ with a witness at another state, i.e. with a fixed vertex set from another time.

**(b) [killed] Crossing at R3k0^{b+1}.**
- After the second break there is a pocket C₂ = p x⁺ w⁺ Q′ m p in the {α, μ}-graph of c₉^{b+1} around z (§2.2).
- The Lock2 chain of R3k0^{b+1} is z ⇝ w₃ in {μ,B} (unchanged by K′). It must leave the region bounded by C₂.
- It can: z–m is an edge with colours (B, μ), and m ∈ C₂ is μ. So the chain leaves through m, which is shared colour μ, and there is no contradiction.
- This is also where degree 6 differs from degree 7. At degree 6 the edge z–m is always a Lock2 edge at R3k0 (c(m) = μ is forced as the fourth colour). At degree 7 the vertex M′ next to z can be A.
- So at degree 6 the single-state picture is *more* permissive, and the obstruction must be dynamic.

**(c) [killed as evidence] "Meets" statistics.**
- K always contains x_{q+2}, x_{q+3} and w⁺ (table, step 8). So K ∩ K′ ⊇ {x₂, x₃, w⁺} in every period.
- w⁺ ∈ Π_b, and the Lock components contain fixed ring vertices.
- [data, `far.py`] On all 15 local continuations (orders 22–24), the "far" parts (minus the 11 hole vertices) are tiny: |Z_b \ hole| ≤ 3. Single and double breaks are not separated by any far intersection: K′_far ∩ Z_b is 1, 1, 1, 0 on the four double breaks and 1–2 on the singles.
- Studio "meets" counts (AE: Lock2 meets K at every state) should be redone with hole vertices removed before they are used as evidence.

**(d) [data] Local supply.**
- Gentri orders 20–24, both orientations: 8,778 step-8 breaks in DL runs.
- Only 15 runs survive to the next step 8. 4 of these break again (24 #3131, #3175, #3611, and #5340 mirrored; 1-based numbering). Only #3611 reaches the failing R3k4 as a DL state.
- So the order-24 example (§7, `ex-24-3611-h0.txt`) is the only local double failure, as in NightLemmaS §5.1. There, the leaving step is step 3 (R1k0 → R3k2, pair (p,z), far). It kills Lock2 of R3k2, which is w₃ ~ w⁺ in {c(m), c(z)}.

## 5. The isolated sub-statement [conjecture]

Fix a break at step 8 of period b. Let Z_b be the G_{J_b}-component of z at R1k2^b. This is a fixed vertex set: z ∈ Z_b, and y, w₂ ∉ Z_b.

By the window lemma, DL at R3k3^{b+1} forces z to re-join w₂ in G_{J_b} by steps 9, 0 and 1. The re-join must recolour a vertex on the boundary of Z_b. Let R_b ⊂ (K₀ ∪ K₁) be the vertices recoloured by the step-0 and step-1 far swaps of period b+1 that are adjacent to Z_b (the "gate" of the healing).

**Σ (one-swap statement).** On a DL run at a Hole6, if steps 8 of periods b and b+1 both break, then the step-0 or step-1 far swap of period b+2 recolours a vertex of R_b ∪ Z_b. That swap's component meets the gate of the first healing, and the swap that heals the second split must reopen the first.

Under the window lemma, Σ would close A₃₄′ on Γ-cycles as follows:
- reopening the first gate splits z from w₂ in G_{J_b} at a state of period b+2 whose Lock2 pair is J_b's pair. By the period-3 rotation of pairs, by the relabelling 2→3, 3→1, 1→2 of period b+2, the J_b pair is the Lock2 pair at positions 1, 4 and 7 of period b+2. So it is the Lock2 pair at R1k1^{b+2}, the state right after step 0 (Lock2 z ~ w₃), and at R3k2^{b+2} (w₃ ~ w⁺);
- one of those states is then not DL.

The last implication is **not proved**. It needs "a reopened gate separates z from w₃, not only from w₂". That is the one planar step left, and it is where a crossing argument with the ring cycle z w⁺ w₂ w₃ y m (one inserted vertex) would enter.

Σ is consistent with Job AA's union rule (73/73: the second break's component meets the last Lock2 witness or the killing component). But it is sharper: it names the swap (step 0 or 1 of period b+2) and a fixed vertex set (R_b ∪ Z_b) with hole vertices removed. **It is untested.**

## 6. Studio test (minimum deliverable)

For all (5,5,5,5,6) Γ-cycles (orders 25–27, both orientations) and for the 73 open double breaks of Job X/AA:
1. For each step-8 break at period b, record:
   - Z_b, the G_J-component of z at R1k2^b, as a vertex set;
   - Π_b, the step-9 component;
   - K₀^{b+1} and K₁^{b+1}, the step-0 and step-1 components;
   - R_b, the vertices of K₀^{b+1} ∪ K₁^{b+1} adjacent to Z_b;
   - all sets also with the 11 hole vertices removed ("far").
2. Window lemma check: at each DL state at positions 9, 0, 2 and 3, the partition of {y, w₂, z} in G_J. It is predicted to match §3 with 0 exceptions.
3. Σ: on the double breaks, does K₀^{b+2} ∪ K₁^{b+2} meet (R_b ∪ Z_b)_far? On Γ-cycles at degree 6 (single breaks only), report the same quantity for the period after a single break. Σ predicts it is mostly empty there, and non-empty in 73/73 double breaks.
   - If Σ holds on the double breaks but also holds often on the single breaks, Σ is true but useless. Report both rates.
4. At (5,5,5,5,7) (14 consecutive-break periods on Γ-cycles), the same quantities. Σ must **fail** at degree 7 where those cycles stay DL. If it holds there too, the "reopened gate kills Lock2" step is false at degree 7, and the degree must enter through the gate geometry (the edge z–m in §4(b)).

## 7. Reproduction

All in `backgroundMaterial/planemap-structural/longtable/local-runs/30-nighta34/`. Gentri lists, `kempe_py.Space` for enumeration, actual-colour π re-implemented in `eng.py` (it matches `escape.pi_of`; it reproduces the NightLemmaS 24 #3611 h0 trace exactly). One core, AC power.

| script | content | time |
|---|---|---|
| `table.py` | §1.1 symbolic period table | < 1 s |
| `witness.py` → `witness-table.txt` | §1.2 lock reductions | < 1 s |
| `scan.py 22,23` / `scan.py 24` → `s2223.jsonl`, `s24.jsonl`, `log*.txt` | T1, T2, F1 and break continuations | 2 min / 8 min |
| `window.py 20,21,22` and `23` | §3 window lemma | 1 / 3 min |
| `ex.py 24 3610 0 0` → `ex-24-3611-h0.txt` | full trace of the order-24 double failure (0-based 3610 = #3611) | < 1 s |
| `far.py` | §4(c) far intersections | 30 s |
