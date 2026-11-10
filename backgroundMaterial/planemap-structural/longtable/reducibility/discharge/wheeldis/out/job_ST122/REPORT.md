# ST-122 check: Opus's 189 can_leave rows and 2 check rows (Studio, 10 Nov 2026)

`check.py` (2ccd0529) ran with `nice -n 15 python3 -I` as one process, standard library only, in about 3 s. It reads files only.
- Outputs: `results.tsv` (4da1f97a), `check.log` (07f1e176).
- I re-ran it independently and got identical results.tsv and controls.
- Inputs match `in/MD5SUMS.st122` (7/7).
- RSST configs come from `loop/k44/rsst.txt`. All 191 verdicts agree with `loop/k44/rsst_verdicts.txt`.

## Result

| class | rows | CONFIRMED | FAILED | iso yes | yes-mirror | no | glue yes | glue no |
|---|---|---|---|---|---|---|---|---|
| C2cons | 168 | 168 | 0 | 107 | 61 | 0 | 0 | 168 |
| D2 | 21 | 21 | 0 | 14 | 7 | 0 | 21 | 0 |
| check (HA5) | 2 | 2 | 0 | 0 | 2 | 0 | 2 | 0 |

**CONFIRMED** means all three of:
1. the witness literal is in the Lean data module its theorem is about;
2. the RSST config is isomorphic to it, mirror allowed;
3. the hC / hD at that index is built: exit 0, sorry 0, error 0, with axioms only propext, Classical.choice, Quot.sound and
   native_decide aux.

Glue is reported but is not part of the verdict. No witness is for a configuration that isn't isomorphic.

**Families:**
- C: CXI 114, CXR 27, CCV 6, CC3V 3, CC2V 2, K108V 16.
- D: HDCV 21 (HDC502).
- check: A5CV 6 / 7 (HA5).

**Literal cross-checks:**
- 170 witnesses against `pats44_f.txt`, the 21 D against `D_todo.tsv`, the 2 check rows against HA5 `extraC.tsv`.
- All are identical except `f8_...55565_........`: its CXInt literal is the mirror of its pats44_f line.

**Isomorphism** was decided twice, independently: by a canonical form (ring rotations, then refinement of the interior, with
the mirror tried separately) and by a direct backtracking matcher. They never disagreed.

## Controls (all as expected)
- self-iso: 382/382
- relabel + rotation: 382/382
- relabel + rotation + reflection: 382/382
- one interior adjacency toggled, not iso: 191/191
- one ring incidence toggled, not iso: 191/191
- perturbed configs vs witness, not iso: 382/382
- chiral configs, both methods agree on yes-mirror: 176/176

## Surprises
1. 16 of the 168 C witnesses are CK108 (K108V.hC_45..85, built), not keep_lean_C (531) as the README says.
2. 70 rows need the mirror. All existing glue has `colorable_of_mirror_occ_*`; any new C glue must have it too.
3. `f8_...55565_........` has two mirrored literals under one name. Glue must use the CXInt.lean literal, the one the hC
   proves.
4. **No occurrence glue exists for any of the 168 C witnesses** (4,304 glue-type .lean files scanned).
   - The 21 D have OCC502 glue (built); the 2 check rows have HA5 glue (built).
   - On the RSST-seed route this glue comes from B6's generic `configOccW_of_rotOcc` (B6A_NOTES), not per entry. That generic
     lemma must cover the mirror branch.
5. The CXI, CXR and CCV All modules are evidenced by their logs only (no status.txt line); their per-entry .lean sources are
   not on disk.
6. HDC502's status.txt repeats lines for HDCV29-38; all are exit 0.

## Action taken
- All 191 are skipped in the ST-120 R queue: their lock dirs are pre-claimed in `job_ST120R/locks`. None had started.
- Nothing is deleted. The list is in `skipped_in_R.tsv`.
- Queue impact: 212 of the 403 remain to build: 177 hD (198 − 21) and 35 hC (205 − 170).
- The R queue's two All modules must be regenerated over the built subset at the end. That is noted for when QDONE comes.
