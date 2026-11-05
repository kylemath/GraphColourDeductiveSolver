# job HCW13: Lean hC for the swarm's 3 critical-path C configurations (Studio, 5 Nov)

**Result:** all 3 are C on both of Studio's engines with the given X, and all 3 have Lean hC. Every module exits 0 with sorry 0;
sorryAx appears 0 times.

**EXTRAFILE:** extra_hcw13.tsv (aa9dbd9b), `name<TAB>kc fields<TAB>X`, as given in the relay.

## Two engines (eng/l0..2.out; kc 07e79fae, cfast de59e72f)
| config | ring | X | kc -C -x X | cfast --fixed X | kc window (own X) |
|---|---|---|---|---|---|
| b7_u5556677_.....5. | 13 | I0-I1 | adm=yes, leftover 0 | C-REDUCIBLE, leftover 0 | C, X = {I0-I1} |
| b7_u.557755_...5... | 12 | I0-I1 | adm=yes, leftover 0 | C-REDUCIBLE, leftover 0 | C, X = {I0-I1} |
| b7_u.5775.._.555... | 12 | I2-I3 | adm=yes, leftover 0 | C-REDUCIBLE, leftover 0 | C, X = {I2-I3} |

None is D. Every X is interior with |X| = 1, so none is rim-pinned.

## Lean (lean/; the CK108 pipeline; build ~/studio_lean_builds/rsst118_fb35d2d1/out_hcw13)
- **CHW13** (gen_ccover3 EXTRAFILE path): XRData for the 3. `w13Entries_ok` (XRData.ok), `w13_admissible_all` and
  `w13_foldSafe_all`, all by native_decide. **Exit 0, 12 s.**
- **HW13V00..02:** `HW13V.hC_i : cReducible18 … = true`, by native_decide. **All exit 0.** Wall time 271 s (ring 13) and 93 / 101 s
  (ring 12).
- **HW13All:** `hC_all (k : Fin 3)`. **Exit 0.**
- **Axioms:** propext, Classical.choice and Quot.sound, plus native_decide aux. The CHW13 `_ok` theorem needs only propext and
  Quot.sound, plus aux.

**Glue:** an occurrence-glue (COcc) module for these 3 is not part of this job. Opus can generate it from the same kc lines.
For the `rfl`, the Conf literal must be identical, name included.
