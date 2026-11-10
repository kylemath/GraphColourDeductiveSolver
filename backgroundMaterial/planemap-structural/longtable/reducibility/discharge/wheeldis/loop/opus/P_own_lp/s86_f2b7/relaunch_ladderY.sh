#!/bin/bash
# s86 (9 Nov 09:50Z): relaunch_ladderX.sh with KEYS from env LKEYS (default the 240-key file). Was: relaunch the GS9 repair ladder.  usage: bash relaunch_ladderX.sh <in-point.json> <check args> <sub-check args> [FAMSUFFIX]
# Needs E86OVR=eng_p1r (240 keys have 89 payer-7 keys > 64 jsepf limit) and STACK=s77 in the ladder's env.
# REPL_SKIPCUR: ANY non-empty value (even 0) skips the current LP point; REPL_INIT feeds it once instead.
N=$(cd $(dirname $0) && pwd); KEYS=${LKEYS:-$N/p1r/cg_keys_r13w16_16fik.txt}
cd $N && E86OVR=$N/eng_p1r STACK=s77 REPL_ENGD=eng_p1r REPL_FAM=${4:-X} REPL_SKIPCUR=1 REPL_ARGS=$2 REPL_ARGS2=$3 REPL_KEYS=$KEYS REPL_PAR=1 REPL_MINMEM=4500 REPL_INIT=${REPL_INIT-$N/eng_p1r/sol_${TAG:-k86GS9}_lp.json} nohup python3 $N/repladder_e.py ${TAG:-k86GS9} $1 60 >> $N/logs/repladder_${TAG:-k86GS9}${4:-X}.out 2>&1 &
