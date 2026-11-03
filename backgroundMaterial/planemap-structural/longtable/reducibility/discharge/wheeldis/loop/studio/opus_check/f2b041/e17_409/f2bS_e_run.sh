#!/bin/zsh
# f2b041 Studio run: TAG, then env overrides (F2B, F2BHALF, DLIST, F2B_SELFTEST_ONLY ...). Own SEPTAG and own solution copy.
cd "$(dirname $0)/../../../../.."   # wheeldis
TAG=$1; SRC=$2; shift 2
F=loop/studio/opus_check/f2b041; S=out/job31/f2bA; R=$F/e17_409/run
cp $SRC $R/sol_$TAG.json
env SEPTAG=f2bS_$TAG L3Q=1 L3TAB=$S/studio_l3qtab_+1.json,$S/studio_l3qtab_-1.json L3Q8=1 L3TAB8=$S/V8/studio_l3qtabV8_+1.json,$S/V8/studio_l3qtabV8_-1.json \
  KILLDIR=$S/kill RPATN=out/job31/s39o_rpatN3_studio.txt HAT5=1 V6=0 FB=0 XO=0 SKIP_LOWER=1 EXPECT_T=17/409 EXPECT_PAT=18159,2257,158 \
  WLP3X_DEF=1 WLP_SEPF=1 DMAXP=17 "$@" nice -n 5 python3 out/job31/st21_check_f2b.py $R/sol_$TAG.json $R/sol_$TAG.json $F/tierA/args_f2b_local_strict.txt > $R/$TAG.log 2>&1
echo "exit $?" >> $R/$TAG.log
