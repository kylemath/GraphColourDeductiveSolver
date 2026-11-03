#!/bin/zsh
# f2b041 Studio run: TAG, then env overrides (F2B, F2BHALF, DLIST, F2B_SELFTEST_ONLY ...). Own SEPTAG and own solution copy.
cd "$(dirname $0)/../../../../.."   # wheeldis
TAG=$1; shift
F=loop/studio/opus_check/f2b041; S=$F/keep/tab; R=$F/keep/run
cp $F/in/gc/sol_c_repaired.json $R/sol_$TAG.json
env SEPTAG=f2bS_$TAG L3Q=1 L3TAB=$S/studio_l3qtab_+1.json,$S/studio_l3qtab_-1.json L3Q8=1 L3TAB8=$S/V8/studio_l3qtabV8_+1.json,$S/V8/studio_l3qtabV8_-1.json \
  KILLDIR=$S/kill CKEEP=$F/keep/keep_lean_C.txt RPATN=out/job31/s39o_rpatN3_studio.txt HAT5=1 V6=0 FB=0 XO=0 SKIP_LOWER=1 EXPECT_T=0.041565 EXPECT_PAT=${EXPECT_PAT:-0,0,0} \
  WLP3X_DEF=1 WLP_SEPF=1 DMAXP=17 "$@" nice -n 5 python3 out/job31/st21_check_f2b.py $R/sol_$TAG.json $R/sol_$TAG.json $F/keep/args/args.txt > $R/$TAG.log 2>&1
echo "exit $?" >> $R/$TAG.log
