#!/bin/bash
# 260-key smoke: main on sol_k86MS5_in05__K3l5j (83675016) with cg_keys_r13w16_16fikp.txt (0470c459) on K3l5j and on K3gB5k
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; J=$W/out/maclane/setup_260; P=sol_k86MS5_in05__K3l5j; B=/tmp/swarm-W17
cd $B; K=$B/tab/cg_keys_r13w16_16fikp.txt; C="RPATN=$B/tab/rpatN3_rotation_justified.txt F2BRULES=$B/tab/rules_A5final_2db75746.json"
env GK=$K $C ARGSF=$B/args_A97F_W13K3l5j_x_studio.txt EXPECT_PAT=18143,710,158 TAG=${P}_zK3l5j_k260 nice -n 15 bash $B/check.sh $B/sol/$P.json 8 > $J/smoke_K3l5j_k260.out 2>&1; echo "K3l5j exit $?"
env GK=$K $C ARGSF=$B/args_A97F_W13K3gB5k_x_studio.txt EXPECT_PAT=18233,780,158 TAG=${P}_zK3gB5k_k260 nice -n 15 bash $B/check.sh $B/sol/$P.json 8 > $J/smoke_K3gB5k_k260.out 2>&1; echo "K3gB5k exit $?"
cd $J; for f in smoke_K3l5j_k260.out smoke_K3gB5k_k260.out; do echo "== $f"; grep -E '^RESULT|senderR2 rows|patterns distinct|exact violated [1-9]|^FAIL|nonzero amounts|gkeys|keys' $f | cut -c1-160 | head -8; done
