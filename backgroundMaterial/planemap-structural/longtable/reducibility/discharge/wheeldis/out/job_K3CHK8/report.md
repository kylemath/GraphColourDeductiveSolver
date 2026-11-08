# K3CHK8 (Studio, 8 Nov): the GL5 binder C kill b7_u.666666_.5...5. X={R0-I0} — PASS
Input: claude/project-thread-phexa1 3a8f9639 ext_handoff_nov3/chk8/kills_AB_0215.tsv (c5000391), 1 entry; its kc line is the one in the relay (cmp clean).

- **Config from the kc line** (our kccheck/ST-32 build_K + iso): r=14 m=9; the kc interior graph with degrees is isomorphic to K of the window
  f7_.666666_.5...5. (Ku: u deg 7, w1..w6 = 6, s1 = s5 = 5; 9 vertices). I0 = u (degree 7: interior I1..I6 + ring R0).
- **Engines** (eng/cfg.out): kc -t 600 -C -x {R0-I0} (07e79fae): classes 199291, reached 138525, adm=yes, leftover 0, C-REDUCIBLE;
  cfast --fixed R0-I0 (de59e72f): reached 138525, bad 60766, C-REDUCIBLE, leftover 0. reached/classes = 138525/199291, as the lead's.
- **Lean admissibility** (gen_ccover3 3c9e7145 EXTRAFILE, lean/gen_raw.lean.txt; built as out/job_HCK3l/lean/CK3L.lean): eqR [(0,0)], eqI [],
  XRData.ok, admissibleX, foldSafeX proved, exit 0, sorry 0 (propext, Quot.sound, Classical.choice + native_decide aux).
- **Rim pin:** I0 has exactly one ring neighbour, R0, so R0's place in I0's rotation is fixed by the configuration. kc rotation of I0
  (rotcheck.kc_rotation): (I3, I2, I1, R0, I6, I5, I4) — R0 sits between I1 and I6, i.e. at the w0 slot of the window ('.' in the name,
  7 in row B) flanked by w1 and w6. X = the spoke u–w0.
- **Occurrence in row B 7/7666666/6567656** (rowcheck8.py = K3CHK occurs(): grow.build2 frame of the row, exact degrees, induced, faces,
  rotation-preserving rotcheck): 2 face-set embeddings, 2 rotation-preserving: I0..I6 -> u, w1..w6, I7, I8 -> s1, s5, and its mirror
  (I1..I6 -> w6..w1, I7, I8 -> s5, s1). Both put R0 on w0 (degree 7 in row B). **Occurs: YES.**
- **Result: PASS.** Lean hC job: out/job_HCK3l (CK3L + K3LV00 + K3LVAll).
