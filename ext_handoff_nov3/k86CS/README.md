# ST-17: Mac check of Opus k86CS sol_crep_qC (dfe5b9cd, t = 0.041565) on W13 + all 8 K-3 kills + rules 363dd708

Family = ST-16 family + pat_K3c_D.out (f8c6eb48, D f9_75..65656_5...55...) + pat_K3c_C.cfast (e9ca2a17, C f9_.56.56555_.5....... X={I0-I5}),
both checked by Studio K3CHK3 (main 9abebe3b). Opus: FEASIBLE at 0.041565 (counts D 18134, C 688, RPAT 158, RPATN 2034 distinct).
args_A97F_W13K3c_x_studio.txt (40c73c2e) = k86MS args + pat=.../pat_K3c_D.out + cpat=.../pat_K3c_C.cfast.
args_A97F_W13K3c_noC_x_studio.txt (8044e1da) = same without the cpat (control).

    R=<repo>/ext_handoff_nov3
    cp $R/k86CS/pat_K3c_D.out $R/k86CS/pat_K3c_C.cfast /tmp/swarm-W17/pat/K3/
    cp $R/k86CS/sol_crep_qC.json /tmp/swarm-W17/sol/
    cp $R/k86CS/args_A97F_W13K3c_x_studio.txt $R/k86CS/args_A97F_W13K3c_noC_x_studio.txt /tmp/swarm-W17/
    RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
    F2BRULES=/tmp/swarm-W17/tab/rules_c67fa1d1_plus_A5_twins.json \
    ARGSF=/tmp/swarm-W17/args_A97F_W13K3c_x_studio.txt EXPECT_PAT=18134,688,158 TAG=sol_crep_qC_zW13K3c_A5 \
    bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qC.json 8
    # control (no K3c C): ARGSF=.../args_A97F_W13K3c_noC_x_studio.txt EXPECT_PAT=18134,687,158 TAG=sol_crep_qC_noK3cC_neg
    #   must FAIL at d9 555657658 (Opus: 2 rows, 0.021860)
