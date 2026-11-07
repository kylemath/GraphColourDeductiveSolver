# job HDK3P: Lean hD for the two q7- k3p D configurations (Studio, 7 Nov)
- **Input:** D_k3p.tsv: the 2 kc lines of k3p_D.out (ring 8): q7-_....556_....56._::::::5 and q7-_....556_....56._::::::5_s5/p6L1=5.
- **Engines** (out/job_JCOV/coverage/k3p/q7_D2_engines.out): kc -C (07e79fae) D=true and dfast18 (07cb1e0b) D=true, both.
- **Lean:** gen_hd f743a82d, MOD HDK3P, PFX hdk3p, batch 1; v4.35.0-rc3, build root ~/studio_lean_builds/rsst118_fb35d2d1/out_hdk3p.
  HDK3P (data), HDK3PV00 (hD_0), HDK3PV01 (hD_1), HDK3PAll (hD_all : Fin 2): **all exit 0, sorry 0**; axioms propext, Classical.choice, Quot.sound
  plus native_decide aux; sorryAx in 0 logs. Module split: module_split.tsv (for occurrence glue).

## Occurrence glue (Opus --hd, 605314cb s76_occ502/hdk3p/lean; HDK3POcc md5 9836aab5)
- Copied byte-identically into in/glue/ and lean/ (cmp clean); COccBridge byte-copied from job_HDB3.
- check_literals (D variant, OCC502 scripts) on HDK3P.lean vs in/glue HK3P_: **2 entries, 0 mismatches**.
- HK3P_00/01, COccHK3P_00/01, HDK3POcc (after HDK3PAll): **all exit 0, sorry 0**; HDK3POcc axioms propext, Classical.choice, Quot.sound + native_decide aux; sorryAx in 0 logs.
