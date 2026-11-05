# job OCC502: Opus's occurrence glue for the 380 D of the 502 cover, compiled on Studio (interim, 5 Nov 10:50Z)

## Source
- **Branches:** claude/project-thread-7uelj0 at 9ca16f45 (hdc/, ctrl3/, hd30/) and d9c28330 (adds hdr5/), folder s76_occ502/.
  Copied read-only into in/; README.md was read first.
- **No Python of theirs was run, and no file was edited.** All **820 compiled .lean files are byte-identical to d9c28330**
  (cmp). The 9ca16f45 files are unchanged in d9c28330.
- **Build root:** out/job_OCC502/lean, which holds byte copies plus a copy of dcheck/COccBridge.lean (already built in dc/). Output
  goes to ~/studio_lean_builds/rsst118_fb35d2d1/out_occ502. LEAN_PATH also carries hd0 (HDCtrl, HD30), out_hdc502 (HDC) and
  out_hdr5 (HDR5).

## Results so far (lean/status.txt): 819 modules, all exit 0, sorry 0, sorryAx 0
| set | modules | result |
|---|---|---|
| hdc | HC_000..369, COccHC_000..369 | 740 / 740 exit 0, about 7 s each (3.2 GB) |
| ctrl3 | HK_00..02, COccHK_00..02, **HDCtrlOcc** | all exit 0 |
| hd30 | H30_00..29, COccH30_00..29, **HD30Occ** | all exit 0 |
| hdr5 | HR_00..04, COccHR_00..04, **HDR5Occ** | all exit 0 |

**Axioms** (`#print axioms`; every print checked):
- HDCtrlOcc: 6 prints. HD30Occ: 60 prints (dEntry_i and colorable_i). HDR5Occ: 10 prints.
- Only propext, Classical.choice, Quot.sound and native_decide auxiliaries appear: hD_i, *Confs_length, and DCheck.R1.check4..9
  for colorable_i.

**HDCOcc:** pending. It imports HDCAll, which is built when HDC502 finishes (370 hD; 97 done now, 0 failed). It is queued
automatically (lean/drive2.sh).
