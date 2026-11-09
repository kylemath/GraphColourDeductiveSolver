#!/bin/bash
# K3l5l harness smoke: main on sol_k86MS5_in07__K3l5j (dd2fcc97) on K3l5l and K3gB5l + 240 keys
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; J=$W/out/maclane/setup_k5l; B=/tmp/swarm-W17; P=sol_k86MS5_in07__K3l5j
cp $B/args_A97F_W13K3l5l_x_studio.txt $B/args_A97F_W13K3gB5l_x_studio.txt $B/pat/K3/pat_K3l5l1_D.out $B/pat/K3/pat_K3l5l2_C.cfast $B/pat/K3/pat_K3l5l_D.out $J/
cd $B; C="GK=$B/tab/cg_keys_r13w16_16fik.txt RPATN=$B/tab/rpatN3_rotation_justified.txt F2BRULES=$B/tab/rules_A5final_2db75746.json"
env $C ARGSF=$B/args_A97F_W13K3l5l_x_studio.txt EXPECT_PAT=18145,712,158 TAG=${P}_zK3l5l_k240 nice -n 15 bash $B/check.sh $B/sol/$P.json 8 > $J/smoke_K3l5l.out 2>&1; echo "K3l5l exit $?"
env $C ARGSF=$B/args_A97F_W13K3gB5l_x_studio.txt EXPECT_PAT=18235,781,158 TAG=${P}_zK3gB5l_k240 nice -n 15 bash $B/check.sh $B/sol/$P.json 8 > $J/smoke_K3gB5l.out 2>&1; echo "K3gB5l exit $?"
cd $J; for f in smoke_K3l5l.out smoke_K3gB5l.out; do echo "== $f"; grep -E '^RESULT|senderR2 rows|patterns distinct|exact violated [1-9]|^FAIL|EXPECT|mismatch' $f | cut -c1-140 | head -6; done
