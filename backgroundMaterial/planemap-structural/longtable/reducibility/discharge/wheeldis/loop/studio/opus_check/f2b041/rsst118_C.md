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
