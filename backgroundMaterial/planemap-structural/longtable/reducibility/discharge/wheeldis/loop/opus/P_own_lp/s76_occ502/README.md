# s76_occ502: occurrence glue for the D side of the 502 cover (Opus, 5 Nov 2026)

Generated with s74_leanglue/gen_occ_kc.py (714ea779; compiled clean on Studio, job OCC13 at main 100c24af).

## hd30/: the 30 HD0 calibration entries (Studio out/job_HD0, main a6ed90d5)
- in/calib30.tsv: byte copy of out/job_HD0/calib30.tsv (md5 6e25c77d).
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hd30/in/calib30.tsv s76_occ502/hd30/lean H30_ --hd HD30 hd30`
  -> H30_00..29.lean, COccH30_00..29.lean, HD30Occ.lean. 30 generated, 0 failed; 60 rotations validated.
- scripts/check_literals.py on Studio's HD30.lean: 30 entries, 0 mismatches. So `HD30.hd30Confs.get k = H30_kk.cf` is the
  same literal. A one-field mutation is caught (negative control).
- Of the 502 cover, nl2180_r13, nl2215_r14 and nl1502_r15 are in this set.
- Compile like OCC13: H30_kk, then COccH30_kk, then HD30Occ. HD30Occ imports HD30All.

## hdc/: the 370 HDC502 entries (Studio out/job_HDC502, main 97e32666)
- in/D_todo.tsv: byte copy of out/job_HDC502/D_todo.tsv (md5 219b58ad), MOD HDC, PFX hdc.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hdc/in/D_todo.tsv s76_occ502/hdc/lean HC_ --hd HDC hdc`
  -> HC_000..369.lean, COccHC_000..369.lean, HDCOcc.lean. 370 generated, 0 failed; 740 rotations validated.
- check_literals.py against Studio's HDC.lean: 370 entries, 0 mismatches. HDCOcc pairs dEntry_i with HC_iii and HDCV.hD_i
  for every i (370/370).
- Compile order per entry: HC_iii, then COccHC_iii. It can follow HDCVnn in the same batch. HDCOcc comes last, after HDCAll.

## ctrl3/: HD0's 3 RSST controls (out/job_HD0/ctrl3.tsv, md5 a025045a; MOD HDCtrl, PFX hdc)
- HK_00..02, COccHK_00..02, HDCtrlOcc. 0 literal mismatches. rsst008 is index 0 and rsst012 is index 2 (cover entries).

## Coverage of the 380 D in cover_pb868.tsv
370 in hdc/, rsst008 and rsst012 in ctrl3/, and nl2180_r13, nl2215_r14, nl1502_r15 in hd30/ (indices 1, 16, 24).
and the 5 RSST of Studio batch HDR5 in hdr5/.
All 380 D names are covered exactly once (checked by name, RSST by number prefix).

## hdr5/: Studio HDR5 (out/job_HDC502/D_rsst5.tsv, md5 e6458c99, main 421efcdb; MOD HDR5, PFX hdr5)
- HR_00..04, COccHR_00..04 and HDR5Occ for rsst001 / 004 / 006 / 024 / 026. 0 literal mismatches against lean_r5/HDR5.lean.

## hdk7/: KILL7, Team B's 7 new kill6 configurations (Studio out/job_KILL7/D_kill7.tsv, md5 d2b3ad70, main 38a1440a)
- MOD HDK7, PFX hdk7 -> HQ_00..06, COccHQ_00..06, HDK7Occ. 7 generated, 14 rotations validated, 0 literal mismatches
  against Studio's lean/HDK7.lean.
- These are off the main line until KILL7 (a)-(c) pass. Their use as kill6 entries also needs the pattern -> Occ step (Job 26).

