# Fellow F: Lemma R\* at a (5,5,6,5,6) hole, a precise reduction and the new kill rules

Research Fellow F, 6 October 2026. **Hand work only.** No program was run on this machine (power limit); files were only read. Labels: **[hand, unreviewed]** = proved here by hand, no second reader; **[sketch]** = argument outlined, details not all written; **[cited]** = taken from a named note; **[memory]** = recalled, not rechecked; **[open]**.

Sources read: StudioMathReviewHPandH.md, MathReviewTheoremHP.md, MathRstar55566.md (move G), interns-2026-10-06/intern-B.md and intern-B-cycle2.md, MathTwoSixNeighbours.md (pattern names N, L, O, cycles Γ₁, Γ₂), MathRstar55656.md (Lemma SS, the certificate walk), the Math message of 15:12 (diamond-free frame), VacancyIcosahedral.lean and RStarCore.lean (for the Lean vocabulary).

## 0. Verdict, first

1. **R\* for the class (5,5,6,5,6) is NOT proved here [open].** I did not find a bound, and I give a reason to expect none from local arguments (§6, self-attack SA-0): in the diamond-free frame the statement is the (5,5,6,5,6) case of the question Tilley studies (Kempe-locking at a degree-5 vertex), which is open in general.
2. **What is proved [hand, unreviewed]:**
   - **Lemma O (exact period 15).** On exact colourings, F is a bijection between DL states with B as inverse. Every F-orbit of DL states is a finite path, and then every state on it fills, or a cycle whose length is a multiple of **15** (not only 5). So R\* fails at v only if some Kempe class contains an F-cycle of length 15k all of whose states are DL (§2).
   - **The move catalogue (§2.3):** at a DL state exactly eight Kempe swaps touch the link (AB, F, G0, B, D2, G, and the two lock swaps). Their images and frame shifts are given. In a targetless class all eight images, and every silent swap, must again be DL.
   - **The G-table (§4.1):** G on all 28 surviving states. G is confined and deterministic exactly at **N2 ↔ N4** (and the mirrors). This joins Γ₁ to Γ₂. At **L2, O6, L1(b,g)** and their mirrors, G kills unless a named {g,d} leak is present.
   - **Lemma W (§4.2), new kill rule plus Jordan side lemma.** This applies at a state with w₃ = w₄ = b and deg x₄ = 6. It is the mirror pair of F-E1′, with the companion swap G0 (the {a,g} swap at x₀). Then **exactly one** of F, G0 kills unless m₄ lies in a named component. Using the Jordan curve of lock 2, that membership is equivalent to a **cut condition on lock 2**: every lock-2 path enters x₄ through w₄ (if m₄ = a) or through w₃ (if m₄ = g). The mirror Lemma W′ handles w₂ = w₃ = b with deg x₃ = 6. These conditions read the side of the m-neighbour relative to a lock curve, as the brief asked.
3. **Case table (§3).** Each of intern B's 20 closed ring patterns (28 states once the m-colours are added) gets its F-image, its G-image and the **complete list of leak predicates a targetless class must satisfy there**. None is killed outright. The new rules add **18 new predicates across 15 of the 28 states**. All of them are "a path exists" or "a path is cut" predicates, and they are listed by name in §3. Two states, O10 and M(O10), carry no local predicate at all.
3a. **Three smaller structural facts [hand, unreviewed].**
   - **Lemma Γ (§2.4):** in a targetless class every F-cycle has length divisible by 30, assuming Math's Γ-tables. The class contains both a Γ₁ cycle and a Γ₂ cycle, joined by the confined G at N2 ↔ N4.
   - **Lemma LC (§4.5):** lock 2 of s *is* lock 1 of F(s), as the same vertex set. So W's cut constraints are carried one step along the cycle as constraints on which exit the next lock uses.
   - **SA-5:** the lock swaps L1 and L2 kill exactly when SS4 and SS3 fail. This gives those predicates without the corrected Lemma SS.
4. **Exact open target (§5).** This is Lemma C★, stated as a finite set of path predicates along one F-cycle of 15k states. It is a planarity statement: the predicates of §3 cannot all hold at every state of an F-cycle. I could not prove it; §6 records why each single-state attempt fails.
5. **Computations wanted (§7).** There are six, each with a stated kill condition. The most important is item 1, a search for targetless (Kempe-closed, all-DL) classes at (5,5,6,5,6) holes in diamond-free triangulations. **One example kills R\* for the class**, and with it the front-1 target as stated.

## 1. Setting in Lean-style language [hand, unreviewed; statements only, not compiled]

Vocabulary as in the library: `ProperOff G h c` (proper off the hole), `pairGraph G h c α β` (the {α,β}-subgraph of G − h), `KempeStep`, `PurePath`, `PureFill G h c m`, `Target G h c` (link uses ≤ 3 colours), `PureClean T h`, `FiveLink`, `NoSeparatingTriangleAt`.

