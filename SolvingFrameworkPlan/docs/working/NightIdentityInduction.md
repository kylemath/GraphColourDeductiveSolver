# Night attempt: induction through the class identity

Research worker (night), written 7 October 2026 at 00:17. This is hand reasoning plus small single-core stdlib checks. The scripts live in the session scratchpad and are not committed; §6 says how to rebuild them. **Nothing here proves the quarter floor, R\*, or any class-level floor.**

Labels:
- [proved]: a complete argument is given, modulo the reviewed tables of `MathQuarterFloorBijections.md` §1–§2 (cited as **QFB**).
- [sketch]: an argument with a named gap.
- [conjecture]: not proved.
- [data]: computed here. All counts are up to renaming, over every degree-5 hole of gentri at the stated orders.

**Prior art, read after my first computation.** `NightEulerHole.md` (Lemma Π, Theorem W, Lemma N) and `NightWindingMeander.md` already contain the "closed unit" of idea 1, namely the π-cycles, together with the mod-5 law and the no-potential lemma that settles idea 3. I re-derived them independently (§1) and only cite them below. My new content is:
- the unit-graph transport data (§1.3);
- the merge-induction analysis (§2), which is new;
- the circularity and torus checks (§4).

---

## 1. Idea 1: closed units

### 1.1 The units are the π-cycles [proved; = NightEulerHole Lemma Π]

QFB §1 gives every state exactly two link-pattern-changing slots. The five QFB bijections (φ_A, φ_B, R₊₃, R₊₂ = R₊₃⁻¹, τ) pair every slot with exactly one other slot. So:
- the slot graph Σ is 2-regular, and in fact directed: the out-slots are {u2, f3} and the in-slots are {u1, f2};
- each Kempe class splits into Σ-cycles;
- these are the smallest sub-structures closed under Lemma A's maps, R₊₂, R₊₃ and τ.

Regrouping QFB's identity by cycle gives, for a cycle Z with r_Z unfilled runs and L_Z long bits:

  val(Z) := 3F_Z − U_Z = Σ_{runs in Z} (3 − ℓ) + 1.5·L_Z.

Here ℓ is the run length. N₀ states are runs with ℓ = 1, Γ-paths with d interior DL states have ℓ = d + 2, and a Γ-cycle is a whole Σ-cycle with val = −|Z|.

**Index advance.** Each step adds a fixed amount to the link index (mod 5):
- +3 out of an unfilled state (R₊₃, or φ_B⁻¹: U_j → F_{j+3});
- +1 out of a filled state (φ_A, or τ).

So F_Z + 3U_Z ≡ 0 (mod 5), and therefore **val(Z) ≡ 0 (mod 5)**. This is NightEulerHole's Corollary 1, which reaches it via token sums.

[data] My code found Σ 2-regular and mutual with 0 failures, and every unit ≡ 0 mod 5, over:
- orders 12–22: 14,109 classes and 185,547 units;
- order 23: 31,795 classes and 559,372 units.

### 1.2 Unit non-negativity is false [data; consistent with NightEulerHole]

