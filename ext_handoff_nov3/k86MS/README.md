# ST-14b: Mac check of Opus k86MS point sol_crep_qM (t = 0.075004) on family W13 + all 6 K-3 kills

PRIORITY: if ST-14 (sol_crep_qK) is still running, this point matters more; finish or stop ST-14 per the instructions given.
Opus: UPPER-R2 FEASIBLE at 0.075004 [P] (ref/upper_M_crep_qM.log; counts D 18133, C 687, RPAT 158, RPATN 2034 distinct).
Family = ST-14 family (k86KS/args_A97F_W13K3_x_studio.txt, incl. pat_K3_D.out) + pat_K3b_D.out (a0b171e2, 3 D) + pat_K3b_C.cfast
(ff6a66bd, f9_655...566_66......5 C X={I5-I6}); Studio K3CHK2 cfcd6497 checked all four.
args_A97F_W13K3b_x_studio.txt = k86KS args + " pat=/tmp/swarm-W17/pat/K3/pat_K3b_D.out cpat=/tmp/swarm-W17/pat/K3/pat_K3b_C.cfast".

    R=<repo>/ext_handoff_nov3
    mkdir -p /tmp/swarm-W17/pat/K3 && cp $R/k86KS/pat_K3_D.out $R/k86MS/pat_K3b_D.out $R/k86MS/pat_K3b_C.cfast /tmp/swarm-W17/pat/K3/
    cp $R/k86MS/sol_crep_qM.json /tmp/swarm-W17/sol/ ; cp $R/k86MS/args_A97F_W13K3b_x_studio.txt /tmp/swarm-W17/
    # rule file c67fa1d1 already in /tmp/swarm-W17/tab/ from ST-14
    RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
    F2BRULES=/tmp/swarm-W17/tab/rules_studio_keep95p131f_W18strict.json \
    ARGSF=/tmp/swarm-W17/args_A97F_W13K3b_x_studio.txt EXPECT_PAT=18133,687,158 TAG=sol_crep_qM_zW13K3b \
    bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qM.json 8
    # negative control: without pat_K3b_* (ST-14 args, which keep pat_K3_D) must FAIL (Opus: 20 rows, max excess 0.0747 d9 555665666)
    RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
    F2BRULES=/tmp/swarm-W17/tab/rules_studio_keep95p131f_W18strict.json \
    ARGSF=/tmp/swarm-W17/args_A97F_W13K3_x_studio.txt EXPECT_PAT=18130,686,158 TAG=sol_crep_qM_zW13K3_neg \
    bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qM.json 8

Expected p0.log: by kind D 18133, C 687 (the exname filter must drop 0 of the K3b C), RPAT 158; rpatN 2,241 lines. If D or C come out
lower, a pattern file was not read (st21 skips missing files silently): stop and report.
