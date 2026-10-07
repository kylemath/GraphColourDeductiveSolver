# NightK4Hypotheses — the exact hypotheses of `sigma_exit_not_DL_k4`

*Long Table, 2026-10-07 06:44. Purpose: reconcile Studio Job BL (1,037,102 Studio-R3 DL states at
word 55556, k = 4, with a DL σ-image) with the compiled theorem `sigma_exit_not_DL_k4`
(`StudioMathLean/.../QuarterSigmaK34.lean`). Lean companion: `QuarterR3AtUnfold.lean` (new,
0 sorry, standard axioms only, appended to `check.sh`).*

**Bottom line.** On a triangulation with link degrees 55556 in rotation order (degree-6 vertex at
x_{j+4}), `K4Ball` holds automatically. Given DL and the Studio's typing (w₀ = B, w₃ = μ),
properness forces w₁ = A and w₂ = B, and leaves **w₄ ∈ {A, μ}**. `R3At` requires **w₄ = A**. So the
only hypothesis the Studio does not check is `c(w_{j+4}) = A`. The 1,037,102 states should all
have `c(w_{j+4}) = μ` (= c(w_{j+3})). Lean's own docstring in `QuarterGammaPeriod` already says
this: at `R3k4`, "locally `z` may have colour `μ`" (z = w_{j+4}). Prediction for Job BU: on all
1,037,102 states, w₄ = μ; on the other 10,859,977 states, w₄ = A and the σ-image is never DL.

Notation, relative to the repeat index j: link `x_j..x_{j+4}` coloured `(α, μ, α, A, B)`, with
α = c(x_j), μ = c(x_{j+1}), A = c(x_{j+3}), B = c(x_{j+4}). Outer ring `w_t` is the third vertex
of the far face on the edge `x_t x_{t+1}`. "Index i" below means j + i (mod 5).

## 0. The theorem

```lean
theorem sigma_exit_not_DL_k4 (K : K4Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) : ¬ DLState P (sigSwap P c j)
```

`ProperOff G h c`: `∀ u v, G.Adj u v → u ≠ h → v ≠ h → c u ≠ c v` (a proper 4-colouring of G − h).
`DLState P c := ∃ j, DoublyLocked P c j`; since σc has repeat index j again (`sigSwap_basic`),
this is `Lock1 (σc) j ∧ Lock2 (σc) j` (`dl_rep`). The proof shows Lock 1 of σc fails.
`Pent M.graph h`: x : Fin 5 → V injective, h ~ x_i, x_i ~ x_{i+1}, and every neighbour of h is
some x_i (so deg h = 5).

## 1. `K4Ball P w m j`, field by field

```lean
structure K4Ball (P : Pent M.graph h) (w : Fin 5 → Fin n) (m : Fin n) (j : Fin 5) : Prop where
  tri : TripleBallP P w j
  nbr3 : ∀ u, M.graph.Adj (P.x (j + 3)) u ↔
    u = h ∨ u = P.x (j + 2) ∨ u = P.x (j + 4) ∨ u = w (j + 2) ∨ u = w (j + 3)
  nbr4 : ∀ u, M.graph.Adj (P.x (j + 4)) u ↔
    u = h ∨ u = P.x (j + 3) ∨ u = P.x j ∨ u = w (j + 3) ∨ u = m ∨ u = w (j + 4)
  ring23 : M.graph.Adj (w (j + 2)) (w (j + 3))
  ring3m : M.graph.Adj (w (j + 3)) m
  ringm4 : M.graph.Adj m (w (j + 4))
  off3 : ∀ i, w (j + 3) ≠ P.x i
  offm : ∀ i, m ≠ P.x i
  offh : w (j + 3) ≠ h ∧ m ≠ h
```
with
```lean
structure TripleBallP (P : Pent M.graph h) (w : Fin 5 → Fin n) (j : Fin 5) : Prop where
  nbr0 : ∀ u, M.graph.Adj (P.x j) u ↔
    u = h ∨ u = P.x (j + 4) ∨ u = P.x (j + 1) ∨ u = w (j + 4) ∨ u = w j
  nbr1 : ∀ u, M.graph.Adj (P.x (j + 1)) u ↔
    u = h ∨ u = P.x j ∨ u = P.x (j + 2) ∨ u = w j ∨ u = w (j + 1)
  nbr2 : ∀ u, M.graph.Adj (P.x (j + 2)) u ↔
    u = h ∨ u = P.x (j + 1) ∨ u = P.x (j + 3) ∨ u = w (j + 1) ∨ u = w (j + 2)
  ring40 : M.graph.Adj (w (j + 4)) (w j)
  ring01 : M.graph.Adj (w j) (w (j + 1))
  ring12 : M.graph.Adj (w (j + 1)) (w (j + 2))
  adj4 : M.graph.Adj (P.x (j + 4)) (w (j + 4))
  adj3 : M.graph.Adj (P.x (j + 3)) (w (j + 2))
  off : ∀ i, w (j + 4) ≠ P.x i ∧ w j ≠ P.x i ∧ w (j + 1) ≠ P.x i ∧ w (j + 2) ≠ P.x i
  offh : w (j + 4) ≠ h ∧ w j ≠ h ∧ w (j + 1) ≠ h ∧ w (j + 2) ≠ h
```

