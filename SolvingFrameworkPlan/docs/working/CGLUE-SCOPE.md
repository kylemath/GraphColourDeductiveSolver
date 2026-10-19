# CGlue scope: the cheapest way to discharge C-soundness before 24 Oct (Long Table, 19 Oct 2026)

Context: `ClaimGlue.lean` (93797745) proves "reducible registry + `Unavoidable R` ⇒ 4-colourable". It leaves
`CGlue R.C` as an explicit hypothesis. Registry head (7360eb92): 1,990 D / 852 C. This note scopes the hypothesis.
Everything below is static reading plus my own scratch scripts on committed data. No engine was re-run: the run of the
Opus checker with C removed was blocked in this session. It is listed as test T1.

**Bottom line.**
- The 24 Oct claim (K ≤ 1 closed) needs CGlue for **one** entry, w66666. That entry can be discharged without any edge
  contraction by a **star reducer**: fill the ring face of the deleted map with one vertex. This is about 400–700
  lines of Lean, 1–2 Studio days, and all of it reuses proved pieces.
- The K = 2 registry's 852 C entries should be scoped as **[E2] with CGlue explicit** in the claim. K = 2 is not closed
  (t* = 2/13), so formalising C for it now would be premature.
- The LP does depend on C. 1,121 of its 1,884 C patterns are not covered by any D pattern. About 31% of kill-table
  cells list only C witnesses.

## (a) What the C checker certifies, and the Lean statement CGlue needs

**What cfast certifies** (`discharge/studio15/cfast.cpp`; Lean mirror `dcheck/C66666.lean`, `CWheels.lean`).
- Run the D-closure (`DCheck.run` semantics). Let `bad` be the ring-colouring classes it does not reach.
- For a fixed contraction set X of configuration edges, `testX` checks that **no bad class extends to the contracted
  configuration**. The extension test is `extC` / Lean `extCAux cf eqR eqI`:
  - a contracted ring–interior edge (t, a) forces col a = col t;
  - a contracted interior edge forces equal colours;
  - every other configuration edge forces different colours;
  - ring vertices identified through X must have equal colours.
- Equivalently: every ring code k with `extCAux k` is in the good set of `runGood`. That is exactly the Lean theorem
  shape `…_extX_reached` (native_decide).
