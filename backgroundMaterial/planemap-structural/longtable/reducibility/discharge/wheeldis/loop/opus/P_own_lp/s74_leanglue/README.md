# s74_leanglue: kc line → Lean occurrence glue for the D side (Team C, 5 Nov 2026)

**For Studio.** This folder has:
- `gen_occ_kc.py`: a generator that turns a kc line into the per-key occurrence modules (`Occ`, `configOcc`, the
  COccBridge bridge) plus new registry glue.
- Regression tests that run without Lean.
- A ring-13 calibration batch of 10 D entries.

Nothing here was compiled. This container has no `lean`, `lake` or `elan`.

**Scope change (coordinator, 5 Nov).** `gen_dred18.py` was dropped. Studio's D template is `out/job_HD0/gen_hd.py` (origin/main
0604923f, md5 b08d0f9d), and this folder uses it as the reference for how D entries are stated (`<PFX>Confs`, `MODV.hD_i`).
Item (4) is now a list of names with kc lines (`calib13/`). The matching occurrence modules for those 10 names are also there.

## Main finding: the rotation was not the gap

`occ24/gen_occ_key.py` already reads the free-completion rotation from a kc line. Its `rotation(r, m, ra, ia)` takes the link
cycles of the configuration plus the ring cycle, and it never uses the wheel name. I checked it in two ways:
- **Validated:** `validate_rotation` finds a coherently oriented disc triangulation whose boundary is the ring cycle, read in one
  direction, with Euler characteristic 1.
- **Cross-checked:** `derive_rotation` is an independent derivation (Hamiltonian link cycles with face-consistency
  backtracking). It agrees with `rotation` on every kc line in the repository's reference sets: **24,941 lines** in the test
  suite, plus **23,721** `loop/k*` input lines with `check`.

The sets are:
- the 49 K=1 keys and 2,855 Studio-D keys;
- CK108 / CKQ5 / CR118;
- every CXRing / CCover / CCover2 / CCover3 / CR118 / CKQ5 Conf literal;
- RSST 633, nl51 8,200, and the XR `configs.in` (12,700).

In every one of these lines, every interior link is an induced cycle. So the rotation is forced, and the `Occ` the generator
states is the only rotation occurrence of that kc line.

What was actually missing:
1. the validation;
2. the step from the per-key `Occ` to the registry's own types (`ClaimGlue.OccursW` / `DEntry` and `CGlue.OccursCXR` /
   `OccursCXF` / `CEntryF`);
3. a batch path that ties gen_hd.py's `hD_i` to each occurrence.

`gen_occ_kc.py` adds all three. It calls occ24's generators unchanged, so their modules come out byte for byte. A fallback
derivation covers kc lines the old routine cannot handle (none were found in the repository; synthetic test T8).

Job 26 (2-ball appears → `Occ`) is still open, and none of this addresses it.

## Files

