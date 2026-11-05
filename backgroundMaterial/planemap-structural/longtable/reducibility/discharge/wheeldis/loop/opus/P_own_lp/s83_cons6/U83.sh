# s83: upperR2 with the s83 engine.  usage: [STACK ARGS FAM KS EGK] bash U83.sh <tag> <sol json> "<extra flags>"
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s83_cons6/env83.sh
TG=$1; SOL=$2; XF=$3; WK=$SD/wr83u_$TG; mkdir -p $WK $P/logs; cd $E83
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=1 work=$WK $XF > $P/logs/upper_$TG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s83U-$TG] STACK=$STACK ARGS=$(basename $ARGS) FAM=$FAM KS=$KS EGK=$(basename ${EGK:-none}) $(basename $SOL) (md5 $(md5sum < $SOL | cut -c1-8)) flags '$XF': $(grep '^conservation' $P/logs/upper_$TG.log | tail -1 | cut -c1-260) | $(grep 'UPPER-R2' $P/logs/upper_$TG.log | tail -1)" >> $P/run.log
rm -rf $WK
