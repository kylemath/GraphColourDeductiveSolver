# s80 Team E: K separation solve on the s80 stack (copy of s77_k6patch/runK77.sh; engine ENG, default $N/eng = s77 eng + f2bx).
# usage: [ENG=..] [FAM=..] [KT=..] [ARGS=..] [F2BX=rules.json] [WARM=csv] FEAS=<sol json> bash runK80.sh <maxit> <threads> <tag> [extra pcheck args]
# checkpoints (in $ENG): rows_<tag>.txt, sol_<tag>_lp.json, sol_<tag>_in.json / _inNN.json; log + copies in $N/runK_<tag>/
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s80_k6A/env80.sh
MI=$1; TH=$2; TAG=$3; shift 3; WK=$S8/wr80_$TAG; mkdir -p $N/runK_$TAG $WK; cp $SC/P/wr70/clsR2_1zfh.bin $WK/ 2>/dev/null
[ -n "$WARM" ] || { echo "runK80: set WARM (csv of row files)"; exit 2; }; [ -n "$FEAS" ] || { echo "runK80: set FEAS"; exit 2; }
echo "$WARM" > $N/runK_$TAG/warmlist.txt; cd $ENG
echo "$(date -u +%H:%M:%SZ) [s80K-$TAG] start ENG=$ENG FAM=${FAM:-base} KT=$KT F2BX=${F2BX:-none} ARGS=${ARGS:-$N/args/args_A97_F.txt} maxit $MI threads $TH feas $FEAS extra: $*" >> $N/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=$TAG $A $CB warm=$WARM feas=$FEAS xcap=3 xpen=1e-3 lpmax=45 threads=$TH maxit=$MI work=$WK "$@" > $N/runK_$TAG/K.log 2>&1
cp sol_$TAG.json rows_$TAG.txt sol_${TAG}_in*.json sol_${TAG}_lp.json $N/runK_$TAG/ 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s80K-$TAG] ended: $(grep '^iter' $N/runK_$TAG/K.log | tail -1 | cut -c1-120)" >> $N/run.log
