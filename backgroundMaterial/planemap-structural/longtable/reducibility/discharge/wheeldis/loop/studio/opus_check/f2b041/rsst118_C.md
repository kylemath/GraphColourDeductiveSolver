# f2b041 (3): the 118 RSST C2cons of the keep95 cover re-proved C. Part 1: two-engine pass on Studio engines

Studio, 3 Nov.

**Result: 118 / 118 PASS, 0 FAIL.** Every entry is C on both engines with the same X, namely kc's own X: kc -C finds it in the
window, and cfast --fixed with that X gives C-REDUCIBLE with leftover 0. No entry is D.

## Method (rsst118/drive118.py, results118.tsv, kcX118.txt)
**Engines.** These are Studio's binaries, not rebuilt: kc loop/kc/kc (07e79fae) and cfast ../studio15/cfast (de59e72f). Both
carry their built-in ring-merge guard.

**Inputs.** The configurations are the RSST kc lines of loop/k44/rsst.txt (explore round 44). The names are the 118 rsst entries of
keep95/dropnames_cover.txt.

**Steps for each entry.**
1. **Window:** `kc -C -s 60 -t 600`, which yields kc's X. Then `cfast --fixed {kc X}`.
2. **Control:** `kc -t 600 -C -x {X}` and `cfast --fixed {X}`, using the round-44 X from loop/k44/rsst_x.txt.

## Counts
| check | pass |
|---|---|
| kc window C (kc X found) | 118 / 118 |
| cfast --fixed kc X, leftover 0 | 118 / 118 |
| **both engines, same X (kc X)** | **118 / 118** |
| cfast --fixed round-44 X, leftover 0 | 118 / 118 |
| kc -x round-44 X accepted (adm=yes, leftover 0) | 107 / 118 |
| kc D | 0 |

**The 11 entries where kc rejects the round-44 X (adm=no)** are rsst459, rsst551, rsst291, rsst509, rsst478, rsst446, rsst296,
rsst270, rsst265, rsst253 and rsst200. Every one of the 11 passes on both engines with kc's own
X.

## X notes
- **kc's X differs from the round-44 X in 47 of 118 entries.** Each one is listed with its two X's in results118.tsv (columns
  kc X / round-44 X). The Lean step will use kc's X, the two-engine X.
- **|X| ≥ 5: none.** kc's X has size 1 in 90 entries, 2 in 2, 3 in 13 and 4 in 13. The round-44 X's are also ≤ 4. The LT override
  (kcf, cfast --nogonthier, admissibleXU) is therefore not needed for size; admissibleXU still applies to the pinned ones.
- **Rim-pinned (X has an R vertex): 27 of 118 kc X's.** These 27 need the per-entry fold check foldSafeX (as for k63f / k63o) in
  the Lean step. The other 91 are interior-only.

## Next (part 2): Lean
- hC per entry by native_decide, through the CCover extra.tsv path:
  - format: name, TAB, kc line, TAB, X, using kc's X;
  - modules: out/lean_ccover*/gen_ccover.py and CXRing XRData, as for the 10 RSST entries in CCover;
  - then the assembly and #print axioms.
- foldSafeX for the 27 pinned entries.
- The earlier scratch Lean build directory was cleaned up, so the olean build against ~/mathlib4-planemap-build is being redone
  first.

## Note: what Lean needs for C that agreesRSST does not give
- **agreesRSST covers D only.** DCheckThms.agreesRSST(c) checks that Studio's D run on an RSST configuration reproduces RSST's
  header fields: the ext count, and D iff RSST's contract size is 0. It is proved per configuration by native_decide (rsst_r*_agree).
  - It says nothing about contraction. For an RSST C2cons entry it only records that the configuration is not D.
  - So no C reducibility follows from agreesRSST. Each C entry needs its own hC.
