#!/bin/bash
# ST-88 T5: the W17 GK self-test (gk_blocks.py: numpy window tables vs gkfam.Win, C++ exact leaf 'e' vs Python rows d = 7..12,
# per-position window bound) with code_gk8 + bin/sep3r_gk8, GKST_ONLY=1 (stops after the self-test; no separator search).
#   (a) the 260 keys alone (amounts from the point);  (b) the 260 keys + the 24 payer-8/9 keys (w6b16s, b8bcafba), each new key
#   given amount 0.01 via KSAMT so the self-test exercises it (the point itself has no amounts for them).
# usage: bash t5_selftest.sh OUTDIR
B=/tmp/swarm-W17; J=$(cd "$(dirname "$0")/.." && pwd); O=${1:-$J/tests}
SOL=$B/sol/sol_repK1MW_04__K3l5j_k260.json; T=$(python3 -I -c "import json,sys; print(repr(json.load(open(sys.argv[1]))['t']))" $SOL)
AMT=$(python3 -I -c "
import sys; sys.path.insert(0, '$B/code_gk8'); import gkfam as G
print(','.join('%s=0.01' % k[0] for k in G.load_keys('$J/in/cg_keys_w6b16s_p8_k86GS14.txt')))")
export PATH=$B/macshim:$PATH
run() {   # TAG GKFILE KSAMT
  env C6LE=1 NOCLAMP=1 F2B7=1 F2BRULES=$B/tab/rules_A5final_2db75746.json RPATN=$B/tab/rpatN3_rotation_justified.txt GK=$2 ${3:+KSAMT=$3} \
    ARGSF=$B/args_A97F_W13K3l5j_x_studio.txt EXPECT_PAT=18143,710,158 EXNAME=$B/tab/exname_keep95p131f.txt DMAXP=26 \
    SOL=$SOL TAG=$1 KILLDIR=$B/kill/patched298 EXPECT_T=$T GKST_ONLY=1 W10ST=1 W10STN=1000 CALD=6 W17CODE=$B/code_gk8 SEPBIN=sep3r_gk8 \
    nice -n 20 bash $B/code_gk8/run17.sh
}
run st88_t5a_k260 $B/tab/cg_keys_r13w16_16fikp.txt "" > $O/t5a_k260.log 2>&1
run st88_t5b_k260p8 $J/tests/cg_keys_k260_plus_w6b16s_p8.txt "$AMT" > $O/t5b_k260p8.log 2>&1
grep -h "W17 GK\|VERDICT\|sep: W17 GK\|FAIL" $O/t5a_k260.log $O/t5b_k260p8.log
