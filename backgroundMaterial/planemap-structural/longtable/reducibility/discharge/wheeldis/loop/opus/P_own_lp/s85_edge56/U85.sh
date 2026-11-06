# s85 upperR2 exhaustive (d = 7..DMAX + Karp tail) with the generic keys.  usage: [STACK ARGS] KEYS=<gkeys> bash U85.sh <tag> <sol> <threads> [extra]
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56
export FAM=full KS=0; unset EGK; . $Z/env85.sh
TAG=$1; SOL=$2; TH=${3:-1}; shift 3; WK=$SD/wr85u_$TAG; mkdir -p $WK $Z/logs; cd $E85
nice -n 12 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=$TH work=$WK gkeys=$KEYS gkwin gkleaf "$@" > $Z/logs/upper_$TAG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s85U-$TAG] STACK=$STACK ARGS=$(basename $ARGS) gkeys $(basename $KEYS) $SOL (md5 $(md5sum < $SOL | cut -c1-8)) extra: $*: $(grep 'UPPER-R2' $Z/logs/upper_$TAG.log | tail -1) $(grep -c Traceback $Z/logs/upper_$TAG.log) tracebacks" >> $Z/run.log
rm -rf $WK