## hdb3/: HDB3, B3's 4 route-F D windows (Studio out/job_HDB3/D_b3.tsv, md5 5c284e10, main 2011563a; MOD HDB3, PFX hdb3)
- in/D_b3.tsv and studio/HDB3.lean, studio/INPUTS.md: byte copies from main 2011563a.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hdb3/in/D_b3.tsv s76_occ502/hdb3/lean HB3_ --hd HDB3 hdb3`
  -> HB3_00..03, COccHB3_00..03, HDB3Occ. 4 generated, 0 failed; 8 rotations validated; every link an induced cycle.
- check_literals.py against studio/HDB3.lean: 4 entries, 0 mismatches; a mutated copy (m 13 -> 12) gives 2 mismatches, exit 1.
- HB3_00 b7_u7577575_.5.5.55 (r14 m12), HB3_01 .555.55 (r14 m13), HB3_02 .565.55 (r15 m13), HB3_03 .5.5755 (r15 m13).
- Compile order: HB3_kk, then COccHB3_kk, then HDB3Occ (imports HDB3All). Using them as separator patterns still needs the
  pattern -> Occ step (Job 26), as for hdk7.

## hcw13/: HCW13, the swarm's 3 W13 C configurations (Studio out/job_HCW13/extra_hcw13.tsv, md5 aa9dbd9b, main 76761697)
- in/extra_hcw13.tsv and studio/{CHW13,HW13All,HW13V00..02}.lean: byte copies from main 76761697.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hcw13/in/extra_hcw13.tsv s76_occ502/hcw13/lean HW3_` (no --hd: C side)
  -> HW3_00..02 (Occ, face-walk form) and COccHW3_00..02 (bridge + registry glue, incl. colorable_of_occ_centry). 3 generated,
  0 failed; 6 rotations validated; every link an induced cycle.
