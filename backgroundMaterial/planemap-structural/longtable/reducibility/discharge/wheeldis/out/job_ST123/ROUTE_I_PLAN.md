# ROUTE_I_PLAN: Lean C glue for 2.126 (rsst003_2o126) with a ring-merging X (ST-123, 10 Nov 2026)

This is a reading and planning note. I built nothing, edited nothing and committed nothing.
Tags: **[read]** means checked in the named file. **[inf]** means my reasoning or estimate. **[C]** means the
lead's hand argument, checked below against our definitions.

Sources read:
- dcheck/: `CGlue.lean` (all of it), `CGlueU.lean`, `COccBridge.lean`, `CXRing.lean` (head and `XRData.ok`),
  `C66666.lean` (`extCAux`), `CContract.lean` (declaration list and data grep), `ClaimGlue.lean:40-120`,
  `DCheckOccWalk.lean:18-27` (`ConfigOccW`), `DCheckPinchGeom.lean:24` (`Cyc`) and `SepAll.lean:29` (`BothSides`);
- W/out/job_RSSTADM/SCOPING.md (§0, §1, §3, Addendum C);
- one generated per-key module pair, as the integration pattern: `W/out/job_HCK5P03/glue_hc/{HK5P03_00,COccHK5P03_00,HK5P03Occ}.lean`;
- `W/out/job_ST114/lean/RSSTWindowBasic.lean`, for `facial_nx` and `nx_inj_left`.

## 0. The configuration in our indices

kc line (`loop/k44/rsst.txt:4`): `rsst003_2o126 8 4 0,1,2;2,3,4;4,5,6;0,6,7 1,2,3;0,2;0,1,3;0,2`.

| vertex | ring nbrs | int nbrs | degree | rotation (cyclic; orientation up to mirror) |
|---|---|---|---|---|
| I0 | R0 R1 R2 | I1 I2 I3 | 6 | R0 R1 R2 I1 I2 I3 |
| I1 | R2 R3 R4 | I0 I2 | 5 | R2 R3 R4 I2 I0 |
| I2 | R4 R5 R6 | I0 I1 I3 | 6 | R4 R5 R6 I3 I0 I1 |
| I3 | R6 R7 R0 | I0 I2 | 5 | R6 R7 R0 I0 I2 |

- `eqR = [(0,0),(2,0),(4,2),(6,2)]` in `(t, a)` form, and `eqI = []`.
- The two X-classes are {I0, R0, R2} and {I2, R4, R6}. I0 ~ I2 is a kept interior edge.
- The lead's labels map to ours as follows: ring 1..8 = R0..R7, P = I0, R = I1, Q = I2, S = I3, and X = {1P, 3P, 5Q, 7Q} = {R0-I0, R2-I0, R4-I2, R6-I2}.
- Labelling `lbl = [0,1,2,3, 0,4,0,5,2,6,2,7]` (I0..I3, then R0..R7). It satisfies every conjunct of `admissibleX` except the last one, because
  L(R0) = L(R2) = 0 and L(R4) = L(R6) = 2 [inf, checked by hand against `admissibleX`, CGlue:375-390].
  - I1's ring neighbours R2, R3, R4 have labels 0, 5, 2, all different from 1.
  - I3's ring neighbours R6, R7, R0 have labels 2, 7, 0, all different from 3.
  - R1 has label 4, which differs from 0. R5 has label 6, which differs from 2.
  - All interior labels are distinct, and |X| = 4.

## 1. Every use of the distinct-ring-label clause / XRingSimple / derived lemmas

Classes:
- **(A)** still true, not needed, or bypassed for a ring merge;
- **(B)** needs a modified lemma or variant (the table says how);
- **(C)** fundamentally needs distinct labels. The argument as written fails when two positions of one class share a label, so a new geometric
  input has to replace it.

