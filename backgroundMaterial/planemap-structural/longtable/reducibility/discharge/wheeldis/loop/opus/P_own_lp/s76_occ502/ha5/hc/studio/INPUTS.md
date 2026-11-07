# A5CV hC inputs (written here: main has no INPUTS.md for job HA5)
- main 7c6ef625, out/job_HA5/hc/. Byte copies: CA5C.lean (md5 0b2b13fb; identical to out/job_ST15/lean/CA5C.lean), module_split.tsv (fb3c3b1f).
  Same md5s as the copies in swarm/round6/W18-rule-audit/from_studio/a5_twins/HA5/hc/.
- EXTRAFILE: out/job_ST15/extraC.tsv (md5 7aebd0a1, 10 rows, kc line + X; added at main 41069d07, unchanged at 7c6ef625) -> ../in/extraC.tsv.
  CA5C.lean's entries have src := "EXTRAFILE"; names, order, rings and X equal module_split.tsv (10/10).
- Studio modules: CA5C (a5cEntries, a5cEntries_ok, a5cEntries_length), A5CV00..09 (`A5CV.hC_i`), A5CVAll (`A5CV.hC_all : Fin 10`,
  assumed in the W3PVAll form; not on main yet).
