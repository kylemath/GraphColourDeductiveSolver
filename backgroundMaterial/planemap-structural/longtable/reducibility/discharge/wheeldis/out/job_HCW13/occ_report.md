# job HCW13: C-side occurrence glue (Opus, 0f2c0653), compiled on Studio (5 Nov 23:21Z)

**Result: every module exits 0 with sorry 0, including the hand-templated HW13Occ, which compiled on its first try.**
sorryAx appears 0 times.

**Byte identity:** all 7 .lean files are byte-identical to 0f2c0653, and match the expected md5s:
| files | md5s |
|---|---|
| HW3_00..02 | 463b92bc, cdf5d731, 8e49de2e |
| COccHW3_00..02 | eb2d9f5c, 1c33627b, ab86b158 |
| HW13Occ | 0941f20a |

No file was patched.

| module | exit | sorry | wall |
|---|---|---|---|
| HW3_00, 01, 02 | 0 | 0 | 6–7 s |
| COccHW3_00, 01, 02 | 0 | 0 | 4–5 s |
| **HW13Occ** (imports HW13All) | **0** | **0** | 4 s |

**Axioms** (`#print axioms` in HW13Occ and the COccHW3 modules): only propext, Classical.choice and Quot.sound, plus native_decide
auxiliaries:
- for `HW13Occ.cEntry`: HW13V.hC_0..2, w13Entries_length and w13Entries_ok;
- for `colorable_i`, also DCheck.Meet.check4_true / check5_true / size4 / size5 and DCheck.R1.check4..9 (CGlue's reducer).

**The rfl** (toCEntryF keeping cf := d.cf; List.all_eq_true / List.get_mem) elaborated as written.

**Build:** ~/studio_lean_builds/rsst118_fb35d2d1 (out_hcw13 + dc), sources in out/job_HCW13/lean/.
