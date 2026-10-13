# A5v in Lean: the statement, a proof on the sphere, and the primal bridge

Long Table (Lean lead for the A5v line), 13 Oct 2026, about 12:39–13:25 MDT. This is a draft
outside the accepted build. Labels: **[compiled]** = Lean, no `sorry`, standard axioms, built
here (not audited); **[hand]** = argument written here, not reviewed; **[data]** = computed.
Nothing outside `axioms/lean/` was changed. Studio Math's modules were compiled from their
read-only sources into a scratch copy and imported, never edited. Compute was `nice -n 10` on
AC power; the full `check.sh` takes about 2 minutes.

## 0. Verdict

1. **A5v is a theorem on the sphere** [compiled]. `SimpleGraph.A5v.a5v`: on every
   `SphericalMap`, at every DL figure-eight state of a degree-5 vertex whose other vertices are
   cubic, the far end of `f k` lies on `X`. It needs no parity clause. The proof uses only
   `Fills`, through a one-curve "Jordan at a vertex" lemma. It uses no Jordan curve theorem, no
   Euler and no dual graph.
2. **The parity form is equivalent by pure counting** [compiled]. `a5v_iff_parity`: in any
   rotation system, if `X` has an even number of vertices besides `v` (TrackU's DL clause), then
   A5v holds iff `|M ∩ E(X, Y)|` is odd. `a5v_parity` is the sphere instance.
3. **Sharper core** [compiled]. `a5v_of_facePot`: in *any* rotation system, A5v holds as soon
   as the loop `X` bounds a set of faces. No degree or `Fills` hypothesis is needed.
   `A5vNeedsFills` shows that the hypothesis cannot be dropped. On a 6-vertex twisted wheel A5v
   fails at a DL state; there `X` bounds nothing and `Fills` fails.
4. **Primal bridge** [compiled], redirected after the scope note
   (`axioms/scope/SCOPE-A5v.md`, commit `359c937c`). `A5vBridge.lean` states the
   Tait ↔ Kempe dictionary in the vocabulary of the Quarter modules (`tM`, `tX`, `tY`,
   `ThreeChains`). It proves:
   - `a5v_primal`: at a doubly locked state with the three-chain structure, both non-matching
     edges of the far triangle of `v`'s matching spoke lie on `X` and not on `Y`;
   - `y_far_iff_inA`: in primal coordinates, A5v **is** `¬inA`;
   - `notInA`: `¬inA` comes from the existing formal D2, `not_reach_alpha_A_of_lock2`;
   - `triangle_step`: the local step of Lemma F.
5. **Non-vacuity** [compiled]. Every hypothesis of `a5v`, `a5v_parity`, `a5v_primal` and
   `triangle_step` holds on explicit 8-vertex spherical maps (`A5vWitness`,
   `A5vBridgeWitness`).
6. **Plug-in point** [compiled]. `T1v` (law + A5v ⇒ no R-cycle, over all finite rotation systems)
   is stated as a `Prop`. `nrcM_sphere_of_T1v : T1v → NRCMSphere` is proved: a future proof of
   T1-v gives the matching-form NRC on every spherical map.

**The gap.** T1-v itself is open. The formal link from `NRCMSphere` to the primal NRC (and so
into `NoFrozenFrame ⇒ RStarFrame ⇒ 4CT`) needs the Tait dual as a formal rotation system (§5).
Even then, NRC closes only the near-rigid part of LPC.

## 1. The statements

All of these are in `A5vJordan.lean`, namespace `SimpleGraph.A5v`. `G : SimpleGraph (Fin n)`
and `R : RotationSystem G` are arbitrary unless `M : SphericalMap n` is written.

```lean
structure Hole5 (R : RotationSystem G) where          -- v of degree 5, darts f 0..f 4 in rotation order
  v : Fin n; f : Fin 5 → G.Dart; fst_f : ∀ i, (f i).fst = v
  next_f : ∀ i, R.next (f i) = f (i + 1); inj : Function.Injective f
structure IsPerfectMatching (G) (Mt : SimpleGraph (Fin n)) : Prop where
  le : Mt ≤ G; unique : ∀ u, ∃! w, Mt.Adj u w
def qGraph (G) (Mt) (v) : SimpleGraph (Fin n)          -- E − Mt with v deleted
def InX H Mt k u := (qGraph G Mt H.v).Reachable (H.f (k + 1)).snd u
def InY H Mt k u := (qGraph G Mt H.v).Reachable (H.f (k + 2)).snd u
structure Fig8 (H : Hole5 R) (Mt) (k : Fin 5) : Prop where   -- TrackU's `dl` minus the parity clause
  mk_adj : Mt.Adj H.v (H.f k).snd
  pairX : (qGraph G Mt H.v).Reachable (H.f (k + 1)).snd (H.f (k - 1)).snd
  pairY : (qGraph G Mt H.v).Reachable (H.f (k + 2)).snd (H.f (k + 3)).snd
  sepXY : ¬ (qGraph G Mt H.v).Reachable (H.f (k + 1)).snd (H.f (k + 2)).snd
  cover : ∀ u, u ≠ H.v → InX H Mt k u ∨ InY H Mt k u
def A5vAt H Mt k : Prop := InX H Mt k (H.f k).snd     -- the far end of f k is on X
def XEven H Mt k : Prop := Even #(xVerts H Mt k)       -- TrackU's parity clause
noncomputable def crossXY H Mt k : ℕ                   -- |Mt ∩ E(X, Y)|, counted at the X ends
def CubicOff [DecidableRel G.Adj] (H : Hole5 R) : Prop := ∀ u, u ≠ H.v → G.degree u = 3
def FacePot (R) (X : G.edgeSet → ZMod 2) (a : R.Face → ZMod 2) : Prop :=   -- X = ∂a
  ∀ d, X (edgeOfDart d) = a (R.faceOf d) + a (R.faceOf d.symm)

theorem jordan_at_vertex_of_facePot (X) (ha : FacePot R X a) (e₁ : R.next d = d₁)
    (e₂ : R.next d₁ = d₂) (h₀ : X d = 0) (h₁ : X d₁ = 1) (h₂ : X d₂ = 0)
    (hfree : XFree G X d₂.snd) : ¬ (freeGraph G X).Reachable d₂.snd d.snd
theorem a5v_of_facePot (hM : IsPerfectMatching G Mt) (hF : Fig8 H Mt k)
    (ha : FacePot R (xEdges H Mt k) a) : A5vAt H Mt k
theorem xEdges_even (hF) (hM) (hc : CubicOff H) : ∀ x, edgeIncidence G (xEdges H Mt k) x = 0
theorem a5v {M : SphericalMap n} (H : Hole5 M.rotation) (hM : IsPerfectMatching M.graph Mt)
    (hc : CubicOff H) (hF : Fig8 H Mt k) : A5vAt H Mt k
theorem a5v_iff_parity (hM) (hF) (hE : XEven H Mt k) : A5vAt H Mt k ↔ Odd (crossXY H Mt k)
theorem a5v_parity (hM) (hc) (hF) (hE) : Odd (crossXY H Mt k)

structure DLOrbit (H) (S : ℕ → SimpleGraph (Fin n)) (k : ℕ → Fin 5) (L : ℕ) : Prop  -- TrackU dynamics:
  -- 0 < L, S periodic, each S t a perfect matching at a Fig8 + XEven state of frame k t,
  -- Disjoint (S t) (S (t+1)), and (S (t+1)).Adj v (f (k t + 3)).snd   (f (k − 2) ∈ M_{t+1})
def kH A B := Nat.card (A ⊔ B).ConnectedComponent
def Word1212 S := ∃ p, ∀ t, kH (S t) (S (t+1)) = if Even (t + p) then 1 else 2
def ChainLaw S := ∀ t, Odd (kH (S t) (S (t+1)) + kH (S (t+1)) (S (t+2)))
def T1v : Prop := ∀ n G [DecidableRel G.Adj] R (H : Hole5 R) S k L,
  CubicOff H → DLOrbit H S k L → ChainLaw S → (∀ t, A5vAt H (S t) (k t)) → ¬ Word1212 S
def NRCMSphere : Prop := ∀ n (M : SphericalMap n) (H : Hole5 M.rotation) S k L,
  CubicOff H → DLOrbit H S k L → ¬ Word1212 S
theorem chainLaw_of_word1212 : Word1212 S → ChainLaw S
theorem nrcM_sphere_of_T1v : T1v → NRCMSphere
```

The primal bridge is `A5vBridge.lean`, namespace `SimpleGraph.A5vBridge`. The setting is
`M : SphericalMap n` (the triangulation `T`), `P : Pent M.graph h`, `c : Fin n → Fin 4` and the
frame `j`, with colours `α μ α A B` at `x j … x (j+4)`:

```lean
def InK u  := (pairGraph M.graph h c α A).Reachable (P.x (j+2)) u   -- K  = K_{αA}(x_{j+2})
def InK' u := (pairGraph M.graph h c α A).Reachable (P.x j) u       -- K' = K_{αA}(x_j)
def InL u  := (pairGraph M.graph h c μ B).Reachable (P.x (j+1)) u   -- L  = K_{μB}(x_{j+1})
def InA := InK P c j (P.x j)                                        -- inA
def tM u w := M.graph.Adj u w ∧ u ≠ h ∧ w ≠ h ∧ tait c u w = enc α + enc A   -- colour-2 class
def tX u w := M.graph.Adj u w ∧ (K–L edge)     def tY u w := M.graph.Adj u w ∧ (K'–L edge)
def ThreeChains := ∀ u ≠ h, (c u ∈ {α,A} → InK u ∨ InK' u) ∧ (c u ∈ {μ,B} → InL u)  -- P2 = (2,1)

theorem notInA (hr : RepeatAt P c j) (hl : Lock2 P c j) : ¬ InA P c j          -- D2
theorem mSpoke / not_tM_spoke / xSpokes / ySpokes                             -- spoke pairing
theorem tM_iff, tX_tY_disjoint, q_edge_cover                                  -- dictionary
theorem triangle_step (hc) (hr) (htri : M.Triangulated) (d) (hX : tX d.fst d.snd)
    (hrh : r ≠ h) : (tX q r ∧ tM r p) ∨ (tM q r ∧ tX r p)                       -- Lemma F step
theorem a5v_primal (hc : ProperOff M.graph h c) (hdl : DoublyLocked P c j)
    (h3 : ThreeChains P c j) (hz : z ≠ h) (e2 : Adj (x (j+2)) z) (e3 : Adj (x (j+3)) z) :
    (tX (x (j+2)) z ∧ tX (x (j+3)) z) ∧ (¬ tY (x (j+2)) z ∧ ¬ tY (x (j+3)) z)
theorem y_far_iff_inA (…) : tY P c j (P.x (j + 2)) z ↔ InA P c j
```

## 2. Proofs [compiled, hand summary]

- **Jordan at a vertex.** Let `X = ∂a`. Write `L(d) = a(face of d)`. Then:
  - `L(next d) = L(d) + X(d)`;
  - `L(d.symm) = L(d)` when `d ∉ X`;
  - `L` is constant around a vertex that meets no edge of `X`.

  For the darts `d = f k`, `f (k+1)`, `f (k+2)` with `X`-values `0, 1, 0`, this gives
  `L(f (k+2)) = L(f k) + 1`. A path from the far end of `f (k+2)` to the far end of `f k`
  through `X`-free vertices would force `L(f (k+2)) = L(f k)`.
- **A5v.** Suppose the far end `w` of `f k` were not on `X`. Then `w` is on `Y` (`cover`), and
  the `qGraph` path inside `Y` avoids `X`. That contradicts the lemma above.
- **The face potential.** On a sphere `Fills` supplies `a`, once `X` is known to be even
  (`xEdges_even`). Evenness uses `CubicOff` and the perfect matching: an `X`-vertex has exactly
  two non-matching darts. At `v` the five spokes carry `0, 1, 0, 0, 1`.
- **Parity form.** The `X`-vertices are matched to `v` (only `w`), to `X` in pairs (an
  involution, `Finset.sum_involution`), or to `Y`. Sum over `ZMod 2`.
- **Primal A5v.** The far corner `z` of the spoke `x (j+2) x (j+3)` is coloured `μ` or `B`, so
  `z ∈ L` by `ThreeChains`. Both of its edges to `K` are `K–L` edges. They are `K'–L` edges iff
  `x (j+2) ∈ K'`, i.e. iff `inA`. D2 excludes `inA` at every `Lock2` state.

## 3. Compile status

`zsh check.sh $HOME/mathlib4-planemap <scratch>`. The toolchain is Lean v4.35.0-rc3. The base is
the PlaneMap build at `~/mathlib4-planemap` (commit `bcff6cd`); its `.olean` tree is cloned
copy-on-write into the scratch directory, as Studio Math's `check.sh` does. The script compiles
Studio Math's `TutteSides` and the 22-module closure of `QuarterLockParity` + `QuarterTait` from
their read-only sources, then the 7 modules here. Last full run: 13:17, 117 s wall, 0 errors,
0 warnings, 0 `sorry`. Every axiom line is `[propext, Classical.choice, Quot.sound]` (28 lines):

| module | `#print axioms` (all standard) |
|---|---|
| `A5vJordan` | `jordan_at_vertex_of_facePot`, `jordan_at_vertex`, `a5v_of_facePot`, `a5v`, `a5v_iff_parity`, `a5v_parity`, `chainLaw_of_word1212`, `nrcM_sphere_of_T1v` |
| `A5vWitness` | `witness_a5v`, `witness_parity`, `witness_a5v_direct` |
| `A5vNeedsFills` | `not_a5v`, `not_parity`, `twisted_X_not_bounding`, `twisted_not_fills` |
| `A5vBridge` | `mSpoke`, `not_tM_spoke`, `xSpokes`, `ySpokes`, `notInA`, `tX_tY_disjoint`, `q_edge_cover`, `triangle_step`, `a5v_primal`, `y_far_iff_inA` |
| `A5vBridgeWitness` | `witness_a5v_primal`, `witness_notInA`, `witness_triangle_step` |

**Sabotage checks** (scratch copies, not kept):
- Putting `A5vAt` on `Y` instead of `X` makes `a5v_of_facePot`, `a5v` and `a5v_parity` fail to
  compile.
- Requiring `X`-value `0` instead of `1` at the middle dart makes `jordan_at_vertex_of_facePot`
  fail.

**Non-vacuity.**
- `A5vWitness` uses the Tait dual of an 8-vertex triangulation with a degree-5 hole
  (`A5vWitnessMap`, `Fills` by a linear certificate). The state is `{04, 15, 27, 36}`, with
  `X = 0‑1‑2‑4‑3‑0` and `Y = 0‑5‑7‑6‑0`, so `|M ∩ E(X,Y)| = 3`.
- `A5vBridgeWitness` uses an 8-vertex triangulation (`A5vPrimMap`) with a doubly locked
  colouring and `K = {2,0,7}`, `K' = {4}`, `L = {1,5,6}`.
- Both were found by the scripts in `scripts/`.

## 4. Dependencies on existing modules (imported read-only, nothing edited)

| used | from |
|---|---|
| `SphericalMap`, `RotationSystem.Fills`, `faceOf`, `faceNext`, `edgeIncidence`, `edgeDart` | base PlaneMap (`SphericalMap.lean`, `RotationSystem.lean`) |
| `sum_edges_at`, `zmod2_add_self`, `zmod2_add_eq_zero`, `tri3` | `TutteSides` (Studio Math) |
| `Pent`, `RepeatAt`, `Lock2`, `DoublyLocked` | `QuarterFloor` |
| `pairGraph`, `Active`, `ProperOff` | `VacancyShortFill`, `VacancySlide` (base) |
| `tait`, `enc`, `tait_cross_iff` | `QuarterEvenCut`, `QuarterTait` |
| **D2**: `not_reach_alpha_A_of_lock2` (Lock2 ⇒ `x j ∉ K_{αA}(x (j+2))`) | `NoFrozen.lean:272` (via `QuarterLockParity`) |
| `gen_smap.py` (primal map) | `StudioMathReview-scripts/` (run read-only); `scripts/gen_smap_faces.py` is our any-face-length copy for the dual |

**Search for ¬inA, as the scope note asked.** `¬inA` at `Lock2` states is already formal:
- `not_reach_alpha_A_of_lock2` (`NoFrozen.lean`; a private copy at `QuarterRotationPlanar.lean:275`
  sits behind `rot3_bijOn_planar`);
- its converse is `reach_alpha_A_of_not_lock2` (`QuarterPairDuality.lean:898`, triangulated);
- `piMove` takes the `rot3` branch exactly at `Lock2` (`QuarterPi.lean:213`), and
  `piMove_kempeStep` is formal.

No new Jordan input is needed on the primal side. `notInA` simply reuses D2.

## 5. The gap, and the most promising route

1. **A5v.** Closed on the sphere, in both matching form (`a5v`, from `Fills`) and primal form
   (`a5v_primal`, from D2). Nothing is left to prove for A5v itself.
2. **Bridge: matching form ↔ primal** (not formal). The library has no Tait dual. The next
   formal step is the Tait dual of `T − h` as a `RotationSystem` on `Fin N`: dual vertices are the
   triangles avoiding `h` plus `v`, and the rotation is induced by `faceNext`. Then identify
   `Hole5`, `Mt` and `Fig8` with `tM`, `tX`, `tY`:
   - Lemma F: the dual walk along `E − Mt` from the spoke `x (j+1) x (j+2)` stays in `tX`. The
     local step is `triangle_step`; only the induction along dual walks is missing.
   - `ThreeChains` ⇔ `E − Mt` connected (on the sphere; scope note §1).

   With that, A5v for real states needs **no dual `Fills`**. `a5v_of_facePot` applies with
   `a := 1_K` (`K` = a set of primal vertices = dual faces), since `∂1_K = δ(K) = E(K, L) = X`
   under `ThreeChains` [hand]. The construction is generated-certificate style for concrete maps,
   but the general dual construction is real work: simplicity of the dual, `Fin N` indexing, and
   the rotation at `v`.
3. **T1-v** (open; `T1v` is stated). `nrcM_sphere_of_T1v` is the formal plug-in. A proof of
   T1-v (exhaustively true for `n ≤ 22` in Run 2, not certified) gives `NRCMSphere`. Two caveats:
   - `NRCMSphere` uses the exact word `1212…`. TrackS's NRC-M also allows even `k(H) ≥ 4` at odd
     states; by the law and `N ≤ 9` the `1212` form is the NRC′ case.
   - From `NRCMSphere` to `NoFrozenFrame` (`FrameNoFrozen.lean`: `rStarFrame_of_no_allDL_orbit`,
     `four_color_of_no_allDL_orbit_frame`, formal) one needs: (i) the bridge above together with
     TrackS S3 (`M_{t+1} = M_{t−1} Δ Y_t`) [hand]; (ii) NRC ⇒ near-rigid LPC [hand, TrackJ];
     (iii) the **open** mixed/higher-chain-count part of LPC.

   The scope note (§0.4–0.5) shows that A5v cannot reach (iii). The known primal frozen classes
   satisfy A5v-primal at every state.
4. **Did the parity form fall out of an existing identity?** Partly; the honest answer:
   - Given XEven, the parity form is equivalent to A5v by counting (`a5v_iff_parity`).
   - XEven itself is lock parity [hand]. `|δ_T(K)| ≡ |X| = |X ∖ v| + 1`, so LP
     (`Lock2 ⇔ |δ(K)|` odd, `QuarterLockParity`) is the statement that `X` has an even number of
     vertices besides `v`.
   - A5v (equivalently the parity) is *not* a counting identity on the abstract graph. The twisted
     wheel satisfies every local degree and matching condition and still violates it. It needs a
     boundary input: `Fills` on the dual sphere, or `X = δ(K)` with `¬inA` (D2) on the primal side.
     Tutte/Euler counting (`TutteSides`, `ChainF`) was not needed.

## 6. Files

| file | content |
|---|---|
| `A5vJordan.lean` | vocabulary, Jordan-at-a-vertex core, `a5v_of_facePot`, `a5v`, parity form, orbits, `T1v`, plug-in |
| `A5vWitnessMap.lean` | generated `SphericalMap` (8 vertices, faces of length 3–5): the Tait dual of an 8-vertex triangulation with a hole |
| `A5vWitness.lean` | non-vacuity of `a5v` and `a5v_parity` |
| `A5vNeedsFills.lean` | twisted wheel: A5v fails, `X` does not bound, `¬ Fills` |
| `A5vBridge.lean` | primal dictionary, D2 ⇒ ¬inA, Lemma F step, `a5v_primal`, `y_far_iff_inA` |
| `A5vPrimMap.lean` | generated primal triangulation (8 vertices, Studio Math's `gen_smap.py`) |
| `A5vBridgeWitness.lean` | non-vacuity of `a5v_primal` and `triangle_step` |
| `check.sh` | full build and regression (about 2 min) |
| `scripts/gen_smap_faces.py` | copy of Studio Math's `gen_smap.py` that accepts faces of any length (for Tait duals) |
| `scripts/flipsearch.py`, `scripts/witness.json` | flip search for a small dual DL-good state |
| `scripts/antisearch.py` | search for a small non-planar A5v violation (gives the twisted wheel at `n = 6`) |
| `scripts/primal_dl.py`, `scripts/primal_witness.json` | search for a small primal DL colouring with `ThreeChains` (run from `scripts/`) |

SHA-256 prefixes at write-up (13:17):

```
7eb4b97a2ec911a7 A5vBridge.lean          ac90286bf480d5e3 A5vBridgeWitness.lean
9a759d2d28739b55 A5vJordan.lean          516b813527a98d6b A5vNeedsFills.lean
6dae2614bebca0a5 A5vPrimMap.lean         6104daf693066ea6 A5vWitness.lean
5d7b3165ba2cd236 A5vWitnessMap.lean      f8c11c661048a5e8 check.sh
```
