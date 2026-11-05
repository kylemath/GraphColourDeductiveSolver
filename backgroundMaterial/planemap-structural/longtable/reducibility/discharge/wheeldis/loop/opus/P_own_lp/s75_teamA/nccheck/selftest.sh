# usage: bash selftest.sh <engdir> <tag> <abs sol> <N>
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
E=$1; TAG=$2; SOL=$3; NN=$4; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3"; WK=$SC/P/wrst_$TAG; mkdir -p $WK; cd $E
nice -n 12 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=1 work=$WK f2bself=$NN > $SC/eng_nc/selftest_$TAG.log 2>&1
rm -rf $WK
