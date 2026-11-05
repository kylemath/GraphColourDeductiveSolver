# s77: upperR2 exhaustive (d=7..17 + Karp tail) on a sol json, patched stack, families FAM (base|rrz|full).  usage: [FAM=..] [KT=..] bash upper77.sh <tag> <sol json> [threads] [extra]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/env77.sh
TAG=$1; SOL=$2; TH=${3:-1}; shift 3; WK=$S7/wr77u_$TAG; mkdir -p $WK; cd $N/eng
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=$TH work=$WK "$@" > $N/logs/upper_$TAG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s77U-$TAG] FAM=${FAM:-base} KT=$KT $SOL (md5 $(md5sum < $SOL | cut -c1-32)): $(grep 'UPPER-R2' $N/logs/upper_$TAG.log | tail -1)" >> $N/run.log
[ -z "$KEEPWK" ] && rm -rf $WK