| file | what |
|---|---|
| `gen_occ_kc.py` | the generator (subcommands `one`, `batch`, `check`; also accepts gen_occ_key.py's own `KEYFILE LINENO NS OUTDIR`) |
| `tests/run_regression.py` | regression suite T1–T8, no Lean (about 3.5 min; `--big` adds the loop/k* lines) |
| `tests/regression_log.txt` | the passing run (origin/main 0604923f) |
| `vendor/` | byte copies of gen_occ_key.py, gen_occ_walk.py, gen_rotbridge.py, gen_hd.py, gen_ccover3.py from origin/main (md5 and blob ids in `vendor/SOURCES.txt`) |
| `calib13/calib13_D_r13.tsv` | **item (4)**: 10 ring-13 D names of `s73_prune/run/cover_final870.tsv`, each with its kc line, verdict file:line and verdict text |
| `calib13/calib13_extra.tsv` | the same 10 as a gen_hd.py / gen_occ_kc.py EXTRAFILE (`name<TAB>r m ringadj intadj`) |
| `calib13/lean/` | generated: `H13_00..09.lean` (Occ, face-walk form), `COccH13_00..09.lean` (bridge + registry glue), `HD13Occ.lean` (ties `HD13V.hD_i` to each), `H13_modules.txt` |

**Import order.** gen_occ_kc.py imports occ24's generators from the first of these that exists:
1. `$OCC24`;
2. `../../../../../../dcheck/occ24`, the repository copy (on origin/main it is identical to `vendor/`);
3. `vendor/`.

The line it prints at start-up names the folder it used.

## The calibration list (item 4)

The list has all 4 rsstD ring-13 entries in the cover, and 6 nl51 entries: the first two by name at m = 10, 11 and 12. The kc
lines are the XR `configs.in` lines, the ones the verdicts were computed on. Each has a `D=true` line in
`out/ext_reruns_a1d1317/p3_s*.tsv` (cfast cfD). The nl lines are identical to `nl51_kc.txt`. The RSST lines list the same
adjacency as DCheckData, sorted.

| # | cover name | kc / Conf name | m | verdict |
|---|---|---|---|---|
| 0 | rsst105 | rsst105_482o611 | 9 | p3_s1.tsv:391 |
| 1 | rsst219 | rsst219_2o226173962 | 9 | p3_s0.tsv:395 |
| 2 | rsst275 | rsst275_1322o1028 | 9 | p3_s11.tsv:396 |
| 3 | rsst383 | rsst383_7322o611 | 9 | p3_s9.tsv:397 |
| 4 | nl0245_r13 | nl0245_r13 | 10 | p3_s11.tsv:224 |
| 5 | nl0417_r13 | nl0417_r13 | 10 | p3_s11.tsv:226 |
| 6 | nl0250_r13 | nl0250_r13 | 11 | p3_s2.tsv:225 |
| 7 | nl0567_r13 | nl0567_r13 | 11 | p3_s0.tsv:235 |
| 8 | nl2179_r13 | nl2179_r13 | 12 | p3_s1.tsv:271 |
| 9 | nl2180_r13 | nl2180_r13 | 12 | p3_s2.tsv:271 |

## What to compile

Use the same LEAN_PATH as rsst118 / `out/lean_ccover3/a6efb310/run.sh`: the dcheck build, which provides COccBridge, CGlue,
ClaimGlue, DCheckOccWalk, DCheckR2D, DCheckTEq and DCheckMirror. Compile in this order:

1. **gen_hd (yours).**
   ```
   python3 out/job_HD0/gen_hd.py <s74>/calib13/calib13_extra.tsv OUT HD13 hd13 5
   ```
   This writes `HD13.lean`, `HD13V00.lean`, `HD13V01.lean` and `HD13All.lean`. `HD13Occ.lean` expects exactly `HD13` / `hd13`.
2. **`calib13/lean/H13_kk.lean`** (k = 00..09). Each imports Mathlib PlaneMap OccToRing / MinimalFrame, DCheckR2D, DCheckTEq,
   DCheckMirror and DCheckOccWalk, like occ24's D-walk modules. Theorems in `SimpleGraph.SphericalMap.H13_kk`:
   - `ring_dinj_of`, `configOcc` (`Occ` → `ConfigOccW` + smaller support);
   - `intAdjOf_eq`, `ringAdjOf_eq`, `cf_sym`, `cf_loop`;
   - `colorable_of_occ_dred`, `colorable_of_mirror_occ_dred`.

   For comparison, the 49 D-walk modules (`D00..D48`, rings 17–19, m 17–19) took 9–12 s each, all clean (`occ24/walkD_results.txt`). The
   ring-13 keys are smaller.
3. **`calib13/lean/COccH13_kk.lean`**. These import COccBridge and `H13_kk`. The first part is gen_rotbridge's text, which is
   already proved for K41 (COccK41):
   - `rot`;
   - `rot_ok` (native_decide);
   - `rotOcc_of_occ`;
   - `local_facts_of_occ`.

   **New, not yet compiled:** the registry glue.
   - `occursW_of_occ : Occ T ring int → ClaimGlue.OccursW cf T`
   - `dEntryOf (hD : DCheck18.dReducible c = true) (hc : c = cf) : ClaimGlue.DEntry`
   - `colorable_of_occ_entry hD hc htri h IH`, `colorable_of_mirror_occ_entry`
   - `occursCXR_of_occ (e : CGlue.CEntry) (he : e.cf = cf) : … → CGlue.OccursCXR e T`, and `occursCXF_of_occ`
   - `colorable_of_occ_centry (e : CGlue.CEntryF) (he : e.cf = cf) …`, `colorable_of_mirror_occ_centry`
4. **`calib13/lean/HD13Occ.lean`** (new, not yet compiled). It imports `HD13All` and the ten `COccH13_kk`, and defines:
   - `HD13Occ.dEntry_i : ClaimGlue.DEntry := H13_kk.dEntryOf HD13V.hD_i rfl`
   - `HD13Occ.colorable_i` (an `Occ` in a triangulation whose smaller maps are colourable ⇒ colourable)
   - `HD13Occ.dEntries`

   The `rfl` is `HD13.hd13Confs.get ⟨i, _⟩ = H13_kk.cf`. Test T6 checks that the two literals agree field by field: name, r, m,
   ringAdj, intAdj.

**Expected axioms:** propext, Classical.choice, Quot.sound and native_decide auxiliaries only (`rot_ok`, `hD_i`,
`hd13Confs_length`, and those DCheckOccWalk already carries). No `sorry`.

**If the new glue fails to elaborate, these are the likely spots and the fixes:**
- **`occursCXR_of_occ`** tries three tactic routes inside `first`: `unfold; rw [he]`, then `cases e; dsimp only at he;
  subst he`, then `cases e; subst he`. So one failing route does not break the file.
- **`colorable_of_occ_entry`** casts with `show ClaimGlue.OccursW c T by rw [hc]; exact …`. If that fails, use `hc ▸
  occursW_of_occ htri h`.
- **`dEntryOf`** closes the side facts with `by subst hc; decide` / `exact cf_sym`.

Each of these is a few lines of `registry_text()` in gen_occ_kc.py. They mirror patterns that already compile: ClaimGlue's
`occursW_of_configOcc`, COccBridge's `occursCXF_of_rot`, and gen_occ_key's `colorable_of_occ_dred` and mirror theorem.

**After this batch compiles,** one call does the whole cover. Run gen_hd.py and gen_occ_kc.py on the same EXTRAFILE with the
same MOD / PFX:
```
python3 gen_occ_kc.py batch EXTRAFILE OUTDIR <PREFIX> --hd MOD PFX
```

## How to run the generator

```
python3 gen_occ_kc.py one 'nl0245_r13 13 10 …' NS OUTDIR            # literal kc line
python3 gen_occ_kc.py one calib13/calib13_extra.tsv:4 NS OUTDIR      # N-th non-blank line (0-based)
python3 gen_occ_kc.py one FILE@nl0245_r13 NS OUTDIR                  # by name
python3 gen_occ_kc.py KEYFILE LINENO NS OUTDIR                        # gen_occ_key.py's argument order (ring form)
python3 gen_occ_kc.py batch EXTRAFILE OUTDIR PREFIX [--hd MOD PFX] [--first N --count K]
python3 gen_occ_kc.py check FILE...                                   # validate the rotation of every kc line, write nothing
```

**Options:**
- `--form walk` (default): the face-walk `Occ` of gen_occ_walk.py. The ring may repeat vertices, `ring_dinj` is derived, and the
  result is `ConfigOccW`.
- `--form ring`: gen_occ_key.py's `Occ` with `ring_inj`.
- `--walk-assume`: keeps `ring_dinj` as an `Occ` field (= `WALK_ASSUME=1`).
- `--no-bridge`: writes only `<NS>.lean`.
- `--no-registry`: writes the bridge exactly as gen_rotbridge.py would.

**Before writing any Lean,** the generator checks:
- the kc line: symmetric, loop-free, positions in range, every ring position touched, interior connected, ring 2..19;
- the rotation: validated, and agreeing with the independent derivation;
- in Python, every Bool goal the modules close by `decide` / `native_decide`: `rotOK` on the bridge rotation, `cf_sym`,
  `cf_loop`, the degree field.

It refuses a key that fails any of these, with the reason.

**Not supported (refused or asserted):**
- ring positions with no interior neighbour;
- a ring chord as a fan apex (gen_occ / dinj_proof assert);
- names containing whitespace, `"` or `\`. Comment delimiters in a name are escaped in doc comments only.

## Regression results (`python3 tests/run_regression.py`, all PASS; log in `tests/regression_log.txt`)

- **T1:** the 49 K=1 keys, `--form ring`, against committed `dcheck/occ24/K00..K48.lean`: **49/49 byte-identical**. This holds
  for the `one` order and for gen_occ_key's own argument order.
- **T2:** the bridge without registry. Against committed **`dcheck/COccK41.lean`: byte-identical.** Against the vendored
  `gen_rotbridge.py` run as a program on each regenerated Kxx: 49/49 identical.
- **T3:** e66666F. The kc line of `CGlue.cf66666` gives a rotation literal **identical to COccBridge's `rot66666`**.
  - **Documented, neutral difference:** `rot66666` is gen_occ_key.rotation's raw orientation. A bridge generated from `Occ`
    reads the rotation off `Occ`'s Nx fields, the orientation gen_key settles on, which is the global reversal.
  - Both are legitimate `RotOcc` hypotheses. In `OccursCXR` the deleted map `G` is not tied to `T`'s rotation, and the other
    orientation is the occurrence in `T.mirror`, which the `*_mirror_*` theorems cover.
  - A generated C bridge therefore uses one convention throughout: Occ's.
- **T4:** the walk form against the vendored gen_occ_walk.py, for the 49 keys, with derived dinj and with `WALK_ASSUME=1`:
  **98/98 byte-identical**. The D00..D48 modules compiled clean on the Studio (walkD_results.txt) but are not committed, so the
  program is the reference.
- **T5a:** the rotation on 24,941 kc lines (the sets above). The old routine's result is valid. The independent derivation is
  valid and equal to it up to global reversal. 0 interior links are non-induced, and 0 have several Hamiltonian cycles.
  - `check` on the 23,721 loop/k* lines: 0 failures.
- **T5b:** the fallback alone (old routine disabled), on the 49 keys. The output differs from the committed modules only in
  where each per-vertex rotation list starts: once the starts are aligned, **49/49 are byte-identical**. So the fallback is
  semantically neutral: same cyclic Nx facts, same statements.
- **T6 (shared Conf path):** for 259 registry entries (CKQ5, CR118, CCover3, and gen_hd.py run on the CKQ5 + CR118 kc lines),
  the generated `def cf` has the same name, r, m, ringAdj and intAdj as the registry literal. So `registry_cf = <NS>.cf` is
  `rfl`. Also, **gen_ccover3.py's EXTRAFILE branch regenerates the committed CKQ5.lean and CR118.lean entry blocks byte for
  byte**, so the C Conf path has not regressed.
  - CK108 has no committed Lean module. Its kc lines (ck108/names.txt) are in T5a.
- **T7:** 110 COcc modules: 49 keys, the 5 CKQ5 entries and 66666, each in walk and ring form. Each has the eight registry
  declarations with `#print axioms`, balanced brackets, and passing Python prechecks.
- **T8:** synthetic fallback and refusal.
  - `syn1`: a degree-3 vertex inside the triangle (I0, R0, R1). The link of I0 is not an induced cycle, so the old routine
    raises; the derivation takes over and the modules are generated.
  - `syn2`: a ring position with no interior neighbour. It is refused before any Lean is written.

## Using the registry glue elsewhere

- **D (gen_hd):** `NS.colorable_of_occ_entry MODV.hD_i rfl htri h IH`, or the entry `NS.dEntryOf MODV.hD_i rfl`.
  `HD13Occ.lean` is the generated form.
- **C (gen_ccover3 / CXRing):** `NS.colorable_of_occ_centry (CC3V.ccF k) rfl htri h IH`. Any `CEntryF` whose `cf` is this kc
  line's literal works, for example `(xrEntries.get _).toCEntryF hok hC`. `NS.occursCXF_of_occ e rfl htri h` gives the
  `OccursCXF` that `CEntryF.colorable` consumes. For a C entry, run gen_occ_kc.py on the same kc line the XRData was built
  from: the `rfl` needs the identical literal, name included.