- **Admissibility, local only.** cfast checks these conditions:
  - no loop inside the free configuration;
  - X off the ring;
  - 1 ≤ |X| ≤ 4;
  - sparse: no triangle with two X edges;
  - a triad when |X| = 4 (Gonthier's `valid_contract`).
- **Not checked:** the global minimal-counterexample conditions. Those are the outside chords and paths between ring
  vertices that X merges, and folded rings. The README says so explicitly.
- **There is no contraction-size bound beyond |X| ≤ 4.** Smallness is free: T/X has strictly fewer vertices whenever
  X ≠ ∅.

**X shapes in the registry head** (852 C entries, from the recorded `fixed X`):

| X shape | entries |
|---|---|
| one interior–interior edge (mostly I0–Ij) | 741 |
| one ring–interior edge | 1 |
| 2 edges (18 interior-only, 10 touching the ring) | 28 |
| 3 edges (5 interior-only, 38 touching the ring) | 43 |
| 4 edges touching the ring, one ring vertex per X-component | 36 |
| **an X-component containing two ring vertices** | **3** |

The three entries in the last row are `f7_..56757_...5...`, `f7_..65757_..55...` and `f7_..65757_..65...`.
- They merge two ring vertices. This is the case Job 21 refused to certify for the six 565xxx wheels.
- They are not sound under the local check alone. **Pull them, or re-check them with a ring-distinct X, before any
  claim cites them.**

Ring sizes run from 9 to 16 (486 of the 852 are ring 14). So the Lean side needs `runGood` for the parametrised
checker (`DCheckT`, table 9–10), not only `DCheck` at ring ≤ 13, which is what C66666 and CWheels use today.

**Precise Lean target.** It replaces `CEntry`/`CGlue` in ClaimGlue; `cf` uses the DCheck18 encoding.
```lean
structure CEntry where
  cf : DCheck18.Conf
  eqR : List (ℕ × ℕ)          -- contracted ring–interior edges (t, a)
  eqI : List (ℕ × ℕ)          -- contracted interior edges (b, a)
  hC  : cReducibleT cf eqR eqI = true   -- ∀ i, extCAux … ks[i] → (runGoodT cf).good[i]   (native_decide, per key)
  hadm : admissibleX cf eqR eqI = true  -- no internal loop, ≤ 1 ring position per X-component, 1 ≤ |X| ≤ 4 (decide)
  hr2 : 2 ≤ cf.r;  hr : cf.r ≤ 19;  hsym; hloop
theorem CEntry.colorable (e : CEntry) (hT : Internally6 T) (h : OccursW e.cf T)
    (IH : SmallerColorable T) : T.graph.Colorable 4
```
`CGlue R.C` then follows by one line, as `DEntry.colorable` does. The proof breaks into six pieces.

| Piece | What it is | Status / template | New Lean (est.) |
|---|---|---|---|
| C1 `runGoodT_sound` | `good[i] → Good cf ks[i]` | The `OuterInv` invariant of `DCheckS1.runRef_sound` already carries `good[j] → Good`. Expose it for the `runGood` copy (or redefine `run` through `runGood`). | 150–300 |
| C2 `extCAux` spec | `extCAux k ↔ ∃ lam` with the X constraints, invariant under `canon` | Copy `extendsQ_sound` plus `canon_rename` | 150–250 |
| C3 tail | realised code with `extCAux` ⇒ `Good` ⇒ `good_sound` with P = codes realised on G ⇒ colourable | Verbatim tail of `ConfigOccW.colorable_of_dReducibleT` (`FaceWalk.kempeMatching`); folded rings are already covered | 150–250 |
| C4 **reducer map** | a SphericalMap T′ with `supportSize T′ < supportSize T` and π : Fin n → Fin n that is the identity off the configuration and maps T-edges outside X to T′-edges | **New geometry.** Do not contract darts. Instead **refill the ring face of the deleted map G** (already given by `OccursW`) with the contracted configuration, using the surgery library of Job 25 (`split`/`RingFace.chordMap`, `growBefore_fills`, `Sep5Star.starMap`, face tracking). Reuse G's isolated interior vertices as the new vertices. | 1,000–2,500 (general X); 300–500 (star only) |
| C5 global loop-freeness | X-merged vertices are not adjacent through the outside | With ≤ 1 ring position per component, the remaining risk is a **folded ring** (two components whose ring positions are the same vertex) and **multi-edges** when refilling a face walk with repeats. Either prove ring positions distinct at the X-touching positions from `NoShortSepCycle` (the w66666 README argument), or require a simple ring for C occurrences. | 150–400 |
| C6 assembly + registry | `CEntry.colorable`, then one `CEntry` per key (`hC` native_decide at rings 14–16: tens of CPU-h, like Job 24b) | Copy `DEntry.colorable` | 100 + generated |

**Total.** Roughly 1,700–3,800 new lines for general CGlue, or 2,000 for single-edge X only, plus per-key native_decide
time. At Job 25's pace (B2, about 1,800 lines in about a day), general CGlue takes **4–7 Studio days**. That does not
fit before 24 Oct next to the binder queue.

**Templates.**
- Gonthier's Coq development is the direct template. `cfreducible` / `check_reducible_valid` (used in
  `c66666/fourcolor_w66666.v`) give C-reducibility of the configuration. `valid_contract` (sparse, |X| ≤ 4, triad; cited
  in the cfast README as `coloring.v`) is the admissibility condition. The embedding and contract files in
  `theories/proof` use Birkhoff no-short-cut facts to rule out loops after contraction in a minimal counterexample.
  Their structure (contract the configuration map, then patch it to the remainder along the ring) is the "refill the
  ring face" plan above.
- Studio has coq-fourcolor 1.4.3 installed (Job 20). It should read the exact file and lemma names there before C4/C5
  is designed; I have not verified them in this container.
- arXiv 2603.24880 (Lemma 8.2) handles the 66666 case with a larger configuration. It is not a template for the glue.

**The star reducer is the cheap special case.**
- If every ≤ 3-colour ring code is good, the reducer is G plus one new vertex joined to every ring vertex. That map is
  smaller whenever the configuration has ≥ 2 interior vertices.
- Its colouring restricted to G is a ring colouring missing a colour. No X, no contraction, no `extCAux` (C2) is
  needed.
- For w66666 the extendable-after-X set is **exactly** the ≤ 3-colour codes (`extX_iff_three`), and
  `three_colour_reached` is already proved. So the star reducer is equivalent to the certified contraction there.
- `Sep5Star.starMap` builds the star for r = 5. It needs generalising to an injective ring of length r, which is the
  same pendant-plus-chords loop.

## (b) How much the LP uses C

**Latest solve.** `loop/opus/P_own_lp/s24d/` (st24b: `sol_st24b.json`, `cert_st24bL.json`, 36 rows) on
`s25/argsA59.txt`, which pins registry 0125c46b (1,897 D / 838 C). It is on branch `claude/project-thread-7uelj0`, not
on main. Nothing newer has been solved; s28q is pricing only. Only bound numbers and pattern counts are recorded here.
No rule detail is.

**C enters the LP through two channels.**
1. **C pattern files** (`cpat=` in argsA59).
   - 1,884 distinct C patterns; the engine log prints the same number.
   - My own re-implementation of the pattern semantics gives D 16,937 and C 1,884, identical to `upper_st24b.log`.
   - **No C name also has a D verdict** (0 of 1,884, and 0 of the 852 registry C, searched across every `.out` file in
     wheeldis).
   - **Subsumption.** A C pattern is covered when a D pattern, under some rotation or reflection, constrains a subset of
     its slots with supersets of its letter sets. **763 of 1,884 are covered by an existing D pattern**, so they could be
     dropped from the LP at no cost.
   - **1,121 are not covered**: d=7 544, d=8 237, d=9 318, d=10 22. Of these, 699 come from the k3x registry, about 405
     from job27 (wheel-level C), and the rest from small files.
   - Registry head alone: **139 of the 852 C entries** are covered by a D pattern of the head or argsA59, so they could
     be swapped for D now. **713 could not.**
