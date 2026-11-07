# JCOV coverage extension (Studio, 7 Nov) — evidence files for the 2b362955 single-justifier stack
Our own files and engines only.

## (1) nl51: the 2,438 names of nl51_needed_for_final.txt (fc1086e5, 17b5f98c)
- nl51_needed_evidence.tsv: one row per name: ring | kc verdict + source | dfast verdict (engine) + source | round-54d verdict.
- **Every one of the 2,438 has a per-config kc record and a dfast/dfast18 record, all D (0 missing; nl51_needed_missing.txt is empty).**
  - Sources: explore round 54d (6368d2f5: loop/k5x/*_kcc.out kc, *_df.out = drive45 dfast for ring <= 16, dfast18 above) and Studio job54d / job54e
    (8fd249f6: A_kcc.out = kc -C -s 60 -t 600, A_df.out = dfast18 07cb1e0b).
  - 251 names have a Studio dfast18 record; 2,187 have explore's dfast (ring 8..15). For a uniform dfast18 record, those 2,187 were rerun on
    dfast18 (07cb1e0b) at nice 20: df18/dfast18_2187.out, ALL 2,187 D=true (last column of nl51_needed_evidence.tsv). Every one of the 2,438 now has a kc D and a dfast18 D record.
## (2) k3x D
- k3x1516/k3x_D_A100.out: the registry (copy of tierA/k3x_D_A100.out).
- The k3x D justifiers at ring 15–16 (19 names, k3x1516/names.txt) had no kc record in our files; **kc -C -s 60 -t 600 (07e79fae) rerun: 19 / 19 D=true** (kc_ring15_16.out).
## (3) k3p and the three q7 configurations: k3p/README.md
## (4) Lean membership: lean_membership.tsv (name | list | module.theorem (file)); summary lean_membership_summary.txt
- CK108: {'hC': 108}
- CR118 (rsst118): {'hC': 118}
- keep_lean_C (531): {'hC': 492, 'CWheels': 18, 'no hC': 21}
- RSST DCheckData: 633 configurations, 633 covered by an agreesRSST theorem (agreesRSST proves D only for contract-0 entries)
- The 21 keep_lean_C names without hC are k63f (18) and k63o (3): K63F/K63O prove only XRData.ok / admissibleX / foldSafeX. HCK63 (next job) builds their hC.
- The JCOV main table out/job_JCOV/justifier_coverage.tsv already counts them (and the 2 cited ones) as engine-only, not Lean.
