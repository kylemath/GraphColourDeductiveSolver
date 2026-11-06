# s78: upperR2 exhaustive (d=7..17 + Karp tail) on a sol json with the s78 engine.  usage: [STACK=s75|s77] [FAM=..] [KS=0|1] bash upper78.sh <tag> <sol json> [threads] [extra]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar/env78.sh
TAG=$1; SOL=$2; TH=${3:-1}; shift 3; WK=$SD/wr78u_$TAG; mkdir -p $WK $N/logs; cd $N/eng
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=$TH work=$WK "$@" > $N/logs/upper_$TAG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s78U-$TAG] STACK=${STACK:-s75} FAM=${FAM:-full} KS=${KS:-0} EGK=$(basename ${EGK:-none}) $SOL (md5 $(md5sum < $SOL | cut -c1-32)) extra: $*: $(grep 'UPPER-R2' $N/logs/upper_$TAG.log | tail -1)" >> $N/run.log
[ -z "$KEEPWK" ] && rm -rf $WK
