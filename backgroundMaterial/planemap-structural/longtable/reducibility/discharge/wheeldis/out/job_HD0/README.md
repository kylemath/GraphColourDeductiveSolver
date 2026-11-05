# job HD0: D-side Lean template (gen_hd.py) and hD calibration (Studio)

`gen_hd.py` (md5 b08d0f9dcdeb7bed6551a9f74cea908a) writes Lean D-reducibility modules from kc lines. It follows the same Conf path as
the C-side generator out/lean_ccover3/a6efb310/gen_ccover3.py, which is behind CR118, CK108 and CKQ5.

**Usage**
```
python3 gen_hd.py EXTRAFILE OUTDIR MOD PFX BATCH
```

**Input (EXTRAFILE)**
- One line per configuration: `name<TAB>r m ringadj intadj`. This is a kc line with its name split off by a TAB.
- `ringadj` / `intadj` are `;`-separated lists, one per interior vertex. Each entry is a `,`-separated list of ring positions
  (0..r−1) or interior vertices (0..m−1). An empty list is written `-`.
- These are the same fields as kc / dfast / cfast input lines.

**Output (in OUTDIR)**
- `MOD.lean`
  - imports DCheck18;
  - `def <PFX>Confs : List DCheck18.Conf`, with the same Conf literal as gen_ccover3's `cf` field: name, r, m, ringAdj, intAdj;
  - `theorem <PFX>Confs_length` (native_decide).
- `MODVkk.lean` (BATCH entries per module)
  - `theorem hD_i : DCheck18.dReducible (<PFX>Confs.get ⟨i, _⟩) = true := by native_decide`;
  - `#print axioms` for each theorem.
  - `hD_i` is exactly the `hD` field of ClaimGlue's `DEntry`. Its soundness is `ConfigOccW.colorable_of_dReducible18` via
    `DEntry.colorable`.
- `MODAll.lean`
  - `theorem hD_all (k : Fin n)`, proved by fin_cases over the hD_i;
  - `#print axioms`.

**Not generated:** the other DEntry side facts (`2 ≤ r`, `r ≤ 19`, `hsym`, `hloop`, each a cheap decide) and the occurrence
(ConfigOccW / OccursW). A kc→Occ generator would add the occurrence part.

**Build:** lean.run.sh / drive.sh compile against a dcheck build (build_r2 → … → DCheck18), with the mathlib oleans read-only and
no lake, as for rsst118. Calibration results are in calib.md once done.
