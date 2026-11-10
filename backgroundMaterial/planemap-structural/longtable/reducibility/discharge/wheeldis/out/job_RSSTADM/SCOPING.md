# SCOPING: porting Gonthier's `valid_contract` route into the Lean C glue (10 Nov 2026)

This is a reading-only estimate. I built nothing, ran no Lean, and read no W6b code.
Tags used below: **[read]** means I checked it in the named file. **[inferred]** means it is my
reasoning or an estimate. **[unverified]** means it comes from memory or another person and I did
not check it in these sources.

Sources read: `in/fourcolor_src/{coloring,contract,birkhoff,embed,geometry}.v`; `in/ADMISSIBILITY.md`,
`in/REPORT.md`. Lean (dcheck/): `ClaimGlue.lean`, `SepAll.lean`, `SideCycle.lean`,
`DCheckPinchGeom.lean`, `DCheckOccWalk.lean`, `CGlue.lean` (admissibility, C4, fold block, C6),
`CXRing.lean` (head), `COccBridge.lean` (head), `C66666.lean` (`extCAux`).

## 0. The shape of Gonthier's argument (what has to be ported) [read]

- `valid_contract r cc` (coloring.v:462) has four conjuncts:
  - off-ring: `[disjoint r & insertE cc]`;
  - sparse: `sparse (insertE cc)`, i.e. no node holds two contract darts;
  - size: `pred4 1 2 3 4 (size cc)`;
  - triad, needed only when `size cc = 4`: `~~ [disjoint kernel r & triad (insertE cc)]`.
- `contract_ring cc p` (contract.v:25) is `scycle rlink p`, `proper_ring p` and `behead p ⊆ insertE cc`. In words: a cycle
  in which every edge except one is contracted.
- All of `sparse_contract_ring`, `contract_ring_max`, `contract3_valid` and `triad_valid` sit under
  `Hypothesis cexG : minimal_counter_example G` (contract.v:31). They are proved **in the big map**, not in the
  configuration.
- `embed_valid_contract` (embed.v:1377) moves validity from the configuration to the big map as `valid_contract [::] ccr`.
  It relies on `embed_sparse` (embed.v:1312, through `embed_inj`/`embedN`) and on `cface_ac_h1`. For the second triad clause
  it also relies on `adj11_edge` (birkhoff.v:545).
- `triad_valid` also uses `pentaG` (minimum arity 5), `scycle_spoke_ring`, `size_spoke_ring`, `fband_spoke_ring` and
  `fcard_adj_max` (birkhoff.v:398-668, about 270 lines of spoke-ring machinery).
- **Plug-in point on our side [read].** `CEntry.colorable_of_contract` (CGlue.lean:1367) already takes
  `hlab : XLoopFree …` as a hypothesis. The labels and `admissibleX` reach it only through `xGraph_labels*`.
  `contract_reducer_of` takes `hadm` but never uses it in its body. hC is untouched:
  - C1–C3 do not use labels;
  - `extCAux_canon` (CGlue.lean:260) needs only `XCompat`;
  - `extCAux` (C66666.lean:85) forces `x = col k t` for every contracted `(t,a)`, so merged ring positions must share a colour.
- **So the port has one target: `¬ ContractRing` in `T` implies `XLoopFree`.** No label argument is needed. Gonthier's
  `contract_coloring` induction is not needed either, because C4a (`contract_subgraph_gen`) already contracts every
  component at once. On these two points W6b's table is right [read].

## 1. Effort estimate

### Assumptions [inferred]

1. **Target.** The target is a new entry type `CEntryV` (`validContract` in place of `admissibleX`/`lbl`, no `XRingSimple`).
2. **Occurrence.** It is `OccursCXF` built from a rotation occurrence (`RotOcc` plus `rotOK`, COccBridge.lean). That gives
   `OccExact`, `NbrInj` and `ApexFacts`, and lets us derive more rotation facts.
3. **Facts about T.** `T` is a triangulation with `NoSep`, `NoShortSepCycle` (ClaimGlue.lean:64, which is a theorem for a
   minimal counterexample, `noShortSep` :88) and minimum degree 5.
   - **Caveat [read]:** today's C interface (`CGlueXF`, and the `hC … htri h hT.smaller` call in ClaimGlue) passes only
     `T.Triangulated`, not `hdeg`. The gate (`four_color_of_smaller_gate`) does supply `hdeg`, so some plumbing is
     needed (piece I).
