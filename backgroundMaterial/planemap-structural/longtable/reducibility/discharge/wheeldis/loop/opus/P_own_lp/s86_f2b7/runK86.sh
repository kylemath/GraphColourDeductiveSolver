# s86 K separation solve with the s86_f2b7 engine (= s85 + flag f2b7) (generic keys: gkeys=<file> gkwin gkleaf; K* enters as key KS, so KS=0 and no EGK).
# usage: [STACK ARGS] WARM=csv FEAS=<sol> KEYS=<gkeys> XF="c6le" bash runK85.sh <maxit> <threads> <tag> [extra]
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s86_f2b7
export FAM=full KS=0; unset EGK; . $Z/env86.sh; Z=$N86
MI=$1; TH=$2; TAG=$3; shift 3; WK=$SD/wr86K_$TAG; mkdir -p $Z/runK_$TAG $WK
[ -n "$FEAS" ] && [ -n "$KEYS" ] || { echo "runK85: FEAS and KEYS required" >&2; exit 2; }
echo "$WARM" > $Z/runK_$TAG/warmlist.txt; cd $E86
echo "$(date -u +%H:%M:%SZ) [s86K-$TAG] start STACK=$STACK ARGS=$(basename $ARGS) FAM=$FAM gkeys $(basename $KEYS) (md5 $(md5sum $KEYS | cut -c1-8)) flags 'gkwin gkleaf $XF' maxit $MI threads $TH feas $FEAS extra: $*" >> $Z/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=$TAG $A $CB warm=$WARM feas=$FEAS xcap=3 xpen=1e-3 lpmax=45 threads=$TH maxit=$MI work=$WK gkeys=$KEYS gkwin gkleaf $XF "$@" > $Z/runK_$TAG/K.log 2>&1
cp sol_$TAG.json rows_$TAG.txt sol_${TAG}_in.json $Z/runK_$TAG/ 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s86K-$TAG] ended: $(grep '^iter' $Z/runK_$TAG/K.log | tail -1 | cut -c1-120)" >> $Z/run.log
