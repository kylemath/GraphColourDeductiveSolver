# Night: W2 — some k ≤ 2 exit is lockless in every period at (5,5,5,5,6)

Night worker, 7 October 2026 (written 03:34 MDT). **Exploratory. Hand bookkeeping plus single-core reads of Studio files (Jobs M, Q, AG). Unreviewed.** MacBook on AC (pmset: AC power, 100%).

Builds on `NightF012.md` (Lemma Fix, roles at k ≤ 2, Lemma W = W1 + W2 + W4), `QuarterGammaPeriod.lean` (`pair_own`, `gseq`), `QuarterSigmaFix.lean` (`lemmaFix`, `low_path_k*`), `QuarterRotation.lean` (`rot3`: π at a DL state swaps the {α,A}-component of x_{j+2}). k = 3, 4 (W1/A₃₄′) are out of scope here.

Labels: [proved] by hand; [data] read by the scripts in §6; [conjecture]; [killed].

## Verdict

1. **[proved] Absolute bookkeeping of positions 4 → 8 (§1).** With p, m, y, z fixed by the hole and colours named at R3k2 as p = 1, m = 2, y = 3, z = 4, the four π-steps 4, 5, 6, 7 are Kempe swaps of pairs {1,3}, {1,2}, {1,4}, {1,3}, and the three fixed-point questions are:
   - F₄ (R3k2): the {3,4}-graph of T − v is acyclic ⇔ the {1,2}-graph is connected;
   - F₆ (R3k1): the {2,4}-graph is acyclic ⇔ the {1,3}-graph is connected;
   - F₈ (R3k0): the {2,3}-graph is acyclic ⇔ the {1,4}-graph is connected.
2. **[proved] No local forcing.** At each of the three states the {A,B}-graph induced on the 11-vertex 2-ball (link, ring, m) is exactly the 6-vertex path P of `low_path_k*`, a tree. So the ring can never supply the cycle; every cycle that prevents a fixed point is global. This matches Studio Job AG (1,656/1,656 states ring- and 2-ball-acyclic). The coordinator's "A/B cycle through the ring" route is dead at degree 6.
3. **[data, new, sharp] W2 is a two-state statement: W2\*.** R3k2 and R3k0 of the same period **never both fail** (fixed point or single-lock). 0 of 140 periods (orders 25–26), 0 of 412 (order 27). All failure pairs are (k2,k1) or (k1,k0). In Job AG's cycle ranks: rank(k2) + rank(k0) ≥ 1 in all 552 periods, with equality in 66.
   - W2\* ⇒ W2 (fixed-point part and single-lock part together).
   - W2\* is specific to the 4-step gap inside the period. Across the period boundary (R3k0 then the next R3k2, 6 steps), both are fixed in 10 of 412 order-27 pairs (both rank 0 in 10 of 552 in Job AG).
   - W2\* is specific to degree 6. At (5,5,5,5,7), Job AF34 has periods with k2, k1, k0 all fixed.
4. **[proved] Lock chains live in the other states' forest pairs (§2).** The pair whose acyclicity is F₄ ({3,4}) carries Lock1 at R3k1 and Lock2 at R3k0. Likewise {2,4} (F₆) carries Lock2@R3k2 and Lock1@R3k0, and {2,3} (F₈) carries Lock1@R3k2 and Lock2@R3k1. So under DL each forest pair contains, at the other two states, long two-coloured link-to-link chains. This is the natural input for a proof. I do **not** have the contradiction.
5. **[data] Task (3), single-lock exits.** They do coincide with a failure at another k ≤ 2:
   - orders 25–26: (S,X,L) ×1 and (L,X,S) ×1;
   - order 27: (S,S,L) ×8 and (L,S,S) ×8.

   But never with failures at both other k, and never at k2 and k0 together (W2\*). "All three k ≤ 2 exits fail" is observed 0 times (0/140, 0/412).
6. **[data, Job AH] The mechanism of W2\* is a create–kill–recreate pattern of {2,3}-cycles (§7).** Assume F₄. Then:
   - the (p,y)-swap K₄ always creates a {2,3}-cycle (60/60), i.e. R1k4 is never a fixed point after a fixed R3k2;
   - the (m,y)-swap K₅ kills every such cycle in 48/60 cases;
   - the (p,z)-swap K₇ then **always** recreates one (48/48).

   K₆ cannot touch the {2,3}-graph. Under time reversal the same holds for F₈ and the {3,4}-graph. So the sharp target is:

   **W2\*\* (two one-step statements).**
   - (a) F₄ ⇒ a {2,3}-cycle exists after K₄.
   - (b) F₄ and the {2,3}-graph is acyclic after K₅ ⇒ K₇ creates a {2,3}-cycle.

   Together (a) and (b) give W2\*, using that K₆ preserves {2,3}.
7. **W4: not attempted** (time). The data status is unchanged from NightF012 (0 failures in 19 cases).

**Status:**
- W2 is reduced to W2\*, which concerns two states four Kempe steps apart, with exact colour bookkeeping.
- W2\* is reduced to the two one-step statements of W2\*\* (0 exceptions, 60 + 48 cases).
- Not proved.

## 1. Bookkeeping [proved]