4. **Statement level.** Everything is stated on `SphericalMap`. Sides come from `CycPotential`/`OnSide`, not from a
   Jordan/disk library. We have no counterpart to Gonthier's `diskN/diskF/chord_ring/fproj`. This is the main reason the
   Lean will be several times longer than the Coq.
5. **Pace.** "Careful pace" means one person on the existing Mathlib fork, with slow elaboration, at about 60–90 checked
   lines a day for planar lemmas and more for data or plumbing. Compute for the per-key `cReducible18` runs is not counted.
6. **Calibration.** Sizes are calibrated on comparable existing Lean:
   - `cyc_sound` (CGlue.lean:947-1080, about 135 lines), which builds a `Cyc` from configuration data and uses
     `apex_sides`;
   - `xGraph_labels_fold` (about 160 lines);
   - the fold block (CGlue.lean:760-1160, about 400 lines);
   - `SepAll.lean` (464 lines for sides, chords and Birkhoff glue).

### Pieces

| # | Piece | Reuse | New | Lean lines | Days |
|---|---|---|---|---|---|
| A | `validContract cf eqR eqI : Bool` with spec lemmas: dedupe, size 1..4, off-ring (automatic: X uses listed edges with an interior end), sparse, triad | `admissibleX` style, `List.all` unpacking | Sparse has to be **graph-triangle** sparse. `Conf` keeps `ringAdj`/`intAdj` apart and has no rotation [read: CXRing data, C66666 `w66666`]. Graph-sparse ⇒ facial-sparse is the sound direction. The triad counts listed neighbours of an interior vertex among X endpoints, plus one endpoint that is neither listed nor equal to the vertex. | 80–150 | 1–2 |
| B | `ContractRing T H k ρ` (a `Cyc` whose edges are all `H`-edges except edge 0) and `contract_ring_max` (k ≤ \|X\|+1) | `Cyc` (DCheckPinchGeom:24) | Count the T-edges of `xGraph` (≤ \|eqR\|+\|eqI\|, using `NbrInj`/`ιinj`); inject the cycle edges into them | 60–120 | 1 |
| C | `XLoopFree` from `¬ContractRing`: take a shortest `H`-path (Mathlib `Walk.toPath`), close it with the offending T-edge, convert to the periodic `ρ : ℕ → Fin n` form, show length ≥ 3 | `XLoopFree`, `contract_reducer_of` | All four conjuncts follow, labels included. One case is a listed non-X edge `(a,t)` with `ρ t = ρ t'` and `(t',a) ∈ eqR`; `NbrInj` excludes it. | 120–200 | 1.5–2.5 |
| D | **Sparse lift:** no facial triangle of `T` contains two `H`-edges | `RotOcc`, `apex_from`, `ApexFacts`, `NbrInj` | `ApexFacts` covers interior edges only. Ring–interior X-edges need a ring-apex form from `RotOcc` (about 60–100 lines). Then a facial T-triangle with two X-edges is a configuration graph triangle with two X-edges. | 150–250 | 2–3 |
| E | **`sparse_contract_ring`:** every contract ring has a non-isolated off-cycle vertex on each side (`BothSides`) | `onSide_of_dartC'`, `side_step_cyc`, `apex_sides`, `exists_cycPotential'`, the `sides_split` idea (SepAll:252) | Induction on length. On an empty side, the facial triangle at the uncontracted edge has its apex on the cycle. If the cycle is a triangle, two X-edges share a face, which contradicts D. Otherwise a chord gives a shorter contract ring whose empty side lies inside the old one. `sides_split` needs an `ICycle`; chorded sub-cycles need a `Cyc` version. | 250–450 | 4–7 |
| F | `contract3_valid`: \|X\| ≤ 3 ⇒ length ≤ 4, and E with `NoShortSepCycle` gives a contradiction | B, E, ClaimGlue:64 | Glue only | 30–60 | 0.5 |
| G | **`triad_valid`:** \|X\| = 4 and a 5-ring | B, E, `NoShortSepCycle` at r = 5 (`¬BothSides2`) and r = 4, `apex_sides` | Steps (i)–(iv) below. Gonthier's 65 lines of Coq rest on about 270 lines of spoke-ring lemmas that we do not have. | 300–500 | 4–7 |
| H | **Triad lift** from the configuration to `T` | `nbr`, `NbrInj`, `ιinj`, `ringOff`, `NoSep`, `RotOcc` | The count is easy. The clause "v is not adjacent to some X endpoint" does **not** lift by `NbrInj` alone, because a folded ring endpoint can equal a listed neighbour of v. It needs Gonthier's `adj11_edge` argument: if v is T-adjacent to both ends of an X-edge, NoSep makes that triangle facial, and the rotation at the X-edge's interior end then gives configuration adjacency. | 100–200 | 1.5–3 |
| I | Integration: `CEntryV`, `OccursCXV`, `CEntryV.colorable`, a hadm-free copy of `contract_reducer_of`, and threading `hdeg` (minimum degree 5) through the C interface in ClaimGlue/CGlue/CGlueU | C6 assembly | Mostly plumbing | 100–200 | 1–2 |
| J | Per-key data: the 51 (plus the 3 held registry entries) as `XRData`-like records with `rotOK`, and one `native_decide` for `validContract` | CXRing format | Data generated by a script. The `cReducible18` hC runs are extra compute (rings 8–14), and none has been run. | 300–500 (data) | 1 |

