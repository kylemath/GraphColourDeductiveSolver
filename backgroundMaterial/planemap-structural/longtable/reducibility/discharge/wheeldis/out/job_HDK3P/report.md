# job HDK3P: Lean hD for the two q7- k3p D configurations (Studio, 7 Nov)
- **Input:** D_k3p.tsv: the 2 kc lines of k3p_D.out (ring 8): q7-_....556_....56._::::::5 and q7-_....556_....56._::::::5_s5/p6L1=5.
- **Engines** (out/job_JCOV/coverage/k3p/q7_D2_engines.out): kc -C (07e79fae) D=true and dfast18 (07cb1e0b) D=true, both.
- **Lean:** gen_hd f743a82d, MOD HDK3P, PFX hdk3p, batch 1; v4.35.0-rc3, build root ~/studio_lean_builds/rsst118_fb35d2d1/out_hdk3p.
  HDK3P (data), HDK3PV00 (hD_0), HDK3PV01 (hD_1), HDK3PAll (hD_all : Fin 2): **all exit 0, sorry 0**; axioms propext, Classical.choice, Quot.sound
  plus native_decide aux; sorryAx in 0 logs. Module split: module_split.tsv (for occurrence glue).
