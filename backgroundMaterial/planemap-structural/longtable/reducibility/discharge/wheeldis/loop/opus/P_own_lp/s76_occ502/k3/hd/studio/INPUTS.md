# HDK3 hD inputs (written here: main has no INPUTS.md for job HDK3)
- main ee839f4e (job HDK3: D_k3.tsv + module_split for the 6 K-3 D kills), out/job_HDK3/. Byte copies: D_k3.tsv (md5 0d49071d, 6 rows; also in/D_k3.tsv),
  module_split.tsv (20dc234c). Same md5s as the copies in swarm/round6/W13-open-row-kills/round6/K3/from_studio/HDK3/.
- EXTRAFILE: D_k3.tsv, the 6 K-3 D kills (kc lines, in module_split.tsv order; K3CHK2's 3 D and K3CHK3's b9_u75..65656 among them), rings 13-14.
- gen_hd.py f743a82d, MOD **HDK3**, PFX **hdk3** (as stated by the Studio), batch 1: HDK3, HDK3V00..05 (`HDK3V.hD_i`), HDK3All.
- HDK3_local_gen_hd_f743a82d.lean: gen_hd.py f743a82d run here on D_k3.tsv with these parameters (the Studio's HDK3.lean is not on main
  or in the shared folder yet).
