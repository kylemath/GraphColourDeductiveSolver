# ST-14: Mac check of Opus k86KS point sol_crep_qK (t = 0.116271) on family W13 + K3

Opus (7 Nov 03:38Z, ref/README.md): UPPER-R2 FEASIBLE at t = 0.116271 [P] on
W13 args + f2b7 rules c67fa1d1 (W18strict, ST-12 two-engine file) + 151 keys + c6le + RPATN 8b90a842
+ the two K-3 D kills (pat_K3_D.out e72617ed: f8_.56.5656_56...55., f9_...575655_...5..65.; Studio K3CHK a6c989e5).

Files: sol_crep_qK.json 0f03f805; pat_K3_D.out e72617ed;
args_A97F_W13K3_x_studio.txt 6d83770d = macpack args_A97F_W13_x_studio.txt (bfca4bc4) + " pat=/tmp/swarm-W17/pat/K3/pat_K3_D.out".
Rule file: ext_handoff_nov3/w18/rules_studio_keep95p131f_W18strict.json (c67fa1d1).

Uses the existing /tmp/swarm-W17 (macpack 8acb1a22 + rpatN add-on v2 f6dc32d3, as in ST-11). If /tmp/swarm-W17 is gone,
re-unpack ext_handoff_nov3/w17macpack/w17_macpack.tar.gz then macpack_addon_rpatN_v2.tar.gz, build.sh, smoke.sh.

    R=<repo>/ext_handoff_nov3
    mkdir -p /tmp/swarm-W17/pat/K3 && cp $R/k86KS/pat_K3_D.out /tmp/swarm-W17/pat/K3/
    cp $R/k86KS/sol_crep_qK.json /tmp/swarm-W17/sol/
    cp $R/k86KS/args_A97F_W13K3_x_studio.txt /tmp/swarm-W17/
    cp $R/w18/rules_studio_keep95p131f_W18strict.json /tmp/swarm-W17/tab/      # md5 c67fa1d1
    # main check (TAG sol_crep_qK_zW13K3):
    RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
    F2BRULES=/tmp/swarm-W17/tab/rules_studio_keep95p131f_W18strict.json \
    ARGSF=/tmp/swarm-W17/args_A97F_W13K3_x_studio.txt EXPECT_PAT=18130,686,158 TAG=sol_crep_qK_zW13K3 \
    bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qK.json 8
    # negative control (must FAIL: crep has 150 rows of d=8 56568567 that only the K3 kills remove):
    RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
    F2BRULES=/tmp/swarm-W17/tab/rules_studio_keep95p131f_W18strict.json \
    TAG=sol_crep_qK_zW13_neg bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_crep_qK.json 8

Expected p0.log: patterns by kind D 18130 (W13 18128 + 2), C 686, RPAT 158; rpatN 2,241 lines (8b90a842);
F2B rules from c67fa1d1; GK 151 keys fe8a97a7. If the pattern line shows D 18128, pat_K3_D.out was not read (st21 skips a
missing pattern file silently): stop and report. Verdict = RESULT: line of logs/<TAG>/summary.txt. If TAG is not honoured
by check.sh, use its default tag and say which. Report both verdicts, d at which the control fails, and the p0 lines.