```lean
namespace SimpleGraph.SphericalMap
variable {n : ℕ} (M : SphericalMap n)

/-- The two-ball of a (5,5,6,5,6) hole. Link `L.port 0..4 = y₀..y₄` in rotation order,
degrees 5,5,6,5,6. `u t` is the outer common neighbour of `y t`, `y (t+1)`; `p`, `q` are the
middle outer neighbours of the degree-6 ports `y₂`, `y₄`. The outer ring is the 7-cycle
u₀ u₁ p u₂ u₃ q u₄. -/
structure Ball55656 (h : Fin n) (L : FiveLink M.graph h) (u : Fin 5 → Fin n) (p q : Fin n) :
    Prop where
  nbr0 : ∀ z, M.Adj (L.port 0) z ↔ z = h ∨ z = L.port 4 ∨ z = L.port 1 ∨ z = u 4 ∨ z = u 0
  nbr1 : ∀ z, M.Adj (L.port 1) z ↔ z = h ∨ z = L.port 0 ∨ z = L.port 2 ∨ z = u 0 ∨ z = u 1
  nbr2 : ∀ z, M.Adj (L.port 2) z ↔
    z = h ∨ z = L.port 1 ∨ z = L.port 3 ∨ z = u 1 ∨ z = p ∨ z = u 2
  nbr3 : ∀ z, M.Adj (L.port 3) z ↔ z = h ∨ z = L.port 2 ∨ z = L.port 4 ∨ z = u 2 ∨ z = u 3
  nbr4 : ∀ z, M.Adj (L.port 4) z ↔
    z = h ∨ z = L.port 3 ∨ z = L.port 0 ∨ z = u 3 ∨ z = q ∨ z = u 4
  ring : M.Adj (u 0) (u 1) ∧ M.Adj (u 1) p ∧ M.Adj p (u 2) ∧ M.Adj (u 2) (u 3) ∧
    M.Adj (u 3) q ∧ M.Adj q (u 4) ∧ M.Adj (u 4) (u 0)
  rot : ∀ i : Fin 5, M.rotation.next ⟨(h, L.port i), port_adj M.graph L i⟩ =
    ⟨(h, L.port (i+1)), port_adj M.graph L (i+1)⟩
  off : ∀ t i, u t ≠ L.port i ∧ p ≠ L.port i ∧ q ≠ L.port i

/-- The frame of an unfilled colouring: the middle index `j` (the port between the two ports
of the repeated colour) and the role renaming `σ` with `σ ∘ c ∘ x = ![0,1,0,2,3]`, where
`x i = L.port (j + 4 + i)`; so x₀ = y_{j-1}, x₁ = y_j (middle), ... Roles 0,1,2,3 = a,b,g,d. -/
structure Frame (h) (L : FiveLink M.graph h) (c : Fin n → Fin 4) (j : Fin 5) (σ : Equiv.Perm (Fin 4)) :
    Prop where
  word : ∀ i : Fin 5, σ (c (L.port (j + 4 + i))) = ![0, 1, 0, 2, 3] i

def x (L : FiveLink M.graph h) (j i : Fin 5) : Fin n := L.port (j + 4 + i)

/-- Lock 1: a {b,g}-path x₁ ~ x₃.  Lock 2: a {b,d}-path x₁ ~ x₄ (both in `G - h`). -/
def Lock1 (c) (j σ) : Prop :=
  (pairGraph M.graph h c (σ.symm 1) (σ.symm 2)).Reachable (x L j 1) (x L j 3)
def Lock2 (c) (j σ) : Prop :=
  (pairGraph M.graph h c (σ.symm 1) (σ.symm 3)).Reachable (x L j 1) (x L j 4)

/-- Doubly locked. -/
def DL (c : Fin n → Fin 4) : Prop :=
  ProperOff M.graph h c ∧ ¬ Target M.graph h c ∧ ∃ j σ, Frame M h L c j σ ∧ Lock1 c j σ ∧ Lock2 c j σ

/-- Whole-component swap: `swap c α β s` exchanges α and β on the {α,β}-component of `s`. -/
def swap (c : Fin n → Fin 4) (α β : Fin 4) (s : Fin n) : Fin n → Fin 4 :=
  fun z => if (pairGraph M.graph h c α β).Reachable s z then Equiv.swap α β (c z) else c z

-- The eight link moves at a framed state (frame j σ; write A B Γ Δ := σ.symm 0,1,2,3):
def moveAB  c := swap c A B (x L j 1)   -- {a,b} of x₁ (contains x₀ x₁ x₂)
def moveF   c := swap c A Γ (x L j 2)   -- {a,g} of x₂ (contains x₃)
def moveG0  c := swap c A Γ (x L j 0)   -- {a,g} of x₀ (no other link vertex)
def moveB   c := swap c A Δ (x L j 0)   -- {a,d} of x₀ (contains x₄)
def moveD2  c := swap c A Δ (x L j 2)   -- {a,d} of x₂ (no other link vertex)
def moveG   c := swap c Γ Δ (x L j 3)   -- {g,d} of x₃ (contains x₄)
def moveL1  c := swap c B Γ (x L j 1)   -- lock-1 component (contains x₃)
def moveL2  c := swap c B Δ (x L j 1)   -- lock-2 component (contains x₄)

/-- A targetless class: nonempty, closed under every whole-component swap, no filled state. -/
def Targetless (Q : Set (Fin n → Fin 4)) : Prop :=
  Q.Nonempty ∧ (∀ c ∈ Q, ProperOff M.graph h c ∧ ¬ Target M.graph h c) ∧
  ∀ c ∈ Q, ∀ α β s, swap M c α β s ∈ Q

/-- **Target theorem [open].** -/
theorem rstar_55656 (htri : M.Triangulated) {h : Fin n} (L : FiveLink M.graph h) {u p q}
    (B : Ball55656 M h L u p q) (hsep : M.NoSeparatingTriangleAt h)
    (hmin : ∀ z, 5 ≤ M.graph.degree z) : PureClean M h := sorry

/-- Equivalent form (Lemma Q, §2): no targetless class at `h`. -/
theorem rstar_55656_iff : PureClean M h ↔ ¬ ∃ Q, Targetless M h Q := sorry
```

**Optional hypothesis (diamond-free frame, Math 15:12).** `(hdia : 6 ≤ M.graph.degree (u 0))`: the common outer neighbour of the adjacent degree-5 pair y₀, y₁ is not of degree 5. **No lemma below uses it.** I record it because a proof that does not use it would also cover the diamond case, which classical reducibility already removes.

**Frame dictionary.** For middle y_j we have x_i = y_{j−1+i}, and S is the set of frame positions of y₂ and y₄:

| middle | x₀..x₄ | degrees | S | intern B | states |
|---|---|---|---|---|---|
| y₃ | y₂ y₃ y₄ y₀ y₁ | 6 5 6 5 5 | 02 | P0 | N1(b,b), N1(b,d), N1(g,b), N2, N3, N4 |
| y₁ | y₀ y₁ y₂ y₃ y₄ | 5 5 6 5 6 | 24 | P2 | L1(b,g), L1(g,a), L1(g,g), L2, L3, L4 |
| y₂ | y₁ y₂ y₃ y₄ y₀ | 5 6 5 6 5 | 13 | P1 | O3, O4, O5, O6, O10 |
| y₀ | y₄ y₀ y₁ y₂ y₃ | 6 5 5 6 5 | 30 | P3 | M(L·) |
| y₄ | y₃ y₄ y₀ y₁ y₂ | 5 6 5 5 6 | 41 | P4 | M(O·) |

