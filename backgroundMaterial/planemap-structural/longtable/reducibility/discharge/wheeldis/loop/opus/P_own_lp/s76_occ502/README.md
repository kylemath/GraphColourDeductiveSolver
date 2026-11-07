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