Take q = 2 (p = x₂), so y = w₁, z = w₂. Ring edges are w_t w_{t+1}, except that y – m – z replaces w₁w₂. The spokes are x_t w_t and x_{t+1} w_t.

The colourings at the R3 states follow from `R3At` with `j = q − k`. At R3k2 (j = 0), let α = 1, μ = 2, A = 3, B = 4. Each step is π = R₊₃, which swaps the {α,A}-component of x_{j+2}. The component contents are from Job O / `pair_own`.

| pos | state | j | link x₀..x₄ | ring w₀..w₄ | m | (p, m, y, z) | step: pair, component ∋ |
|---|---|---|---|---|---|---|---|
| 4 | R3k2 | 0 | 1 2 1 3 4 | 4 3 4 2 3 | 2 | 1 2 3 4 | K₄: {1,3} of x₂ = p; ∋ p, y, x₃ |
| 5 | R1k4 | 3 | 1 2 3 1 4 | — | 2 | 3 2 1 4 | K₅: {1,2} of x₀; ∋ x₀, x₁, m, y |
| 6 | R3k1 | 1 | 2 1 3 1 4 | 4 2 4 2 3 | 1 | 3 1 2 4 | K₆: {1,4} of x₃; ∋ x₃, x₄, m, z |
| 7 | R1k3 | 4 | 2 1 3 4 1 | — | 4 | 3 4 2 1 | K₇: {1,3} of x₁; ∋ x₁, x₂ = p, z |
| 8 | R3k0 | 2 | 2 3 1 4 1 | 4 2 3 2 3 | 4 | 1 4 2 3 | — |

(The R1 ring columns are omitted; only the R3 rings are needed.) Each row was checked against `R3At` and `pair_own`, and it reproduces NightF012 §1.4.

**Fixed-point questions.** At R3@k ≤ 2 the {α,μ} link vertices are x_j, x_{j+1}, x_{j+2}, which form a contiguous arc. So Lemma Fix plus duality gives "fixed ⇔ {A,B} acyclic ⇔ {α,μ} connected". This yields F₄, F₆ and F₈ as in Verdict 1.

**Which steps change which pair-graph.** A {a,b}-swap preserves the {a,b}-graph and the complementary graph, and changes the other four.

| pair (and complement) | K₄ {1,3} | K₅ {1,2} | K₆ {1,4} | K₇ {1,3} |
|---|---|---|---|---|
| {3,4} / {1,2} (F₄) | changes | — | changes | changes |
| {2,4} / {1,3} (F₆) | — | changes | changes | — |
| {2,3} / {1,4} (F₈) | changes | changes | — | changes |

So:
- the {2,3}-graph at R3k0 is the {2,3}-graph at R3k2, rewritten on K₄, K₅ and K₇;
- the {3,4}-graph at R3k0 is the {3,4}-graph at R3k2, rewritten on K₄, K₆ and K₇.

p's colour goes 1 → 3 (K₄) → 3 → 3 → 1 (K₇): p is swapped out and back by the two {1,3}-steps.

The full colour change of the 2-ball from R3k2 to R3k0 is:

| vertex | x₀ | x₁ | x₂ = p | x₃ | x₄ | w₀ | w₁ = y | w₂ = z | w₃ | w₄ | m |
|---|---|---|---|---|---|---|---|---|---|---|---|
| change | 1→2 | 2→3 | 1 | 3→4 | 4→1 | 4 | 3→2 | 4→3 | 2 | 3 | 2→4 |

**Local graphs [proved].** Listing the 2-ball edges with both ends in {A,B} gives:
- pos 4, {3,4}: x₃x₄, x₃w₂, x₄w₄, w₄w₀, w₀w₁, i.e. the path y w₀ w₄ x₄ x₃ z;
- pos 6, {2,4}: x₄x₀, x₄w₃, x₀w₀, w₀w₁, w₂w₃, i.e. the path y w₀ x₀ x₄ w₃ z;
- pos 8, {2,3}: x₀x₁, x₀w₄, x₁w₁, w₂w₃, w₃w₄, i.e. the path y x₁ x₀ w₄ w₃ z.

m is coloured μ or α at all three states, so it is never in {A,B}. Hence the 2-ball {A,B}-graph is a 6-vertex path, with no cycle, at every k ≤ 2 state. This is why degree 6 differs from degree 7: there, Job AG sees ring cycles in 440/916-type states, yet fixed points still occur, so the ring is not the mechanism at either degree.

## 2. Lock chains and forest pairs [proved]

At R3 with frame (α, μ, A, B):
- Lock1 is a {μ,A}-chain from x_{j+1} to x_{j+3};
- Lock2 is a {μ,B}-chain from x_{j+1} to x_{j+4}.

From the table:

| state | Lock1 pair, ends | Lock2 pair, ends | own forest pair |
|---|---|---|---|
| R3k2 (pos 4) | {2,3}: x₁ → x₃ | {2,4}: x₁ → x₄ | {3,4} |
| R3k1 (pos 6) | {3,4}: x₂ → x₄ | {2,3}: x₂ → x₀ | {2,4} |
| R3k0 (pos 8) | {2,4}: x₃ → x₀ | {3,4}: x₃ → x₁ | {2,3} |

