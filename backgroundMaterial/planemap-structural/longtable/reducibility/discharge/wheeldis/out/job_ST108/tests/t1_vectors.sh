#!/bin/bash
# ST-108 T1 / T2: W6b's per-row HATBB coefficient vectors (in/hbrows16x_GS16.json, in/hbrows16x_GS20.json) recomputed by code_gk9
# (st21_w17.py HBVEC stage: hb_pic = the HATBB_SPEC 3 picture on the K3l5j stack's pmask / MASK / MASK8 / f2b extras, hbfam.row_counts).
# usage: bash t1_vectors.sh LOG [HBPLANT] [extra env ...]     (HBPLANT = '' for T1, outposs / nomirror / inmirror for the T2 controls)
B=/tmp/swarm-W17; J=$(cd "$(dirname "$0")/.." && pwd); LOG=$1; PL=${2:-}; shift 2 2>/dev/null
SOL=$B/sol/sol_repK1MW_04__K3l5j_k260.json; T=$(python3 -I -c "import json,sys; print(repr(json.load(open(sys.argv[1]))['t']))" $SOL)
export PATH=$B/macshim:$PATH
env C6LE=1 NOCLAMP=1 F2B7=1 F2BRULES=$B/tab/rules_A5final_2db75746.json RPATN=$B/tab/rpatN3_rotation_justified.txt GK=$J/tests/cg_keys_k260p_plus_hatbb.txt \
  ARGSF=$B/args_A97F_W13K3l5j_x_studio.txt EXPECT_PAT=18143,710,158 EXNAME=$B/tab/exname_keep95p131f.txt DMAXP=26 \
  SOL=$SOL TAG=st108_t1 KILLDIR=$B/kill/patched298 EXPECT_T=$T HBVEC=$J/in/hbrows16x_GS16.json,$J/in/hbrows16x_GS20.json HBPLANT=$PL "$@" \
  W17CODE=$B/code_gk9 SEPBIN=sep3r_gk9 nice -n 20 bash $B/code_gk9/run17.sh > $LOG 2>&1
grep -h "^HBVEC\|VERDICT\|HATBB\|FAIL\|Error\|Traceback" $LOG