2. **Kill tables** (`s25/f/kill/kill6_U{7,8,9}.json`). Their forbidden set is RSST's 582 two-engine configurations
   (249 D2 + **333 C2cons**) plus the k3x registry.
   - **1,752 of 5,648 killed cells (31%) list only C witnesses.**
   - Those witnesses are 16 distinct configurations: 12 RSST C2cons (e.g. `rsst025_122o126`, `rsst031_122o368`) and 4
     registry f7 C (e.g. `f7_...5565_.......`, `f7_...5566_.....5.`).
   - Caveat: the witness lists look capped (lengths 1, 2 or 6), so some of these cells may also have an unlisted D
     witness.

**Binding.**
- The lower certificate (dual, 36 rows) is valid without C. Removing C kills adds rows to the primal, and a dual over a
  subset of rows stays valid. So the 2/13 lower bound does not depend on C.
- Unavoidability, though, comes from a FEASIBLE upper at t* ≤ 0. That upper does depend on which cases C kills.
- Whether st24b's upper survives without C is not decidable statically. That is **test T1**. Given 1,121 uncovered C
  patterns and the C-only kill cells, my prior is that it does **not** survive: removing C would re-open rows.

## (c) Recommendation

1. **Before 24 Oct: discharge CGlue for w66666 only, by the star reducer** (Studio, Lean).
   - The K ≤ 1 claim rests on all D entries plus w66666 (the five 66666-centred K = 1 keys). The gate text currently
     says "C-glue not formalized".
   - Work:
     - generalise `starMap` to an injective r-ring face (r = 10);
     - C1 for `runGood` at ring 10;
     - ring distinctness of the 10-ring from `Internally6` (the review argument: R_a = R_b gives a separating 4-cycle);
     - the C3 tail with P restricted to ≤ 3-colour codes.
   - Size and cost: about 400–700 lines, 1–2 Studio days.
   - Result: `four_color_of_unavoidable` for the K ≤ 1 registry with **no CGlue hypothesis**, i.e. `R.C = []` plus a
     proved `W66666Entry.colorable`. This is the only route with a gate payoff.
2. **K = 2: scope C as [E2], with CGlue explicit.** Wording: "C entries (852 at 7360eb92) are two-engine C (cfast and
   kc -C, same X) with the computational half Lean-checkable as in CWheels.lean. Soundness of C-reducibility in Lean is
   an explicit hypothesis (CGlue)." Do not start general CGlue until K = 2 has a FEASIBLE upper at t* ≤ 0, because the
   C set it needs is unknown until then.
3. **Shrink C cheaply in the meantime** (Opus/Studio, minutes to hours):
   - drop the 763 covered C patterns and the 139 covered registry C (no LP change by construction; check that dcount is
     unchanged);
   - pull or re-check the 3 two-ring-vertex X entries;
   - run D on larger windows for the 16 C-only kill witnesses.
4. **After K = 2 closes**, if C is still needed:
   - first the star test (T2) across the needed C set;
   - then general C4 by face refilling for single-interior-edge X (87% of the registry);
   - Coq `check_reducible` on a sample as a second engine.
   - Estimated 4–7 Studio days.

## Falsification tests

- **T1. LP dependence on C** (Opus or Studio, minutes; the upper check runs in seconds).
  - Re-run the st24b upper check with every C pattern source excluded, and the kill tables rebuilt with a D-only
    forbidden set.
  - Prediction: violators appear, so C is binding.
  - If it stays FEASIBLE at 2/13, C is not needed for this solve, and route (2) becomes "replace C by D" at zero cost.
  - Also run it with only the 1,121 uncovered C patterns kept. It must equal the full run, or my subsumption code is
    wrong.
- **T2. Star test** (Studio, one cfast flag; the D-closure is already computed).
  - For each C entry, report whether every ≤ 3-colour code is reached.
  - w66666 must pass (`three_colour_reached`). Franklin's 666666 must fail, as must the 66667 control, which is
    neither D nor C.
  - The pass fraction tells how much of the registry the cheap reducer covers.
- **T3. Lean sabotage for the w66666 glue.**
  - The proof must fail if `three_colour_reached` is replaced by the 66667 wheel's closure, or if the ring-distinctness
    hypothesis is dropped.
  - `#print axioms` must show only the standard axioms plus native_decide.
- **Kill line for recommendation 1.** If generalising `starMap` to r = 10 needs a Jordan-type fact that is not in the
  repo, or the gluing breaks by 23 Oct 18:00Z, keep "C-glue not formalized" in the gate text. K ≤ 1 then stays [E2] for
  the five 66666-centred keys.

Scratch scripts (not in the repo): `cscope2.py` (C/D subsumption, X shapes) and `kill.py` (kill-table witnesses) in this
session's scratchpad.
