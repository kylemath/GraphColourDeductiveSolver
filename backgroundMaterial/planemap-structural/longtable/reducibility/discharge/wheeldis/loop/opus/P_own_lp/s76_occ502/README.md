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
