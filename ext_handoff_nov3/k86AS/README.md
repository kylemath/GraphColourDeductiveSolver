# ST-16: Mac check of Opus k86AS sol_crep_qA (ae4a873a, t = 0.063430) on W13 + 6 K-3 kills + rule file 363dd708 (ST-15 [E2])

Family = ST-14b args (k86MS/args_A97F_W13K3b_x_studio.txt, b2f01470; pattern files already in /tmp/swarm-W17/pat/K3/) + rules
rules_c67fa1d1_plus_A5_twins.json (363dd708, ext_handoff_nov3/w18/a5/) + rpatN 8b90a842 + 151 keys + c6le.

    R=<repo>/ext_handoff_nov3
    cp $R/k86AS/sol_crep_qA.json /tmp/swarm-W17/sol/
    cp $R/w18/a5/rules_c67fa1d1_plus_A5_twins.json /tmp/swarm-W17/tab/        # md5 363dd708
    RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
    F2BRULES=/tmp/swarm-W17/tab/rules_c67fa1d1_plus_A5_twins.json \
    ARGSF=/tmp/swarm-W17/args_A97F_W13K3b_x_studio.txt EXPECT_PAT=18133,687,158 TAG=sol_crep_qA_zW13K3b_A5 \
    bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qA.json 8
    # control A (rules): same but F2BRULES=.../rules_studio_keep95p131f_W18strict.json (c67fa1d1), TAG=sol_crep_qA_zW13K3b_c67neg: must FAIL
    #   (crep at 0.041565 has 163 violated rows on c67fa1d1, incl. d7 5569757; at 0.06343 d9 555665666-type rows exceed too)
    # control B (kills): 363dd708 but ARGSF=/tmp/swarm-W17/args_A97F_W13K3_x_studio.txt EXPECT_PAT=18130,686,158, TAG=sol_crep_qA_zW13K3_A5neg: must FAIL

Expected p0: D 18133, C 687, RPAT 158; rpatN 2,241; F2B rules from rules_c67fa1d1_plus_A5_twins.json.
Opus: UPPER-R2 FEASIBLE at 0.063430 [P] (ref/upper_A_crep_qA.log); next binder d9 555657658.
