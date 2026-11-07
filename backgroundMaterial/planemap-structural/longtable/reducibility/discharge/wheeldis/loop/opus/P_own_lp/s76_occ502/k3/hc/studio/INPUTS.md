# K3CHK2 / K3CHK3 hC inputs (written here: main has no INPUTS.md for these jobs)
- main d208ddf0 (Lean hC done: K3C2V.hC_0, K3C3V.hC_0; exit 0, sorry 0). Byte copies from out/job_K3CHK2/ and out/job_K3CHK3/:
  - ../in/extraC_K3CHK2.tsv = job_K3CHK2/extraC.tsv (md5 6eb0ffd8): b9_u655...566_66......5, r14 m10, X I5-I6.
  - ../in/extraC_K3CHK3.tsv = job_K3CHK3/extraC.tsv (md5 1fdedb3b): b9_u.56.56555_.5......., r13 m9, X I0-I5.
  - CK3C2.lean (f469e29b; k3c2Entries, k3c2Entries_ok, k3c2Entries_length), K3C2V00.lean (c961c90a; K3C2V.hC_0).
  - CK3C3.lean (21f11a08; k3c3Entries, k3c3Entries_ok, k3c3Entries_length), K3C3V00.lean (2862bb8d; K3C3V.hC_0).
  Same md5s as the copies in swarm/round6/W13-open-row-kills/round6/K3/from_studio/K3CHK2/ and K3CHK3/; unchanged on origin/main 90e4c5c1.
- Not on main: K3C2VAll / K3C3VAll (`hC_all : Fin 1`). The Studio built only the V00 modules for these one-entry jobs. HK3C2Occ / HK3C3Occ need them.