In words:
- **Neighbourhoods (exact, "iff").** N(x₀) = {h, x₄, x₁, w₄, w₀}; N(x₁) = {h, x₀, x₂, w₀, w₁};
  N(x₂) = {h, x₁, x₃, w₁, w₂}; N(x₃) = {h, x₂, x₄, w₂, w₃}; N(x₄) = {h, x₃, x₀, w₃, m, w₄}.
  Because these are "iff", x₀..x₃ have degree ≤ 5 and x₄ degree ≤ 6. They are exactly 5 and 6
  once the listed vertices are distinct. The distinctness follows from the `off` fields below:
  the w's and m are not link vertices and not h.
- **Ring adjacencies.** w₄~w₀, w₀~w₁, w₁~w₂, w₂~w₃, w₃~m, m~w₄. So the outer path of the degree-6
  vertex x₄ is (x₃,) w₃, m, w₄ (, x₀). There is **no** w₃~w₄ edge: m sits between them.
- **Extra adjacencies.** x₄~w₄ and x₃~w₂ (these are also implied by nbr4/nbr3).
- **Off-link / off-h (non-coincidence).** w₀, w₁, w₂, w₃, w₄, m ≠ every x_i, and ≠ h. This
  excludes coincidences like w_s = x_{s+3}. It does **not** say the w's are pairwise distinct or
  distinct from m. The proof never needs that.
- Nothing is assumed about the neighbourhoods of w's or m.

## 2. `R3At P w c j`, exactly

```lean
def R3At (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  DoublyLocked P c j ∧ c (w j) = c (P.x (j + 4)) ∧ c (w (j + 1)) = c (P.x (j + 3)) ∧
    c (w (j + 2)) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x (j + 1)) ∧
    c (w (j + 4)) = c (P.x (j + 3))
```
That is, DL at j **and the full ring (w₀, w₁, w₂, w₃, w₄) = (B, A, B, μ, A)**: five colour
equalities, not two. Its sub-part `OuterBABA` = (w₀, w₁, w₂, w₄) = (B, A, B, A) is what the proof
uses (via `lock1_after_sigma_iff` → `sigma_component_iff`). It makes the σ-component exactly
{x₀, x₁, x₂}. In particular **w₄ = A is needed so that the {α, μ}-component of x₁ does not leak
out of x₀ through w₄**.

Unfolded (Lean: `r3At_iff`, proved by `Iff.rfl`):
```
RepeatAt:  c x0 = c x2, c x1 ≠ c x0, c x3 ≠ c x0, c x4 ≠ c x0,
           c x1 ≠ c x3, c x1 ≠ c x4, c x3 ≠ c x4
Lock1:     x1 ⇝ x3 in pairGraph(G, h, c, μ, A)
Lock2:     x1 ⇝ x4 in pairGraph(G, h, c, μ, B)
Ring:      c w0 = c x4, c w1 = c x3, c w2 = c x4, c w3 = c x1, c w4 = c x3
```

## 3. Locks, `DoublyLocked`

```lean
def RepeatAt (c : V → Fin 4) (j : Fin 5) : Prop :=
  c (P.x j) = c (P.x (j + 2)) ∧
  c (P.x (j + 1)) ≠ c (P.x j) ∧ c (P.x (j + 3)) ≠ c (P.x j) ∧ c (P.x (j + 4)) ≠ c (P.x j) ∧
  c (P.x (j + 1)) ≠ c (P.x (j + 3)) ∧ c (P.x (j + 1)) ≠ c (P.x (j + 4)) ∧
  c (P.x (j + 3)) ≠ c (P.x (j + 4))
def Lock1 (c : V → Fin 4) (j : Fin 5) : Prop :=
  (pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable (P.x (j + 1)) (P.x (j + 3))
def Lock2 (c : V → Fin 4) (j : Fin 5) : Prop :=
  (pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable (P.x (j + 1)) (P.x (j + 4))
def DoublyLocked (c : V → Fin 4) (j : Fin 5) : Prop :=
  RepeatAt P c j ∧ Lock1 P c j ∧ Lock2 P c j
```
`pairGraph G h c a b`: edges uv of G with u, v ≠ h and both coloured in {a, b}. So:
- Lock 1: a {μ, A}-Kempe chain in G − h from x_{j+1} to x_{j+3}.
- Lock 2: a {μ, B}-Kempe chain in G − h from x_{j+1} to x_{j+4}.

## 4. `sigSwap` (σ) — and not `sigma`