Steps of G:
1. Exactly one vertex `y0` lies on one side. E gives at least one; `¬BothSides2` gives at most one.
2. All neighbours of `y0` are on the cycle (`side_step_cyc`). With degree ≥ 5, `y0` is adjacent to all 5 cycle vertices.
3. All X endpoints are on the cycle. Otherwise the ring uses at most 3 X-edges, so its length is at most 4, a contradiction.
4. Take the triad vertex `x0`. If `x0 = y0`, it is adjacent to every endpoint, a contradiction. Otherwise `x0` has 3
   neighbours on the cycle, two of them non-consecutive. Together with `y0` they form a 4-cycle; `apex_sides` at a `y0`-edge
   puts vertices on both sides, which contradicts `NoShortSepCycle` at r = 4. This needs the facial triangles at `y0` to be
   consecutive cycle pairs, which comes from NoSep (the triangle `y0, p_i, p_{i+2}` is not facial).

**Total [inferred]: about 1,500–2,600 lines (1,200–2,100 of proof plus 300–500 of data), about 17–30 person-days, central
estimate 23.**
- **The hardest step is G (`triad_valid`).** E (`sparse_contract_ring`) is close behind. Both are planar arguments that
  Gonthier gets from his disk and spoke-ring library. Here they must be redone with potentials.
- **Second hardest: H's non-adjacency clause and D's ring-apex facts.** In both, folds matter.
- **Low risk: A, B, F, I, J.**
- **Main schedule risks:**
  - E's induction may need a general "sub-cycle side ⊆ cycle side" lemma for chorded cycles. `sides_split` covers only
    induced sub-cycles.
  - G step 4 needs the rotation at `y0`, which is not a configuration vertex, so no `RotOcc` fact applies. It has to come
    from NoSep plus triangulation.

**A cheaper alternative [inferred]: W6b's chord route.**
- It means:
  - relaxing `admissibleX`'s ring-distinct conjunct;
  - a per-pair certificate in the style of `cycCertB`: X-path P of length l ≤ 3, plus a P-edge whose two face apexes are
    configuration vertices off the cycle;
  - a soundness lemma copied from `cyc_sound`.
- Estimated at 400–700 lines and 6–10 days. Covers the 51 (all have l ≤ 3).
- It does not cover general 4-edge X that need 5-cycles, and it keeps `XRingSimple`.
- `Cyc` asks only for `T.Adj` [read], so a cycle that contains the outside chord is accepted. `apex_sides` works on any
  cycle edge with `Nx` facts, so the certificate's crossing edge should be a P-edge, not the chord. That settles W6b's open
  question "do `Cyc`/`apex_sides` accept a G-edge": they do.

## 2. Birkhoff clause: is `BothSides2` the same as Gonthier's 5-cycle clause?

**Gonthier [read]:**
- birkhoff.v:345-346: `Theorem Birkhoff (r : seq G) : size r <= 5 -> scycle rlink r -> nontrivial_ring (size r == 5) r = false.`
- The definition of `nontrivial_ring` is in a file not supplied (snip/jordan). From memory [unverified] it is
  `(m < fcard face (diskF r)) && (m < fcard face (diskFC r))`.
- That reading is consistent with every use I read:
  - `nontrivial0P` produces a face in `diskF` and one in `diskFC` (contract.v:194);
  - `triad_valid` refutes `nontrivial1P` by exhibiting **two** distinct faces on each side (contract.v:195-207).
