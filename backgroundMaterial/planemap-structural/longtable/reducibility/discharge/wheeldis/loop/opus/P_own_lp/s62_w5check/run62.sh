# usage: bash run62.sh <tag> <cert> [extra flags]   -- lowerR2 exactly as run60.sh, engine copy s62_w5check/eng
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s62_w5check/env62.sh
tag=$1; cert=$2; shift 2; F="$FUP f2b=$RULES"; mkdir -p $Y/work_$tag; cd $E
python3 pcheck.py lowerR2 $F $X cert=$cert xcap=3 $A work=$Y/work_$tag "$@" > $Y/logs/lower_$tag.log 2>&1