**Order-17 floor class (gentri 17 #1, hole 0; 64 states, F = 16).** It has six units: lengths 4, 4, 4, 8, 16 and 28, with F = 1, 1, 1, 2, 4 and 7. **Every unit has val = 0.**
- The d = 9 and d = 5 DL chains sit in the 28-unit and the 16-unit.
- They are paid exactly by N₀ runs inside the same unit.
- So in this class the floor *is* a sum of non-negative units. That makes it the wrong place to look for a counterexample.

**First negative units:**

| order, gentri, hole | negative unit | val | rest of class |
|---|---|---|---|
| 17 #3, holes 0 and 16 | pure Γ-cycle, \|Z\| = 20, F = 0 | −20 | one unit, val +80 |
| 20 #58 h18 and 20 #60 h19 | mixed: \|Z\| = 21, F = 4 | −5 | first mixed negative unit |
| 21 #96 h2 and 21 #134 h0 | \|Z\| = 14, F = 1 | −10 | |

Counts of negative units:
- order 22: 17 negative units in 17 classes (3 of them pure Γ-cycles);
- order 23: 13 negative units in 13 classes (1 of them a Γ-cycle);
- never more than one negative unit per class.

Together with the all-DL rotation cycles of length up to 880 (flipped A₇; not re-run here), this means **"each closed unit has RHS ≥ 0" is false** [data]. Any proof must move charge between units.

### 1.3 Transport between units [data, new]

Make each class a unit graph: two units are adjacent iff some Kempe swap joins one of their states. The swap is necessarily link-pattern-preserving, since every pattern-changing swap stays inside a unit.

For each class with a negative unit I solved the transport problem as a max-flow: the deficit −val is to be paid from the surplus of positive units within unit-graph distance r.

- **Orders 17–23: in all 36 such classes, r = 1 suffices.**
- The adjacent surplus is 120–280 against a deficit of 5–20.
- The eccentricity of the negative unit is 1–3.

**Caveat.** This is weak evidence, and I report it as such. Negative-winding units are huge (for example 153 states), so radius 1 in the unit graph is cheap. The known growth of the matching radius (6 pooled at order 24) lives *inside* the units, not between them.

## 2. Idea 2: merge induction at a second vertex w

### 2.1 The exact decomposition [proved]

**Setup.**
- Let w ∉ N[v] have degree 5, with link y₀..y₄.
- Let E_k be the set of states of G = T − v with c(y_k) = c(y_{k+2}).
- Let T_k = (T − w)/(y_k ≡ y_{k+2}). This is a planar triangulation with n − 2 vertices; v has degree 5 and an unchanged link.

**Double cover.** The link of w avoids c(w), so it is a proper 3-colouring of C₅. That colouring has exactly two equal distance-2 pairs, so every state lies in exactly two of the E_k. Hence, for every class C of G:

  **2·val(C) = Σ_k val(C ∩ E_k).**

**Restriction map.** ρ_k : E_k → states(T_k − v) is injective. Its image is exactly the set of colourings of T_k − v whose w-link uses 3 colours. The colourings in which the w-link uses 4 colours are the ones that are **unfilled at w**.

**Induction step.** Let Ĉ_k be the union of the T_k-classes that meet ρ_k(C ∩ E_k), and let X_k = Ĉ_k ∖ ρ_k(C ∩ E_k). The induction hypothesis on T_k gives val(Ĉ_k) ≥ 0, so

  2·val(C) ≥ −Σ_k val(X_k).

The step closes iff Σ_k val(X_k) ≤ 0.

### 2.2 Which term fails [data, orders 12–19; 15,036 (class, w, k) slices]

1. **X_k is never small, and it has the wrong sign.**
   - X_k = ∅ in only 42 of the 15,036 slices.
   - val(X_k) > 0 in 14,441 slices.
   - X_k consists of colourings unfilled at w, together with (in 192 slices) images of *other* G-classes that T_k merges in.
   - **Example (17 #1, hole 0, the floor class).** At w = 14, k = 3: the slice has val = −11, the T_k class is exactly at the floor (val = 0), and X_k has val = +11. **A floor-tight class of the smaller graph contains a slice strictly below the floor.**
   - Over all w and k of this class, slice values range over −11…+12, while Ĉ_k values range over 0…30.
2. **The slices are not unions of units.** Slice values are 1, −4, −7, −11, 12, 22, 24, 26, and so on, not ≡ 0 mod 5. So the π-cycles of C are cut by E_k: a π-move can change the colours on w's link. Meanwhile val(Ĉ_k) ≡ 0 mod 5 in T_k, as Theorem W predicts.
   - So the terms N₀, L_F, d(P) and D_cyc have **no restriction** to slices.
   - Locks move in both directions under T → T_k: deleting w can break a lock path through w, and identifying y_k ≡ y_{k+2} can create one. So none of the RHS terms is monotone under the merge, in either direction [sketch, with one example of each direction in mind; not enumerated].
3. **The slices are not even class-closed.** In 350 of the 15,036 slices, C ∩ E_k meets 2 or more T_k-classes. Merging coarsens the classes of G − w, but slicing by E_k can disconnect them.

**Verdict [proved as a reduction, data for the sign].** The merge induction turns "floor for T at v" into "Σ_k val(X_k) ≤ val-type bound". That is a statement about the **two-hole** graph T − v − w restricted to states unfilled at w. It is not weaker than the original. The quantity that fails is exactly the unfilled-at-w part X_k: it is positive in 96 % of slices, and the hypothesis on T_k cannot see it.

## 3. Idea 3: weights

**Lemma N (NightEulerHole) settles telescoping [proved].**
- Any weight that moves charge only along slot moves (π^{±1}) preserves each unit's total.
- A unit with val < 0 exists from order 17 (§1.2).
- So no weighting along Γ-paths can work, including global weights such as "proportional to path length".

A weighting must therefore move charge along **pattern-preserving** swaps, between units. The only shape that survives is a transport between units (§1.3). There, the data show radius 1 in the unit graph up to order 23.

## 4. Circularity and the torus

**Circularity.** In a targetless class (Theorem A) every unit is a Γ-cycle with val < 0, and there is no positive unit to pay. So the transport lemma below forbids targetless classes. **It implies R\* and hence has 4CT strength.** It is not an easier lemma, only a sharper location.
- Test at 17 #3: the Γ-cycle (−20) is adjacent only to the +80 unit, via t-chain swaps (NightWindingMeander §3). The lemma holds there.
- Test at the length-880 all-DL cycles (flipped A₇): not run. That is the obvious next check of the lemma.

**Torus (coordinator input; n = 16 frozen example, local-runs/18-torus-floor) [data].**
- On this graph the slot structure breaks:
  - L2 fails: there are states with lock 2 but R₊₃ undefined, including the frozen DL state;
  - 4 of the 11 states have non-mutual slots.
- The two classes have val = 14 and −1, neither ≡ 0 mod 5.
- So §1.1 uses planarity, as it must, through pd2's non-crossing pairing.
- §2.1 is surface-free, and §2.2 is a failure, so neither proposes a lemma that the torus could falsify.
- The transport lemma is vacuous on the torus, where there are no units. So planarity would have to enter it a **second** time, globally, which agrees with NightEulerHole §4.

## 5. Most promising next lemma [conjecture]

**Transport Lemma T.** In every Kempe class at a degree-5 hole of a planar triangulation, every π-cycle Z with w(Z) > 0 is joined, by a single link-pattern-preserving Kempe swap (in practice a t-chain: {α,μ} or {A,B}, or a chain off the link), to π-cycles of negative winding whose total surplus is at least 5·w(Z). The assignment must be injective across the positive cycles of the class.

- [data] Holds with radius 1 on all 36 positive cycles, orders 17–23.
- Lemma T implies the floor, so it has 4CT strength.
- Its first sub-case is NightWindingMeander's Conjecture E_t, "every positive cycle has an escape into a negative cycle", which is weaker because it carries no capacity.
- Lemma T is the cleanest place where a planarity-based global argument (Jordan or Heawood parity along the token meander) would have to bite.

## 6. Reproduction (scratchpad, stdlib, on `local-runs/common/kempe_py.py`)

- `sigma.py`: slots, the 2-regular check and Σ-cycle values.
- `units.py`: the mod-5 check, negative units, and unit-graph max-flow transport radius (order 23 took 15 min on one core).
- `merge2.py` and `mscan.py`: for T_k = (T − w)/(y_k ≡ y_{k+2}), compute the slices C ∩ E_k, the hit T_k-classes Ĉ_k, and the extras X_k.
- `torus_test.py`: the slot structure on the n = 16 frozen torus example.
