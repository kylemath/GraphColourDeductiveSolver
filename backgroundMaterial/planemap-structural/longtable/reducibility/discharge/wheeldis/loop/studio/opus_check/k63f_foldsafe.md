# k63f: foldSafeX audit of the 111 rim-pinned C entries of main aa74d7ec (Studio, 21 Oct)

**Result: all 111 PASS foldSafeX (CGlue.lean:828), proved in Lean by native_decide. There are 0 FAILs.**
- **Also proved:** all 111 pass admissibleX and the full XRData.ok (admissibleX ∧ foldSafeX ∧ 2 ≤ r ≤ 19 ∧ a symmetric, loop-free
  interior ∧ ring indices < r).
- **So:** no FAIL is among the 154 A83 cover entries or the 143 A78 cover entries.

## Inputs
- **The list:** explore's loop/k63/pinnedX_main_aa74d7ec.txt (claude/project-thread-nh6pv2 at 98d22da8, md5 89197dcc): 111 names with
  r, m and X.
- **X:** the k3x_C.cfast X at main aa74d7ec (kc's X, as recorded in the registry). For all 111 it is identical in the list, at aa74d7ec
  and at Studio's HEAD.
- **Configuration data:** the twoeng / gen_cxring source rule (the first loop/k*/ cfast block with an accepted C line, plus its sibling
  .txt). It takes the occurrence data from 23 source files in loop/k43, loop/k44 and loop/k47 (A_cf.out, the r* / s52r1
  _kills_cf.cfast and their .txt). All are byte-identical at aa74d7ec.
- **Labels:** one per X-component, as for CXRing.

## Method (out/lean_k63f/aa74d7ec/)
- **Generator:** gen_ccover3.py (the CCover2 / CCover3 generator, which is gen_cxring's rule) with ONLY = the 111 names. It writes
  K63F.lean with `k63Entries : List XRData`.
- **The theorems, proved in the 2a4bc4cf Lean build (dcheck sources unchanged):**
  - `k63_foldSafe_all : k63Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true` by native_decide;
  - `k63_admissible_all` (admissibleX), likewise;
  - `k63_ok_all : k63Entries.all XRData.ok = true`;
  - `k63Entries_length = 111`.
- **The build:** lean exit 0, sorry 0, error 0.
- **#print axioms** of k63_foldSafe_all and k63_ok_all: [propext, Quot.sound, the theorem's own native_decide aux].
- **#eval:** `k63Fails` (the entries failing any of the three) = [] and the foldSafeX count = 111 / 111.
- **Every FAIL confirmed in Lean:** none to confirm. Every PASS is covered by the proved `all` theorems; no Python mirror was needed.

## Overlap with Studio's existing Lean batches
- **CXRing (2a4bc4cf):** 91. **CCover (1c56a79e):** 1. **CCover3 (a6efb310):** 1.
- **Not yet in Lean:** 18. These pass here too, so they are fold-safe under CGlue's definition. Their hC (the C verdict) is not proved
  in this audit.
- **The "89 ring-X entries already passing in CXRing / CCover":** in Studio's batches, 91 of the 111 are in CXRing (its xrEntries_ok
  already includes foldSafeX) and 1 is in CCover.

## Per name
| name | ring | X (kc) | source | foldSafeX | Studio Lean batch | in A83 cover (154) | in A78 cover (143) |
|---|---|---|---|---|---|---|---|
| f10_...5565655_........5. | 13 | I0-I3,I1-I2,R0-I1,R8-I3 | explore:r56d | PASS | — |  |  |
| f10_...5565655_........56 | 14 | I0-I3,I1-I2,R0-I1,R8-I3 | explore:r56d | PASS | — |  |  |
| f10_...5565655_......6.5. | 14 | I0-I3,I3-I9,R11-I3 | explore:r56d | PASS | — |  |  |
| f10_...5565655_.....6..5. | 14 | I0-I3,I1-I2,R0-I1,R9-I3 | explore:r56d | PASS | — |  |  |
| f10_...5565655_....6...5. | 14 | I0-I3,I1-I2,R0-I1,R9-I3 | explore:r56d | PASS | — |  |  |
| f10_...5566655_...5...65. | 14 | I0-I3,I1-I2,R0-I1,R9-I3 | explore:r58k | PASS | — |  |  |
| f10_..55656556_.......5.. | 14 | I0-I1,I2-I3,I3-I4,R7-I1 | explore:r56d | PASS | — |  |  |
| f10_..55656556_..5....... | 14 | I0-I3,I1-I2,R0-I1,R9-I3 | explore:r56d | PASS | — |  |  |
| f10_..55656655_.......... | 14 | I0-I5,I0-I7,R4-I7 | explore:r10a | PASS | CXRing |  |  |
| f10_.5.5565655_........5. | 14 | I0-I3,I1-I2,R0-I1,R9-I3 | explore:r56d | PASS | — |  |  |
| f10_.5565.5565_.......... | 14 | I0-I2,I5-I6,R0-I0,R7-I5 | explore:r56d | PASS | — |  |  |
| f10_.5565.5565_......5... | 14 | I0-I2,I5-I6,R0-I0,R7-I5 | explore:r56d | PASS | — |  |  |
| f7_...5576_...5.5. | 11 | I0-I2,I3-I4,R2-I0,R8-I3 | explore:- | PASS | CXRing | yes | yes |
| f7_...5585_....55. | 11 | I0-I2,R6-I2 | explore:- | PASS | CXRing |  |  |
| f7_...5675_.....55 | 11 | I0-I3,I1-I4,R0-I1,R6-I3 | explore:- | PASS | CXRing | yes | yes |
| f7_...5675_.....65 | 12 | I0-I3,I1-I4,R0-I1,R6-I3 | explore:- | PASS | CXRing | yes | yes |
| f7_...5675_....58. | 14 | I0-I3,I4-I6,R2-I0,R0-I4 | explore:r7a | PASS | CXRing |  |  |
| f7_...5675_....585 | 14 | I0-I3,I4-I7,R2-I0,R0-I4 | explore:r7a | PASS | CXRing |  |  |
| f7_...5676_..55.5. | 12 | I0-I1,I3-I4,R0-I0,R2-I3 | explore:- | PASS | CXRing |  |  |
| f7_...5676_..56.5. | 13 | I0-I1,I2-I3,R2-I0,R8-I2 | explore:r57f | PASS | — |  |  |
| f7_...5676_..5665. | 14 | I0-I1,I2-I3,I2-I6,R2-I0 | explore:r57f | PASS | — |  |  |
| f7_...5775_...5.55 | 12 | I0-I2,I3-I6,R7-I2,R0-I3 | explore:- | PASS | CXRing | yes | yes |
| f7_...5775_...5.65 | 13 | I0-I3,I2-I7,R2-I2,R8-I3 | explore:- | PASS | CXRing | yes | yes |
| f7_...5856_...556. | 12 | I0-I2,R6-I2 | explore:- | PASS | CXRing |  |  |
| f7_...6576_...5.5. | 12 | I0-I2,I3-I4,R2-I0,R8-I3 | explore:- | PASS | CXRing | yes | yes |
| f7_...6676_...555. | 13 | I0-I2,R0-I0 | explore:- | PASS | CXRing | yes | yes |
| f7_..55785_....55. | 13 | I1-I2,R10-I2 | explore:- | PASS | CXRing |  |  |
| f7_..56576_.....5. | 12 | I0-I1,I4-I5,R7-I1,R1-I4 | explore:- | PASS | CXRing | yes | yes |
| f7_..56666_.....5. | 12 | I0-I3,R8-I4 | explore:- | PASS | CXRing | yes | yes |
| f7_..56676_..5..5. | 13 | I0-I2,I0-I5,I3-I4,R0-I0 | explore:- | PASS | CXRing | yes | yes |
| f7_..56758_...5... | 14 | I0-I4,I1-I5,R1-I0,R8-I5 | explore:r7a | PASS | CXRing |  |  |
| f7_..56758_...5.5. | 14 | I0-I4,I1-I5,R1-I0,R8-I5 | explore:r7a | PASS | CXRing |  | yes |
| f7_..56766_...655. | 14 | I0-I3,I3-I6,R0-I0 | explore:r57a | PASS | — |  |  |
| f7_..56766_.56.5.. | 14 | I0-I1,I0-I4,R0-I0 | explore:r57f | PASS | — |  |  |
| f7_..57576_..5..5. | 13 | I0-I1,I4-I5,R1-I4 | explore:- | PASS | CXRing |  |  |
| f7_..57576_.56..5. | 14 | I0-I1,I2-I3,R10-I2 | explore:- | PASS | CXRing |  |  |
| f7_..57675_..5..5. | 13 | I0-I3,R4-I3 | explore:- | PASS | CXRing |  |  |
| f7_..58576_..55.5. | 14 | I0-I2,I2-I7,R5-I2 | explore:- | PASS | CXRing |  |  |
| f7_.556776_.5.5.5. | 14 | I0-I2,I0-I6,R0-I0 | explore:r7b2 | PASS | CXRing |  |  |
| f7_5676676_5..5..5 | 14 | I1-I7,I5-I6,R11-I6,R13-I7 | explore:r58j | PASS | CCover3 | yes |  |
| f8_...55576_......5. | 12 | I0-I3,I1-I2,R0-I0,R2-I1 | explore:- | PASS | CXRing | yes | yes |
| f8_...55585_.....55. | 12 | I0-I2,R8-I2 | explore:- | PASS | CXRing |  |  |
| f8_...55655_........ | 10 | I0-I2,R1-I0 | explore:- | PASS | CXRing | yes | yes |
| f8_...55665_...5.... | 11 | I0-I1,I4-I5,R7-I1,R2-I4 | explore:- | PASS | CXRing | yes | yes |
| f8_...55675_...5..5. | 12 | I0-I1,I4-I5,R7-I1,R2-I4 | explore:- | PASS | CXRing |  |  |
| f8_...55685_...5655. | 13 | I0-I1,R6-I1 | explore:s52r1 | PASS | CXRing |  |  |
| f8_...55685_...56556 | 14 | I0-I1,R7-I1 | explore:s52r1 | PASS | CXRing |  |  |
| f8_...55755_.....5.. | 11 | I0-I2,R1-I0 | explore:- | PASS | CXRing | yes | yes |
| f8_...55755_.....66. | 12 | I0-I2,R1-I0 | explore:- | PASS | CXRing |  |  |
| f8_...56576_....5.5. | 13 | I0-I3,I1-I2,R0-I0,R2-I1 | explore:- | PASS | CXRing | yes | yes |
| f8_...56585_....655. | 13 | I0-I1,R6-I1 | explore:r54d | PASS | CXRing |  |  |
| f8_...56585_....6556 | 14 | I0-I1,R7-I1 | explore:r54d | PASS | CXRing |  |  |
| f8_...56585_....665. | 14 | I0-I4,R9-I4 | explore:r56c | PASS | CCover | yes | yes |
| f8_...56585_...6655. | 14 | I0-I1,R6-I1 | explore:r54d | PASS | CXRing |  |  |
| f8_...56656_......5. | 12 | I0-I1,I4-I5,R8-I1,R2-I4 | explore:- | PASS | CXRing | yes | yes |
| f8_...56665_......55 | 12 | I0-I2,I4-I5,R5-I2,R7-I4 | explore:r8b | PASS | CXRing |  |  |
| f8_...56665_.....65. | 13 | I0-I3,I3-I6,R5-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_...56665_.....655 | 13 | I0-I3,I3-I6,R5-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_...56665_....6.5. | 13 | I0-I3,I3-I6,R8-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_...56665_....6.55 | 13 | I0-I3,I3-I6,R8-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_...56665_...5.65. | 13 | I0-I3,I3-I7,R5-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_...57656_...5..5. | 13 | I0-I1,I4-I5,R8-I1,R6-I5 | explore:- | PASS | CXRing |  |  |
| f8_...65576_...66.5. | 14 | I0-I2,I1-I5,R0-I0,R2-I5 | explore:r56b | PASS | — |  |  |
| f8_...65676_...56.5. | 14 | I0-I5,I1-I2,R2-I0,R0-I2 | explore:r54c | PASS | CXRing |  | yes |
| f8_...65856_...6556. | 14 | I0-I1,R8-I1 | explore:r54d | PASS | CXRing |  |  |
| f8_..556856_..5655.. | 14 | I0-I1,R7-I1 | explore:s52r1 | PASS | CXRing |  | yes |
| f8_..556856_..5655.6 | 16 | I0-I1,R9-I1 | explore:s52r1 | PASS | CXRing |  |  |
| f8_..565856_...655.. | 14 | I0-I1,R7-I1 | explore:r54d | PASS | CXRing |  |  |
| f8_..566656_..5.6... | 14 | I0-I3,I3-I8,R5-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_..566656_..56.... | 14 | I0-I3,I3-I8,R8-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_..566656_.55..... | 13 | I0-I3,I1-I2,R1-I1,R7-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_..566656_.55.6... | 14 | I0-I3,I3-I9,R5-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_..566656_.556.... | 14 | I0-I3,I3-I9,R8-I3 | explore:r8b | PASS | CXRing |  |  |
| f8_..585656_..556... | 14 | I0-I1,R5-I1 | explore:r54d | PASS | CXRing | yes |  |
| f8_.5558565_......6. | 14 | I0-I1,I6-I8,R0-I0,R9-I6 | explore:- | PASS | CXRing |  |  |
| f8_.5558565_..5...6. | 14 | I0-I1,I6-I9,R0-I0,R9-I6 | explore:- | PASS | CXRing |  |  |
| f8_.5558565_..56..6. | 14 | I0-I1,I6-I10,R0-I0,R9-I6 | explore:- | PASS | CXRing |  |  |
| f8_.5566765_.....5.. | 14 | I0-I1,I0-I3,R0-I0 | explore:- | PASS | CXRing |  | yes |
| f8_.5566766_.....55. | 15 | I0-I7,I1-I8,R0-I0 | explore:r61c | PASS | — |  |  |
| f8_.656.656_.55..66. | 14 | I0-I1,I0-I3,I1-I7,R9-I8 | explore:r58e | PASS | — |  |  |
| f9_...555665_.....6... | 13 | I0-I4,I4-I7,R6-I4 | explore:r9e | PASS | CXRing |  |  |
| f9_...555665_.....6.6. | 14 | I0-I4,I4-I7,R7-I4 | explore:r9e | PASS | CXRing |  |  |
| f9_...555665_....57... | 13 | I0-I1,I1-I7,R6-I1 | explore:r9e | PASS | CXRing |  |  |
| f9_...555665_....57.6. | 14 | I0-I1,I1-I7,R7-I1 | explore:r9e | PASS | CXRing |  |  |
| f9_...555665_...5.6... | 13 | I0-I4,I4-I8,R6-I4 | explore:r9e | PASS | CXRing |  |  |
| f9_...555665_...5.6.6. | 14 | I0-I4,I4-I8,R7-I4 | explore:r9e | PASS | CXRing |  |  |
| f9_...555665_...757... | 14 | I0-I1,I1-I7,R6-I1 | explore:r9e | PASS | CXRing |  |  |
| f9_...555665_..5.57... | 14 | I0-I6,I6-I9,R10-I6 | explore:r9g | PASS | CXRing |  |  |
| f9_...555675_.....6.5. | 14 | I0-I2,I2-I8,R7-I2 | explore:r9f | PASS | CXRing |  |  |
| f9_...556655_...5...5. | 12 | I0-I1,I2-I3,R7-I1,R9-I2 | explore:r9e | PASS | CXRing |  |  |
| f9_...556655_...5...56 | 13 | I0-I1,I2-I3,R8-I1,R10-I2 | explore:r9e | PASS | CXRing |  |  |
| f9_...556655_...5..75. | 13 | I0-I1,I1-I7,R7-I1 | explore:r9e | PASS | CXRing |  |  |
| f9_...556655_...57..56 | 14 | I0-I1,I1-I7,R8-I1 | explore:r9e | PASS | CXRing |  |  |
| f9_...565665_.....6.5. | 14 | I0-I3,I3-I7,R10-I3 | explore:r9d | PASS | CXRing |  |  |
| f9_...565665_...5.6... | 14 | I0-I3,I3-I8,R10-I3 | explore:r9d | PASS | CXRing |  |  |
| f9_...565665_...5.6.5. | 14 | I0-I3,I3-I8,R10-I3 | explore:r9d | PASS | CXRing |  |  |
| f9_...565665_..55.6... | 14 | I0-I3,I3-I8,R10-I3 | explore:r9d | PASS | CXRing |  |  |
| f9_...656566_...5...5. | 14 | I0-I3,I1-I2,R1-I1,R7-I3 | explore:r9b | PASS | CXRing |  |  |
| f9_...656656_...5...5. | 14 | I0-I5,I1-I2,R10-I1,R8-I5 | explore:- | PASS | CXRing | yes | yes |
| f9_..5556756_.....5... | 14 | I0-I1,I6-I7,R0-I0,R5-I7 | explore:r9f | PASS | CXRing |  |  |
| f9_..5565675_......5.. | 14 | I0-I1,I0-I5,I1-I8,R4-I5 | explore:- | PASS | CXRing | yes | yes |
| f9_..5566556_..5...5.. | 13 | I0-I1,I2-I3,R8-I1,R10-I2 | explore:r9e | PASS | CXRing |  |  |
| f9_..5566556_..5...5.5 | 14 | I0-I1,I2-I3,R9-I1,R11-I2 | explore:r9e | PASS | CXRing |  |  |
| f9_..5566556_..57..5.. | 14 | I0-I1,I1-I8,R8-I1 | explore:r9e | PASS | CXRing |  |  |
| f9_..5656565_......... | 13 | I0-I2,I0-I4,R6-I2 | explore:r9b | PASS | CXRing | yes |  |
| f9_..5656565_.......6. | 14 | I0-I2,I0-I4,R7-I2 | explore:r9b | PASS | CXRing |  | yes |
| f9_..5656565_......6.. | 14 | I0-I2,I0-I4,R7-I2 | explore:r9b | PASS | CXRing |  |  |
| f9_..5665556_....6.... | 14 | I0-I5,I5-I8,R10-I5 | explore:r9e | PASS | CXRing | yes |  |
| f9_..5665556_....6.5.. | 14 | I0-I5,I5-I9,R10-I5 | explore:r9e | PASS | CXRing |  |  |
| f9_..5665556_....75... | 14 | I0-I1,I1-I8,R5-I1 | explore:r9e | PASS | CXRing |  |  |
| f9_.56565656_......... | 14 | I0-I2,I0-I4,R7-I2 | explore:r9b | PASS | CXRing |  |  |