- lean/HW13Occ.lean (hand template, CC3All's ccF pattern): cEntry k := (w13Entries.get k).toCEntryF w13Entries_ok (HW13V.hC_all k);
  colorable_k / colorable_mirror_k := HW3_kk.colorable_of_(mirror_)occ_centry (cEntry k) rfl. The rfl needs toCEntryF's cf = d.cf
  (CXRing.lean:45, cf := d.cf) and identical literals: scripts/check_literals_c.py (regex allows "{\n name") on CHW13.lean:
  3 entries, 0 mismatches; a mutated copy (m 9 -> 8) gives 1 mismatch, exit 1. NOT compiled here (no Lean in this container).
- Compile order: HW3_kk, COccHW3_kk, then HW13Occ (imports HW13All). HW3_00 b7_u5556677_.....5. (r13 m9), HW3_01
  b7_u.557755_...5... (r12 m8), HW3_02 b7_u.5775.._.555... (r12 m8). Pattern -> Occ (Job 26) still open, as for hdk7/hdb3.

## hcw13r2/: HCW13R2, the swarm's W13 round-2 C configurations (Studio main 4327360c: extraA.tsv md5 36f52f74 (4, cover-4), extraB.tsv md5 1bb1a1a9 (41))
- in/extra{A,B}.tsv and studio/{CW2A,CW2B,W2AV00..03,W2AVAll}.lean: byte copies from main 4327360c (W2BV* not on main yet).
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hcw13r2/in/extraA.tsv s76_occ502/hcw13r2/lean HW2A_` (C side), same for extraB with HW2B_
  -> HW2A_00..03 + COccHW2A_00..03 (4 generated, 0 failed, 8 rotations validated) and HW2B_00..40 + COccHW2B_00..40 (41, 0 failed, 82).
- lean/HW2AOcc.lean, lean/HW2BOcc.lean: scripts/gen_cocc_batch.py (new: the HW13Occ template as a generator; regression: it regenerates
  hcw13/lean/HW13Occ.lean byte for byte). Imports W2AVAll / W2BVAll; cEntry k := (w2xEntries.get ..).toCEntryF w2xEntries_ok (W2xV.hC_all k).
- check_literals_c.py: CW2A.lean 4 entries, 0 mismatches; CW2B.lean 41 entries, 0 mismatches. NOT compiled here (no Lean in this container).
- Compile order: HW2x_kk, COccHW2x_kk, then HW2xOcc (after W2xVAll).

## hcw13r3/, hcw13r4/: pre-generated for HCW13R3 (27 C, extra_hcW13r3_x1.tsv md5 a3151887, swarm 1ff3dbd3) and HCW13R4 (4 C, extra_hcW13r4.tsv md5 3ea965c5, swarm 7e96e85a)
- HWR3_00..26 + COccHWR3_kk + HWR3Occ (imports W3VAll, w3Entries, W3V.hC_all); HWR4_00..03 + COccHWR4_kk + HWR4Occ (W4VAll, w4Entries, W4V).
  27 / 4 generated, 0 failed. Entry k = line k of the EXTRAFILE: run check_literals_c.py on CW3.lean / CW4.lean before compiling; if Studio
  reorders the rows, regenerate from its EXTRAFILE (the two commands above).

## hdw13/: HDW13, swarm W13's 27 D kill windows (Studio out/job_HDW13/D_w13.tsv, md5 5e86ee15, main a9611b67; MOD HDW13, PFX hdw13)
- in/D_w13.tsv and studio/{D_w13.tsv,INPUTS.md,module_split.tsv}: byte copies from main a9611b67.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hdw13/in/D_w13.tsv s76_occ502/hdw13/lean HWD_ --hd HDW13 hdw13`
  -> HWD_00..26, COccHWD_00..26, HDW13Occ (imports HDW13All, uses HDW13V.hD_k). 27 generated, 0 failed; 54 rotations validated; every link an induced cycle.
- Names in HWD_modules.txt equal module_split.tsv's names and D_w13.tsv's order (27/27).
- Literal check: studio/HDW13_local_gen_hd_f743a82d.lean is gen_hd.py f743a82d (main out/job_HD0) run here on in/D_w13.tsv with
  MOD HDW13, PFX hdw13, batch 1. check_literals.py against it: 27 entries, 0 mismatches. A mutated copy (one name renamed) gives
  11 mismatches, exit 1. Rerun check_literals against the Mac's own HDW13.lean when it lands.
- Compile order: HWD_kk, then COccHWD_kk, then HDW13Occ.

## hcw13r3p/: HCW13R3P, the 9 rim-pinned W13 round-3 C configurations (|X| = 3 or 4 with an R-I edge; Studio out/job_HCW13R3P, main c06fc8da)

- in/{extra.tsv (6a279607), module_split.tsv (935bd8c5)} and studio/CW3P.lean are byte copies from main c06fc8da.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hcw13r3p/in/extra.tsv s76_occ502/hcw13r3p/lean HWR3P_` (C side).
  This produced HWR3P_00..08 and COccHWR3P_00..08: 9 generated, 0 failed, 18 rotations validated, every link an induced cycle.
- lean/HWR3POcc.lean comes from `scripts/gen_cocc_batch.py ... HWR3POcc W3PVAll W3PV w3pEntries HWR3P_`. It imports W3PVAll and
  uses `W3PV.hC_all k`, `w3pEntries_ok` and `w3pEntries_length`. X, eqR and eqI stay inside the XRData. The glue reads only cf, so the
  template is the one used for HCW13R2/R3.
- check_literals_c.py on CW3P.lean gives 9 entries, 0 mismatches. A copy with one intAdj entry changed gives 1 mismatch and exit 1.
- Module names and their order match module_split.tsv (9/9). Compile order: HWR3P_kk, then COccHWR3P_kk, then HWR3POcc (after W3PVAll).
  This was not compiled here, because this container has no Lean.
- **Studio build (14:16Z, 6 Nov):** done on main at ff255ae2. The glue compiled unmodified and byte-identical to e1285b69 (HWR3POcc e4316ee9). All 30 modules are clean, with sorry 0. `W3PV.hC_all` has the assumed `Fin 9` form.

## hdw18n/: HDW18N, the 15 nl51 witnesses of the W18 428 without Lean hD (Studio out/job_HDW18N/D_w18n.tsv, md5 4df706df, main 2c3559f1; MOD HDW18N, PFX hdw18n)
- in/D_w18n.tsv and studio/{D_w18n.tsv,INPUTS.md (fe64d854),module_split.tsv (f4f07fcf)}: byte copies from main 2c3559f1. 15 rows, rings 10-14.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hdw18n/in/D_w18n.tsv s76_occ502/hdw18n/lean HWN_ --hd HDW18N hdw18n`
  -> HWN_00..14, COccHWN_00..14, HDW18NOcc (imports HDW18NAll, uses HDW18NV.hD_k). 15 generated, 0 failed; 30 rotations validated; every link an induced cycle.
- Names in HWN_modules.txt equal module_split.tsv's names and rings and D_w18n.tsv's order (15/15); HDW18NOcc pairs HWN_kk with HDW18NV.hD_k for every k.
- Literal check: studio/HDW18N_local_gen_hd_f743a82d.lean is gen_hd.py f743a82d (main out/job_HD0) run here on in/D_w18n.tsv with
  MOD HDW18N, PFX hdw18n, batch 1. check_literals.py against it: 15 entries, 0 mismatches. A mutated copy (nl0065_r10 m 7 -> 6) gives
  1 mismatch, exit 1. Rerun check_literals against the Mac's own HDW18N.lean when it lands. NOT compiled here (no Lean in this container).
- Compile order: HWN_kk, then COccHWN_kk, then HDW18NOcc (after HDW18NAll). HDW18NOcc md5 d39cdcea.

## hdk3p/: HDK3P, the two q7- k3p D configurations (ring 8) (Studio out/job_HDK3P/D_k3p.tsv, md5 592580c5, main 1c1ad4b6; MOD HDK3P, PFX hdk3p)
- in/D_k3p.tsv and studio/{D_k3p.tsv,module_split.tsv (6a293bb1),HDK3P.lean (eafaf56a, from lean/)}: byte copies from main 1c1ad4b6.
  studio/INPUTS.md is written here (main has none for this job; it records the commit, md5s and the gen_hd parameters from report.md).
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/hdk3p/in/D_k3p.tsv s76_occ502/hdk3p/lean HK3P_ --hd HDK3P hdk3p`
  -> HK3P_00..01, COccHK3P_00..01, HDK3POcc (imports HDK3PAll, uses HDK3PV.hD_k). 2 generated, 0 failed; 4 rotations validated; every link an induced cycle.
- Names in HK3P_modules.txt equal module_split.tsv's names and rings (2/2); HDK3POcc pairs HK3P_kk with HDK3PV.hD_k. The names contain
  `/`, `=` and `:` (`..._s5/p6L1=5`); they appear only in string literals and doc comments, with no `/-` or `-/` in them.
- check_literals.py against studio/HDK3P.lean (Studio's own file): 2 entries, 0 mismatches. A mutated copy (entry 1 m 7 -> 6) gives
  1 mismatch, exit 1. gen_hd.py f743a82d run here on in/D_k3p.tsv reproduces HDK3P.lean, HDK3PV00/01 and HDK3PAll byte for byte.
  NOT compiled here (no Lean in this container).
- Compile order: HK3P_kk, then COccHK3P_kk, then HDK3POcc (after HDK3PAll). HDK3POcc md5 9836aab5.

## ha5/hd/: HDA5T, the 35 D witnesses of the W18 A-5 frame twins (Studio out/job_HA5/D_a5.tsv, md5 a90ee34a, main 7c6ef625; MOD HDA5T, PFX hda5t)
- in/D_a5.tsv and studio/{D_a5.tsv,module_split.tsv (9a38e6a1, from hd/)}: byte copies from main 7c6ef625. 35 rows, rings 11-15.
  studio/INPUTS.md is written here (main has none for job HA5). PFX hda5t is lower-case MOD as in every earlier hD job (main does not state it);
  it only appears in HDA5TOcc's docstring.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/ha5/hd/in/D_a5.tsv s76_occ502/ha5/hd/lean HA5D_ --hd HDA5T hda5t`
  -> HA5D_00..34, COccHA5D_00..34, HDA5TOcc (imports HDA5TAll, uses HDA5TV.hD_k). 35 generated, 0 failed; 70 rotations validated; every link an induced cycle.
- Names in HA5D_modules.txt equal module_split.tsv's names and rings and D_a5.tsv's order (35/35); HDA5TOcc pairs HA5D_kk with HDA5TV.hD_k for every k.
- Literal check: studio/HDA5T_local_gen_hd_f743a82d.lean is gen_hd.py f743a82d run here on in/D_a5.tsv with MOD HDA5T, PFX hda5t, batch 1
  (its module names HDA5TV00..34 equal module_split.tsv's). check_literals.py against it: 35 entries, 0 mismatches. A mutated copy
  (tw_d7_w6_0_16_fx_0 m 10 -> 9) gives 1 mismatch, exit 1. Rerun check_literals against the Mac's own HDA5T.lean when it lands. NOT compiled here (no Lean in this container).
- Compile order: HA5D_kk, then COccHA5D_kk, then HDA5TOcc (after HDA5TAll). HDA5TOcc md5 d4bfcb76.

## ha5/hc/: A5CV, the 10 C witnesses of W18 A-5 (9 frame twins + W13 kill6_C p515) on CA5C (Studio out/job_HA5/hc, main 7c6ef625)
- studio/{CA5C.lean (0b2b13fb, = out/job_ST15/lean/CA5C.lean),module_split.tsv (fb3c3b1f)}: byte copies from main 7c6ef625. in/extraC.tsv (7aebd0a1) is
  the EXTRAFILE out/job_ST15/extraC.tsv (main 41069d07, unchanged at 7c6ef625). Its names, order, rings and X equal module_split.tsv and CA5C.lean (10/10).
  studio/INPUTS.md is written here (main has none for job HA5).
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/ha5/hc/in/extraC.tsv s76_occ502/ha5/hc/lean HA5C_` (C side, as for HCW13R2/R3P)
  -> HA5C_00..09 and COccHA5C_00..09: 10 generated, 0 failed, 20 rotations validated, every link an induced cycle.
- lean/HA5COcc.lean comes from `scripts/gen_cocc_batch.py ha5/hc/lean/HA5C_modules.txt HA5COcc A5CVAll A5CV a5cEntries HA5C_ ...` (run from s76_occ502).
  It imports A5CVAll and uses `A5CV.hC_all k`, `a5cEntries_ok` and `a5cEntries_length`. Regression first: the same script reproduces
  hcw13r3p/lean/HWR3POcc.lean (e4316ee9, Studio-compiled) byte for byte. A5CVAll is not on main yet; `A5CV.hC_all : Fin 10` is assumed in the W3PVAll form.
- check_literals_c.py on CA5C.lean gives 10 entries, 0 mismatches. A copy with one intAdj entry of p515 changed gives 1 mismatch and exit 1.
  NOT compiled here (no Lean in this container).
- Compile order: HA5C_kk, then COccHA5C_kk, then HA5COcc (after A5CVAll). HA5COcc md5 56ddb34b.

## k3/hd/: HDK3, the 6 K-3 D kills (Studio out/job_HDK3/D_k3.tsv, md5 0d49071d, main ee839f4e; MOD HDK3, PFX hdk3)
- in/D_k3.tsv and studio/{D_k3.tsv,module_split.tsv (20dc234c)}: byte copies from main ee839f4e. 6 rows, rings 13-14.
  studio/INPUTS.md is written here (main has none for job HDK3).
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/k3/hd/in/D_k3.tsv s76_occ502/k3/hd/lean HK3D_ --hd HDK3 hdk3`
  -> HK3D_00..05, COccHK3D_00..05, HDK3Occ (imports HDK3All, uses HDK3V.hD_k). 6 generated, 0 failed; 12 rotations validated; every link an induced cycle.
- Names in HK3D_modules.txt equal module_split.tsv's names and rings and D_k3.tsv's order (6/6); HDK3Occ pairs HK3D_kk with HDK3V.hD_k for every k.
- Literal check: studio/HDK3_local_gen_hd_f743a82d.lean is gen_hd.py f743a82d run here on in/D_k3.tsv with MOD HDK3, PFX hdk3, batch 1
  (its module names HDK3V00..05 equal module_split.tsv's). check_literals.py against it: 6 entries, 0 mismatches. A mutated copy
  (b9_u75..65656_5...55... m 11 -> 10) gives 1 mismatch, exit 1. Rerun check_literals against the Mac's own HDK3.lean when it lands. NOT compiled here (no Lean in this container).
- Compile order: HK3D_kk, then COccHK3D_kk, then HDK3Occ (after HDK3All). HDK3Occ md5 2c6fae49.

## k3/hc/: the two K-3 C kills, K3CHK2 (b9_u655...566_66......5, X = {I5-I6}) and K3CHK3 (b9_u.56.56555_.5......., X = {I0-I5}) (Studio main d208ddf0)
- in/extraC_K3CHK2.tsv (6eb0ffd8) and in/extraC_K3CHK3.tsv (1fdedb3b) are the jobs' extraC.tsv; studio/{CK3C2.lean (f469e29b), K3C2V00.lean (c961c90a),
  CK3C3.lean (21f11a08), K3C3V00.lean (2862bb8d)}: byte copies from main d208ddf0. studio/INPUTS.md is written here.
- Two one-entry jobs, as HCW13R2 handled its separate A and B jobs (one gen_occ_kc run and one gen_cocc_batch run each; gen_cocc_batch.py takes one
  verdict module per run):
  `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/k3/hc/in/extraC_K3CHK2.tsv s76_occ502/k3/hc/lean HK3C2_` (C side), same for K3CHK3 with HK3C3_
  -> HK3C2_00 + COccHK3C2_00 and HK3C3_00 + COccHK3C3_00. Each: 1 generated, 0 failed, 2 rotations validated, every link an induced cycle.
- lean/HK3C2Occ.lean, lean/HK3C3Occ.lean: `scripts/gen_cocc_batch.py k3/hc/lean/HK3CJ_modules.txt HK3CJOcc K3CJVAll K3CJV k3cjEntries HK3CJ_ ...` (J = 2, 3; run
  from s76_occ502, the script unchanged). They import K3CJVAll and use `K3CJV.hC_all k`, `k3cjEntries_ok` and `k3cjEntries_length`.
  **K3C2VAll / K3C3VAll are not on main:** the Studio built only CK3CJ and K3CJV00 (`K3CJV.hC_0`). HK3CJOcc compiles only once the Studio adds
  K3CJVAll with `theorem hC_all (k : Fin 1)` in the W3PVAll form (`fin_cases k; exact hC_0`). HK3CJ_00 and COccHK3CJ_00 do not need it.
- check_literals_c.py: CK3C2.lean 1 entry, 0 mismatches; CK3C3.lean 1 entry, 0 mismatches. Copies with one intAdj entry changed give 1 mismatch
  and exit 1 for each. NOT compiled here (no Lean in this container).
- Compile order: HK3CJ_00, COccHK3CJ_00, then HK3CJOcc (after K3CJVAll). HK3C2Occ md5 a9c9c9e0, HK3C3Occ md5 44b1e377.
- **Studio (main 55cee157):** K3C2VAll / K3C3VAll added (97a2b762 / 8c110745, the form assumed above); the Studio's commit reports the glue
  copied byte-identical, check_literals 1/0 and 1/0, and the C glue built with all exit 0, sorry 0.

## ha5b/hd/: HDA5B, the 45 D witnesses new in W18 A-5 FINAL (Studio out/job_HA5b/D_a5b.tsv, md5 1dcb2cef, main 59a296b2; MOD HDA5B, PFX hda5b)
- in/D_a5b.tsv and studio/{D_a5b.tsv,HDA5B.lean (c9358df1, from hd/),module_split.tsv (531ef16c, from hd/),INPUTS.md (1efaef77)}: byte copies from
  main 59a296b2 (same md5s as swarm/round6/W18-rule-audit/from_studio/a5_final/HA5b/). 45 rows, rings 14-16.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/ha5b/hd/in/D_a5b.tsv s76_occ502/ha5b/hd/lean HA5BD_ --hd HDA5B hda5b`
  -> HA5BD_00..44, COccHA5BD_00..44, HDA5BOcc (imports HDA5BAll, uses HDA5BV.hD_k). 45 generated, 0 failed; 90 rotations validated; every link an induced cycle.
- Names in HA5BD_modules.txt equal module_split.tsv's names and rings and D_a5b.tsv's and HDA5B.lean's order (45/45); HDA5BOcc pairs HA5BD_kk with HDA5BV.hD_k for every k.
- check_literals.py against studio/HDA5B.lean (the Studio's own file): 45 entries, 0 mismatches. A mutated copy (tw_d7_w6_0_1978_fx_0 m 11 -> 10)
  gives 1 mismatch, exit 1. gen_hd.py f743a82d run here on in/D_a5b.tsv reproduces HDA5B.lean byte for byte. NOT compiled here (no Lean in this container).
- Compile order: HA5BD_kk, then COccHA5BD_kk, then HDA5BOcc (after HDA5BAll). HDA5BOcc md5 fadfc64c.

## ha5b/hc/: A5BV, the 9 C witnesses new in W18 A-5 FINAL on CA5B (Studio out/job_HA5b, main 59a296b2)
- in/extraC.tsv (872ac38f) and studio/{CA5B.lean (99eec150),A5BV00..08.lean,A5BVAll.lean (fb9ce760),module_split.tsv (13fc50fc),INPUTS.md (1efaef77)}:
  byte copies from main 59a296b2 (same md5s as the shared a5_final/HA5b/ copies). Names, order, rings and X of extraC.tsv equal module_split.tsv and CA5B.lean (9/9).
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/ha5b/hc/in/extraC.tsv s76_occ502/ha5b/hc/lean HA5BC_` (C side, as for A5CV)
  -> HA5BC_00..08 and COccHA5BC_00..08: 9 generated, 0 failed, 18 rotations validated, every link an induced cycle.
- lean/HA5BCOcc.lean comes from `scripts/gen_cocc_batch.py ha5b/hc/lean/HA5BC_modules.txt HA5BCOcc A5BVAll A5BV a5bEntries HA5BC_ ...` (run from s76_occ502).
  It imports A5BVAll and uses `A5BV.hC_all k`, `a5bEntries_ok` and `a5bEntries_length`. A5BVAll is on main this time, and its `hC_all (k : Fin 9)` has the W3PVAll form.
- check_literals_c.py on CA5B.lean gives 9 entries, 0 mismatches. A copy with one intAdj entry of tw_d8_w7_p1_132_fx_0 changed gives 1 mismatch and exit 1.
  NOT compiled here (no Lean in this container).
- Compile order: HA5BC_kk, then COccHA5BC_kk, then HA5BCOcc (after A5BVAll). HA5BCOcc md5 d0ab975b.

## k3/hdk3b/: HDK3B, the K-3 D kill b8_u.5665675_.....55. (Studio out/job_HDK3b/D_k3b.tsv, md5 e2338150, main a02fa4af; MOD HDK3B, PFX hdk3b)
- in/D_k3b.tsv and studio/{D_k3b.tsv,module_split.tsv (6b8d2862),HDK3B.lean (7c619ece),HDK3BAll.lean,HDK3BV00.lean}: byte copies from main a02fa4af
  (same md5s as the shared K3/from_studio/HDK3b/ copies). 1 row, ring 14. studio/INPUTS.md is written here (main has none for this job).
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/k3/hdk3b/in/D_k3b.tsv s76_occ502/k3/hdk3b/lean HK3BD_ --hd HDK3B hdk3b`
  -> HK3BD_00, COccHK3BD_00, HDK3BOcc (imports HDK3BAll, uses HDK3BV.hD_0). 1 generated, 0 failed; 2 rotations validated; every link an induced cycle.
- Name and ring in HK3BD_modules.txt equal module_split.tsv's (1/1).
- check_literals.py against studio/HDK3B.lean (the Studio's own file): 1 entry, 0 mismatches. A mutated copy (m 10 -> 9) gives 1 mismatch, exit 1.
  gen_hd.py f743a82d run here on in/D_k3b.tsv reproduces HDK3B.lean, HDK3BV00 and HDK3BAll byte for byte. NOT compiled here (no Lean in this container).
- Compile order: HK3BD_00, then COccHK3BD_00, then HDK3BOcc (after HDK3BAll). HDK3BOcc md5 4b959797.

## k3/hc/ (K3CHK4): the K-3 C kill b8_u.56656.._...66..., X = {I2-I3} (Studio main c69e9a35, out/job_K3CHK4/)
- in/extraC_K3CHK4.tsv (24a3a8bb) and studio/{CK3C4.lean (3cbe5121),K3C4V00.lean (a00c3935),K3C4VAll.lean (736c23e4),module_split_hC_K3CHK4.tsv (2364c901)}:
  byte copies from main c69e9a35 (same md5s as the shared K3/from_studio/K3CHK4/ copies). studio/INPUTS.md updated.
- `python3 s74_leanglue/gen_occ_kc.py batch s76_occ502/k3/hc/in/extraC_K3CHK4.tsv s76_occ502/k3/hc/lean HK3C4_` (C side, as for K3C2/K3C3)
  -> HK3C4_00 + COccHK3C4_00: 1 generated, 0 failed, 2 rotations validated, every link an induced cycle. Name and ring equal module_split_hC.tsv's.
- lean/HK3C4Occ.lean: `scripts/gen_cocc_batch.py k3/hc/lean/HK3C4_modules.txt HK3C4Occ K3C4VAll K3C4V k3c4Entries HK3C4_ ...` (run from s76_occ502).
  It imports K3C4VAll (on main this time; `K3C4V.hC_all : Fin 1`, the W3PVAll form) and uses `k3c4Entries_ok` and `k3c4Entries_length`.
- check_literals_c.py on CK3C4.lean: 1 entry, 0 mismatches. A copy with one intAdj entry changed gives 1 mismatch, exit 1. NOT compiled here (no Lean in this container).
- Compile order: HK3C4_00, COccHK3C4_00, then HK3C4Occ (after K3C4VAll). HK3C4Occ md5 e010e982.
