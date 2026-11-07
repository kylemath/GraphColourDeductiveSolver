# JCOV extension (3): k3p files and the three q7 configurations (Studio, 7 Nov)
Files: k3p_D.out and k3p_C_keep95p131f.cfast (copies of loop/studio/opus_check/f2b041/tierA/k3p_D.out and keep95p131f/k3p_C_keep95p131f.cfast).
Kc lines: q7_D2.kc (the two q7- D configurations, from k3p_D.out) and q7u.kc (q7u, from nl51-format registry).

| configuration | kind | registry | Lean | engines rerun here (6/7 Nov, Studio binaries) |
|---|---|---|---|---|
| q7-_....556_....56._::::::5 | D (r=8, m=6) | k3p_D.out "D=true (two engines)" | **no hD** | kc -C (07e79fae): D=true; dfast18 (07cb1e0b): D=true (q7_D2_engines.out) |
| q7-_....556_....56._::::::5_s5/p6L1=5 | D (r=8, m=7) | k3p_D.out "D=true (two engines)" | **no hD** | kc -C: D=true; dfast18: D=true |
| q7u_.556676_.5...6._::::::5 | C (r=14, m=10, X={I0-I2}) | keep95p131f_C (k3x13 cover) | **hC: K108V.hC_5 (K108V00.lean), K108V.hC_all** (CK108) | kc -C: C-REDUCIBLE X={I0-I2}; cfast --fixed I0-I2 (de59e72f): see q7u_engines.out |

Neither q7- D has a Lean hD; they are ring 8 and can be added to a gen_hd batch in minutes if wanted.
