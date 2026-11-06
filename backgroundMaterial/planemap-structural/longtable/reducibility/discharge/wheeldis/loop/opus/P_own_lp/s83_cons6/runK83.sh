# s83 K separation solve with the s83 engine (flags in $XF, e.g. c6le).  usage: [STACK ARGS FAM KS EGK] WARM=csv FEAS=<sol> XF="c6le" bash runK83.sh <maxit> <threads> <tag> [extra]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s83_cons6/env83.sh
MI=$1; TH=$2; TAG=$3; shift 3; WK=$SD/wr83K_$TAG; mkdir -p $P/runK_$TAG $WK
[ -n "$FEAS" ] || { echo "runK83: FEAS required" >&2; exit 2; }
echo "$WARM" > $P/runK_$TAG/warmlist.txt; cd $E83
echo "$(date -u +%H:%M:%SZ) [s83K-$TAG] start STACK=$STACK ARGS=$(basename $ARGS) FAM=$FAM KS=$KS EGK=$(basename ${EGK:-none}) flags '$XF' maxit $MI threads $TH feas $FEAS extra: $*" >> $P/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=$TAG $A $CB warm=$WARM feas=$FEAS xcap=3 xpen=1e-3 lpmax=45 threads=$TH maxit=$MI work=$WK $XF "$@" > $P/runK_$TAG/K.log 2>&1
cp sol_$TAG.json rows_$TAG.txt sol_${TAG}_in.json $P/runK_$TAG/ 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s83K-$TAG] ended: $(grep '^iter' $P/runK_$TAG/K.log | tail -1 | cut -c1-120)" >> $P/run.log
