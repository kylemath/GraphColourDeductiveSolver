# job HCW13R3P: Lean hC and occurrence glue for the 9 rim-pinned W13 round-3 C configurations (Studio, 6 Nov)

**Result:** 9 / 9 are C on kc and cfast with the given X, where |X| is 3 or 4 and X includes an R-I edge. All 9 have Lean hC plus occurrence glue, and all 30 modules exit 0 with sorry 0.

## Inputs
- extra_hcW13r3.tsv (29efa850), from claude/project-thread-phexa1 at 1ff3dbd3. Its 9 rows whose X has a comma form extra.tsv (6a279607). The other rows are byte-equal to HCW13R3's
  |X| = 1 file (a3151887). module_split.tsv is 935bd8c5. extra.tsv, module_split.tsv and CW3P.lean were pushed first at c06fc8da.
- **Is it a small step?** Yes. gen_ccover3 (3c9e7145) already handles multi-edge X with an R edge: union-find on X, then eqR for R-I edges and eqI for I-I edges. Earlier Lean C batches had
  the same shape: rsst118 (CR118) has 27 R-edge X entries and 28 multi-edge ones, and CK108 has 1. CW3P is the gen_ccover3 output with ccEntries renamed to w3pEntries, plus the
  admissible/foldSafe theorems as in CW3. Its structure matches CW3 except for the doc header.
- **Glue:** e1285b69, s76_occ502/hcw13r3p/lean/. All 20 files are copied byte-identically into in/glue/ (317f16a1), and the build copies also match on cmp. HWR3POcc md5 e4316ee9.

## Engines and hC (eng/verdicts.tsv; kc -t 600 -C -x X 07e79fae, cfast --fixed X de59e72f; Lean v4.35.0-rc3, out_hcw13r3p, nice 15)
| # | name | ring | X | kc | cfast | hC module | exit | sorry | wall |
|---|---|---|---|---|---|---|---|---|---|
| 0 | b7_u55.5657_5..6... | 12 | {I0-I6,I4-I8,R0-I0,R7-I4} | C | C | W3PV00 (W3PV.hC_0) | 0 | 0 | 76 s |
| 1 | b7_u557565._5..6... | 12 | {I0-I3,I5-I8,R0-I0,R10-I5} | C | C | W3PV01 (W3PV.hC_1) | 0 | 0 | 73 s |
| 2 | b7_u557565._5...7.. | 13 | {I0-I3,I5-I8,R0-I0,R7-I5} | C | C | W3PV02 (W3PV.hC_2) | 0 | 0 | 337 s |
| 3 | b7_u557565._5..7... | 13 | {I0-I3,I5-I8,R0-I0,R11-I5} | C | C | W3PV03 (W3PV.hC_3) | 0 | 0 | 344 s |
| 4 | b7_u55.5657_5..6..7 | 13 | {I0-I6,I4-I9,R0-I0,R8-I4} | C | C | W3PV04 (W3PV.hC_4) | 0 | 0 | 314 s |
| 5 | b7_u557565._5.76... | 13 | {I0-I3,I5-I9,R0-I0,R11-I5} | C | C | W3PV05 (W3PV.hC_5) | 0 | 0 | 302 s |
| 6 | b7_u557565._57.6... | 13 | {I0-I3,I5-I9,R0-I0,R11-I5} | C | C | W3PV06 (W3PV.hC_6) | 0 | 0 | 305 s |
| 7 | b7_u5575657_5..6... | 13 | {I0-I3,I0-I7,I5-I9,R4-I5} | C | C | W3PV07 (W3PV.hC_7) | 0 | 0 | 345 s |
| 8 | b7_u5..5777_...55.5 | 14 | {I0-I3,I0-I5,R0-I0} | C | C | W3PV08 (W3PV.hC_8) | 0 | 0 | 2,353 s |

| module | exit | sorry | wall |
|---|---|---|---|
| CW3P | 0 | 0 | 3 s |
| W3PVAll | 0 | 0 | 4 s |
| HWR3P_00..08 (9) | 0 | 0 | 7 s max |
| COccHWR3P_00..08 (9) | 0 | 0 | 5 s max |
| **HWR3POcc** (after W3PVAll) | **0** | **0** | 4 s |

**The form Opus assumed:** W3PVAll provides `W3PV.hC_all (k : Fin 9) : cReducible18 (w3pEntries.get (k.cast w3pEntries_length.symm)).cf … .eqR … .eqI = true`, the
same form as W3VAll. HWR3POcc, which uses `W3PV.hC_all k`, compiles against it with exit 0 and sorry 0.

**Axioms:**
- CW3P (ok, admissible, foldSafe): propext and Quot.sound, plus native_decide aux.
- W3PVAll: propext, Classical.choice and Quot.sound, plus native_decide aux.
- HWR3POcc (19 prints): the same three axioms, plus native_decide aux.
- sorryAx appears in 0 logs.

**Independence:** the C verdicts come from Studio kc and cfast, our engines. hC is the repo cReducible18 kernel via our gen_ccover3. Only the occurrence glue is Opus-generated, and I compiled
it unmodified. I read no Opus engine code and ran no Opus scripts for this job.
