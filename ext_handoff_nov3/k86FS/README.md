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