- **Per entry, Lean needs four things.** All four already exist in dcheck and were used for CXRing, CCover, CCover2, CCover3, K63F
  and K63O.
  1. **The contraction X as data, checked locally.** This is the `XRData` record (CXRing.lean): cf, eqR / eqI and lbl. `XRData.ok`
     bundles three checks, decided by native_decide:
     - `admissibleX`: X is a forest of edges between the listed vertices, the contraction stays loop-free, and the ring-merge
       guard holds (CGlue.lean:375);
     - `foldSafeX`: when X pins a group to rim vertices, no fold creates a loop (CGlue.lean:828);
     - the induced-adjacency side condition.

     Since |X| ≤ 4 here, `admissibleX` suffices. `admissibleXU` (CGlueU.lean, no |X| cap) is not needed.
  2. **The C reachability certificate.** `cReducible18 cf eqR eqI = true` (CGlue.lean:137, through DCheck18's run on the contracted
     colourings), one native_decide theorem per entry. This is the hC, and it is the expensive step.
  3. **Glue.** `cGlueXF` (CGlue) turns `XRData.ok` + hC into C-reducibility of an occurrence: the colouring extends after
     contracting X. No new glue is needed.
  4. **Assembly.** `hC_all` over the list (fin_cases), then `#print axioms`. The expected axioms are propext, Classical.choice and
     Quot.sound, plus the native_decide aux.
- **Reused here:**
  - the CXRing XRData type and the gen_ccover3.py generator (the EXTRAFILE path, as for CCover's 10 RSST entries);
  - CGlue's admissibleX / foldSafeX / cReducible18 / cGlueXF;
  - the CCover3 per-entry module layout.
  - CGlueU (admissibleXU) and CWheels are not needed: no |X| ≥ 5, and no wheels.
- **Files** (rsst118/lean/):
  - CR118.lean holds the 118 XRData entries with kc's X, and proves `r118Entries_ok` (admissibleX ∧ foldSafeX ∧ the side condition
    for all 118, including the 27 pinned), `r118_admissible_all`, `r118_foldSafe_all` and the length.
  - R118V00..19 hold hC_0..hC_117, six per module.
  - R118All proves `hC_all`.
- **Build:** the dcheck chain at main fb35d2d1 (build_r2 → … → CGlue → CXRing), rebuilt into ~/studio_lean_builds/rsst118_fb35d2d1.
  The mathlib oleans are read-only, there is no lake, and it runs at nice 15.

## Part 2: Lean (done, 4 Nov 02:16Z)
**Result: 118 / 118 hC proved in Lean.**

**Build.** The dcheck chain at main fb35d2d1 (build_r2, DCheckPinch, DCheckPinchGeom, DCheckOccWalk, ClaimGlue, C66666, CContract,
CGlue and CXRing) built with exit 0 into ~/studio_lean_builds/rsst118_fb35d2d1 (lean/build.log). The mathlib oleans were read-only,
there was no lake, and the build ran at nice 15.

**Modules** (lean/status.txt):
- **CR118:** exit 0, sorry 0, error 0. It proves:
  - `r118Entries_ok`, i.e. XRData.ok (admissibleX ∧ foldSafeX ∧ the side condition) for all 118 entries, including the 27
    rim-pinned ones;
  - `r118_admissible_all`;
  - `r118_foldSafe_all`;
  - `r118Entries_length`.
- **R118V00..R118V19:** all 20 modules exit 0 with sorry 0 and error 0. They prove hC_0..hC_117
  (`cReducible18 cf eqR eqI = true`, by native_decide). Wall time per module ran from 899 s to 14,278 s, at about 3.0 GB RSS each.
- **R118All:** exit 0. It proves `hC_all (k : Fin 118)` by fin_cases.

**Axioms** (`#print axioms`): R118V.hC_all depends on propext, Classical.choice and Quot.sound, plus the per-entry native_decide aux
(hC_k._native.native_decide.ax_1_1) and r118Entries_length's aux. The CR118 theorems have the same form. sorryAx appears 0 times
in all logs.

**With part 1, the 118 RSST C2cons of the keep95 cover are:**
- C on both Studio engines with kc's X (part 1, 2c275fc1);
- C-reducible in Lean: XRData.ok plus hC, which feed CGlue's cGlueXF exactly as for CXRing, CCover, CCover2 and CCover3.

**Still open on the keep95p131 C side:** the 13 k3x C entries of the 131, and the core95 entries that are not yet Lean-backed. Their
status is in Opus's list; they have not been checked here.
