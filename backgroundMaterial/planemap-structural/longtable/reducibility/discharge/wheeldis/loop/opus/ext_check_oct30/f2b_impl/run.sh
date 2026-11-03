#!/bin/bash
# usage: run.sh NAME SOL KILLDIR(tier A dir) MODE(on|off|half) BIN(new|old) XO(0|1) [extra env VAR=val ...]
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
W=$S/mainwt/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; O=$S/ext_f2b
NAME=$1; SOL=$2; KD=$3; MODE=$4; BIN=$5; XO=$6; shift 6
T=$(python3 -I -c "import json,sys; print(repr(json.load(open(sys.argv[1]))['t']))" $SOL)
mkdir -p $O/logs $O/tab_$NAME
cd $W
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
env ST21=$W/out/job31/st21_check.py SEPTAG=f2b_$NAME OUTD=$O/tab_$NAME SKIP_LOWER=1 L3Q=1 L3TAB=$KD/studio_l3qtab_+1.json,$KD/studio_l3qtab_-1.json L3Q8=1 L3TAB8=$KD/studio_l3qtabV8_+1.json,$KD/studio_l3qtabV8_-1.json \
  WLP3X_DEF=1 WLP_SEPF=1 HAT5=1 V6=0 DMAXP=17 CALD=${CALD:-9} FB=0 XO=$XO KILLDIR=$KD RPATN=out/job31/s39o_rpatN3_studio.txt EXPECT_PAT=18159,2257,158 EXPECT_T=$T NVIOL=20 \
  F2B_MODE=$MODE F2B_BIN=$BIN F2B_RULES=$KD/full2ball_extra_rules.json "$@" \
  python3 $O/st21_f2b.py $SOL $W/loop/studio/opus_check/s44A83/cert_q44nfA83L.json $S/ext_studio/args_a100_minus1.txt > $O/logs/$NAME.log 2>&1
echo "EXIT $?" >> $O/logs/$NAME.log
