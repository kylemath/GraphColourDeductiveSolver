#!/bin/bash
# K3l5n / K3gB5n harness smoke: main on sol_k86MS5_in07__K3l5j (dd2fcc97) with 240 keys
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; J=$W/out/maclane/setup_k5n; B=/tmp/swarm-W17; P=sol_k86MS5_in07__K3l5j
cd $B; C="RPATN=$B/tab/rpatN3_rotation_justified.txt F2BRULES=$B/tab/rules_A5final_2db75746.json"
run(){ env GK=$B/tab/$1 $C ARGSF=$B/args_A97F_W13$2_x_studio.txt EXPECT_PAT=$3 TAG=${P}_z$2_$4 nice -n 15 bash $B/check.sh $B/sol/$P.json 8 > $J/smoke_$2_$4.out 2>&1; echo "$2 $4 exit $?"; grep -E '^RESULT|senderR2 rows|patterns distinct|exact violated [1-9]' $J/smoke_$2_$4.out | cut -c1-110; }
run cg_keys_r13w16_16fik.txt K3l5n 18147,712,158 k240
run cg_keys_r13w16_16fik.txt K3gB5n 18237,781,158 k240
echo SMOKEDONE