- `diskF r` excludes `fband r`. In the triangulation, its faces are vertices off the cycle, strictly on one side.
- `scycle rlink` allows chords.

**Ours [read], ClaimGlue.lean:64 and SepAll.lean:29, :411:**
```
def NoShortSepCycle T := ∀ r ρ c, Cyc T r ρ → r ≤ 5 → CycPotential T r ρ c →
    BothSides T r ρ c → (r = 5 → BothSides2 T r ρ c) → False
def BothSides2 … := ∀ b : ZMod 2, ∃ x x' y y', x ≠ x' ∧ ¬ OnCyc r ρ x ∧ OnSide T c b x ∧ T.Adj x y ∧
    ¬ OnCyc r ρ x' ∧ OnSide T c b x' ∧ T.Adj x' y'
```
- `Cyc` is chords-allowed (DCheckPinchGeom:24). It is proved for minimal counterexamples by
  `colorable_of_short_separating_cycle` (SepAll:450), with no `sorry` in SepAll/Sep5/ClaimGlue [read].

**Verdict: equivalent for cycle lengths 3–5 [inferred from the definitions].**
- Both say:
  - a cycle of length ≤ 4 has an empty side;
  - a 5-cycle has a side with at most one off-cycle vertex.
- The encodings differ, and none of the differences matters:
  - Ours asks for non-isolated vertices. This rules out vacuous `OnSide` for vertices outside the support; Gonthier's maps
    have no isolated faces.
  - Ours quantifies over every potential `c`. Potentials of one cycle differ only by a constant, so this is not stronger in
    substance.
  - Gonthier also covers ring sizes 0–2. These are irrelevant in a simple graph.
- **For the port:** `¬BothSides2` together with E's `BothSides` gives exactly the "one vertex `y0` on one side" fact that
  `triad_valid` needs, so no strengthening of B2 is required. Two things are still missing:
  - Gonthier's consequences of that fact (`y0` adjacent to all 5, `fcard_adj_max`). They are new work (piece G).
  - Minimum degree 5. It is not part of `NoShortSepCycle` and is not passed to the C glue today.

## 3. W6b's chord argument (ADMISSIBILITY.md "Is adding it sound?", and RSST-NONE2): issues

Line numbers refer to `in/ADMISSIBILITY.md`.

1. **The Jordan step is not proved (l.156-160), and W6b says so (l.175-177).**
   - The claims: "Inside the configuration disc, P separates the two ring arcs… Outside the disc, the chord separates them
     too."
   - This assumes:
     - the configuration is an embedded closed disc;
     - the outside is a disc;
     - the two arcs share no T-vertex.
   - `ConfigOccW` allows folds and pinches, and `XRingSimple` constrains only touched positions. If an untouched vertex of
     one arc is folded onto a vertex of the other arc, the arcs are joined off C, so they are not on opposite sides, and the
     witness for "both sides" disappears.
   - The fix is the apex certificate, which needs no disc picture.
2. **l.148 assumes more than `XRingSimple`.** The claim: "If either end of e is interior, e is a listed configuration
   edge, so the local check excludes it."
   - The label check compares `L a` with `L(m+t)` by **position**. It is sound in T only if `ρ t` cannot equal a touched
     position of the same component.
   - That holds under `XRingSimple`. It fails in the fold-allowed setting (`OccursCXF`) unless `foldSafeX` is extended,
     which W6b leaves "not checked" (l.203).
3. **The 5-cycle case (l.162-163) is asserted, not argued.** The claim: "The only shape that allows a single vertex is gap
   2 with the middle ring vertex adjacent to all 3 inner vertices; kc -C2 refuses that shape."
   - The single vertex could also be an outside or interior vertex on a side whose arc vertices are on the cycle. The
     argument also rests on kc source behaviour (an unchecked comment, l.108).
   - It is moot for the 51 (l ≤ 3). It is a real gap for the general relaxation, and also for the Lean entries
     "4-edge X without a triad" that `admissibleX` admits (l.405-407).
4. **The table entry "global no-loop fact proved once" (l.107-108, written before RSST-NONE2) is misleading.**
   - Gonthier proves it in the big map from **lifted** sparse and triad, using minimum arity 5 and Birkhoff at size 5.
   - Neither our C++ nor our Lean has the lift.
