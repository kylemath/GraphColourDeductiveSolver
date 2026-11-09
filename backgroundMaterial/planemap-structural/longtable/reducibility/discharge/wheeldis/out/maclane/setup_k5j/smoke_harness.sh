#!/bin/bash
# K3l5j harness smoke: main on sol_k86MS4_in03__K3l5i (1faae9ad) on K3l5j + 240 keys, 4 procs, nice 15, ST-67 undisturbed
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; J=$W/out/maclane/setup_k5j
cp /tmp/swarm-W17/args_A97F_W13K3l5j_x_studio.txt /tmp/swarm-W17/pat/K3/pat_K3l5j_C.cfast $J/
cd /tmp/swarm-W17; P=sol_k86MS4_in03__K3l5i
GK=/tmp/swarm-W17/tab/cg_keys_r13w16_16fik.txt RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt F2BRULES=/tmp/swarm-W17/tab/rules_A5final_2db75746.json ARGSF=/tmp/swarm-W17/args_A97F_W13K3l5j_x_studio.txt EXPECT_PAT=18143,710,158 TAG=${P}_zK3l5j_k240 nice -n 15 bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/$P.json 4 > $J/smoke_harness_main.out 2>&1
echo "check exit $?"; grep -E '^RESULT|senderR2 rows|patterns distinct|exact violated [1-9]' $J/smoke_harness_main.out | cut -c1-160
