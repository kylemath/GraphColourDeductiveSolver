# M_deleted_rows: independent check of Studio's 163 option-F sender-row deletions (bd8472d9, out/job30f)

Script mcheck.py (own 2-ball model built from oriented faces, own matcher; reuses only wlp.py's senders/isR5/isR6),
output mcheck.out. Matcher: exact degrees, induced, interior triangles onto faces, rotation-faithful at every interior
vertex (K's rotation from its unique planar embedding with ring + hub; model rotations, full for v/a_k, known arcs for
t_k/q; ring-gap positions must match with one offset) under one global mirror; never onto a 9. All embeddings of each K
with free t/q slots are collected; every filling of the union of their slots (plus the q/t slots of touched 5-/6-wheels)
over 5..9 is enumerated.

- Row enumeration (own, tcount logic): 19,626 rows; all 163 deleted rows are among them.
- **163/163 deletions confirmed, by K alone** (no filling escapes; R5/R6 impossibility never needed).
  Every one is killed by k42_rsst025_xxxxxxx5 (ring 9, interior 5: degrees 6,5,5,5,7).
- Symmetry closure: image of each deleted row under every dihedral map fixing its word (reflection with
  z_a<->z_e/side swap, and rotations) is also deleted: 0 failures.
- Rotation check: for the 10 configurations with 2-connected interiors it never rejected an embedding that passed
  degrees+induced+triangles (9,302 wildcard embeddings on 3,000 rows), consistent with C1; on rsst062 (excluded) it does
  reject, as expected.
- Completeness: random 200 kept rows (seed 1): 0 should have been deleted. A full run over all 19,463 kept rows was
  started (full.py) but stopped at its 30-min limit (rows with ~9 free slots are slow); not completed.
