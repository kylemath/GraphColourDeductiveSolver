# s80: upperR2 exhaustive (d=7..17 + Karp tail) on a sol json (= upper77.sh with ENG / F2BX).  usage: [ENG=..] [FAM=..] [F2BX=..] [ARGS=..] bash upper80.sh <tag> <sol json> [threads] [extra]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s80_k6A/env80.sh
TAG=$1; SOL=$2; TH=${3:-1}; shift 3; WK=$S8/wr80u_$TAG; mkdir -p $WK; cd $ENG
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=$TH work=$WK "$@" > $N/logs/upper_$TAG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s80U-$TAG] ENG=$ENG FAM=${FAM:-base} F2BX=${F2BX:-none} ARGS=${ARGS:-args_A97_F} KT=$KT $SOL (md5 $(md5sum < $SOL | cut -c1-32)): $(grep 'UPPER-R2' $N/logs/upper_$TAG.log | tail -1)" >> $N/run.log
[ -z "$KEEPWK" ] && rm -rf $WK