5. **RSST-NONE2 l.445 is wrong.** The claim: "In Gonthier's route the loop argument runs in the big map, so folds of
   touched ring positions do not affect it."
   - Folds do not affect the big-map argument **given** T-level sparse and triad. They do affect the **lift**:
     - Sparse lifts only with `NbrInj` plus rotation facts for ring–interior edges. `ApexFacts` covers interior edges only.
     - The triad's non-adjacency clause does not lift through `NbrInj` (l.442 says "true degree, NbrInj"). A folded ring
       endpoint can be a listed neighbour of the triad vertex. Gonthier needs `adj11_edge` and NoSep (embed.v:1395-1401).
6. **l.442 underrates the lift ("25 lines, on top of embed.v's morphism").**
   - Those 25 lines rely on `embed_inj`, `embedN`, `embed_sparse` and `cface_ac_h1`, which are hundreds of lines of
     embed.v.
   - Our counterpart (`RotOcc`/`NbrInj`/`ApexFacts`) is weaker. It is local and allows folds.
7. **l.437 "Nothing new for the length-5 case" holds for the hypothesis (§2) but not for its use.** `triad_valid` also
   needs minimum degree 5 and the common-neighbour bound (`fcard_adj_max`). The minimum degree is not available in the
   current C interface.
8. **Several claims rest only on engine runs.** "Every local condition holds", "kc and cfast put ring edges in the loop
   check" (l.149) and "cfast ringEq" are engine or source claims, not proofs. hC (`cReducible18`) has **not** been run in
   Lean on any of the 51 (l.210). My reading of `extCAux` (C66666:85) agrees that merged ring positions are handled
   correctly, so the remaining risk is compute, not logic.
9. **The 384/384 `valid_contract` check is a consistency check of W6b's own translation (l.384-386), not evidence about
   Gonthier's encodings.** W6b says so. It does not show that Gonthier's `configurations.v` contracts equal RSST's.
10. **Minor points:**
    - "admissibleX plus the triad implies valid_contract" (l.413) also needs deduplicated eqR/eqI (W6b notes it).
    - "graph-sparse implies facial-sparse" (l.436) is the right direction, but A must then be stated with graph triangles,
      ring-consecutive pairs included, because `Conf` has no rotation.
    - W6b's open question (l.202/227) "do `Cyc`/`apex_sides` accept a non-configuration edge" is answered: yes. `Cyc` needs
      only `T.Adj` [read].

## 4. Recommendation [inferred]

- **For the 51 now:** the chord certificate (§1 alternative). It costs about 6–10 days and keeps `XRingSimple`. The
  crossing edge should be on P, and its two apexes should be checked to be configuration vertices off C. For l = 2 that
  edge is a ring–interior edge, which `cycCertB` does not support today.
- **The full `validContract` route** costs about 17–30 days. It is worth doing only if general 4-edge X with 5-cycle contract
  rings, or folded-ring C entries, are needed. Start with pieces E and G, the risky ones, before writing A or J.

## Addendum A (10 Nov, ~11:45Z): Birkhoff clause rechecked against revsnip.v

Source: `revsnip.v` staged at `ext_handoff_nov3/rsst/adm/fourcolor_src/revsnip.v` (commit 815b38bba), md5 3607bab1, copied
to `in/fourcolor_src/revsnip.v`. Reading only; no Lean written.

**Confirmed. `NoShortSepCycle` (with `BothSides` / `BothSides2`) states the same thing as birkhoff.v:345 for ring sizes 3-5.**

What changed since §2:
- **The definition is now [read], no longer from memory.** revsnip.v:66-67:
  `Definition nontrivial_ring m (r : seq G) := (m < fcard face (diskF r)) && (m < fcard face (diskFC r)).`
  The header (revsnip.v:15-17) says diskF r / diskFC r are the faces strictly inside / strictly outside r.
- **Both reflection lemmas are [read]:**
  - revsnip.v:94-95 (`nontrivial_ring 0`) says each of diskF r and diskFC r has a dart.
  - revsnip.v:103-105 (`nontrivial_ring 1`) says each has two darts x, y with `~~ cface x y`. That means two distinct faces
    on each side.

The translation. Gonthier's faces are the regions of the map, which are our vertices.
- `scycle rlink r` is a simple ring of regions, each consecutive pair adjacent. That is our `Cyc`: ρ injective below r,
  cyclically adjacent, chords allowed.
