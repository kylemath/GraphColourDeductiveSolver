# K3CHK2 / K3CHK3 hC inputs (written here: main has no INPUTS.md for these jobs)
- main d208ddf0 (Lean hC done: K3C2V.hC_0, K3C3V.hC_0; exit 0, sorry 0). Byte copies from out/job_K3CHK2/ and out/job_K3CHK3/:
  - ../in/extraC_K3CHK2.tsv = job_K3CHK2/extraC.tsv (md5 6eb0ffd8): b9_u655...566_66......5, r14 m10, X I5-I6.
  - ../in/extraC_K3CHK3.tsv = job_K3CHK3/extraC.tsv (md5 1fdedb3b): b9_u.56.56555_.5......., r13 m9, X I0-I5.
  - CK3C2.lean (f469e29b; k3c2Entries, k3c2Entries_ok, k3c2Entries_length), K3C2V00.lean (c961c90a; K3C2V.hC_0).
  - CK3C3.lean (21f11a08; k3c3Entries, k3c3Entries_ok, k3c3Entries_length), K3C3V00.lean (2862bb8d; K3C3V.hC_0).
  Same md5s as the copies in swarm/round6/W13-open-row-kills/round6/K3/from_studio/K3CHK2/ and K3CHK3/; unchanged on origin/main 90e4c5c1.
- Not on main: K3C2VAll / K3C3VAll (`hC_all : Fin 1`). The Studio built only the V00 modules for these one-entry jobs. HK3C2Occ / HK3C3Occ need them.
- K3C2VAll / K3C3VAll were added by the Studio at main 55cee157 (97a2b762 / 8c110745), in the W3PVAll form assumed above.
- K3CHK4 (main c69e9a35, out/job_K3CHK4/): ../in/extraC_K3CHK4.tsv = extraC.tsv (24a3a8bb): b8_u.56656.._...66..., r13 m8, X I2-I3.
  CK3C4.lean (3cbe5121; k3c4Entries, k3c4Entries_ok, k3c4Entries_length), K3C4V00.lean (a00c3935; K3C4V.hC_0), K3C4VAll.lean (736c23e4; K3C4V.hC_all : Fin 1),
  module_split_hC_K3CHK4.tsv = module_split_hC.tsv (2364c901). Same md5s as the copies in K3/from_studio/K3CHK4/.
- HCK3i (main 23782a2c; job folder added in 203b0660, out/job_HCK3i/): ../in/extraC_HCK3i.tsv = extraC.tsv (2c361133): b7_u.5785.._55555.. (r13 m10) and
  b9_u...575655_....5.... (r13 m8), both X I0-I3. CK3I.lean (3561cf6e; k3iEntries, k3iEntries_ok, k3iEntries_length), K3IV00.lean (868a8f49; K3IV.hC_0),
  K3IV01.lean (2cc82a73; K3IV.hC_1), K3IVAll.lean (31b8a873; K3IV.hC_all : Fin 2), module_split_HCK3i.tsv = module_split.tsv (e316f87a).
  Same md5s as the copies in K3/from_studio/HCK3i/. The s86 cfast list s86_f2b7/w13/pat_K3i_C.cfast (44e053c2) names them f7_.5785.._55555.. and
  f9_...575655_....5.... with these windows, the same r, m and X = {I0-I3}.
- HCK3j (main 93236129, out/job_HCK3j/): ../in/extraC_HCK3j.tsv = extraC.tsv (15ad840d): b9_u.56575.55_...5...5. (r14 m10), X I0-I3, not rim-pinned.
  CK3J.lean (6759cd9c; k3jEntries, k3jEntries_ok, k3jEntries_length), K3JV00.lean (e3e5a398; K3JV.hC_0), K3JVAll.lean (f387d3d4; K3JV.hC_all : Fin 1),
  module_split_HCK3j.tsv = module_split.tsv (6678d6ec). Same md5s as the copies in K3/from_studio/HCK3j/. s86_f2b7/w13/pat_K3j_C.cfast (26650f73)
  names it f9_.56575.55_...5...5. with this window, the same r, m and X = {I0-I3}.