```lean
noncomputable def sigSwap (c : Fin n → Fin 4) (j : Fin 5) : Fin n → Fin 4 :=
  kswap M.graph h c (c (P.x j)) (c (P.x (j + 1))) (P.x (j + 1))
-- kswap G h c a b s := swap c a b {v | (pairGraph G h c a b).Reachable s v}
```
σ swaps α ↔ μ on the whole **{α, μ}-component of x_{j+1}** in G − h. That component always contains x₀, x₁, x₂.
Under R3At it is **exactly** {x₀, x₁, x₂} (`sigma_component_iff`). Do not confuse it with
`QuarterPi.sigma`, which is the token sum (`2j+1` on U_j, `2i+4` on F_i), a `Fin 5` and not
a move. After σ the link is (μ, α, μ, A, B) with the same repeat index j. The proof shows the
new Lock 1, a {α, A}-chain from x₁ to x₃, dies at x₃. In σc, x₃'s neighbours are x₂ (μ), x₄ (B),
w₂ (B) and w₃ (μ); none is α or A. This works only because w₂, w₃ were not recoloured, which is
what the triple component guarantees.

## 5. What a Studio state (55556, k = 4, w₀ = B, w₃ = μ, both locks) can fail

The Studio's `TypeR3` (Lean `QuarterGammaPeriod.TypeR3`) is `c(w j) = B ∧ c(w (j+3)) = μ`.

| hypothesis | status on a 55556 triangulation, k = 4, DL, Studio-R3 |
|---|---|
| K4Ball (all fields) | **automatic** (§6) |
| RepeatAt, Lock1, Lock2 | given (DL) |
| w₀ = B, w₃ = μ | given (Studio type) |
| w₁ = A | **forced**: w₁ ~ x₁ (μ), x₂ (α), w₀ (B) |
| w₂ = B | **forced**: w₂ ~ x₂ (α), x₃ (A), w₃ (μ) |
| **w₄ = A** | **not forced**: w₄ ~ x₄ (B), x₀ (α), w₀ (B), m. Not adjacent to w₃. So w₄ ∈ {A, μ} |

Ring coincidences (w_s = x_{s+3}, m = x_i) are excluded by K4Ball's `off` fields, and on a
triangulation they never arise at 55556 unless the link is a clique (§6). The degree-6 vertex's
outer path (w₃, m, w₄) is part of K4Ball and also automatic. So **the single failing condition is
w₄ = μ**. Then x₀ (α) ~ w₄ (μ) puts w₄ in σ's component. When m = α (m ∈ {α, A} here, since
m ~ x₄ (B) and w₃, w₄ (μ)), the component also reaches m and w₃. That recolours w₃ to α, and Lock 1 of σc can pass
x₃ → w₃. This is exactly the leak the theorem excludes.

Lean (`QuarterR3AtUnfold.lean`): `typeR3_k4_ring` (w₁ = A, w₂ = B, w₄ ∈ {A, μ}) and
**`r3At_k4_iff : R3At P w c j ↔ c (w (j + 4)) = c (P.x (j + 3))`** under `Hole6 P w m q`,
q = j + 4, ProperOff, DoublyLocked, TypeR3.

## 6. Is K4Ball automatic from degrees? Yes.

`hole6_of_degrees` (QuarterHole6Bridge): on a triangulation (`htri`), with `P` listed in rotation
order (`rot`), deg x_q = 6, deg x_i = 5 for i ≠ q, and the link not a 5-clique, there are w, m with
`Hole6 P w m q`. The no-clique condition is automatic when a proper colouring of G − h exists.
No separating-triangle hypothesis is used: a coincidence w_s = x_{s+3} propagates and forces a link
clique. `Hole6.k4Ball` (QuarterPeriodJ) turns `Hole6 P w m q` with q = j + 4 into `K4Ball P w m j`.
Here w_t is exactly the Studio's far-face vertex on edge x_t x_{t+1}. m is the extra
neighbour of x_q between w_{q−1} and w_q in rotation. **So the discrepancy is entirely R3At's extra
condition w₄ = A.**

## 7. The predicate the Studio should implement (R3At at k = 4)

With j the repeat index, q = j + 4 the degree-6 position, and indices mod 5:
```
alpha = c[x[j]]; mu = c[x[j+1]]; A = c[x[j+3]]; B = c[x[j+4]]
R3At(c, j) :=
     c[x[j]] == c[x[j+2]]
  && mu != alpha && A != alpha && B != alpha && mu != A && mu != B && A != B
  && reach_{mu,A}(x[j+1] -> x[j+3])   in G - h      # Lock1
  && reach_{mu,B}(x[j+1] -> x[j+4])   in G - h      # Lock2
  && c[w[j]]   == B        # w0  (Studio has this)
  && c[w[j+1]] == A        # w1  (forced at 55556, k=4)
  && c[w[j+2]] == B        # w2  (forced at 55556, k=4)
  && c[w[j+3]] == mu       # w3  (Studio has this)
  && c[w[j+4]] == A        # w4  <-- the missing check
```
At 55556, k = 4 it is the Studio's R3 plus `c[w[j+4]] == A` (equivalently `!= mu`). Then
`c[m] == alpha` follows (Lemma D, `m_col_k4`). Sanity check for Job BU: Studio-R3 ∧ w4 = A ⇒ σ-image
not DL, with no exceptions (theorem). The 1,037,102 exceptions should all have w4 = μ.
