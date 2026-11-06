# job HDW13: Lean hD and occurrence glue for swarm W13's 27 D kill windows (Studio, 6 Nov)

**Result:** all 27 windows are D on dfast18, cfast and kc, and all 27 have Lean hD plus occurrence glue. All 84 modules exit 0 with sorry 0 and error 0;
sorryAx appears in 0 logs.

## Inputs
- **EXTRAFILE:** D_w13.tsv (5e86ee15), from claude/project-thread-phexa1 at 5e44c524, ext_handoff_nov3/w13d/. It has 27 rows in the swarm's list order, and the copies of
  fname_to_window.txt and pat_W13_all_D.out are in in/. gen_hd f743a82d, MOD HDW13, PFX hdw13, batch 1. D_w13.tsv and module_split.tsv were pushed first at a9611b67.
- **Glue:** c54336d9, s76_occ502/hdw13/lean/. All 56 files are copied byte-identically into in/glue/ (ab7782be), and the build copies in lean/ also match on cmp. HDW13Occ md5 8cbf49a0.
  COccBridge is byte-copied from job_HDB3.
- **check_literals** (D variant, out/job_OCC502/in/scripts/check_literals.py, run the same way as for HDB3) on HDW13.lean against in/glue HWD_: **27 entries, 0 mismatches**.

## Engines and hD (eng/; dfast18 07cb1e0b, cfast de59e72f, kc -C -s 60 -t 600 07e79fae; Lean v4.35.0-rc3 in ~/studio_lean_builds/rsst118_fb35d2d1/out_hdw13)
| # | window | ring | dfast18 | cfast | kc | classes = reached | hD module | exit | sorry | CPU (user) | RSS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | b7_u55575.._576.... | 11 | D | D | D | 7,381 | HDW13V00 | 0 | 0 | 8 s | 514 MB |
| 1 | b7_u555755._576.... | 11 | D | D | D | 7,381 | HDW13V01 | 0 | 0 | 7 s | 514 MB |
| 2 | b7_u55575.._5766... | 12 | D | D | D | 22,144 | HDW13V02 | 0 | 0 | 36 s | 515 MB |
| 3 | b7_u555755._5766... | 12 | D | D | D | 22,144 | HDW13V03 | 0 | 0 | 33 s | 515 MB |
| 4 | b7_u5557557_576.... | 12 | D | D | D | 22,144 | HDW13V04 | 0 | 0 | 35 s | 515 MB |
| 5 | b7_u5..5776_5..55.5 | 13 | D | D | D | 66,430 | HDW13V05 | 0 | 0 | 243 s | 519 MB |
| 6 | b7_u5556..6_776...6 | 13 | D | D | D | 66,430 | HDW13V06 | 0 | 0 | 183 s | 519 MB |
| 7 | b7_u556775._5.55... | 13 | D | D | D | 66,430 | HDW13V07 | 0 | 0 | 223 s | 519 MB |
| 8 | b7_u557666._56..5.. | 13 | D | D | D | 66,430 | HDW13V08 | 0 | 0 | 204 s | 519 MB |
| 9 | b7_u5556667_75....6 | 13 | D | D | D | 66,430 | HDW13V09 | 0 | 0 | 164 s | 519 MB |
| 10 | b7_u5557557_...676. | 13 | D | D | D | 66,430 | HDW13V10 | 0 | 0 | 155 s | 519 MB |
| 11 | b7_u556775._5655... | 13 | D | D | D | 66,430 | HDW13V11 | 0 | 0 | 169 s | 519 MB |
| 12 | b7_u56.5776_5..55.5 | 13 | D | D | D | 66,430 | HDW13V12 | 0 | 0 | 170 s | 519 MB |
| 13 | b7_u555755._57667.. | 13 | D | D | D | 66,430 | HDW13V13 | 0 | 0 | 160 s | 519 MB |
| 14 | b7_u5557557_5..676. | 13 | D | D | D | 66,430 | HDW13V14 | 0 | 0 | 157 s | 519 MB |
| 15 | b7_u5557557_576...7 | 13 | D | D | D | 66,430 | HDW13V15 | 0 | 0 | 182 s | 519 MB |
| 16 | b7_u5557557_576..6. | 13 | D | D | D | 66,430 | HDW13V16 | 0 | 0 | 166 s | 519 MB |
| 17 | b7_u5557557_5766... | 13 | D | D | D | 66,430 | HDW13V17 | 0 | 0 | 178 s | 519 MB |
| 18 | b7_u5..5777_...5555 | 14 | D | D | D | 199,291 | HDW13V18 | 0 | 0 | 1,340 s | 532 MB |
| 19 | b7_u5666.67_..5..55 | 14 | D | D | D | 199,291 | HDW13V19 | 0 | 0 | 1,134 s | 531 MB |
| 20 | b7_u5666677_5....55 | 14 | D | D | D | 199,291 | HDW13V20 | 0 | 0 | 997 s | 526 MB |
| 21 | b7_u5666677_55...55 | 14 | D | D | D | 199,291 | HDW13V21 | 0 | 0 | 823 s | 532 MB |
| 22 | b7_u5557557_5..6767 | 14 | D | D | D | 199,291 | HDW13V22 | 0 | 0 | 825 s | 532 MB |
| 23 | b7_u5557557_57.676. | 14 | D | D | D | 199,291 | HDW13V23 | 0 | 0 | 854 s | 533 MB |
| 24 | b7_u5557557_5766..7 | 14 | D | D | D | 199,291 | HDW13V24 | 0 | 0 | 932 s | 532 MB |
| 25 | b7_u5557557_57667.. | 14 | D | D | D | 199,291 | HDW13V25 | 0 | 0 | 907 s | 525 MB |
| 26 | b7_u5757677_555..55 | 14 | D | D | D | 199,291 | HDW13V26 | 0 | 0 | 761 s | 528 MB |

Total hD CPU: 11,048 s (3.07 h), run 8 at a time.

## Other modules
| module | exit | sorry | wall |
|---|---|---|---|
| HDW13 | 0 | 0 | 2 s |
| HDW13All | 0 | 0 | 2 s |
| HWD_00..26 (27) | 0 | 0 | 12 s max |
| COccHWD_00..26 (27) | 0 | 0 | 5 s max |
| **HDW13Occ** (after HDW13All) | **0** | **0** | 4 s |

**Axioms:**
- HDW13All (hD_all): propext, Classical.choice and Quot.sound, plus native_decide auxiliaries (hD_0..26, hdw13Confs_length).
- HDW13Occ (54 prints, for the 27 dEntry and colorable entries plus mirrors): the same three axioms, plus native_decide auxiliaries (hD_k, hdw13Confs_length,
  DCheck.R1.check4..9).

No other axioms appear, and sorryAx appears 0 times.

**Independence:** the D verdicts come from Studio dfast18, cfast and kc, our engines. hD is the repo DCheck18.dReducible kernel via our gen_hd. Only the occurrence
glue (H/COcc/HDW13Occ) is Opus-generated, from a byte copy of our D_w13.tsv. I compiled it unmodified. check_literals is Opus's script, run because the relay asked
for it. I read no Opus engine code.
