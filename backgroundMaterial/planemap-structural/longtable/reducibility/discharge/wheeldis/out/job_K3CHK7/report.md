# K3CHK7 (ST-26): bulk reducibility of all 174 K-3 / K-4 hits (Studio, 7 Nov)
Input: 5a390b30 ext_handoff_nov3/k3/chk7/all_K3_K4_hits_kc.tsv (e9fb030d): 174 configs (98 D, 76 C) with kc lines. Table: per_config.tsv.
- **Parse:** every kc line's name, ring and m equal the listed config (174 / 174).
- **D (98):** kc -C -s 60 -t 600 (07e79fae) D + dfast18 (07cb1e0b) D — **98 / 98 PASS** (90 run here, 8 reused: identical name + kc line already run on the same
  engines in the Mac K-3 pack out/job_K3 or K3CHK..K3CHK5; listed in per_config.tsv "reused:").
- **C (76):** kc -t 600 -C -x X: adm=yes, leftover 0; cfast --fixed X (de59e72f): C-REDUCIBLE, leftover 0 — **76 / 76 PASS** (72 run here, 4 reused from K3CHK2..K3CHK5
  with identical kc line and X). **Lean admissibility** (lean/CK3C7.lean, gen_ccover3 XRData for all 76 with their X): XRData.ok, admissibleX, foldSafeX proved (exit 0, sorry 0).
  **Rim-pinned: 4** (per_config.tsv column 9); the other 72 interior-only.
- **Result: 174 / 174 PASS.** Lean hD/hC waits for a later request.
