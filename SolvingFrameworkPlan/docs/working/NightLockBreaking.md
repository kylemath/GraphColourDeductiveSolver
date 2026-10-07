# Night: lock-breaking link-free components at DL states

Night worker, 7 October 2026 (written 00:46 MDT). **Exploratory. Hand work plus small single-core checks. Unreviewed.**

Cited notes:
- **NF** = `StudioMathLean/.../PlaneMap/NoFrozen.lean` (`not_reach_alpha_A_of_lock2`, `not_reach_alpha_B_of_lock1`, `lock_separates`);
- **QRP** = `QuarterRotationPlanar.lean` (`kempe_hex`, `rot3Def_iff_lock2`);
- **WM** = `NightWindingMeander.md`; **CS** = `NightClosedSets.md`; **CB** = `NightCycleBound.md`;
- **R25/R26** = `longtable/local-runs/25-transport`, `26-transport-adversarial`.

Labels: [proved] complete argument here, modulo the cited Lean files; [sketch] gap named; [conjecture]; [data] scratchpad scripts of §5.

**Nothing here proves the floor, R\*, or an escape statement.** §2.4 shows that the cycle-level statement asked for is itself of 4CT strength.

## Verdict

1. **Breaking has an exact Hex form** [proved; data 0 mismatches]. A link-free swap at a DL state breaks a lock iff it glues the two {α,A} link components K_A⁰, K_A, or the two {α,B} link components K_B⁰, K_B. In other words, it undoes one of NF's two separations.
   - Consequence: a swap that breaks lock 2 meets *every* m–b path of L₂, so K ∩ L₂ is an m–b vertex cut of L₂. The same holds for lock 1 with L₁.
   - "Meeting a lock" (R26's working definition of "lock-breaking") is necessary but far from sufficient. 53% of meeting swaps break at order 22, and only 15% do on the +160 cycle.
2. **Target 1: the per-state dichotomy is proved, but its second case is not small** [proved + data].
   - Either some link-free component meets L₁ ∪ L₂, or the state is *lock-saturated* (LS): every component through a lock vertex is one of the 8 link components.
   - LS has an exact description (Lemma 1.3).
   - Jordan forces one structural fact: L₂ never enters a bounded face of L₁, and vice versa. Also, every μ-corner of a bounded face of L₁ has a single α vertex inside it (Lemma 1.4).
   - Correction to the task's premise: only **2** link components belong to the {α,μ}/{A,B} pairs (Λ_αμ, Λ_AB), not 5.
   - The data kill the hoped-for second-case shape. LS states are mostly **saturated** (every component meets the link, CS's 4,822 states). There the lock chains are not short: they contain *every* μ, A and B vertex.
   - "LS ⇒ saturated" fails at order 21 (29 states, all with one free degree-6 vertex).
   - "LS ⇒ saturated or free vertices only" fails at order 22 (4 states with short locks and 2–3-vertex link-free {μ,A}/{μ,B} chains).
3. **Target 2: cycle level** [proved structure + data; no bound].
   - Along a Γ-cycle the swapped colour matching cycles with period 3 (Prop 2.1).
   - A link-free swap in the swapped matching persists one step and commutes with π. This gives "ladder rungs" (Lemma 2.2).
   - [data] On every positive π-cycle at orders ≤ 22 and on the A₇ +160 cycle, every run of consecutive DL states without a breaking component has length ≤ 3. The run length is ≤ 1 on the 17#3 and +160 cycles. So there is at least one breaking state per 4 steps, which is more than |Z|/5 = w(Z).
   - **But any statement forcing even one breaking swap per Γ-cycle implies 4CT** (Prop 2.4). It cannot be proved from Jordan and Euler at single states. The torus also breaks it (a frozen state has no link-free component at all).
4. **Target 3: the residual** is the gap between *meeting* and *gluing* (§3). A lock-meeting swap fails to break iff the Hex cut it makes in L₁ or L₂ is repaired through recoloured vertices. In a minimal counterexample every such cut is repaired. Lemma R_LB states the residual exactly.

---

## 0. Setting

- G = T − h, where T is a plane triangulation and deg h = 5.
- A DL state has link word (α, μ, α, A, B) at x_j, …, x_{j+4}, with m = x_{j+1}, a = x_{j+3} and b = x_{j+4}.
- L₁ is the {μ,A}-component of m (it contains a). L₂ is the {μ,B}-component of m (it contains b).
- A component is **link-free** if it contains none of x₀…x₄.
- The 8 link components (CS Lemma C2) are:
  - Λ_αμ ∋ x_j, m, x_{j+2};
  - Λ_AB ∋ a, b;
  - L₁ and L₂;
  - K_A ∋ x_{j+2}, a and K_A⁰ ∋ x_j;
  - K_B ∋ x_j, b and K_B⁰ ∋ x_{j+2}.
- The three colour matchings are T = {αμ | AB}, X = {αA | μB} and Y = {αB | μA}.
- Terminology:
  - **meeting**: a link-free K meets L₁ ∪ L₂. This is R26's "lock-breaking".
  - **breaking**: swapping K gives a non-DL state.
- A link-free swap keeps the link colours, so it keeps the unfilled pattern and j. Hence its image is non-DL iff lock 1 or lock 2 fails there.

## 1. One DL state

**Lemma 1.1 (half-safety; CS §1) [proved, graph-only].**
- A link-free swap can break lock i only if it meets L_i, because the colours on L_i are otherwise untouched.
- {μ,A}- and {α,B}-swaps preserve lock 1.
- {μ,B}- and {α,A}-swaps preserve lock 2.
- Only t-chains ({α,μ}, {A,B}) can break both locks.

**Lemma 1.2 (Hex form of breaking) [proved, modulo NF and QRP `kempe_hex` with its mirror].** Let K be link-free at a DL state s, and let t = swap_K(s). Then:
- t fails lock 2 ⇔ in t, x_j and a are joined by an {α,A}-path. That is, the swap glues K_A⁰ to K_A.
- t fails lock 1 ⇔ in t, x_{j+2} and b are joined by an {α,B}-path. That is, the swap glues K_B⁰ to K_B.

*Proof.*
- t is unfilled with the same j and the same physical colour roles.
- `kempe_hex` gives (x_j ~_{αA} a) ∨ Lock2.
- NF (`not_reach_alpha_A_of_lock2`) gives Lock2 ⇒ ¬(x_j ~_{αA} a).
- So Lock2(t) ⇔ ¬(x_j ~_{αA} a in t). Lock 1 follows by the mirror statements, which are formal as "R₊₂ defined ⇔ Lock1" in the night log.
- In s the two components are separate, by NF. ∎

[data] Orders 17–20, every degree-5 hole of gentri, every link-free swap at every DL state: 51,872 swaps. Glue ⇔ non-DL in every case (29,286 glue and non-DL; 22,586 neither).

Broken locks by colour pair, matching Lemma 1.1:
- lock 2 is broken by {A,B}, {μ,A}, {α,B} and {α,μ} swaps;
- lock 1 is broken by {A,B}, {α,A}, {μ,B} and {α,μ} swaps;
- only {A,B} and {α,μ} swaps break both.

**Corollary 1.2′ (breaking ⇒ cutting) [proved; Jordan].** If swapping K breaks lock 2, then K ∩ L₂ meets every m–b path of L₂ (and symmetrically for lock 1).

*Proof.*
- Let P₂ be any m–b path in L₂ in s. The closed curve h–m–P₂–b–h separates x_j from {x_{j+2}, a}: in the rotation at h, x_j lies alone in the arc from b to m.
- The gluing {α,A}-path of t from x_j to a avoids h, so it meets P₂. It cannot meet P₂ at m or b, whose colours μ and B are unchanged.
- So it meets an interior vertex of P₂. That vertex is μ or B in s and α or A in t, so it has changed colour and lies in K. ∎

The converse fails, because a cut can be repaired through vertices that the swap recolours into μ/B. [data] Only 388,374 of 736,720 meeting swaps break at order 22. On the +160 cycle the figure is 582 of 3,998.

**Lemma 1.3 (the dichotomy) [proved, graph-only].** At a DL state, exactly one of the following holds.
- (a) Some link-free component meets L₁ ∪ L₂.
- (b) **LS (lock-saturated)**: all three of these hold:
  - (i) L₁ and L₂ have the same μ-vertices, M, and M ⊆ Λ_αμ;
  - (ii) every A-vertex of L₁ lies in Λ_AB ∩ (K_A ∪ K_A⁰);
  - (iii) every B-vertex of L₂ lies in Λ_AB ∩ (K_B ∪ K_B⁰).

*Proof.*
- Each vertex v lies in exactly three components, one for each pair containing col(v).
- For each pair, the components meeting the link are those through the link vertices of its two colours:
  - {α,μ}: Λ_αμ. The link vertices x_j, m, x_{j+2} are consecutive on the link cycle, so they lie in one component.
  - {A,B}: Λ_AB (a and b are adjacent).
  - {μ,A}: L₁.
  - {μ,B}: L₂.
  - {α,A}: K_A and K_A⁰.
  - {α,B}: K_B and K_B⁰.
- (a) fails iff, for every lock vertex v, its three components are among these. Reading this off for col(v) ∈ {μ, A, B} gives (i)–(iii). For example, a μ-vertex of L₁ needs its {μ,B}-component to be L₂.
- Distinctness of K_A and K_A⁰ (that is, NF) is not needed here. ∎

[data] The script asserts LS ⇔ (i)–(iii) on all 386,700 DL states of orders 16–22, with no failure.

Remarks.
- Each of L₁ and L₂ has at least one interior μ-vertex and one interior A- or B-vertex. The reason: x_{j+1}x_{j+3} is not an edge unless x_{j+2} has degree 3. So (b) never holds vacuously: M ≠ ∅.
- The task's count "≤ 5 link-meeting {μ,α}/{A,B}-components" is in fact exactly 2. The {α,μ}/{A,B} part of (b) says M ⊆ Λ_αμ and that the A- and B-vertices of the locks lie in Λ_AB.

**Lemma 1.4 (Jordan non-entry) [proved; sphere].** Assume LS. Let F be a face of the plane graph L₁ that does not contain h ("bounded face"), and write int F for its interior.
- (1) No B-vertex of int F is adjacent to a μ-vertex of ∂F.
- (2) Hence, at every μ-corner u of F, the neighbours of u inside the angle are a single α-vertex w_u, adjacent to both L₁-neighbours of u along ∂F. No μ-vertex of L₁ is a leaf pointing into F.
- (3) L₂ ∩ int F = ∅.

The same holds with L₁ and L₂ exchanged (and A and B exchanged).

*Proof.*
- (1) Let y ∈ int F be B and adjacent to u ∈ M. By LS(i), u ∈ L₂, so y ∈ L₂. The {α,B}-component of y has no μ- or A-vertex, so it cannot meet ∂F ⊆ L₁. By planarity it therefore lies in int F.
  - The link vertices x_j, x_{j+2} and b are adjacent to h and not in L₁, so they lie in h's face.
  - So the {α,B}-component of y is link-free and meets L₂. This is case (a), a contradiction.
- (2) Neighbours of u strictly inside an angle of F are not in L₁, and an A-neighbour would be an L₁-edge. So they are α or B, and by (1) they are all α. Consecutive neighbours are adjacent, so the angle contains exactly one of them. For a leaf, the angle would contain deg u − 1 ≥ 4 of them.
- (3) An L₂-path from int F to b ∈ h-face leaves F through a vertex of ∂F ∩ L₂ ⊆ M. The previous vertex on the path is a B-vertex of int F adjacent to it, which (1) excludes. ∎

So in case (b) the two lock chains do not nest. Each bounded face of L₁ is surrounded on its μ-corners by single α-vertices. The minimal such face is a hexagon μAμAμA around one degree-6 α-vertex w, whose {α,B}-component is {w}. This is exactly the "free vertex" shape found in the data (§1.5).

**1.5 What the second case looks like [data].** Exhaustive gentri, every degree-5 hole:

| order | DL | saturated | LS | LS, not saturated | of which free-vertex only | other |
|---|---|---|---|---|---|---|
| 16 | 144 | 0 | 0 | 0 | 0 | 0 |
| 17 | 775 | 136 | 136 | 0 | 0 | 0 |
| 18 | 1,345 | 90 | 90 | 0 | 0 | 0 |
| 19 | 3,523 | 161 | 161 | 0 | 0 | 0 |
| 20 | 17,979 | 1,169 | 1,169 | 0 | 0 | 0 |
| 21 | 65,395 | 3,266 | 3,295 | 29 | 29 | 0 |
| 22 | 297,539 | 9,402 | 9,571 | 169 | 165 | **4** |
| A₇ h22 class (21,078 states) | 5,364 | 0 | 0 | 0 | 0 | 0 |

Key to the columns:
- Saturated = no link-free component at all (CS's 4,822 states at orders 17–21; reproduced exactly).
- Free vertex = a link-free singleton {v} at a degree-6 vertex whose six neighbours use only two colours. Its three variants are α in a μA-hexagon, μ in an αB-hexagon, and α in an AB-hexagon.

How the three kinds of LS state look:
- **Saturated states:** the locks are maximal, not short. Saturation means {μ,A}, {μ,B}, {α,μ} and {A,B} are connected (WM 2.2). So L₁ ∪ L₂ contains every μ, A and B vertex, and only α-vertices lie outside the locks. The figures are 9 of 11 off-link vertices at order 17 and 12–13 of 15 at order 21.
  - The task's guess that in case (b) the lock chains are "short or hugging the link" is **wrong for these states**: here the locks fill the sphere.
- **Free-vertex states:** these are Lemma 1.4's minimal configuration. They are harmless, since swapping recolours one vertex and lands on a DL state, but they are link-free and not lock-meeting.
- **The 4 "other" states:**
  - order-22 gentri #545 hole 6;
  - #611 hole 18;
  - #647 holes 13 and 19.
  - Here the locks are **short**, with 5–6 off-link vertices each. The link-free components are {μ,A}- and {μ,B}-chains of 2–3 vertices whose μ-vertices avoid L₂ (respectively L₁). Only in these states does the "short lock" picture hold.

Conjectures killed tonight:
- "LS ⇒ saturated" (order 21);
- "LS ⇒ saturated, or every link-free component is a free vertex" (order 22).

Saturated DL states can sit **on a Γ-cycle**: the order-22 Γ-cycle at gentri #418 hole 21 (L = 20, w = +4, class of 252 states) has 4 saturated states out of 20. So case (b) occurs along the cycles that matter.

## 2. Along a Γ-cycle

**Prop 2.1 (matching rotation) [proved].** Let s′ = R₊₃s, so that (α′, μ′, A′, B′) = (α, B, μ, A) in physical colours.
- Then T(s′) = Y(s), X(s′) = T(s) and Y(s′) = X(s).
- The swapped matching is always X (K_A is an {α,A}-component). So along a Γ-cycle the swapped physical matching runs X, T, Y, X, … with period 3.
- The repeated colour α is constant, and μ runs through μ → B → A with period 3.
- The lock pairs at each state are the non-α halves of X and Y. The new lock 1 is the old lock 2 (CS E1).

**Lemma 2.2 (persistence and ladder rungs) [proved].** Let K be a link-free component at a DL state s, of a pair in X(s) (so {α,A} or {μ,B}).
- (1) K is still a link-free component at s′, of a pair in Y(s′).
  - Swapping K_A does not change the {α,A}- or {μ,B}-subgraph as a partition.
  - K is unchanged as a vertex set, so it stays link-free.
- (2) swap_K(R₊₃ s) = R₊₃(swap_K s). The reason is that K_A(swap_K s) = K_A(s).
- (3) If K meets L₂(s), it meets L₁(s′) = L₂(s): meeting persists for one step.
- (4) Suppose t = swap_K(s) is non-DL. By Lemma 1.1, t keeps lock 2, so π(t) = R₊₃t, λ(t) = +1, and π(t) = swap_K(π s).
  - So the exits s → t and π(s) → π(t) are a **rung pair** landing on consecutive states of one π-cycle N.
  - The step t → π(t) is a positive step of N. The negative steps of N lie elsewhere on N, so a single rung does not by itself carry negative winding.
- (5) At s′ the pair of K lies in Y(s′), which can only break lock 2 (Lemma 1.1). Persistence beyond one step fails in general, because the next swap (of matching T(s)) can re-partition K's pair.

**2.3 Data on positive π-cycles** (every positive cycle at orders 17–22, every degree-5 hole of gentri, plus the A₇ h22 class).

"Meeting" = states with a lock-meeting link-free component; "breaking" = states with a breaking one; "max run" = the longest cyclic run of DL states with no breaking component.

| cycle | L | w | DL states | meeting | breaking | max run |
|---|---|---|---|---|---|---|
| 17 #4 h0, h16 (WM's 17#3) | 20 | +4 | 20 | 20 | 10 | 1 |
| 20 #59 h18, #61 h19 | 21 | +1 | 11 | 10 | 8, 9 | 2 |
| 21 #97 h2, #135 h0 | 14 | +2 | 11 | 10, 9 | 4, 7 | 3, 1 |
| 22, 14 positive non-Γ cycles | 14–21 | +1, +2 | 10–11 | 7–11 | 4–9 | ≤ 3 |
| 22 #418 h21 (Γ) | 20 | +4 | 20 | 16 | 8 | 3 |
| 22 #649 h0, h21 (Γ) | 20 | +4 | 20 | 20 | 20 | 0 |
| A₇ h22, the +160 cycle | 800 | +160 | 800 | 800 | 490 | 1 |
| A₇ h22, the two +4 cycles | 20 | +4 | 20 | 20 | 12 | 1 |

Reading:
- On every Γ-cycle observed, breaking states number at least ⌈L/4⌉, which exceeds L/5 = w.
- Every state of the +160 cycle meets, but only 490 of 800 break. Of the meeting swaps on that cycle, 85% are repaired (§1).

**Prop 2.4 (the cycle-level target is 4CT-strength) [proved].** Consider the statement "every Γ-cycle has at least one breaking link-free swap". It implies 4CT, and so does any per-step version.

*Proof.* Let T be a minimal counterexample. It has a degree-5 vertex h, and G = T − h is 4-colourable. Every Kempe class of G is targetless, hence swap-closed and unfilled, hence all DL (CS C1). So no swap lands on a non-DL state. Each class is a union of Γ-cycles (CS C3), and none of them has a breaking swap. ∎

Consequences:
- The requested lemma "one lock-breaking exit per 5 steps" would be a proof of 4CT. No combination of Lemmas 1.2–1.4, Prop 2.1, Lemma 2.2, Jordan and single-state Euler counts can give it, because each of these holds verbatim in a planar minimal counterexample.
- **Torus:** a frozen state has no link-free component at all, so no meeting and no breaking. The statement fails there, as it must.

**What is not 4CT-strength:** the *meeting* version, [conjecture] "every Γ-cycle that is not a whole Kempe class has a state with a lock-meeting link-free component".
- In a counterexample, meeting swaps just land on other DL states.
- It would follow from WM Corollary 2.3 if LS implied saturation, but that implication is false (§1.5). The free-vertex and short-lock states block it.
- [data] It holds on all Γ-cycles observed (each has ≥ 16 of 20 meeting states).

## 3. Honest assessment: where the second case resists

1. **The per-state dichotomy is exact but not useful by itself.**
   - Case (b) occurs:
     - on the sphere in about 3% of DL states at order 22 (9,571 of 297,539);
     - in three shapes (saturated, free vertex, short locks);
     - including on Γ-cycles (#418).
   - Jordan gives only Lemma 1.4 (non-nesting of the locks, single α at μ-corners). That constrains the *geometry* of case (b) but does not exclude it, because saturated states exist.
   - Excluding them is WM's saturation question: a Γ-cycle of saturated states is a whole targetless class, which is R\*-strength.
2. **Case (a) is not enough either.** Meeting is not breaking.
   - By Lemma 1.2 and Corollary 1.2′, a meeting swap breaks a lock iff the cut it makes in L₁ or L₂ is not repaired through the vertices it recolours into the lock colours.
   - Repair is common: 47% of meeting swaps at order 22 and 85% on the +160 cycle are repaired.
   - Repair is the only thing that happens in a minimal counterexample.
3. **Residual lemma (precise; 4CT-strength by Prop 2.4).**

   **R_LB.** Let T be a plane triangulation, h a vertex of degree 5, and Z a Γ-cycle of the π-permutation on a Kempe class of T − h. Then some s ∈ Z has a link-free component K such that, in swap_K(s), x_j is {α,A}-connected to a, or x_{j+2} is {α,B}-connected to b. (By Lemma 1.2 this is "K glues K_A⁰ to K_A, or K_B⁰ to K_B".)

   The transport form adds: summed over Z with the cycles reached, the glued exits reach total |winding| ≥ w(Z) (R26: ≥ 4 w(Z) in the data).
4. **Where a proof would have to get its strength.**
   - R_LB says that the two NF separations cannot be maintained against every link-free swap along an entire Γ-cycle.
   - The sphere input available (NF, `kempe_hex`, Lemma 1.4) maintains them state by state. What fails in a counterexample is only a *global* count, of the same kind as the reducibility input of 4CT.
   - The data regularity "max run ≤ 3 (≤ 1 on 17#3 and +160)" is the sharpest observed form, and it too is 4CT-strength.

## 4. Status

| Item | Status |
|---|---|
| Breaking ⇔ gluing K_A⁰–K_A or K_B⁰–K_B (Hex form) | [proved] mod NF + QRP; 51,872 swaps, 0 mismatches |
| Breaking lock i ⇒ K ∩ L_i is an m–(a/b) cut of L_i | [proved] (Jordan) |
| Dichotomy: lock-meeting link-free component, or LS (i)–(iii) | [proved], graph-only; asserted on all DL states, orders 16–22 |
| LS ⇒ locks do not nest; single α at μ-corners of bounded faces | [proved] (sphere) |
| LS ⇒ saturated | **false** (order 21, 29 free-vertex states) |
| LS ⇒ saturated or free vertices only | **false** (order 22, 4 short-lock states) |
| Matching period 3 along Γ-cycles; persistence and ladder rungs | [proved] |
| ≥ 1 breaking state per 4 consecutive DL states on positive cycles | [data] orders ≤ 22 and A₇; 4CT-strength |
| Meeting version for non-whole-class Γ-cycles | [conjecture], not 4CT-strength |
| R_LB / one breaking exit per Γ-cycle | ⇒ 4CT [proved]; open |

## 5. Reproduction (session scratchpad, not committed)

- `lb.py N…`: imports `longtable/local-runs/common/kempe_py.py` (state enumeration) and R26's `lib26.Eng` (π, λ, DL).
  - For every DL state it computes link-free, meeting and breaking components, asserts Lemma 1.1's "only meeting swaps can break", and asserts LS ⇔ (i)–(iii) of Lemma 1.3.
  - It also records saturated and free-vertex states, and per positive π-cycle the counts and max run of §2.3.
  - Run times: orders 16–20 take 8 s; orders 21–22 take 130 s on a single core, AC power.
- `hexchk.py`: Lemma 1.2 on orders 17–20 (glue ⇔ non-DL), with breaking counted by pair and lock.
- `ls21.py`, `ls22.py`: list the LS-but-unsaturated states (§1.5). `g418.py`: the #418 h21 Γ-cycle state by state.
- `a7.py`: `run_dd/best-A7_exc.json` hole 22, seed 1, the 21,078-state class (3 s).
- Indices: gentri numbering is 1-based in these scripts (R25/R26 numbering). WM's "17 #3" is "17 #4" here.