- "Strictly inside / outside" excludes `fband r`, the ring's own regions. That is our `¬ OnCyc`.
- `fcard face (diskF r)` counts the regions strictly on one side. That is the number of off-cycle vertices with
  `OnSide T c b`.
- m = (size r == 5):
  - size ≤ 4 (m = 0): Gonthier says some side has no region. Ours says ¬`BothSides`.
  - size 5 (m = 1): Gonthier says some side has at most one region. Ours says ¬`BothSides2`; since `BothSides2.both`,
    the extra `BothSides` hypothesis in `NoShortSepCycle` adds nothing at r = 5.

The encoding differences, each checked:
1. **`T.Adj x y` (non-isolated).** `OnSide T c b x` is `∀ d, d.fst = x → c (faceOf d) = b` (SideTriangle.lean:273). It
   holds vacuously, for both b, at a vertex with no darts. Without the Adj clause such a vertex would satisfy `BothSides`
   on its own. With it, only vertices that have darts count, and these are exactly Gonthier's regions. This is a needed
   guard, not a weakening; in a connected map with n ≥ 2 it excludes nothing real.
2. **The side split: `c` against `diskF` / `diskFC`.** [inferred]
   - Off the cycle, `c` is constant on all darts at a vertex (`side_constC'`, DCheckPinchGeom.lean:112-115), and it flips
     exactly across cycle edges (`CycPotential`).
   - So along any dual path, `c` changes parity at each crossing of the cycle. Each class {x off cycle : `OnSide T c b x`}
     is therefore exactly one Jordan side. This holds for every potential `c`; a second potential only swaps b ↔ 1 - b,
     and both `BothSides` and `BothSides2` are symmetric in b.
   - This step stays [inferred], not [read]: `diskN` / `diskF` are defined in snip.v, which is not staged. If an exact
     match is wanted, staging snip.v (its `diskN` / `diskF` / `diskFC` definitions) would settle it.
3. **Sizes 0-2.** Gonthier covers them; `Cyc` needs 3 ≤ r. In a simple-graph triangulation a 2-ring of distinct regions
   would need a double edge, and a 0- or 1-ring has no inside. So nothing is lost.
4. **Scope.** Both are proved for a minimal counterexample: Gonthier's `Section Birkhoff` assumes
   `minimal_counter_example G` (birkhoff.v:172); ours is `MinimalCounterexample.noShortSep` (ClaimGlue.lean). The two
   theorems have the same strength in the setting where the C glue uses them.

Consequence for the port: §2's conclusion stands. ¬`BothSides2` plus `BothSides` gives `triad_valid`'s one-region side
exactly. The valid_contract port stays ON HOLD (relay 11:30Z).

## Addendum B (10 Nov, ~11:55Z): the side step of Addendum A, now from snip.v

Source: `snip.v` staged at `ext_handoff_nov3/rsst/adm/fourcolor_src/snip.v` (commit 8095a6831), md5 4688980d, copied to
`in/fourcolor_src/snip.v`. Reading only; no Lean written.

**Result: the step is now [read] at the level of Gonthier's definitions and lemmas, with no refutation.** The OnSide
classes of any cycle potential `c` are exactly diskF r and diskFC r, up to swapping b ↔ 1 - b. The only remaining
[inferred] item is the dictionary between the two formalisms (stated below). Any comparison of a hypermap with our
SphericalMap needs it, and it is the same dictionary §2 and Addendum A use.

**Dictionary [inferred, standard duality].** Gonthier's G is the plain cubic dual of our triangulation T:
- G-faces (regions) = T-vertices;
- G-nodes (3-orbits) = T-triangles (`T.Face`);
- G-edges {x, edge x} = T-edges;
- dart y of ring r is the dart at region ρ_t whose `edge y` lies in region ρ_{t+1} (`rlink x y := cface (edge x) y`,
  geometry.v:662).

Definitions and lemmas used, all [read]:
- (D1) snip.v:81-87: `diskN := has (dconnect x) r`, `diskE := diskN \ r`, `diskF := diskN \ fband r`, and
  `diskFC := (¬diskN) \ fband r`. So diskF and diskFC partition the darts off `fband r` by membership in diskN, which is a
  definition and needs no proof.
- (L1) snip.v:89 `diskN_node`: diskN is node-closed. A T-triangle is therefore wholly in or wholly out of diskN, so
  δ(f) := [f ⊆ diskN] is well defined on `T.Face`.
