#!/bin/bash
# K3l5m / K3gB5m harness smoke: main on sol_k86MS5_in07__K3l5j (dd2fcc97) with 240 and 260 keys
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; J=$W/out/maclane/setup_k5m; B=/tmp/swarm-W17; P=sol_k86MS5_in07__K3l5j
cp $B/args_A97F_W13K3l5m_x_studio.txt $B/args_A97F_W13K3gB5m_x_studio.txt $B/pat/K3/pat_K3l5m_D.out $J/
cd $B; C="RPATN=$B/tab/rpatN3_rotation_justified.txt F2BRULES=$B/tab/rules_A5final_2db75746.json"
run(){ env GK=$B/tab/$1 $C ARGSF=$B/args_A97F_W13$2_x_studio.txt EXPECT_PAT=$3 TAG=${P}_z$2_$4 nice -n 15 bash $B/check.sh $B/sol/$P.json 8 > $J/smoke_$2_$4.out 2>&1; echo "$2 $4 exit $?"; grep -E '^RESULT|senderR2 rows|patterns distinct|exact violated [1-9]' $J/smoke_$2_$4.out | cut -c1-110; }
run cg_keys_r13w16_16fik.txt K3l5m 18146,712,158 k240
run cg_keys_r13w16_16fikp.txt K3l5m 18146,712,158 k260
run cg_keys_r13w16_16fik.txt K3gB5m 18236,781,158 k240
run cg_keys_r13w16_16fikp.txt K3gB5m 18236,781,158 k260
