#!/bin/bash
# ST-81 step 2: W17 main of sol_k86GS12_in01 (1b80964d) on K3l5k + 260 keys
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; J=$W/out/job_ST81; B=/tmp/swarm-W17; P=sol_k86GS12_in01
cd $B; env GK=$B/tab/cg_keys_r13w16_16fikp.txt RPATN=$B/tab/rpatN3_rotation_justified.txt F2BRULES=$B/tab/rules_A5final_2db75746.json ARGSF=$B/args_A97F_W13K3l5k_x_studio.txt EXPECT_PAT=18143,711,158 TAG=${P}_zK3l5k_k260 nice -n 15 bash $B/check.sh $B/sol/$P.json 8 > $J/main_K3l5k_k260.out 2>&1; echo "exit $?"
grep -E '^RESULT|senderR2 rows|^  (five|nofive)|cons2 6-balance|patterns distinct|DP margin|Karp|exact violated [1-9]' $J/main_K3l5k_k260.out | cut -c1-140; grep -o "nonzero amounts [0-9]* (sum [0-9.e-]*" $J/main_K3l5k_k260.out | head -1; cat $B/logs/${P}_zK3l5k_k260/viol_d*.txt 2>/dev/null | grep -v '^#' | sort -u | head -12
