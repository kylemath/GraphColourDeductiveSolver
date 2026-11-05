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

## HDC502 batches
These need Studio's HDC502 EXTRAFILE(s) and MOD / PFX. They are generated once those are on main.
