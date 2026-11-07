# ST-19: Mac check of Opus k86FS sol_rep2_08 (4b8892bd, t = 0.040940235683) on W13 + 8 K-3 kills + rules 2db75746 (A5 FINAL, ST-18 [E2])

Family = ST-17 args (k86CS/args_A97F_W13K3c_x_studio.txt, 40c73c2e; EXPECT_PAT 18134,688,158) with F2BRULES = 2db75746
(ext_handoff_nov3/w18/a5final/rules_c67fa1d1_plus_A5_twins.json; NOTE same file name as 363dd708: copy it under a NEW name) + rpatN 8b90a842 + 151 keys + c6le.
Opus: UPPER-R2 FEASIBLE d7..17 + Karp (ref/upper_F_rep2_08.log). The point has 1,402 links with some six-end in-out < 0: fine under c6le.
Control: sol_rep2_08_tneg.json = the same point with only "t" lowered to 0.040939 (must FAIL, expected at d8).

    R=<repo>/ext_handoff_nov3
    cp $R/w18/a5final/rules_c67fa1d1_plus_A5_twins.json /tmp/swarm-W17/tab/rules_A5final_2db75746.json   # check md5 2db75746
    cp $R/k86FS/sol_rep2_08.json $R/k86FS/sol_rep2_08_tneg.json /tmp/swarm-W17/sol/
    RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt F2BRULES=/tmp/swarm-W17/tab/rules_A5final_2db75746.json \
    ARGSF=/tmp/swarm-W17/args_A97F_W13K3c_x_studio.txt EXPECT_PAT=18134,688,158 TAG=sol_rep2_08_zK3c_A5F \
    bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_rep2_08.json 8
    # control: same env, TAG=sol_rep2_08_tneg_zK3c_A5F, point sol_rep2_08_tneg.json

## ST-22 (Opus calls it ST-20): sol_rep3c_02.json (232318ea, t = 0.040445649101), same family and commands as ST-19 (TAG sol_rep3c_02_zK3c_A5F).
Control sol_rep3c_02_tneg.json: t lowered to 0.04044 only; must FAIL (Opus expects conservation rows, not window rows).

## ST-24: sol_rep2e_082.json (e5b72242, t 0.040254423450) on K3e = K3c + pat_K3d_D (f8_.5665675_.....55., K3CHK4) + pat_K3e_D (f8_...56556_...5.66., K3CHK5)
   ARGSF=/tmp/swarm-W17/args_A97F_W13K3e_x_studio.txt EXPECT_PAT=18136,688,158 TAG=sol_rep2e_082_zK3e_A5F
   control: ARGSF=.../args_A97F_W13K3d_x_studio.txt EXPECT_PAT=18135,688,158 TAG=sol_rep2e_082_zK3d_neg (no K3e D) must FAIL (d8 76756556/56557667 expected)
## ST-25: sol_rep2f_082.json (12e7e3d6, t 0.039811058450) on K3f = K3e + cpat pat_K3f_C (f8_.56656.._...66... X={I2-I3}, K3CHK4/6)
   ARGSF=/tmp/swarm-W17/args_A97F_W13K3f_x_studio.txt EXPECT_PAT=18136,689,158 TAG=sol_rep2f_082_zK3f_A5F
   control: ARGSF=.../args_A97F_W13K3e_x_studio.txt EXPECT_PAT=18136,688,158 TAG=sol_rep2f_082_zK3e_neg (no K3f C) must FAIL (d8 76566575 class expected)
Copy pat_K3d_D.out pat_K3e_D.out pat_K3f_C.cfast to /tmp/swarm-W17/pat/K3/, the args files to /tmp/swarm-W17/, the sols to sol/. Same rules (rules_A5final_2db75746.json), RPATN 8b90a842.