- (L2) snip.v:101 `diskN_E`: every ring dart y is in diskN.
- (L3) revsnip.v:193 `diskN_edge_ring`: for y ∈ r, `edge y ∉ diskN` (this needs `proper_ring r`, which holds for size ≥ 3).
- (L4) snip.v:123 `diskE_edge`: diskE is edge-closed.

The argument [inferred from the read facts]:
1. **δ is a potential for the cycle.** For adjacent T-triangles f, f' across T-edge e, δ(f) + δ(f') = cycInd(e):
   - e a cycle edge. Its darts are y ∈ r and edge y. By (L2) and (L3), y ∈ diskN and edge y ∉ diskN, so the sum is 1.
     That equals cycInd(e), because the r ≥ 3 cycle edges are distinct.
   - e not a cycle edge, chords included. Neither of its darts is in r: every ring dart lies on a cycle edge, and
     `edge y ∈ r` would force ρ_t = ρ_{t+2}. Then (L4), together with x ∈ diskN ∧ x ∉ r ⇔ x ∈ diskE (and `edge` an
     involution), gives x ∈ diskN ⇔ edge x ∈ diskN. So the sum is 0 = cycInd(e).
2. **Any potential is δ or δ + 1.** For `c` with `CycPotential T r ρ c`, c + δ is constant across every
   triangle–triangle adjacency (`CycPotential` is the same equation over `faceOf d`, `faceOf d.symm`). The dual of a
   connected triangulation is connected, so c = δ + k for a constant k. (`Internally6.connected`; Gonthier's G is
   `connected`.)
3. **The sides agree.** Take an off-cycle vertex x with a dart (the `T.Adj` guard). `OnSide T c b x` says every triangle
   at x has c = b, which is δ = b + k at every triangle at x. With (L1) and (D1):
   - b = 1 + k ⇔ region x ⊆ diskN ⇔ x ∈ diskF;
   - b = k ⇔ x ∈ diskFC.

   Hence {x : `OnSide T c (1+k) x`} = diskF r and {x : `OnSide T c k x`} = diskFC r, as region sets, and the counts are
   equal: `fcard face (diskF r)` is the number of such x.

Consequence: Addendum A's verdict moves from "confirmed, one step inferred" to **confirmed from the definitions**:
`NoShortSepCycle` with `BothSides` / `BothSides2` is birkhoff.v:345 for sizes 3-5, through the dictionary above.
Step 1's chord case needed no extra hypothesis, so chords are handled the same way on both sides.

## Addendum C (ST-118, 10 Nov ~15:20Z): cheapest sound Lean route for exactly 2.126 and 128.1324802

Context [read]: RSST-SUB2 (sub2 REPORT.md, MD5SUMS 2db58574) covers 143,535 of the 143,961 none-only full-world leaves with our own
admissibility. That leaves 426 leaves: 345 at d6 need 2.126, and 81 at d7 need 128.1324802. Of these, 329 are N up to ring 16
for |X| ≤ 4. So these two configs are needed themselves.

**The two configs [read, loop/k44 rsst.txt / rsst_verdicts_C2.txt]:**

| config | ring, m | RSST X (kc: adm=no) | shape |
|---|---|---|---|
| 2.126 = rsst003_2o126 | 8, 4 | {R0-I0, R2-I0, R4-I2, R6-I2} | two X-stars; I0 pins R0 and R2 (gap 2, R1 between); I2 pins R4 and R6 (R5 between); I0 ~ I2 is an interior edge |
| 128.1324802 = rsst065_128o1324802 | 12, 8 | {R0-I5, R10-I5, R6-I4, R8-I4} | the same shape; I5 pins R10 and R0 (R11 between); I4 pins R6 and R8 (R7 between); I4 ~ I5 is an interior edge |

So both are "double ring-merge" X:
- |X| = 4.
- There are two X-components. Each is a star (ring, interior, ring), and each meets the ring twice, at distance 2.

**Why our C path refuses them today [read, CGlue.lean:375-394].** `admissibleX` ends with "distinct ring positions have
distinct labels". The docstring says outright that "the three registry entries with an X-component through two ring vertices
fail this".
- The hC computation already handles merged ring positions: `extCAux cf eqR eqI` (C66666:85) and `cReducibleT` take eqR as
  data.
- So what blocks these two is the **glue's label clause** together with the loop-freeness that `admissibleX` + `XRingSimple`
  supply. It is not the colouring computation.

