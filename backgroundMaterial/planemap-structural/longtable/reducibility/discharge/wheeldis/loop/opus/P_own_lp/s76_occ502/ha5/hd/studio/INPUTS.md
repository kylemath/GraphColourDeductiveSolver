# HDA5T hD inputs (written here: main has no INPUTS.md for job HA5)
- main 7c6ef625 (job HA5: module splits for the A-5 twin witnesses), out/job_HA5/. Byte copies: D_a5.tsv (md5 a90ee34a, 35 rows; also in/D_a5.tsv),
  hd/module_split.tsv -> module_split.tsv (9a38e6a1). Same md5s as the copies in swarm/round6/W18-rule-audit/from_studio/a5_twins/HA5/.
- EXTRAFILE: D_a5.tsv, the 35 D witnesses of the W18 A-5 frame twins (kc lines), rings 11-15, in module_split.tsv order.
- gen_hd.py f743a82d, MOD **HDA5T**, PFX **hda5t** (PFX not stated on main; lower-case MOD as in every earlier hD job), batch 1:
  HDA5T, HDA5TV00..34 (`HDA5TV.hD_i`), HDA5TAll. The PFX only appears in HDA5TOcc's docstring.
- HDA5T_local_gen_hd_f743a82d.lean: gen_hd.py f743a82d run here on D_a5.tsv with these parameters (the Studio's HDA5T.lean is not on main yet).
