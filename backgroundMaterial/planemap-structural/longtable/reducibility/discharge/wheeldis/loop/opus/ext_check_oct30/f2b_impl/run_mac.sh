#!/bin/bash
# Mac Studio runner for the remaining degrees.  Prerequisites (adjust the four paths below):
#   REPO   = the Studio worktree (contains backgroundMaterial/.../wheeldis with bin/sep3r_l3q etc. built, out/job31/st21_check.py)
#   F2B    = a copy of this folder ext_f2b  (f2b.py, st21_f2b.py, f2b_selftest.py, sep3r_f2b.cpp, run.sh)
#   GC     = the outside team's gcoct26 folder (kill_upgraded/tierA/*, the two sol_*.json)
#   ARGS   = args_a100_minus1.txt (the A100-minus-1 pattern set; in ext_studio)
# build once:  c++ -O2 -std=c++17 -o $F2B/sep3r_f2b $F2B/sep3r_f2b.cpp
# usage: run_mac.sh c|xo1 DSTART DSTOP     e.g.  run_mac.sh c 8 9   or   run_mac.sh c 10 17   (the last call also does DP 18..30 and Karp only if DSTOP>=17)
# Each call is one process (about 1 core).  Run c and xo1 in parallel (2 processes), or split degrees.
REPO=${REPO:?set REPO to .../discharge/wheeldis}; F2B=${F2B:?}; GC=${GC:?}; ARGS=${ARGS:?}
WHICH=$1; DS=$2; DE=$3
K=$GC/kill_upgraded/tierA
if [ "$WHICH" = c ]; then SOL=$GC/sol_c_repaired.json; XO=0; else SOL=$GC/sol_unified_a100_tierA_full2ball_xo1_buffered.json; XO=1; fi
T=$(python3 -I -c "import json,sys; print(repr(json.load(open(sys.argv[1]))['t']))" $SOL)
mkdir -p $F2B/logs $F2B/tab_${WHICH}_$DS
cd $REPO
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
EXTRA=""; if [ "$DE" != 17 ]; then EXTRA="DSTOP=$DE"; fi
env ST21=$REPO/out/job31/st21_check.py SEPTAG=f2b_${WHICH}_$DS OUTD=$F2B/tab_${WHICH}_$DS SKIP_LOWER=1 L3Q=1 L3TAB=$K/studio_l3qtab_+1.json,$K/studio_l3qtab_-1.json L3Q8=1 L3TAB8=$K/studio_l3qtabV8_+1.json,$K/studio_l3qtabV8_-1.json \
  WLP3X_DEF=1 WLP_SEPF=1 HAT5=1 V6=0 DMAXP=17 CALD=6 FB=0 XO=$XO KILLDIR=$K RPATN=out/job31/s39o_rpatN3_studio.txt EXPECT_PAT=18159,2257,158 EXPECT_T=$T NVIOL=20 \
  F2B_MODE=on F2B_BIN=new F2B_RULES=$K/full2ball_extra_rules.json DSTART=$DS $EXTRA \
  python3 $F2B/st21_f2b.py $SOL $REPO/loop/studio/opus_check/s44A83/cert_q44nfA83L.json $ARGS > $F2B/logs/mac_${WHICH}_d${DS}-${DE}.log 2>&1
echo "EXIT $?" >> $F2B/logs/mac_${WHICH}_d${DS}-${DE}.log
