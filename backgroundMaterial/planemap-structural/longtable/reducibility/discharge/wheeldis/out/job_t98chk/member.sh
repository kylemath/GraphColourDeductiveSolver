#!/bin/bash
# usage: member.sh FAMILY EXPECT d LINK SWORD : is the row killed on that W17 family? (env as run17.sh, kill dir patched298)
B=/tmp/swarm-W17; R=$B/wd; S=$R/out/job31/f2bA; W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd $R && env HATRR=1 ZH=1 ZR=1 ZCAP=3 Q7=1 Q7M=1 Q7CAP=3 F2B=$B/tab/rules_A5final_2db75746.json L3Q=1 L3TAB=$S/studio_l3qtab_+1.json,$S/studio_l3qtab_-1.json \
  L3Q8=1 L3TAB8=$S/V8/studio_l3qtabV8_+1.json,$S/V8/studio_l3qtabV8_-1.json KILLDIR=$B/kill/patched298 RPATN=$B/tab/rpatN3_rotation_justified.txt \
  HAT5=1 V6=0 FB=0 XO=0 SKIP_LOWER=1 EXPECT_T=0.014 EXPECT_PAT=$2 WLP3X_DEF=1 WLP_SEPF=1 DMAXP=17 W10_HERE=$R W10_ST16=$B/st16 C6LE=1 NOCLAMP=1 F2B7=1 \
  GK=$B/tab/cg_keys_r13w16_16fik.txt nice -n 10 python3 $W/out/job_t98chk/member.py $B/sol/sol_k86GS20_in03.json $B/args_A97F_W13$1_x_studio.txt $3 $4 $5