In frame notation the ring is the 7-cycle w₄ [m₀] w₀ [m₁] w₁ [m₂] w₂ [m₃] w₃ [m₄] w₄, with m_t present iff t ∈ S. The mirror M (t ↦ 2 − t, g ↔ d, w_t ↦ w_{1−t}, m_t ↦ m_{2−t}) exchanges S = 13 ↔ 41 and 24 ↔ 30, fixes 02, and exchanges F ↔ B, G0 ↔ D2, L1 ↔ L2; it fixes AB and G.

## 2. Reductions [hand, unreviewed unless marked]

### 2.1 Lemma Q (targetless classes) [cited: Long Table / Math, 6 Oct; restated]
R\* fails at v iff there is a targetless class Q (definition `Targetless`, §1).
- (⇐) is immediate.
- (⇒) Take the Kempe class of a colouring that reaches no filled state.
- Every state of Q is DL. An unfilled non-DL state fills in one swap (Unlock, HP review step 0).
- Consequently every pattern met in Q is one of the **28 surviving states** of MathTwoSixNeighbours §3 (intern B's 20 w-patterns). Every other admissible pattern has a one-move kill, so one of its images would be a non-DL state inside Q.

### 2.2 Lemma O (orbits; exact period 15) [hand, unreviewed]
Let D be the set of DL colourings of T − v (exact colours, not up to permutation). On D:
1. **F and B are mutually inverse partial bijections.** If F(s) ∈ D then B(F(s)) = s.
   - F(s) has link (a,b,g,a,d) and is read in the frame x′_i = x_{i+3}, so x′₀ = x₃ and a′ = a, d′ = c(x′₄) = c(x₂) = g.
   - B at F(s) swaps the {a,g}-component of x₃ in F(s). That is exactly K_F with its colours exchanged.
   - Symmetrically, F(B(s)) = s.
2. **Paths fill.** The F/B graph on D has in- and out-degree ≤ 1, so its components are paths or cycles. Take a path, and let s_end be its F-end, so F(s_end) ∉ D. F(s_end) is unfilled (its link has four colours), hence non-DL, hence fills in one swap. So a state at F-distance k from s_end fills within k + 2 swaps. A path is finite because D is finite.
3. **Cycle length ≡ 0 (mod 15).** Write a DL state's link by its middle index j and the colour triple (β, γ, δ) = (c(x₁), c(x₃), c(x₄)). The repeated colour A is fixed (MathRstar55656 4.1).
   - F sends j ↦ j + 3 (mod 5) and (β, γ, δ) ↦ (δ, β, γ). Indeed the new middle is x₄ (colour δ), the new x′₃ = x₁ has colour β, and the new x′₄ = x₂ has colour γ after F.
   - The link colouring determines the frame. So F^k(s) = s forces 3k ≡ 0 (mod 5) **and** k ≡ 0 (mod 3), that is, 15 | k.
   - Math's "5 | k" is the up-to-permutation version.

**Corollary O.** In a targetless class every state lies on an F-cycle of length 15k, and the class is a union of such cycles. ∎

### 2.3 The eight link moves [hand, unreviewed]
At a DL state the bichromatic components that meet the link are exactly the following eight:
- the {a,b}-component of x₁, which contains x₀, x₁, x₂;
- the two {a,g}-components, K_F ∋ x₂, x₃ and K₀ ∋ x₀. They are distinct by Jordan.
- the two {a,d}-components, K_B ∋ x₀, x₄ and K_D2 ∋ x₂. They are distinct by Jordan.
- the {b,g} lock-1 component K₁ ∋ x₁, x₃;
- the {b,d} lock-2 component K₂ ∋ x₁, x₄;
- the {g,d}-component K_G ∋ x₃, x₄.

Every image is unfilled. Each image, read in its own frame, is as follows:

| move | swapped | image link | new middle (shift) | roles a′b′g′d′ (actual colours) | old lock kept | new lock(s) to check |
|---|---|---|---|---|---|---|
| AB | K_AB | (b,a,b,g,d) | x₁ (0) | b a g d | none | {a,g} x₁~x₃, {a,d} x₁~x₄ |
| F | K_F | (a,b,g,a,d) | x₄ (+3) | a d b g | lock 2 | {d,g} x₄~x₂ |
| G0 | K₀ | (g,b,a,g,d) | x₄ (+3) | g d b a | lock 2 | {d,a} x₄~x₂ |
| B | K_B | (d,b,a,g,a) | x₃ (+2) | a g d b | lock 1 | {g,d} x₃~x₀ |
| D2 | K_D2 | (a,b,d,g,d) | x₃ (+2) | d g a b | lock 1 | {g,a} x₃~x₀ |
| G | K_G | (a,b,a,d,g) | x₁ (0) | a b d g | none | {b,d} x₁~x₃, {b,g} x₁~x₄ |
| L1 | K₁ | (a,g,a,b,d) | x₁ (0) | a g b d | lock 1 | {g,d} x₁~x₄ |
| L2 | K₂ | (a,d,a,g,b) | x₁ (0) | a d g b | lock 2 | {d,g} x₁~x₃ |

The "old lock kept" column: F and G0 swap a ↔ g, so the {b,d}-subgraph does not change. The other entries are similar.

**New endpoint (starvation) rules read off the table.** Each is a one-move kill, with radius ≤ 2.
- F: x₂ has no d-neighbour (F-starvation), or x₄ has no g-neighbour after F (F-E1′).
- **G0:** x₂ has no d-neighbour (this is already F-starvation), or **x₄ has no a-neighbour after G0 (G0-starvation, new)**.
- B and D2: the mirrors (B-starvation, B-E1″, **D2-starvation**).
- G: E1 fails after G. This is possible only when deg x₁ = 6, w₀ and w₁ have different colours, and exactly one of them lies in K_G (used at O6, §4.1).

A targetless class must defeat all of these at every state, together with every silent swap (Lemma SS, corrected form, MathRstar55656 §2 and the review note).

### 2.4 Lemma Γ (orbit structure inside a targetless class) [hand, unreviewed; depends on Math's F-tables, cited]
Assume the F-transition tables of MathTwoSixNeighbours §5 [cited, hand, single reader].
1. Γ₁ is a deterministic 10-cycle of patterns. **Every Γ₂ pattern walk also has period 10.** Every F-arrow of Γ₂ follows the scheme

   N1(·) → L1(·) → M(O4 | O5) → O10 → M(L4) → N4 → L4 → M(O10) → O4 | O5 → M(L1(·)) → N1(·),

   and branches occur only inside the slots N1(·), L1(·), O4|O5 and M(L1(·)). The ten Γ₁ patterns are distinct, and so are the ten slots.
2. There is no F- or B-arrow between Γ₁ and Γ₂. So in a targetless class each F-cycle lies wholly in Γ₁ or wholly in Γ₂. Its length is divisible by lcm(15, 10) = **30**. It meets N2 (for Γ₁) or N4 (for Γ₂) exactly once every 10 steps.
3. **G joins the two families (new, §4.1).** At N2 and N4, K_G = {x₃, x₄} (confined), and G maps N2 ↔ N4 by exchanging the colours of x₃ and x₄ only.
   - Hence a targetless class contains **both** a Γ₁ cycle and a Γ₂ cycle. So |Q| ≥ 60.
   - Each N2 state s of the Γ₁ cycle has a partner G(s) on a Γ₂ cycle, and the partner differs from s only at x₃ and x₄.

*Proof.* (1) and (2) are read off Math's arrow lists; the period follows from the distinctness of the pattern slots. (3) is §4.1. ∎

**Use.** At the pair (s, G(s)) the four locks live on the **same** colouring of T − {v, x₃, x₄}. Write c for that common colouring. In N2 we have x₃ = g and x₄ = d, the unique b-neighbour of x₃ is w₂, and the unique b-neighbour of x₄ is w₄. So:
- (i) w₂ ~ x₁ in the {b,g}-graph of c (lock 1 of s);
- (ii) w₄ ~ x₁ in the {b,d}-graph of c (lock 2 of s);
- (iii) w₂ ~ x₁ in the {b,d}-graph of c (lock 1 of G(s));
- (iv) w₄ ~ x₁ in the {b,g}-graph of c (lock 2 of G(s)).

All four paths lie in T − {v, x₃, x₄}. The {b,g}-paths leave x₁ through w₀ and the {b,d}-paths through w₁. (iii) and (iv) are exactly the two silent-starvation leaks Math needs at N2, so this coupling **re-derives Math's SS predicates at N2 without Lemma SS**. Self-attack SA-3 (§6) shows that the four paths can coexist in a plane graph. So Lemma Γ alone gives no contradiction.

## 3. Case table: intern B's 20 closed ring patterns [hand, unreviewed]

I re-derived the 49 admissible patterns and the 28 survivors of MathTwoSixNeighbours §3 independently, from admissible colours, E1–E3 and ring properness. I agree with all of them: S = 02 has 7/6, S = 24 has 10/6, S = 13 has 11/5, and the mirrors give 30 and 41. Intern B's 20 w-strings are exactly these 28 states with the m-colours forgotten. The w-strings are w₀w₁w₂w₃w₄.

**Predicate names.** All are evaluated in the state itself. K₁ and K₂ are the lock components, K_AB is the {a,b}-component of x₁, and so on (§2.3).
- **AB★**: w₃ ∈ K_AB. Without it, AB starves the degree-5 member of {x₃, x₄} that sees w₃ as its only b-neighbour. [cited intern B, Math]
- **SS3**: w₂ ∈ K₂. Silent {b,d}-swap at w₂, when x₃ has degree 5, w₂ = b and w₃ = a. [Math at L2 and N2; **new at N4 and L4**]
- **SS4**: w₄ ∈ K₁. The mirror of SS3, when x₄ has degree 5, w₄ = b and w₃ = a. [Math at N2 and M(L2); **new at N4 and M(L4)**]
- **G01**: w₀ ∈ K_G and w₁ ∈ K_G. [Math (SS) at O6; **new (G) at L1(b,g)**]
- **Grun**: {w₀, w₁, m₂} ⊂ K_G (and Grun′ = {w₀, w₁, m₀} ⊂ K_G, its mirror). [**new**, §4.1]
- **W34-a**: m₄ ∈ K_F, equivalently w₃ is not joined to x₁ in K₂ − x₄. [E1′ part cited Math; **cut form new**, §4.2]
- **W34-g**: m₄ ∈ K₀, equivalently w₄ is not joined to x₁ in K₂ − x₄. [**new**, §4.2]
- **W23-a / W23-d**: the mirrors. m₃ ∈ K_B (equivalently w₃ is not joined to x₁ in K₁ − x₃), or m₃ ∈ K_D2 (equivalently w₂ is not joined to x₁ in K₁ − x₃). [**new**]

**Status rule.** A state is *killed with bound b* if some move sequence of length b − 1 reaches a non-DL state whatever the outside is. It is *open with condition P* if every local kill fails exactly when P holds. P is then a conjunction of the predicates listed; a targetless class needs P at every visit.

| # | intern B | w-string | state(s) | F-image [cited] | G-image [§4.1] | predicates a targetless class must satisfy | status |
|---|---|---|---|---|---|---|---|
| 1 | P0 | gdbab | N2 (m₀ d, m₂ g) | L3 | **N4, confined** | SS3 ∧ SS4 ∧ [G(s) DL] | open; Γ₁ |
| 2 | P0 | dgbab | N4 (m₀ g, m₂ d) | L4 | **N2, confined** | SS3 ∧ SS4 ∧ [G(s) DL] | open; Γ₂ |
| 3 | P0 | gddbg | N1(b,b), N1(b,d), N1(g,b) | L1(g,g), L1(b,g), L1(g,a) | N1(b,b): self or N3; others self | AB★ | open; Γ₂ (N1(g,d) killed by AB, bound 2) |
| 4 | P0 | dgdbg | N3 (m₀ = m₂ = b) | L2 | self or N1(b,b) | AB★ | open; Γ₁ |
| 5 | P2 | gdbab | L2 (m₂ g, m₄ g) | M(O3) | self if Grun, **else kill (bound 3)** | SS3 ∧ Grun | open; Γ₁ |
| 6 | P2 | gddbb | L1(b,g) | M(O5) | self if G01, **else kill (bound 3)** | AB★ ∧ G01 ∧ W34-g | open; Γ₂ (L1(b,a) killed by F-E1′) |
| 6′ | P2 | gddbb | L1(g,a) | M(O4) | self | W34-a (AB★ automatic: w₄ ∈ K_AB, m₄ = a joins w₃) | open; Γ₂ |
| 6″ | P2 | gddbb | L1(g,g) | M(O4) | self | AB★ ∧ W34-g | open; Γ₂ |
| 7 | P2 | dgbag | L4 (m₂ d, m₄ b) | M(O10) | self | SS3 | open; Γ₂ |
| 8 | P2 | dgdbg | L3 (m₂ b, m₄ a) | M(O6) | self | AB★ | open; Γ₁ |
| 9 | P1 | ggdab | O10 | M(L4) | self | **none found** | open; Γ₂ (locally free) |
| 10 | P1 | gdbab | O6 | M(L3) | self if G01; non-DL if exactly one of w₀, w₁ ∈ K_G (bound 2); O7 (killed) if neither (bound 3) | G01 | open; Γ₁ |
| 11 | P1 | dgdbg | O3 | M(L2) | self | AB★ | open; Γ₁ |
| 12 | P1 | ddbbg | O4 (m₃ a), O5 (m₃ d) | M(L1(g,·)); M(L1(b,g)) | self | O4: W23-a (AB★ automatic). O5: AB★ ∧ W23-d | open; Γ₂ |
| 13 | P3 | gdbab | M(L2) | N3 | self if Grun′, else kill (bound 3) | SS4 ∧ Grun′ | open; Γ₁ |
| 14 | P3 | gdbbg | M(L1(b,g)), M(L1(g,a)), M(L1(g,g)) | N1(g,b), N1(b,d), N1(b,b) | as row 6 | mirrors of rows 6, 6′, 6″ (W23 in place of W34) | open; Γ₂ |
| 15 | P3 | dgdab | M(L4) | N4 | self | SS4 | open; Γ₂ |
| 16 | P3 | dgdbg | M(L3) | N2 | self | AB★ | open; Γ₁ |
| 17 | P4 | ddbag | M(O10) | O4 or O5 (m₁ branched) | self | none found | open; Γ₂ (locally free) |
| 18 | P4 | gdbab | M(O6) | O3 | as row 10 | G01 | open; Γ₁ |
| 19 | P4 | ggdbb | M(O4), M(O5) | O10, O10 | self | M(O4): W34-a. M(O5): AB★ ∧ W34-g | open; Γ₂ |
| 20 | P4 | dgdbg | M(O3) | O6 | self | AB★ | open; Γ₁ |

**Reading the table.**
- **No row is killed outright.** Every kill found needs a named path to be absent. This agrees with intern B's closure claim, now with five more moves (G, G0, D2, L1, L2) and the corrected SS. For the lock swaps L1 and L2 I checked only endpoint starvation. It fires exactly when SS4 or SS3 fails, so it adds no new predicate (SA-5).
- **The predicate that recurs is AB★, at 12 states.** It is a single {a,b}-path from an m-vertex (or from w₂, w₄) to w₃. It is the leak the radius-5 certificate shows (intern B cycle 2).
- **Two locally free states**, O10 and M(O10), carry no predicate at all. Any argument must reach them through their neighbours on the cycle.
- **The new predicates W34 and W23 are statements about which side of a lock curve an m-vertex lies on** (§4.2). These are the only predicates here that constrain the lock paths themselves, not just the existence of a leak.

## 4. Lemmas and proofs

### 4.1 Lemma G-image (the G move on the 28 states) [hand, unreviewed]

**Image rule.** G swaps K_G, the {g,d}-component of x₃, which contains x₄. The image has link (a,b,a,d,g), and it is read in the same frame with roles g ↔ d. Hence:
- A ring vertex coloured g or d keeps its role letter if it lies in K_G, and changes letter (g ↔ d) if it does not.
- Ring vertices coloured a or b are unchanged.

*Proof.* A vertex of K_G changes colour g ↔ d, and the roles change g ↔ d too, so its letter is kept. A vertex outside K_G keeps its colour, so its letter flips. ∎

**Local membership in K_G.** The seeds are the g/d outer neighbours of x₃ and x₄: w₂ if it is d, m₃ if it is d, w₄ if it is g, and m₄ if it is g (w₃ ∈ {a,b} is never one). Membership then spreads along runs of consecutive g/d ring vertices. Any other ring vertex is *branched*: it is in K_G iff an outside {g,d}-path joins it to K_G.

**Consequence for a degree-5 x₁.** w₀ and w₁ are adjacent and coloured {g,d}, so they lie in K_G together or not at all, and E1 always survives G.

**Table (base states; the mirrors follow because G commutes with M).**

| state | K_G (local) | branched g/d ring vertices | image |
|---|---|---|---|
| N1(b,b) | x₃ x₄ w₂ w₄ | {w₀,w₁} | self, or N3 if {w₀,w₁} ∉ K_G |
| N1(b,d) | x₃ x₄ w₂ w₄ m₀ w₀ w₁ | none | self |
| N1(g,b) | x₃ x₄ w₂ m₂ w₁ w₀ w₄ | none | self |
| **N2** | **x₃ x₄** (w₂ = b, w₃ = a, w₄ = b) | **none: confined** | **N4** (all g/d letters flip) |
| N3 | x₃ x₄ w₂ w₄ | {w₀,w₁} | self, or N1(b,b) |
| **N4** | **x₃ x₄** | **none: confined** | **N2** |
| L1(b,g) | x₃ x₄ w₂ m₄ | {w₀,w₁} | self, or L3(b,g) (B-starved, so a kill) |
| L1(g,a), L1(g,g) | everything g/d | none | self |
| L2 | x₃ x₄ m₄ | the run {w₀,w₁,m₂} | self, or L4(b,g) (B-starved, so a kill) |
| L3 | x₃ x₄ w₂ w₄ w₀ w₁ (w₄ ~ w₀ at S = 24) | none | self |
| L4 | x₃ x₄ w₄ w₀ w₁ m₂ | none | self |
| O3, O4, O5, O10 | everything g/d | none | self |
| O6 | x₃ x₄ m₃ | w₀ and w₁ **separately** (m₁ = a between them) | self if both are in K_G; non-DL (E1 at x₁ fails) if exactly one is; O7 (B-starved) if neither |

**Proof of the two confinement entries (N2 and N4), written out.**

At N2 (S = 02):
- x₃ has degree 5 and neighbours x₂ (a), x₄ (d), w₂ (b) and w₃ (a).
- x₄ has degree 5 and neighbours x₃, x₀ (a), w₃ (a) and w₄ (b).
- So the {g,d}-component of x₃ is {x₃, x₄}.
- The image has every g/d ring letter flipped: (w₀, w₁, m₀, m₂) = (g, d, d, g) becomes (d, g, g, d). That is N4.

N4 is identical, with the letters flipped back. The swap changes exactly two vertices. ∎

**Proof of the L2 entry.** K_G is locally {x₃, x₄, m₄}. Here m₄ is adjacent to w₃ (a) and w₄ (b) only, inside the ball.
- The ring run w₀ (g), w₁ (d), m₂ (g) is consecutive, so it is all in K_G or all out.
- If it is out, the image has w = dgbab with m₂ = d and m₄ = g, which is L4(b,g).
- In L4(b,g), x₀ (degree 5) has outer neighbours w₄ = b and w₀ = d, with no g. So B-starvation applies, and the radius is ≤ 3 (G, B, fill). ∎

**Proof of the L1(b,g) and O6 entries.** These are the same argument.
- At L1(b,g), the out case gives w = dgdbb with m₂ = b and m₄ = g, which is L3(b,g). It is B-starved: x₀ sees b and d.
- At O6, w₀ and w₁ flip independently.
  - If exactly one flips, x₁'s outer letters (w₀, m₁, w₁) become (x, a, x) for a single letter x, so x₁ lacks g or d and a lock fails at once.
  - If both flip, the result is O7 = (dag, b, d, a, b), which is B-starved. ∎

### 4.2 Lemma W (the w₃ = w₄ = b rule, with its Jordan side form) [hand, unreviewed]

**Setting.** A DL state with deg x₄ = 6, w₃ = w₄ = b, and therefore m₄ ∈ {a, g} (m₄ ≠ d, and m₄ ≠ b since it is adjacent to w₃). This occurs exactly at L1(·,·) (S = 24) and at M(O4), M(O5) (S = 41).

**(W1) Kill rule.**
- If m₄ = a: F(s) is non-DL unless m₄ ∈ K_F.
- If m₄ = g: G0(s) is non-DL unless m₄ ∈ K₀.

*Proof.*
- Both F and G0 put the new middle at x₄ with roles (b′, g′, d′) = (d, b, ·). F has d′ = g, and G0 has d′ = a.
- E1 at the new middle requires x₄ to have a neighbour of colour d′ after the move.
- The neighbours of x₄ are v, x₃, x₀, w₃, m₄, w₄.
  - x₃ ∈ K_F, so F makes it a. x₃ ∉ K₀, so it stays g under G0.
  - x₀ ∉ K_F, so it stays a under F. x₀ ∈ K₀, so G0 makes it g.
  - w₃ and w₄ are b and untouched.
- **Case F.** x₄ has a g-neighbour after F iff m₄ was a and lies in K_F, or m₄ was g and lies outside K_F.
- **Case G0.** x₄ has an a-neighbour after G0 iff m₄ was g and lies in K₀, or m₄ was a and lies outside K₀.
- If m₄ = a, G0 is harmless, and F needs m₄ ∈ K_F. If m₄ = g, F is harmless, and G0 needs m₄ ∈ K₀. ∎

**(W2) Jordan side lemma.** Let P be any lock-2 path, that is, a {b,d}-path x₁ → x₄ in T − v. Let C = v x₁ P x₄ v.
- If P enters x₄ through w₃, then m₄ lies on x₀'s side of C, so m₄ ∉ K_F.
- If P enters through w₄, then m₄ lies on x₃'s side, so m₄ ∉ K₀.

*Proof.*
- The rotation at x₄ is (v, x₃, w₃, m₄, w₄, x₀). C uses the edges x₄v and x₄w_e, where w_e ∈ {w₃, w₄} is the entry vertex.
  - For e = 3, the two angular sectors at x₄ are {x₃} and {m₄, w₄, x₀}.
  - For e = 4, they are {x₃, w₃, m₄} and {x₀}.
- m₄ is not on C, because it is coloured a or g. Neighbours of x₄ in one sector lie in one face of C.
- The rotation at v puts x₀ on one side of C and x₂, x₃ on the other (HP Jordan fact).
- K_F is a connected {a,g}-set that contains x₂ and avoids C (C carries only v, b and d). So K_F lies on x₂'s side. Likewise K₀ lies on x₀'s side. ∎

**(W3) Cut form.** In a targetless class:
- if m₄ = a, no lock-2 path enters x₄ through w₃. Equivalently, w₃ is not joined to x₁ in K₂ − x₄.
- if m₄ = g, no lock-2 path enters through w₄. Equivalently, w₄ is not joined to x₁ in K₂ − x₄.

*Proof.* Combine W1 and W2. For the equivalence: a lock-2 path entering through w_e gives, by deleting x₄, a path from x₁ to w_e in K₂ − x₄. Conversely, a simple path from x₁ to w_e in K₂ − x₄, followed by the edge to x₄, is a lock-2 path. ∎

**Mirror (W′).** For deg x₃ = 6 and w₂ = w₃ = b, so that m₃ ∈ {a, d}:
- if m₃ = a, B is non-DL unless m₃ ∈ K_B, which forces w₃ to be cut from x₁ in K₁ − x₃;
- if m₃ = d, D2 is non-DL unless m₃ ∈ K_D2, which forces w₂ to be cut from x₁ in K₁ − x₃.

This occurs at O4, O5 and M(L1(·,·)).

**Remark.** W gives the first predicates in this class that **restrict the lock paths themselves**. A targetless class must route every lock-2 path into x₄ on one prescribed side of m₄. In the certificate graph, the target of computation item 3 (§7) is whether this routing ever fails on a Γ₂ cycle.

### 4.3 Lemma SS3/SS4 (silent starvation at a degree-5 singleton, corrected form) [hand, unreviewed]
**SS3.** Let x₃ have degree 5, with w₂ = b and w₃ = a (so w₂ is the only b-neighbour of x₃). If w₂ ∉ K₂, then swapping the {b,d}-component Y of w₂ gives a non-DL state, so the radius is ≤ 2.

*Proof.*
- Y meets no link vertex. The only {b,d} link vertices are x₁ and x₄, and both are in K₂.
- The Math-lead fix requires Y ∩ N(x₃) = {w₂}. The d-neighbours of x₃ are only x₄ (degree 5: its neighbours are x₂, x₄, w₂, w₃). And x₄ ∉ Y.
- After the swap, x₃ has no b-neighbour, so lock 1 fails. ∎

SS4 is the mirror statement. I checked the hypotheses at N2, N4, L2 and L4 (SS3), and at N2, N4, M(L2) and M(L4) (SS4); the L4 case is in the next line. At L4, Y ⊇ {w₂, m₂}, and m₂ is not adjacent to x₃, so the fix condition still holds.

**Negative checks (where SS is locally blocked)** [hand]:
- L2 at x₄: w₄'s {b,g}-component contains m₄, which is a g-neighbour of x₄.
- L4 at x₄: m₄'s {a,b}-component reaches w₂ and then x₂; its {b,g}-component contains w₄, which is a g-neighbour of x₄.
- O6 and O10 at x₄: w₄ is adjacent to w₀ (g), and w₀ is adjacent to x₁.
- O10 at x₃: m₃'s {a,b}-component runs w₃, w₄, x₀; its {b,d}-component contains w₂, which is a d-neighbour of x₃.

These are why O10 is "locally free".

### 4.4 Automatic AB★ [hand, unreviewed]
At L1(g,a), AB★ holds automatically:
- w₄ = b is adjacent to x₀, so w₄ ∈ K_AB.
- m₄ = a is adjacent to w₄, so m₄ ∈ K_AB.
- w₃ is adjacent to m₄, so w₃ ∈ K_AB.

At O4 the same happens through w₂ (b, adjacent to x₂), then m₃ (a), then w₃. So AB never kills at these two states, whatever the outside looks like. ∎

### 4.5 Lemma LC (lock chain along F) [hand, unreviewed]
Let s be DL and suppose F(s) is DL. Then **lock 1 of F(s) is the same set as lock 2 of s**: the same vertex set with the same colours. In particular, K₁(F(s)) = K₂(s).

*Proof.*
- F exchanges a and g on K_F, so the {b,d}-subgraph of T − v does not change.
- The roles of F(s) are b′ = d and g′ = b, so lock 1′ is the {b,d}-component of x′₁ = x₄, which is K₂(s). ∎

The mirror statement: lock 2 of B(s) is lock 1 of s.

**Consequence: W3 propagates one step.**
- Let W34-a hold at s. That is, w₃ is cut from x₁ in K₂ − x₄.
- In F(s) this reads: w′₀ is cut from x′₃ in K₁′ − x′₁, where x′₁ = x₄, x′₃ = x₁ and w′₀ = w₃.
- So every lock-1 path of F(s) leaves the middle x′₁ through w′₁ = w₄, never through w′₀.
- For L1(g,a) → M(O4), the outer neighbours of the middle of M(O4) are (w₀, m₁, w₁) = (g, d, g). The inherited constraint says that **of the two g-exits of the middle, only w₁ is used by lock 1**.
- This constraint is not a one-move kill, because no Kempe component can be swapped to exploit a cut inside K₁. It is a **memory** constraint carried along the cycle. That is exactly the kind of information the vdred_joint depth-14 result is reported to use ([guidance], MathTwoSixNeighbours §5).

## 5. Exact open target [open]

**Lemma C★.** Let Q be a targetless class at a (5,5,6,5,6) hole of a triangulation with no separating triangle. By §2, Q contains a Γ₁ F-cycle Z₁ and a Γ₂ F-cycle Z₂, each of length divisible by 30, joined by confined G at N2 ↔ N4. Lemma C★ claims the following set of conditions **cannot all hold** in a plane triangulation:
- the predicates of §3 at every state of Z₁ and Z₂;
- the four-path coupling of §2.4 at every N2/N4 pair;
- the inherited exit constraints of §4.5 at every successor of a W-state.

Candidate first steps toward it:
- **(C★-a)** On Z₂, the W-states come in the order L1 → M(O4|O5) → … → O4|O5 → M(L1) within each 10-step period, so there are four cut constraints per period. By Lemma LC, two of them sit on the same lock component, seen from two consecutive frames. A plane argument that two consecutive cut constraints force one swap from §2.3 to fail would kill every Γ₂ cycle. By Lemma Γ(3), that would kill every targetless class.
- **(C★-b)** On Z₁ the only predicates are AB★ (6 states per period), SS3/SS4/Grun (L2, M(L2), N2) and G01 (O6, M(O6)). The certificate shows that AB★ can hold at every state (all {a,b} connected). So any proof on Z₁ must use SS and Grun, and these are what the certificate's fill exploits at M(L2).

I could not prove C★-a or C★-b. §6 records why the single-state versions fail.

## 6. Self-attacks [hand]

- **SA-0 (is the target true at all?).** Attack: a targetless class at a (5,5,6,5,6) vertex of a diamond-free, no-separating-triangle triangulation.
  - I cannot build one by hand. The obstruction found today (frozen classes are never DL) rules out only the most rigid kind.
  - Tilley's paper (as cited by the team, *Mathematics* 6(12):309, 2018) studies exactly Kempe-locking at degree-5 vertices. [memory] My recollection is that he conjectures every Kempe-locked triangulation contains a Birkhoff diamond.
  - If so, then in the diamond-free frame Lemma R\* at (5,5,6,5,6) is a special case of an open conjecture. That is why I do not expect a short local proof.
  - **Unresolved; this is computation item 1.**
- **SA-1 (Lemma O).** Can an F-cycle have length 5 or 10 in exact colours?
  - The frame is unique: four colours on five vertices give exactly one repeated colour, on a non-adjacent pair, so the middle is unique.
  - The triple (β, γ, δ) rotates with order 3, so length 5 or 10 would return a permuted link. **Survives.**
  - Weak point: "B(F(s)) = s" assumes F(s) is DL. If F(s) is not DL, the orbit simply ends, which is the path case.
- **SA-2 (G-table).** Tried coincidences among ring vertices, for example m₄ = w₁. This creates a 4-cycle v x₁ w₁ x₄, which is allowed.
  - The confinement at N2/N4 reads only the colours of the five listed neighbours of x₃ and x₄, so it is immune.
  - At L1/L2, a coincidence can only merge runs, which turns "branched" into "forced in". That removes kills; it never creates them. The listed kills therefore remain conditional, as stated. **Survives.**
- **SA-3 (Lemma Γ coupling as a contradiction).** I tried to show that paths (i)–(iv) of §2.4 cannot coexist. **Failed; I built a counter-picture.**
  - Put one b-vertex z outside the ring.
  - Join z to w₀ and to w₂ through g-vertices, and to w₁ and to w₄ through d-vertices. This is a cone over the ring, so it is plane.
  - All four paths go through z. Hence no contradiction comes from one N2/N4 pair, which matches Math's single-state negative at O6.
- **SA-4 (Lemma W).**
  - (a) Could a lock-2 path enter x₄ through m₄, x₀ or x₃? No: their colours are a/g, a and g.
  - (b) Could m₄ lie on the lock-2 curve C? No: it is a or g.
  - (c) Coincidence m₄ = w₁. Then m₄ = w₁ is g and adjacent to x₂ (a), so m₄ ∈ K_F, so m₄ ∉ K₀, and W1 kills by G0. That is consistent with W2, since the prediction is a kill.
  - (d) Is W1's F-part the same as Math's F-E1′? For m₄ = a, yes. The G0 half and the m₄ = g case are new.
  - **Survives.**
- **SA-5 (lock swaps L1 and L2).** I first thought their endpoint conditions never fire here. **Corrected on checking:**
  - After the L2-swap, x₃ needs a d-neighbour. x₄ (d) is in K₂ and turns b, so the only candidate is w₂ (b), which turns d iff w₂ ∈ K₂. So L2-swap kills exactly when SS3 fails.
  - Likewise the L1-swap kills exactly when SS4 fails.
  - So **SS3 and SS4 also follow from the lock swaps, with no appeal to the corrected Lemma SS.** This is a cleaner proof of the same predicates, and it does not need the Math-lead fix.
  - When w₃ = b (or w₂ = d), the swap is harmless.
- **SA-6 (Grun).** Could the run {w₀, w₁, m₂} be split? No: it consists of consecutive ring vertices coloured g, d, g, which are pairwise adjacent along the ring. **Survives.**
- **SA-7 (whole Γ₁ cycle).** Can all Γ₁ predicates hold along a 30-cycle? AB★ holds everywhere in the certificate's class. The certificate's fill used the **failure** of SS4 at M(L2). I found no reason why an adversary cannot leak SS4 too. **Open; this is computation item 2.**

## 7. Computations requested (for the coordinator's machine; nothing was run here)

All of these are fresh scripts, stdlib only, with no producer imports. Each item gives its input, what to compute, the expected result, and what would kill which claim.

1. **Targetless-class search (most important).**
   - Input: plantri triangulations with minimum degree 5 and no separating triangle (`-m5 -c4`), orders 12 to 24 (larger as the budget allows). Filter to those with a degree-5 vertex v whose link degrees are (5,5,6,5,6) up to rotation and reflection. Flag diamond-free graphs separately (no edge of two degree-5 vertices whose two common neighbours both have degree 5).
   - Compute the Kempe classes of the proper 4-colourings of T − v, up to colour permutation, by union–find over whole-component swaps. Report any class with no filled state.
   - Expected: none. **One example kills R\* for the class** and the front-1 target as stated. Report it with its face list and one colouring.
   - Budget: one core, about one hour, stopping at the first order that exceeds 20 minutes.
2. **F-cycle census.**
   - Input: the same graphs, plus the Phase C cert graphs and the (5,5,6,5,6) holes in studiointel's tables.
   - Compute: for every DL state, follow F and B on exact colourings, and report every orbit that closes (a cycle) with its length.
   - Expected: every cycle length ≡ 0 (mod 15) (Lemma O), and ≡ 0 (mod 30) when Math's Γ-tables are right (Lemma Γ).
   - **Kills:** a cycle length not divisible by 15 kills Lemma O. A cycle of length 15 (odd multiple) kills Lemma Γ(2) or Math's Γ-tables.
   - Also report the fraction of DL states lying on cycles. If it is always 0, the conjecture "no F-cycles at (5,5,6,5,6)" is the right target, and it would prove R\* by Lemma O.
3. **Predicate audit.**
   - For every DL state at (5,5,6,5,6) holes in the data, compute:
     - its pattern, and assert it is one of the 49 admissible patterns;
     - for each of the 28 survivors, the truth value of each predicate of §3;
     - whenever a predicate is false, the named kill sequence (G, then B; F; G0; D2; SS3/SS4 swap or lock swap; AB), asserting that it reaches a non-DL state within the bound in §3.
   - **Kills:** a false predicate without the predicted kill kills the corresponding lemma (§4.1–§4.4).
   - Additionally, at every W-state, compute both sides of W3 (membership m₄ ∈ K_F or m₄ ∈ K₀, and the cut condition) and assert they are equal. A mismatch kills Lemma W2.
4. **G-table check.**
   - For every DL state, compute K_G, apply G, and compare the image pattern with §4.1.
   - Assert K_G = {x₃, x₄} at every N2 and N4 state.
   - Kill: any mismatch.
5. **Lock chain check.** For every DL s with F(s) DL, assert K₂(s) = K₁(F(s)) as vertex sets. A failure kills Lemma LC. Trivial to run.
6. **Certificate replay.** On `91a307d1852a1764` hole 22 (cert/ directory), along Math's 5-swap witness walk (s, s₋₁, s₋₂, s₋₃), print the §3 pattern and the predicate values at each state.
   - Expected: AB★ true at the dgdbg states, and SS4 false at s₋₃ = M(L2), which matches Math.
   - Also print the radius of the L2-swap move at s₋₃. Expected 2 (SA-5); otherwise SA-5 is wrong.

## 8. Ledger

- **[hand, unreviewed]:**
  - Lemma O, with the exact period 15;
  - the move catalogue (§2.3) and the G0/D2 starvation rules;
  - Lemma Γ(3) (the N2 ↔ N4 link) and the 30-divisibility given Math's tables;
  - the G-table (§4.1);
  - Lemma W (W1–W3 and the mirror W′);
  - SS3/SS4 together with the lock-swap proof (SA-5);
  - automatic AB★ (§4.4);
  - Lemma LC and its consequence;
  - the 28-state re-derivation;
  - the §3 table.
- **[cited]:** Math's F/B transition tables and Γ₁, Γ₂ (MathTwoSixNeighbours §5); intern B's AB★; Math's SS predicates at Γ₁; Unlock; the Jordan facts; Lemma Q.
- **[memory]:** the content of Tilley's conjecture (SA-0).
- **[open]:** R\* for (5,5,6,5,6); Lemma C★; the "no F-cycles" conjecture.
- **Nothing here is machine-checked or second-read.** The likeliest slips are in the §3 predicate column (about 60 hand component checks) and in the S = 13 G-entries.
