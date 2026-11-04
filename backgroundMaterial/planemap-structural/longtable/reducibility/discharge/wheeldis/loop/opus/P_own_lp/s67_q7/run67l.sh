# usage: bash run67l.sh <tag> <cert> [flags]  -- lowerR2 in the s62 stack (RULES gcoct26 full2ball, exname_rm128) with the s67 engine copy
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s62_w5check/env62.sh
E=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s67_q7/eng; Y=$(dirname $E)
tag=$1; cert=$2; shift 2; F="$FUP f2b=$RULES"; mkdir -p $Y/work_$tag; cd $E
python3 pcheck.py lowerR2 $F $X cert=$cert xcap=3 $A work=$Y/work_$tag "$@" > $Y/logs/lower_$tag.log 2>&1