| # | file:line | lemma / def | what it needs the clause (or XRingSimple) for | under a merge (s ≠ t, gap 2, same label) | class |
|---|---|---|---|---|---|
| 1 | CGlue:375-390 | `admissibleX` (last conjunct) | the conjunct itself | false for 2.126 for every `lbl`: L(R0) = L(I0) = L(R2) is forced | **B**: `admissibleXM` = `admissibleX` without the last conjunct (the CGlueU pattern of dropping a conjunct) |
| 2 | CGlue:392 | `XRingSimple` | touched positions visited once | not used on our route | A (bypassed: we use `OccursCXR`) |
| 3 | CGlue:479-488 | `xLabel_ring` | `XRingSimple` makes `Classical.choose` return `t` itself | false in general under folds; true if every pair with ρ s = ρ t has equal labels | **B**: `xLabelM_ring` with the hypothesis `hcoh : ∀ s t touched, ρ s = ρ t → L(m+s) = L(m+t)` |
| 4 | CGlue:567, :587 | `xGraph_labels` (constancy along X-edges, `hoffL`) | through #3 | survives with `hcoh` | **B** (through #3) |
| 5 | CGlue:617 | `xGraph_labels`, non-X ring edge case | `XRingSimple` gives t = t' when ρ t = ρ t' | the D1 fold (R1 = R0, say) must be excluded instead | **B**: use the D1 conjunct of `foldSafeX` with `excl_sound` / `cycEx_sound`, exactly as `xGraph_labels_fold` does at :1240-1262 |
| 6 | CGlue:633-637 | `xGraph_labels`, G-edge case | `hArg`: two touched positions s ≠ t have different labels, so a G-edge between them is not inside one class | **fails**: the chord ρ0 ~ ρ2 (or ρ4 ~ ρ6) would become a loop | **C**: replace with a chord exclusion (NoSep + `RotOcc`, §2 M3) |
| 7 | CGlue:646-704 | `contract_reducer_of` | takes `hadm` but **never uses it** [read] | the body does not use it | **B** (trivial): a verbatim copy without `hadm`, as `contract_reducer_ofU` already is |
| 8 | CGlue:706-727 | `contract_reducer` | passes `hadm`, `hs` to `xGraph_labels` | not used on our route | A (bypassed) |
| 9 | CGlue:1107-1118 | `kInt_touched` | `hArg'`: a label names one touched position, so `kInt` (label ↦ ring **vertex**) is single-valued | **fails**: label 0 names both ρ0 and ρ2, which are distinct vertices | **C**: vertex-valued `xKappa` cannot work; use a label-valued κ (#3) |
| 10 | CGlue:1166-1172, :1206 | `xGraph_labels_fold` | through #9 | fails | **C** (its D1/D2 blocks are reusable logic) |
| 11 | CGlue:828 | `foldSafeX` | uses labels, not the distinct clause | true for 2.126 with the `lbl` above [inf]: D1 pairs are exclB via I0/I2 (NbrInj); D2 has only (I0, I2), with pairs {0,2}×{4,6}, all exclB | A (reused as is) |
| 12 | CGlue:1322-1336 | `CEntry.hadm` field | packaging | no `CEntry` can be built for 2.126 | **B**: new structure `CEntryM` without `hadm`/`lbl`-admissibility, with `hadmM`, `hfold`, `hcoh`, `hchord` |
| 13 | CGlue:1340 | `OccursCX` (`XRingSimple`) | occurrence condition | not used | A (bypassed) |
| 14 | CGlue:1367-1389 | `CEntry.colorable_of_contract` | only forwards `e.hadm` to #7 | the pull-back itself is label-free | **B** (trivial): copy for `CEntryM` |
| 15 | CGlue:1391, :1422, :1467 | `CEntry/CEntry1/CEntryF.colorable` | call #4 or #10 | not used | A (bypassed) |
| 16 | CGlueU:37-159 (:153) | `xGraph_labelsU` | as #6 | fails | **C** (mirror of #6) |
| 17 | CGlueU:221-380 (:234-237, :273) | `xGraph_labels_foldU` | as #9 | fails | **C** (mirror of #9) |
| 18 | CGlueU:161 | `contract_reducer_ofU` | `admissibleXU` keeps the distinct clause | blocks as #7 | **B** (same remedy as #7) |
| 19 | CGlueU:385 | `CEntryU` | packaging | not used | A |
| 20 | CXRing:37, :48 | `XRData.ok`, `toCEntryF` | requires `admissibleX` | false for 2.126 | **B**: a `CEntryM` instance written by hand (one config, no data list) |
| 21 | COccBridge:233, :240 | `occursCXF_of_rot`, `OccursCXR` (take `e : CEntry`) | only `e.cf` is read | cannot be applied without a `CEntry` | **B**: cf-level variants `OccursCXRc cf`, 5-10 lines |
| 22 | CGlue:126-150, :169, :249-289, :291-370; C66666:85 | `cReducibleT`, `extCAux_complete`, `XCompat`, `extCAux_canon`, `colorable_of_goodT`, `colorable_of_cReducible18`, `extCAux` | no labels; eqR is data. `extCAux` forces x = col k t for every contracted (t, a), so merged positions get one colour | holds | A |
| 23 | CContract (whole file) | C4a `contract_subgraph_gen` and friends | no configuration data at all [read: grep] | any H ≤ T.graph | A |

**Counts: A = 9 (#2, 8, 11, 13, 15, 19, 22, 23, plus `ClaimGlue`, which has no use), B = 9 (#1, 3/4 as one, 5, 7, 12, 14, 18, 20, 21),
C = 5 (#6, 9, 10, 16, 17).** The grouping is mine. #3 and #4 are one change.

**Key finding [read].**
- Every (C) use is inside **C4b**, the label argument that proves `XLoopFree`. More precisely:
  - CGlue:635: the G-edge chord case.
  - CGlue:1107/1206: the single-valued label ↦ vertex map.
  - Their CGlueU copies.
- None is in:
  - C4a (`CContract`);
  - the reduced map's ring or its colouring correspondence (`contract_reducer_of` ignores `hadm`, and `XCompat`/`extCAux` take eqR as data);
  - hC.
- `CEntry.colorable_of_contract` already takes `hlab : XLoopFree …` as an argument. So (i-a) is **not** a generalisation of the contraction
  soundness. It is:
  - hadm-free copies of two short wrappers;
  - one modified label lemma.
- This is the low end of Addendum C's 4–8 pd, and below it.

## 2. Plan for 2.126 only (new files only)

### (i-a) M1: plumbing and M2: the merge label lemma (`dcheck/CGlueM.lean`, imports `COccBridge`)

```lean
def admissibleXM (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ) : Bool := -- admissibleX minus the last conjunct

theorem ConfigOccW.contract_reducer_ofM ... -- = contract_reducer_of with the `hadm` binder deleted (body verbatim)

/-- Touched positions folded together carry one label. -/
def RingCoh (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n) : Prop :=
  ∀ s t, s < cf.r → t < cf.r → touchedB eqR s = true → touchedB eqR t = true →
    ρ s = ρ t → lbl.getD (cf.m + s) 0 = lbl.getD (cf.m + t) 0

/-- No T-edge inside one class between two touched ring positions. -/
def NoClassChord (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n) (T : SphericalMap n) : Prop :=
  ∀ s t, s < cf.r → t < cf.r → touchedB eqR s = true → touchedB eqR t = true →
    lbl.getD (cf.m + s) 0 = lbl.getD (cf.m + t) 0 → ¬ T.Adj (ρ s) (ρ t)

theorem xLabelM_ring (hoff : ∀ t a, ρ t ≠ ι a) (hcoh : RingCoh cf eqR lbl ρ) (ht : t < cf.r)
    (htouch : ∃ a, (t, a) ∈ eqR) : xLabel cf eqR lbl ρ ι (ρ t) = .inl (lbl.getD (cf.m + t) 0)

theorem ConfigOccW.xGraph_labels_merge (hadm : admissibleXM cf eqR eqI lbl = true)
    (hsafe : foldSafeX cf eqR eqI lbl = true) (hloop : …) (O : ConfigOccW T G …)
    (hex : OccExact …) (hNI : NbrInj …) (hCN : CommonNbr …) (htri) (hNS : NoShortSepCycle T)
    (hcoh : RingCoh cf eqR lbl ρ) (hch : NoClassChord cf eqR lbl ρ T) :
    XLoopFree cf eqR eqI ρ ι G
```

The proof of `xGraph_labels_merge` is `xGraph_labels` (κ = `xLabel`, which is label-valued), with three changes:
- `xLabel_ring` is replaced by `xLabelM_ring`.
- The non-X ring edge case (old :617) takes t' from the choice, uses `hcoh` for its label, and uses `foldSafeX`'s D1 conjunct with
  `excl_sound`/`cycEx_sound` when t' ≠ s. This is the D1 block of `xGraph_labels_fold`.
- The G-edge case (old :635) gets s, t with equal labels and x = ρ s ≠ ρ t = y; `hch` contradicts `G ≤ T` (`O.hG`).
- The interior-edge case needs no fold argument, because κ(ι a) = L a directly.

Then the wrappers:

```lean
structure CEntryM where
  cf; eqR; eqI; lbl; hC : cReducible18 cf eqR eqI = true; hadmM : admissibleXM … = true
  hfold : foldSafeX … = true; hcohB : coherB … = true; hchordB : chordB … rot = true
  rot : Fin m → List (Fin m ⊕ ℕ); hrot : rotOK (Conf.of18 cf) rot = true
  hr2 hr hsym hloop hrr
def OccursCXRM (e : CEntryM) (T) : Prop := ∃ G ρ ι, ConfigOccW … ∧ RotOcc T ρ ι e.rot
theorem CEntryM.colorable_of_contract …   -- copy of CGlue:1367, calling contract_reducer_ofM
theorem CEntryM.colorable (htri) (h : OccursCXRM e T) (IH) : T.graph.Colorable 4
```

Fixing `rot` in the entry, rather than existentially, is what lets `chordB` be decided.

### (i-b) M3: the certificate for 2.126 (`dcheck/CGlueM.lean`, continued)

The bad events for 2.126, with our refutations:

| event | instances | refuted by |
|---|---|---|
| E1 fold inside a star | ρ0 = ρ2, ρ4 = ρ6 | not a loop under the label κ (same label). It is never needed. NbrInj would also exclude it. |
| E2 fold across stars (`RingCoh`) | ρ0 = ρ4, ρ0 = ρ6, ρ2 = ρ4, ρ2 = ρ6 | `exclB` holds: c = I0 has p ∈ {0, 2}, and its interior neighbour I2 has q ∈ {4, 6}. `excl_sound` (CGlue:867) uses `CommonNbr` (= NoSep + `ApexFacts`, `commonNbr_of_apex`) and `NbrInj`: the common neighbour would be ρ p' with p' ∈ ringAdj I0 ∩ ringAdj I2 = ∅. |
| E3 D1: a class meets a non-X neighbour | ρ1 ∈ {ρ0, ρ2}; ρ5 ∈ {ρ4, ρ6} | `foldSafeX` D1 → `exclB` via c = I0 (or I2) seeing both (`NbrInj`, from `RotOcc.nbrInj`). I1 and I3 carry no class label, so their edges are automatic. |
| E4 chord inside a star (`NoClassChord`) | T.Adj ρ0 ρ2; T.Adj ρ4 ρ6 | ι0 ~ ρ0, ρ2 (`OccExact`). `NoSep` makes the triangle `Facial`. `facial_nx` puts it at ι0: Nx(ι0, ρ0, ρ2) or Nx(ι0, ρ2, ρ0). `RotOcc.nx_at` / `R.nx` with `nx_func` / `nx_inj_left` make ρ2 the slot just before or just after `inr 0` in rot(I0), namely `inr 1` or `inl 3`. ρ2 = ρ1 contradicts `NbrInj`; ρ2 = ι3 contradicts `disj`. The same holds at I2 with neighbours `inr 5` and `inl 1`. |
| E5 interior edge I0–I2 inside a class | — | labels 0 ≠ 2 under `hcoh`. This is the E2 events. |
| E6 T-edge across stars | e.g. ρ0 ~ ρ4 | harmless (it stays an edge) |

New pieces:
- `coherB cf eqR lbl`: for all touched s, t with L s ≠ L t, `s == t || exclB cf s t || cycEx cf s t`. Its soundness, `RingCoh` via
  `excl_sound`/`cycEx_sound`, is about 40 lines.
- `facial_nx`: copy the 6 lines from ST-114 `RSSTWindowBasic.lean:30` (it uses `nx_tri`, which the generated modules already use).
  `nx_inj_left` is 5 lines.
- `RotOcc.facial_ring_slot`: if `rot c` has `inr p` at index j and `Facial T (ι c) (ρ p) w`, then w is the slotV at j+1 or at j-1
  (mod length). About 50–70 lines.
- `chordB cf eqR rot`: for all pairs `(s,c), (t,c) ∈ eqR` with s ≠ t, and every index j with `rot c[j] = inr s`, neither neighbouring slot
  is `inr t`. Its soundness gives `NoClassChord` when every label class with two touched positions is a star with one centre. For
  2.126 that is true by the labels, and it is checked by `decide` as `starB`. Together about 60–90 lines.
- An orientation remark: `chordB` checks both neighbours, so the mirror occurrence needs nothing extra.

### (i-c) M4: integration

- **Per-key occurrence module** for rsst003_2o126 (ring 8, 4 interior), from `gen_occ_kc.py` (`W/out/job_OCC13/in/`), as in HCK5P03.
  It provides:
  - `Occ`, `rot`, `rot_ok`, `rotOcc_of_occ`, `configOcc`, `cf`, `cf_sym`, `cf_loop`;
  - the mirror form.
  It is generated, a few hundred lines.
- **`C2o126.lean`:**
  - `CEntryM` with `hC := by native_decide` (`cReducible18 cf [(0,0),(2,0),(4,2),(6,2)] []`; ring 8, so seconds to minutes);
  - `hadmM`, `hfold`, `hcohB`, `hchordB` by `decide`;
  - `colorable_0` and `colorable_mirror_0` from `Occ`, as `HK5P03Occ`.
- **Registry hook:**
  - `RegistryRM := RegistryR + CM : List CEntryM`;
  - `four_color_of_unavoidableCRM`, a copy of CGlue:1499 / COccBridge `four_color_of_unavoidableCR`, about 40 lines.
- **Plumbing not needed.** No `hdeg` plumbing is needed: minimum degree is never used, because E1–E6 are triangles or folds.

### Sizes and order

| step | content | hand lines | pd |
|---|---|---|---|
| S0 | falsification first: `decide` sanity theorems (`admissibleXM` true, `admissibleX` false, `foldSafeX` true) and the hC run on Studio | 30 | 0.25 (+ minutes of compute) |
| M1 | `admissibleXM` with its spec unpack, `contract_reducer_ofM`, `CEntryM`, `colorable_of_contract` copy | 120–160 | 0.5 |
| M2 | `xLabelM_ring`, `xGraph_labels_merge` | 180–250 | 1–1.5 |
| M3 | `coherB` and soundness, `facial_nx`, `RotOcc.facial_ring_slot`, `chordB`/`starB` and soundness | 150–230 | 1.5–2 |
| M4 | generated Occ module, `C2o126.lean`, `OccursCXRM`, registry copy | 80–120 (+ generated) | 1–1.5 |
| **total** | | **560–790** | **4.25–5.75, central ≈ 4.75 pd** (was 7–13) |

- **Order:** S0 → M1 → M3's `RotOcc.facial_ring_slot`, which is the only new geometric lemma and so the de-risk → M2 → rest of M3 → M4.
- **Parallel work:** the Occ-module generation and the hC run can go to Studio at S0.
- **Risks:**
  - elaboration of the `xGraph_labels_merge` case split: the original is about 125 lines and was slow;
  - index bookkeeping in `facial_ring_slot`: modular slot arithmetic, the same pattern as `RotOcc.nx_at` / `apex_from`.

## 3. First concrete Lean step (can start now; no existing module edited)

Create `dcheck/CGlueM.lean` (`import COccBridge`) containing:
1. the `cf2o126 : DCheck18.Conf` literal from the kc line: `ringAdj := #[#[0,1,2],#[2,3,4],#[4,5,6],#[0,6,7]]`, `intAdj := #[#[1,2,3],#[0,2],#[0,1,3],#[0,2]]`;
2. `lbl2o126 := [0,1,2,3,0,4,0,5,2,6,2,7]`;
3. `admissibleXM`, and the three `decide` theorems: `admissibleXM … = true`, `admissibleX … = false`, `foldSafeX … = true`;
4. `contract_reducer_ofM`, a verbatim copy of CGlue:646-704 without `hadm`.

Compile it the way the job folders do (`lake env lean` from dcheck). CGlue, CGlueU and COccBridge are not `lean_lib` targets in
`lakefile.lean` either [read: grep], so **no existing file needs editing**, not even the lakefile.
- If a later consumer outside dcheck wants `CEntryM` in the registry, it imports `CGlueM`.
- Nothing in CGlue or COccBridge has to change.
- The optional cleanup would edit CGlue:646 to drop the unused `hadm` binder. It is not needed and is not recommended (it would break call sites).

## 4. The lead's hand arguments [C], checked against our Lean

### (1) Do Claims A/B hold under our Internally6 / NoSep / NoShortSepCycle?

**Definitions [read].**
- `Internally6` (ClaimGlue:69) bundles Triangulated, minDeg 5, `NoSep` and `NoShortSepCycle`.
- The C glue does not take `Internally6`. `CEntryF.colorable` derives `NoSep` and `NoShortSepCycle` from `MinimalCounterexample` and
  `htri`. The facts are the same, and minDeg is not needed.
- `NoSep` (SideTriangle): every triangle is `Facial`.
- `NoShortSepCycle` (ClaimGlue:64): no `Cyc` of length ≤ 5 with `BothSides`, plus `BothSides2` when r = 5.
- `Cyc` (DCheckPinchGeom:24) needs only T-adjacency and injectivity, so chords are allowed.
- `BothSides` (SepAll:29) needs a non-isolated off-cycle vertex on each `CycPotential` side.

**Claim A** (8 ring vertices distinct in 2.126). Suppose ρ i = ρ j with i ≠ j.
- **Consecutive positions:** distinct, because `FaceWalk` edges are G-edges.
- **"p = q impossible":** our `NbrInj` (`RotOcc.nbrInj`, from true degree + `chain_inj`). ✓
- **"p ~ q gives a separating triangle":** our `exclB`/`excl_sound`.
  - NoSep makes the triangle facial, `ApexFacts` makes v a configuration ring vertex adjacent to both, and `NbrInj` forces i = j.
  - The content is the same, phrased as "facial ⇒ configuration apex" rather than "separating". ✓
- **Which pairs are left.**
  - The inner neighbour sets are: R0 {I0,I3}, R1 {I0}, R2 {I0,I1}, R3 {I1}, R4 {I1,I2}, R5 {I2}, R6 {I2,I3}, R7 {I3}.
  - The interior graph is K4 minus I1I3.
  - So `exclB` fails only when N(i) = {I1} and N(j) = {I3}, which is the **single pair (R3, R7)** (lead's 4 and 8).
- **"{p,q} = {R,S} gives a separating 4-cycle x,R,P,S":** this applies in our framework.
  - The cycle is `Cyc T 4 (cyc4 v ι1 ι0 ι3)`, injective by `disj` and `ιinj`, with the potential from `exists_cycPotential'`.
  - `apex_sides` on the cycle edge ι0–ι1 gives its two face apexes, R2 and I2 (from rot(I0)), on opposite sides. Both are off the cycle:
    - ρ2 ≠ v by `exclB(2,3)`;
    - I2 ∉ {ι0, ι1, ι3}.
  - Both are non-isolated, so `BothSides` holds with r = 4, and `NoShortSepCycle` is contradicted. ✓
  - **Caveat [read]:** our decidable `cycCertB` (CGlue:801) would **reject** this certificate. It requires the chosen path edge to have
    no common ring neighbour, but I1–I0 share R2, I0–I3 share R0, and the I2 path has R4 and R6. So Claim A is true in our framework,
    but its (R3, R7) case needs a `cycCertB` variant that allows a ring apex certified off-cycle by `exclB`. That is about 1–1.5 pd.
  - **2.126 does not need it:** no X-class touches R3 or R7.

**Claim B** (T/X loopless).
- **"1~3 gives triangle 1,3,P which separates 2":** in our Lean the triangle ι0, ρ0, ρ2 is *facial* by NoSep. The `RotOcc` rotation at
  I0 then contradicts it, because R0's rotation neighbours are R1 and I3 (E4). ✓
  - It needs `RotOcc`, not just `ApexFacts`: `ApexFacts` covers interior edges only, and this triangle has one interior vertex.
  - So the C occurrence must be `OccursCXR`-style, not bare `OccursCXF`.
- **"Two classes meeting excluded by Claim A":** only the 4 cross pairs {R0,R2}×{R4,R6} are needed, and all are `exclB` via I0 ~ I2 (E2). ✓
- **Missing from the hand argument:** the D1 events R1 ∈ {R0,R2} and R5 ∈ {R4,R6}. Each would turn the kept edge I0–R1 (or I2–R5) into
  a loop. They are excluded by `NbrInj` (E3). ✓
- With E3 added, Claim B holds and is exactly E1–E6.

### (2) Does our OccursC / OccursCXF require an injective ring? **No** [read].

- `ConfigOccW` (DCheckOccWalk:18) has `ring : FaceWalk G r ρ`, which allows folds and pinches, together with `ιinj`, `ringOff`, `hG`, `nbr`.
- `OccursC`/`OccursW` (ClaimGlue) are `ConfigOccW` plus the support bound.
- `OccursCX` (CGlue:1340) adds `OccExact` and `XRingSimple`, which is injectivity at touched positions only.
- `OccursCXF` (CGlue:1459) adds `OccExact`, `NbrInj` (the ring neighbours of *one* interior vertex are distinct) and `ApexFacts`.
- `OccursCXR` (COccBridge) is `ConfigOccW` + `RotOcc` + `rotOK`.
- The generated `Occ` structures have no `ring_inj`. `ring_dinj_of` derives dart-distinctness only.
- Only `ConfigOcc` has `ring.inj`, and the C path does not use it.

### (3) Is the clause used only to exclude ring coincidences and loops? **Yes** [read, §1].

- Every (C) use is in C4b, the loop-freeness proof. Each one excludes either:
  - a chord or loop inside a class (CGlue:635), or
  - a ring coincidence that would make the label ↦ vertex map multivalued (CGlue:1107).
- So yes: the per-config lemma for 2.126 consists of:
  - one merge label lemma (M2);
  - a decidable check: `foldSafeX` (existing), `coherB` and `chordB`;
  - their soundness from `excl_sound`, NoSep and `RotOcc` (M3).
- It needs no general ring-merge theory, no T-level circuit lemma and no Claim A (the (R3, R7) case is never needed).
- The lead's "T-level loopless lemma" is also not needed for 2.126. The label κ reduces looplessness directly to E1–E6.
- **pd: 4.25–5.75, central ≈ 4.75.**

### (4) Would the lead's loopless lemma generalise to other ring-merge C configs? pd.

**Today's demand.** Only 2.126 needs a ring merge (128.1324802 has been replaced by a rule). The 51 none configs use the chord route.

**Cheap generalisation [inf].** M2 is already generic. M3's `chordB` covers any config whose merged classes are single-centre stars.
- A class with two centres needs a 4- or 5-cycle certificate for its chords: a ring–I–I–ring path plus T-edge, which is the lead's
  length-4/5 case. That is the `cycCertB` ring-apex variant above.
- Cost: +1.5–3 pd.

**The lead's T-level lemma.** Statement: loopless ⇔ no facial triangle with two X-edges and no degree-5 vertex with 4 rim edges in X.
Two corrections against our definitions:
- It should read "a circuit with **exactly** one edge outside X". A circuit made only of X-edges is harmless for `XLoopFree`, which
  constrains non-X edges only.
- "length 4: non-separating, so it has a chord" needs the lemma "a `Cyc` with an empty side in a triangulation has a chord / ear". We
  do not have it. It is SCOPING piece E.

In our Lean the lemma would cost:
- B (length bound): 1 pd;
- C (shortest H-path closed to a `Cyc`): 1.5–2.5 pd;
- an E-lite (empty side ⇒ chord or ear, chorded `Cyc`): 3–5 pd, the main risk;
- the degree-5 case: `¬BothSides2` at r = 5, `side_step_cyc`, minDeg; this needs `hdeg` plumbing through the C interface, 0.5–1 pd;
- the lift of the lead's two decidable checks (inner-vertex consecutiveness via `RotOcc`; a shared ring end must be an apex of pq via
  `ApexFacts`): 1–1.5 pd.

**Total ≈ 8–13 pd, central 10**, on top of M1 (shared). It generalises to all |X| ≤ 4 configs, but nothing needs it now.

### Nice-to-have: does Claim A hold for every config with interior diameter ≤ 2? [inf] **Yes**, with one caveat.

**Argument.** Suppose ρ i = ρ j.
- If some inner neighbours p, q are equal or adjacent, `exclB` applies.
- Otherwise pick p, q at interior distance 2 through m, and take the 4-cycle v, p, m, q.
  - The two face apexes of the cycle edge m–p are the rotation neighbours of p in rot(m). Each lies in a different arc between p and q,
    because p and q are non-adjacent.
  - By `apex_sides` they lie on opposite sides.
  - An apex is ≠ q (q is not adjacent to p).
  - An apex is ≠ v. If v = ρ k with k a ring neighbour of p, `NbrInj` at p gives k = i. Then m is an inner neighbour of i that is
    adjacent to q, and `exclB` would already have applied.
  - So `BothSides` holds and r = 4 contradicts `NoShortSepCycle`.

**Caveats.**
- Each ring vertex must have an inner neighbour (true in kc free completions [unverified in general]).
- The Lean form needs the same `cycCertB` ring-apex variant (1–1.5 pd).
- Diameter here means diameter in `intAdj`.