### (i) A per-config route for just these two [inf]

What has to be shown in T for an occurrence (`OccursCXF`, folds allowed) is that contracting X makes no loop and that the
contraction is well defined. The X-components are stars of radius 1, so every "contract ring" (a cycle made of H-edges except
one T-edge, piece B) has length 3: X-path a–I–b plus one T-edge a~b. The bad events are a finite list:

1. **A chord inside a star**, e.g. R0 ~ R2 in T.
   - The triangle R0 I0 R2 is facial by NoSep, so R0 and R2 are consecutive in rot(I0).
   - But rot(I0) is known in full from the occurrence (I0 is interior, `RotOcc`): it has R1 between R0 and R2, and other
     neighbours on the far side. Contradiction.
2. **A fold inside a star**, R0 = R2 in T: excluded by `NbrInj` at I0.
3. **A fold across stars**, e.g. R0 = R4.
   - The two components would merge, and the interior edge I0 I2 would become a loop.
   - Refute it with: v ~ I0, v ~ I2 and I0 ~ I2 make a triangle, facial by NoSep, so v is next to I2 in rot(I0). That is
     false in the occurrence's rotation of I0. There are 4 such pairs per config.
4. **A T-edge across stars** is harmless: it stays an edge after contraction.

What does **not** arise for these two:
- **Issue 1 (the Jordan step):** every bad cycle is a triangle, so NoSep alone suffices. No disc picture is needed.
- **Issues 3 and 7 (5-cycle / triad, min degree / `fcard_adj_max`):** with only stars there is no contract ring of length 4 or 5,
  so the triad condition is vacuous and min degree is not needed. Rotation at I0 / I2 comes from the occurrence.
- **Issue 4 (the global no-loop fact) and issue 6 (embed.v-sized lift):** replaced by the finite check above.

What remains:
- **Issues 2 and 5 (labels by position under folds; ring–interior lift):** these become the fold cases 2–3 above. They need
  the ring-apex form of `RotOcc` for R–I edges (piece D's 60–100 lines).
- **Issue 8 (no hC run yet):** run `cReducible18` with these eqR. Ring 8 and ring 12 need about 0.1–0.5 CPU-h.
- **Issue 10 (dedupe):** trivial for fixed data.

**Pieces and sizes:**
- **(i-a) Glue generalisation.** Allow an X-component to meet the ring twice in `admissibleX` / `xLabel` / the contraction
  soundness (CGlue + CContract C4a): ring labels equal exactly on eqR-merged pairs, which must be non-adjacent and distinct in
  T. 300–600 lines, **4–8 pd**. This is the main risk: if the distinct-label clause is used deep inside C4a, it is the upper
  end.
- **(i-b) Per-config certificate**, as a decidable list of the bad events above, each with its refutation (NoSep triangle +
  rotation position, or `NbrInj`), checked by `native_decide` on the two `XRData`. 150–300 lines plus data, **2–3 pd**. This
  is cycCertB extended to R–I edges, but only for triangles.
- **(i-c) Integration:** a `CEntryM` (merge) variant, `OccursCXF` threading, and two hC runs. 100–200 lines, **1–2 pd**.

**Total (i): about 550–1,100 lines, 7–13 pd, central ≈ 10 pd.**

### (ii) The general `valid_contract` port [read, §1]

About 1,500–2,600 lines, **17–30 pd, central 23**.
- It also needs (i-a): piece I's "hadm-free contract_reducer_of" is the same label generalisation.
- On top of that it adds E (sparse_contract_ring) and G (triad_valid). Those are the two hardest planar pieces, and these two
  configs never need them.

### Recommendation [inf]

**Route (i).** It costs about 10 pd against 23, and it avoids the two riskiest pieces (E, G) entirely.
- Its only real risk is (i-a). That work is shared with (ii), so (i) loses nothing if the general port is wanted later.
- **Start with a ½-day read of how CContract / CGlue use the distinct-ring-label clause.** That read settles the 4- vs 8-pd
  spread of (i-a), before any Lean is written.
- **Order:**
  1. that read;
  2. (i-a);
  3. (i-b) for 2.126 first (ring 8, small data, a quick hC);
  4. (i-b) for 128.1324802;
  5. (i-c).
- Not needed if the 345 + 81 leaves get substitutes from windows above ring 16 or with |X| > 4. The report notes that 97 of the
  426 still have 352 unscreened windows, but 329 do not.
