#!/bin/bash
# ST-108 T3: the W17 GK self-test (gk_blocks.py, as code_gk8's T5) plus the HATBB self-test (hb_blocks.py HBST: per-edge bound,
# C++ exact leaf 'e' vs Python rows d = 7..12, 18, 26 with planted HATBB slots), code_gk9 + bin/sep3r_gk9, GKST_ONLY=1, on the
# 260 keys of tab/cg_keys_r13w16_16fikp.txt + the 14 HATBB keys (tests/cg_keys_k260p_plus_hatbb.txt), each HATBB key at amount
# 0.01 via KSAMT (the point has no HATBB amounts). Point sol_repK1MW_04__K3l5j_k260 (ST-88 T5's).
# usage: bash t3_selftest.sh LOG TAG [extra env ...]   (controls: HBPLANT_SEP=inflip (C++ only), HBPLANT=outposs (Python only))
B=/tmp/swarm-W17; J=$(cd "$(dirname "$0")/.." && pwd); LOG=$1; TG=$2; shift 2
SOL=$B/sol/sol_repK1MW_04__K3l5j_k260.json; T=$(python3 -I -c "import json,sys; print(repr(json.load(open(sys.argv[1]))['t']))" $SOL)
AMT=$(python3 -I -c "
import sys; sys.path.insert(0, '$B/code_gk9'); import hbfam as H
print(','.join('%s=0.01' % k[0] for k in H.load_keys('$J/in/cg_keys_w6b16x_hatbb.txt')))")
export PATH=$B/macshim:$PATH
env C6LE=1 NOCLAMP=1 F2B7=1 F2BRULES=$B/tab/rules_A5final_2db75746.json RPATN=$B/tab/rpatN3_rotation_justified.txt GK=$J/tests/cg_keys_k260p_plus_hatbb.txt KSAMT=$AMT \
  ARGSF=$B/args_A97F_W13K3l5j_x_studio.txt EXPECT_PAT=18143,710,158 EXNAME=$B/tab/exname_keep95p131f.txt DMAXP=26 \
  SOL=$SOL TAG=$TG KILLDIR=$B/kill/patched298 EXPECT_T=$T GKST_ONLY=1 W10ST=1 W10STN=1000 CALD=6 "$@" \
  W17CODE=$B/code_gk9 SEPBIN=sep3r_gk9 nice -n 20 bash $B/code_gk9/run17.sh > $LOG 2>&1
grep -h "W17 GK\|HATBB\|VERDICT\|sep: W17\|sep: HB\|FAIL\|Traceback\|Error" $LOG | grep -v "W17 GK amounts\|W17 HATBB amounts\|^KSAMT"
