# s78 K separation solve (keeppen xpen=1e-3, moving in-point, s75 engine + K*).  usage: [STACK=s75|s77] [FAM=full] [KS=1] [WARM=csv] FEAS=<sol json> bash runK78.sh <maxit> <threads> <tag> [extra pcheck args]
# checkpoints (eng/): rows_<tag>.txt (rows added in THIS run), sol_<tag>_lp.json (LP point), sol_<tag>_in.json / _inNN.json (in-point candidates -> upperR2 with upper78.sh, same STACK/FAM/KS)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar/env78.sh
MI=$1; TH=$2; TAG=$3; shift 3; WK=$SD/wr78_$TAG; mkdir -p $N/runK_$TAG $WK
WARM=${WARM:-$W7POOL,$WX75,$WK75}; [ -n "$FEAS" ] || { echo "runK78: FEAS=<sol json> required" >&2; exit 2; }
echo "$WARM" > $N/runK_$TAG/warmlist.txt; cd $N/eng
echo "$(date -u +%H:%M:%SZ) [s78K-$TAG] start STACK=${STACK:-s75} FAM=${FAM:-full} KS=${KS:-0} EGK=$(basename ${EGK:-none}) KT=$KT maxit $MI threads $TH feas $FEAS extra: $*" >> $N/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=$TAG $A $CB warm=$WARM feas=$FEAS xcap=3 xpen=1e-3 lpmax=45 threads=$TH maxit=$MI work=$WK "$@" > $N/runK_$TAG/K.log 2>&1
cp sol_$TAG.json rows_$TAG.txt sol_${TAG}_in.json $N/runK_$TAG/ 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s78K-$TAG] ended: $(grep '^iter' $N/runK_$TAG/K.log | tail -1 | cut -c1-120)" >> $N/run.log