The three pairs avoiding colour 1 (p's colour at R3k2 and R3k0) are each:
- the forest pair at one state;
- a lock pair at the other two.

Suggested route to W2\* (not completed). Assume F₄ and F₈.
- Take the {3,4} Lock2-chain Λ₈ from x₃ to x₁ at R3k0, and pull it back to R3k2 through K₇, K₆ and K₄.
- The {3,4}-graph is unchanged by K₅. At R3k2 the end x₁ has colour 2, so Λ₈ must be cut by the rewrites: x₁ ∈ K₅ ∩ K₇.
- The hope is that the pieces of Λ₈, together with P₄ and F₄'s forest structure (equivalently the {1,2}-graph at R3k2 being connected), force a {2,3}-cycle at R3k0. Symmetrically, use Lock1@R3k2 ({2,3}, x₁ → x₃) pushed forward through K₄, K₅ and K₇.

I could not close either argument by hand.

## 3. Data [data]

`nightw2/w2.py` reads jobm labels. L = lockless, X = fixed point, S = single-lock. The tuples are the per-period patterns (k2, k1, k0).

| pattern | 25–26 | 27 |
|---|---|---|
| L L L | 86 | 296 |
| X X L / L X X | 14 / 14 | 24 / 24 |
| X L L / L L X | 5 / 5 | 17 / 17 |
| L X L | 10 | 12 |
| L S L | 4 | — |
| S X L / L X S | 1 / 1 | — |
| S S L / L S S | — | 8 / 8 |
| S L L / L L S | — | 3 / 3 |
| **k2 and k0 both non-L** | **0** | **0** |
| all three non-L (W2 failure) | 0 | 0 |

- Across the period boundary, the pairs (k0, next k2) include (X,X) ×10 and (S,S) ×2 at order 27.
- The patterns are exactly mirror-symmetric, (a,b,c) ↔ (c,b,a): k2 ↔ k0 under orientation reversal.

`nightw2/w2rank.py` reads Job AG global {A,B} cycle ranks (552 periods, degree 6):
- min rank(k2) + rank(k0) = 1, attained in 66 periods: (0,0,1) ×33 and (1,0,0) ×33;
- rank(k0) + rank(next k2) = 0 in 10 periods.

## 4. Status

| item | status |
|---|---|
| Bookkeeping §1 (pairs, components, F₄/F₆/F₈ in absolute colours, change table) | [proved] (from `R3At`, `pair_own`, Job O contents) |
| 2-ball {A,B}-graph = path P at k ≤ 2 (no local cycle) | [proved]; Job AG 1,656/1,656 |
| Lock pairs = forest pairs of the other states (§2) | [proved] |
| **W2\***: R3k2 and R3k0 of one period never both fail | [conjecture], 0/140, 0/412; rank sum ≥ 1 in 552/552 |
| W2\* ⇒ W2 | [proved] (trivial) |
| W2\* over the 6-step gap (k0, next k2) | [killed] (10 × both fixed at 27) |
| "all three k ≤ 2 fail" | 0 observed; single-lock exits do pair with one other failure (2 + 16 cases) |
| Ring/2-ball A/B cycle route | [killed] at degree 6 (no local cycle exists) |
| W4 | not attempted |

## 5. Studio requests (exact tests)

1. **W2\* on runs.** On every maximal DL run at (5,5,5,5,6) holes (orders 25–27, both orientations), at every R3k2 state whose next four π-steps stay DL, test "R3k2 fixed ⇒ R3k0 not fixed" and the rank sum ≥ 1.
   - If it holds on runs, W2\* is a 4-step Kempe statement independent of Γ-closure, and a hand proof is plausible.
   - If not, record the first counterexample (rotation system and the five colourings).
2. **Where the cycle comes from.** At every period with rank(k2) = 0, take a {2,3}-cycle at R3k0 and report which of K₄, K₅, K₇ (recoloured vertices) it meets. Also report whether it meets the pulled-back Lock1@R3k2 chain ({2,3}, x₁ → x₃).

   Hypothesis H: every {2,3}-cycle at R3k0 meets K₇ ∖ K₄, i.e. it is created by the last (p,z) step, which returns p to colour 1. Report the mirror statement too.
3. ~~Intermediate ranks~~: answered from Job AH (§7). α = colour 1 at every state of positions 4–8, so the frame ranks AB, μA and μB give all three non-1 pairs at every intermediate state.
5. **For W2\*\*(a) and (b), the coordinator's question.** At the 60 F₄ periods, output one {2,3}-cycle C₅ after K₄, together with:
   - whether C₅ passes through p (now colour 3) or y's neighbourhood;
   - |C₅ ∩ K₄| (the old 1-vertices now coloured 3);
   - whether C₅ separates h from some vertex of K₄.

   In the 48 kill cases, also output C₈ and |C₈ ∩ K₇|. Lemma Fix's direction ⇐ suggests looking at C₅ as the boundary of the {1,4}-component that K₄ cut off.

   The coordinator asked whether the A/B cycle at position 4 always passes through y or z. That cannot be read from AG/AH, which record ranks and not cycles. Note that in the F₄ case the position-4 {3,4}-graph has no cycle at all, so the relevant cycles are the {2,3}-cycles C₅ and C₈ above.
4. **Dump the 66 rank-sum-1 periods** (rotation system plus colourings at positions 4–8) as hand-check witnesses.

## 7. Job AH traces [data]

Script: `nightw2/w2trace.py`, output in `outtrace.txt`. The rows are the ranks of the three pair-graphs avoiding colour 1 at positions 4–8, over 552 degree-6 periods (orders 25–27, both orientations). Colour 1 = α at every one of these states. The frame pairs by position are:

| pos | (μ, A, B) |
|---|---|
| 4 | (2,3,4) |
| 5 | (4,2,3) |
| 6 | (3,4,2) |
| 7 | (2,3,4) |
| 8 | (4,2,3) |

**Checks of §1.**
- Lemma Fix: fixed ⇔ own-pair rank 0 at positions 4, 6 and 8 in 552/552 periods.
- The change table's invariances hold in 552/552: r₃₄(5) = r₃₄(6), r₂₄(4) = r₂₄(5), r₂₃(6) = r₂₃(7) and r₂₄(7) = r₂₄(8).

**W2\*:** r₃₄(4) + r₂₃(8) ≥ 1 in 552/552 periods.

**F₄ (r₃₄(4) = 0), 60 periods:**
- r₂₃(5) ≥ 1 in 60/60, so K₄ creates a {2,3}-cycle. When F₄ fails, r₂₃(5) = 0 is possible (16 periods).
- r₂₃(6) = 0 in 48/60, so K₅ kills it, and then r₂₃(8) ≥ 1 in 48/48, so K₇ recreates it.
- In the other 12/60 the cycle survives K₅ and K₇.

**F₈, 60 periods:** the mirror image of F₄.
- r₃₄(7) ≥ 1 in 60/60.
- r₃₄(6) = 0 in 48/60, and then r₃₄(4) ≥ 1.

**Position 6:** all three non-1 pairs are acyclic at once in 86 periods. So the middle state alone is no obstruction, and K₄/K₇, the two {1,3}-swaps through p, carry the forcing.

## 8. W2′: a cycle through y or z, i.e. a K_σ-escape at y or z (written 03:38 MDT, after Job AI)

Job AI (`jobuv/jobai-summary.txt`) found that in 552/552 periods some {A,B}-cycle at position 4, 6 or 8 passes through y or z. All cycles hug v, with 4–5 vertices on v's side. Every fixed point is made by **one** swap:
- step 5 kills the last {A,B}-cycle before R3k1 (99/100 cases);
- step 7 kills the last one before R3k0 (60/60 cases);
- the killed cycle is short and avoids y and z.

### 8.1 Fan lemma [proved; direction ⇐ uses the boundary-parity argument of Lemma Fix]

Setting:
- R3@k, k ≤ 2, frame (α, μ, A, B);
- u ≠ h is a vertex coloured A or B;
- K_σ is the {α,μ}-component of x_{j+1}; it contains the contiguous link arc x_j, x_{j+1}, x_{j+2} (`low_roles`).

Then:

  **u lies on an {A,B}-cycle of T − h ⇔ some {α,μ}-neighbour of u lies outside K_σ.**

*Proof.*
- (⇒) This is the argument of `acyclic_of_sigmaFixed`, applied at u itself.
  - Let C pass through u with edges u b₁ and u b₂.
  - The two rotation arcs of u between b₁ and b₂ each contain an {α,μ}-neighbour, because consecutive neighbours are adjacent and coloured off u's colour.
  - The Jordan lemma (`alternating_walks_intersect`) separates these two neighbours by C, so they lie in different {α,μ}-components.
  - At most one of them is in K_σ.
- (⇐) Let v₀ be an {α,μ}-neighbour of u outside K_σ, and let S be its {α,μ}-component.
  - S contains no link vertex: the link's α/μ vertices form one arc inside K_σ.
  - So the face-boundary graph of S (`bdGraph`, as in `not_acyclic_of_not_sigmaFixed`) avoids h and consists of {A,B}-edges, with even degrees.
  - Going around u, the faces u v₀ · meet S. Some face at u misses S, namely one at the K_σ-neighbour of u where u has one; see the next paragraph for why one exists.
  - So u has positive even degree in that graph, and u lies on a cycle of it. ∎

Why u has a K_σ-neighbour:
- at R3@k ≤ 2, both y and z are adjacent to p and m, which lie in K_σ;
- so for u ∈ {y, z} both kinds of face occur whenever a neighbour outside K_σ exists.

### 8.2 W2′, Lean-ready, and W2′ ⇒ W2 (fixed-point part) [proved, trivial]

Setting: on an all-DL π-orbit at a `Hole6 P w m q`, with s n = π^[n] s, j_n the repeat index, y = w (q+4) and z = w q. The statement:

```
W2' : ∀ b, ∃ n ∈ {10b+14, 10b+16, 10b+18}, ∃ u ∈ {y, z}, ∃ v,
        M.graph.Adj u v ∧ Active h (s n) α_n μ_n v ∧
        ¬ (pairGraph M.graph h (s n) α_n μ_n).Reachable (P.x (j_n + 1)) v
```

Here α_n = s n (x j_n) and μ_n = s n (x (j_n+1)). The indices 10b+14, 10b+16, 10b+18 are the positions 4, 6, 8 of a period, since `gamma_period_ten` starts at R3k4 = position 0.

The conclusion is literally ¬ `SigmaFixed` at that state. **No Lemma Fix and no duality is needed for W2′ ⇒ "not all three fixed".** By the fan lemma, W2′ is equivalent to Job AI's statement, that some {A,B}-cycle at position 4, 6 or 8 passes through y or z.

### 8.3 Where the escape can be: explicit vertex names [proved]

These use the §1 colourings, with q = 2, p = x₂, y = w₁ and z = w₂. The {α,μ}-neighbours of y and z inside the 2-ball are:

| state | {α,μ} | y's ball {α,μ}-nbrs | z's ball {α,μ}-nbrs | in K_σ for sure | **ring candidate** |
|---|---|---|---|---|---|
| pos 4, R3k2 | {1,2} | x₁, p, m | m, p, **w₃** (2) | x₁, p, m | **w₃** (via z) |
| pos 6, R3k1 | {1,3} | x₁, p, m | m, p, x₃ | all | none |
| pos 8, R3k0 | {1,4} | **w₀** (4), x₂ = p, m | m, p, x₃ | p, m, x₃ | **w₀** (via y) |

(m, x₁ and x₃ are in K_σ via the arc and the edges p m, p x_{q±1}.) So W2′ says that at least one of the following holds:
- (i) at R3k2, w₃ ∉ K_σ, i.e. w₃ (colour μ = 2) is not {1,2}-joined to the link arc;
- (ii) at R3k0, w₀ ∉ K_σ, i.e. w₀ (colour μ = 4) is not {1,4}-joined to the link arc;
- (iii) some outer neighbour of y or z (outside the 2-ball) escapes K_σ at one of the three states.

(i) and (ii) are mirror images under time reversal; the mirror orientation reads the cycle backwards, and k2 ↔ k0. In either case the escaping vertex is the ring vertex across w₄ from the y–z side, and the cycle given by the fan lemma passes through z (in i) or y (in ii). This matches Job AI's most common ring sets, which contain w₃w₄ or w₀w₄.

### 8.4 What is still missing [conjecture], and the exact Studio test

I have no hand argument that (i), (ii) or (iii) occurs. The proposed mechanism goes through the Lock chains of §2:
- Lock2@R3k2 is the {2,4}-chain x₁ → x₄. It runs through w₃'s side of the ring, since w₃ (2) is adjacent to x₄ (4).
- Lock1@R3k0 is the {2,4}-chain x₃ → x₀, adjacent to w₀.
- "Both (i) and (ii) fail" would mean that w₃ is {1,2}-attached to the arc at R3k2 and w₀ is {1,4}-attached at R3k0. With the lock chains in the complementary pairs, the hope is that the four swaps K₄–K₇ cannot realise both attachments. I could not close this.

Studio test (cheap, ranks not needed). At each of the 552 periods, record:
1. the booleans E(pos, u) = "u has an {α,μ}-neighbour outside K_σ", for u ∈ {y, z} and pos ∈ {4, 6, 8}; W2′ says their OR is 1;
2. whether the escape is the ring candidate (w₃ at position 4, w₀ at position 8) or an outer neighbour;
3. the minimal sufficient sub-statement. Is (i) ∨ (ii) alone always true? If yes, W2′ reduces to two named ring vertices and two states, which is the Lean-sized target.
4. also on all maximal DL runs, as in §5.1, to see whether Γ-closure is needed.

## 9. Job AI cycle bases: W2\*\*, Hypothesis H, and the two-state W2′ [data]

Script: `nightw2/w2ai.py`, output in `outai.txt`. It reads `jobuv/jobai.json`, 552 degree-6 periods. The cycles at position 5 are {2,3}-cycles and those at position 7 are {3,4}-cycles (§1 colours).

`jobai.json` stores only |K| for each step, not K's vertex set. So "|C₅ ∩ K₄|" and "C₈ created by K₇ ∖ K₄" **cannot be read**. They go to Job AK as §5.2 and §5.5.

### Findings

**W2\*\*(a), F₄ ⇒ a {2,3}-cycle at position 5: 60/60.** But the word "created" is wrong in 19/60 periods: the position-4 {2,3}-rank is already ≥ 1 there (§7 traces: r₂₃(4) = 0 in 41/60). The correct statement is "rank ≥ 1 after K₄", not "K₄ creates a cycle".

**The position-5 cycles under F₄ are far.**
- 72 cycles in total, of lengths 6 / 8 / 10 = 63 / 8 / 1.
- **None passes through p, y or z.** Two pass through m.
- So the cycle-through-p version of the hypothesis is **[killed]**. The cycle that K₄ leaves or creates is a short far cycle. Its ring vertices are two consecutive w's (Job AI).

**The kill case, F₄ with r₂₃(6) = 0, 47 C₈ cycles in 45 periods:**
- C₈ passes through y and/or z in 40/47 (y and z: 36, y only: 2, z only: 2);
- it passes through neither in 5/47 (in those periods another position-8 cycle, or none of y/z, see below);
- it never passes through p;
- |C₈ ∩ ⋃C₅| = 2–5 in 43/47 and 0 in 2/47.

So C₈ is generally **not** the old C₅ restored: it is a new cycle, mostly through y and z, that reuses 2–3 vertices of C₅.

**F₈ (mirror): {3,4}-rank ≥ 1 at position 7 in 60/60.** Again no cycle through p, y or z.

**Sharpest form of W2′, [data, new] — two states, not three.** At R3k2 or at R3k0 there is an {A,B}-cycle through y or z: **552/552**. The (pos4, pos6, pos8) through-y/z patterns are:

| pattern | periods |
|---|---|
| TTT | 390 |
| TFT | 32 |
| TTF | 24 |
| FTT | 24 |
| TFF | 41 |
| FFT | 41 |

Position 6 is never needed. In particular F₄ ⇒ at R3k0 an {A,B}-cycle through y or z, and mirror-wise F₈ ⇒ the same at R3k2. This combines W2\* (§3) and Job AI's y/z statement, and it is the Lean target I propose:

```
W2'' : ∀ b, ∃ n ∈ {10b+14, 10b+18}, ∃ u ∈ {y, z}, ∃ v, M.graph.Adj u v ∧
        Active h (s n) α_n μ_n v ∧ ¬ (pairGraph M.graph h (s n) α_n μ_n).Reachable (P.x (j_n + 1)) v
```

(the K_σ-escape form, ⇔ a cycle through u by the fan lemma §8.1). Its local candidates (§8.3) are:
- w₃ at R3k2, through z;
- w₀ at R3k0, through y;
- an outer neighbour of y or z.

### Hand attempt at (a) [not proved]

Assume F₄, i.e. the {1,2}-graph at R3k2 is connected (= K_σ). K₄ is the {1,3}-component of p.

Plan: show that the {1,4}-graph at position 5 is disconnected. The position-5 link is 1 2 3 1 4, whose {1,4}-vertices x₃, x₄, x₀ form a contiguous arc. So by the Lemma Fix duality this is equivalent to a {2,3}-cycle at position 5.

The {1,4}-graph at position 5 consists of:
- the 4-vertices;
- the 1-vertices outside K₄;
- the old 3-vertices of K₄.

The data rule out the natural local witness: no position-5 cycle meets p, y or z. So the disconnected {1,4}-piece is a small far component cut off by K₄. Its boundary is the 6-cycle on two consecutive w's (Job AI).

I could not derive it from F₄ and the lock chains. The missing ingredient is how K₄ (size 4–10) sits against the Lock1@R3k2 {2,3}-chain x₁ → x₃ (§2), which passes next to K₄ at x₃. Job AK §5.2 / §5.5 (K₄'s vertex list against C₅) is needed before the next attempt.

## 10. W2″ in fan form: the two ring candidates [proved parts; conjecture]

Colours are those of §1, named at R3k2: α = 1, μ = 2, A = 3, B = 4; q = 2, p = x₂, y = w₁, z = w₂.

| | R3k2 (pos 4) | R3k0 (pos 8) |
|---|---|---|
| α/μ pair | {1,2} | {1,4} (α = 1 at x₂ = p, μ = 4 at x₃) |
| K_σ | {1,2}-component of x₁ | {1,4}-component of x₃ |
| K_σ contains | x₀, x₁, p, m | x₂ = p, x₃, x₄, m (m = 4) |
| ring candidate | w₃ (colour 2), escape through z | w₀ (colour 4), escape through y |

**W2″ fails** iff, at both R3k2 and R3k0, every α/μ-neighbour of y and of z lies in K_σ of that state. In particular:
- **(F-i)** w₃ ∈ K_σ(4);
- **(F-ii)** w₀ ∈ K_σ(8).

### 10.1 The candidates are never recoloured [proved]

w₃ is coloured 2 and w₀ is coloured 4, both at pos 4 and at pos 8 (from `R3At` at both states, §1 table). The four swaps are K₄ {1,3}, K₅ {1,2}, K₆ {1,4}, K₇ {1,3}.

- **w₃:** if w₃ ∈ K₅, it becomes 1. After that only K₆ and K₇ act, and they swap {1,4} and {1,3}, so w₃ could never return to 2. Hence **w₃ ∉ K₅**. K₄, K₆ and K₇ do not involve colour 2, so w₃ is coloured 2 at every one of positions 4–8.
- **w₀:** if w₀ ∈ K₆, it becomes 1. Then K₇ can only make it 3, never 4 again. Hence **w₀ ∉ K₆**. K₄, K₅ and K₇ do not involve 4, so w₀ is coloured 4 throughout.

### 10.2 What (F-i) and (F-ii) force on the swaps [proved]

- **(F-i) ⇒ K₄ cuts every {1,2}-path from x₁ to w₃.**
  - K₅ is the {1,2}-component of x₀ at pos 5, and it contains x₁ (Job O / `pair_own`: x₀, x₁, m, y ∈ K₅). Since w₃ ∉ K₅, there is no {1,2}-path x₁ → w₃ at pos 5.
  - The {1,2}-graph at pos 5 is the pos-4 graph with K₄'s 1-vertices removed (they become 3) and K₄'s 3-vertices added.
  - Adding vertices cannot destroy a path. So if a {1,2}-path x₁ → w₃ existed at pos 4 (F-i), **every** such path passes through a 1-vertex of K₄, the {1,3}-component of p.
  - Equivalently, at pos 5 there is a {3,4}-separation (Hex/duality, h allowed) between x₁ and w₃, and at pos 4 it did not exist.
- **(F-ii) ⇒ K₇ creates a {1,4}-path from x₃ to w₀.**
  - The {1,4}-graph is unchanged by K₆, and K₆ is the {1,4}-component of x₃ at pos 6. Since w₀ ∉ K₆, there is no {1,4}-path x₃ → w₀ at pos 6 or at pos 7.
  - At pos 8 the {1,4}-graph gains K₇'s old 3-vertices (now 1) and loses K₇'s old 1-vertices.
  - So under (F-ii), **every** {1,4}-path x₃ → w₀ at pos 8 passes through an old-3 vertex of K₇. K₇ is the {1,3}-component of x₁ at pos 7 and contains p and z.

The two statements are time-reverses of each other: K₄ ↔ K₇ are the two {1,3}-swaps through p, and w₃ ↔ w₀ under the mirror. So **the ring part of W2″ fails only if the first {1,3}-swap through p disconnects w₃ from x₁ in {1,2}, and the last {1,3}-swap through p connects w₀ to x₃ in {1,4}.**

### 10.3 Attempted contradiction via the locks [not closed]

The locks at R3k2 are:
- Lock1: a {2,3}-chain Λ₁ from x₁ to x₃;
- Lock2: a {2,4}-chain Λ₂ from x₁ to x₄.

w₃ (colour 2) is adjacent to x₃ and x₄, so it can lie on Λ₁ or Λ₂. The Jordan curve h x₁ Λ₂ x₄ h puts x₂ and x₃ on one side and x₀ on the other. But a {1,2}-path shares colour 2 with both lock chains, so neither chain blocks it, and **Jordan separation gives nothing directly**.

The usable separation is the one in 10.2: at pos 5, a {3,4}-walk separating x₁ from w₃.
- The pos-5 link is 1 2 3 1 4, so its {3,4}-vertices are x₂ (3) and x₄ (4). These are not adjacent, so the separating {3,4}-walk may pass x₂ h x₄.
- That is exactly a {3,4} "lock" on the R1k4 state, from p (now 3) to x₄.
- I could not exclude it at the same time as (F-ii).

### 10.4 Cleanest sub-statement and Studio test

**Sub-statement R (ring escape).** On every period of a (5,5,5,5,6) Γ-cycle:
- (i) w₃ ∉ K_σ(R3k2), or
- (ii) w₀ ∉ K_σ(R3k0).

R implies W2″ (fan lemma, through z or y), and so W2.

By 10.2, R is equivalent to: **not both** "K₄ disconnects w₃ from x₁ in {1,2}" and "K₇ connects w₀ to x₃ in {1,4}".

Studio test (Job AK addendum). At each of the 552 periods, and on all maximal DL runs containing positions 4–8, record:
1. the booleans w₃ ∈ K_σ(pos 4), w₀ ∈ K_σ(pos 8), and the escape at y or z through outer neighbours (if R fails);
2. at pos 4, whether every {1,2}-path x₁ → w₃ meets K₄ ∩ colour 1, i.e. whether w₃ ∉ {1,2}-component of x₁ after K₄ (10.2 says this is forced whenever w₃ ∈ K_σ(4); a check of the bookkeeping);
3. the R1k4 state's {3,4} p–x₄ connection (10.3).

If R holds with 0 failures, the next hand target is the single coupling between the two {1,3}-swaps through p.

If R fails somewhere, W2″ needs the outer neighbours of y and z, and the next step is the rotation at y and z outside the 2-ball.

## 11. Job AK: W2 needs the closure; the open-run counterexample p25 #668 h18 (written 03:51 MDT)

Job AK found that W2\*, W2″ and R hold on all 552 Γ-periods but **fail on open DL runs**: W2\* fails in about 19% of open windows. So no 4-step Kempe proof of W2 exists, and W2, like A₃₄′, needs the Γ-closure. That makes §10.2's reduction a statement about runs, not a proof route.

### 11.1 R1k4: p and x₄ are {3,4}-connected [proved, trivial]

At R1k4 (pos 5, j = 3) the §1 link is x₃..x₂ = 1, 4, 1, 2, 3, so the frame is α = 1, μ = x₄ = 4, A = x₁ = 2, B = x₂ = p = 3. Lock2 at that state is the {μ,B} = {4,3}-chain from x_{j+1} = x₄ to x_{j+4} = x₂ = p. So "p ∼ x₄ in {3,4} at R1k4" **is Lock2 of the R1k4 state**, and it holds on every DL window (Job AK: 0 exceptions). This is the {3,4} separation of §10.3: it exists, and it is a lock.

### 11.2 The counterexample, traced by hand and by script [data]

Script: `nightw2/ce668.py`, output in `outce668.txt`, with its own R₊₃ engine. It reproduces Studio's five colourings up to colour names; Studio stores canonical colourings. Hole 18, link (7, 17, 19, 9, 8), p = 17 (x₁), y = 6, z = 20, m = 16.

| pos | state | Lock1 | Lock2 | σ fixed | Σ over 6 pairs of cycle rank | Σ components |
|---|---|---|---|---|---|---|
| 3 | R1k0 | **0** | 1 | – | – | – |
| 4 | R3k2 | 1 | 1 | **1** | **0** | 8 |
| 5 | R1k4 | 1 | 1 | – | 1 | 9 |
| 6 | R3k1 | 1 | 1 | **1** | 2 | 10 |
| 7 | R1k3 | 1 | 1 | – | 3 | 11 |
| 8 | R3k0 | 1 | 1 | **1** | 4 | 12 |
| 9 | R1k2 | 1 | **0** | – | 6 | 14 |

**The DL run is exactly the window, positions 4–8.**
- Its predecessor (pos 3) lacks Lock1.
- Its successor (pos 9) loses Lock2 immediately.
- In the closure language, the window failure is surrounded by lock death at distance 1 on both sides, so c = 1 here.
- At R3k2 **every one of the six pair-graphs is a forest.** The total rank then rises by exactly 1 per step until the run dies.

### 11.3 Which locks die, in the §1 colours [proved bookkeeping]

- **pos 3 (R1k0, j = 2).** Undoing step 3 (the {α,A}-swap of x₄'s component, which contains x₀) gives link x₀..x₄ = 4, 2, 1, 3, 1. So α = 1, μ = 3, A = 4, B = 2.
  - **Lock1@pos 3 is a {3,4}-chain x₃ → x₀**, in F₄'s forest pair.
- **pos 9 (R1k2, j = 0).** Step 8 swaps {1,2} on x₄'s component, which contains x₀. That gives link 1, 3, 1, 4, 2, so α = 1, μ = 3, A = 4, B = 2.
  - **Lock2@pos 9 is a {2,3}-chain x₁ → x₄**, in F₈'s forest pair.

So the two locks that died are chains in the forest pairs of the two outer fixed points, at the states one step outside the window. Proposed lemma family, for Job AL to test at scale:

> **L-death.** If R3k2, R3k1 and R3k0 of a DL window are all fixed points, then Lock1 fails at the preceding R1k0, or Lock2 fails at the following R1k2. Mirror: the roles are exchanged under time reversal.
> (Weaker: the run leaves DL within c steps of the window, for a small c.)

On a Γ-cycle every state is DL, so L-death (or its weak form) ⇒ W2's fixed-point part.

### 11.4 An exact Euler identity for the total cycle rank [proved]

Let c be a proper 4-colouring of T − h, with T a triangulation on n vertices and deg h = 5. Then:

  **Σ_{6 pairs} rank(ab) = Σ_{6 pairs} comp(ab) − 8.**

*Proof.*
- Every edge of T − h lies in exactly one pair-graph, so Σ E_ab = (3n − 6) − 5.
- Every vertex lies in exactly three pair-graphs, so Σ V_ab = 3(n − 1).
- Hence Σ (E − V + C) = ΣC − 8. ∎

**At a DL state, comp(α,A) ≥ 2 and comp(α,B) ≥ 2.**
- The Lock2 chain {μ,B} from x_{j+1} to x_{j+4}, closed through h, separates x_{j+2} from x_j. An {α,A}-path from x_{j+2} to x_j cannot cross it, since the colours are disjoint and h is deleted.
- The Lock1 chain does the same for {α,B}.

So at a DL state the total rank is ΣC − 8 ≥ 0, with equality iff:
- {α,A} and {α,B} have exactly two components each;
- the other four pair-graphs are connected;
- all six are forests.

p25 #668 at R3k2 is exactly this extremal state, and it was checked numerically at positions 4–9.

**Conjectured refined duality** (consistent with the identity; not proved):

  rank(ab) = comp(cd) − 1 if cd's link vertices form one arc or two arcs joined in cd, and comp(cd) − 2 otherwise.

At a DL state the arcs {α,μ}, {A,B} are single, and {μ,A}, {μ,B} are joined by the locks. The correction terms then sum to 2, which matches the identity.

**Reading.** W2's fixed points are low-total-rank events. A potential proof of W2 on a Γ-cycle could use the total rank R(s) = ΣC − 8, which returns to its value after one cycle length L:
- three fixed points in a window force R small at R3k2;
- the question is whether a Γ-orbit can pass through such a near-extremal state.

At p25 #668 it cannot stay DL: R climbs 0 → 4 across the window and both neighbouring locks are dead. Job AL request: record R(s) along every Γ-cycle and along every open run around each W2\* failure, together with the first lock-death distance.

## 6. Reproduction

Scripts are in `backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/nightw2/`. Each runs on a single core in under 1 s.

- `python3 w2.py` and `python3 w2.py ../jobr27/` write `out2526.txt` and `out27.txt`.
- `python3 w2rank.py` writes `outrank.txt`, from `../jobuv/jobag.json`.
- `python3 w2trace.py` writes `outtrace.txt`, from `../jobuv/jobah.json`.
- `python3 w2ai.py` writes `outai.txt`, from `../jobuv/jobai.json`.
- `python3 ce668.py` writes `outce668.txt`, from `../jobuv/jobak-counterexample.json`. It uses its own R₊₃ and R₊₂ engine, and checks against Studio's colourings up to colour names.
