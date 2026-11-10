# s86 p1r: runK86.sh on the engine copy eng_p1r (flag p1r goes in XF).  Identical to ../runK86.sh except that E86 (the engine dir env86.sh
# selects, = s86_f2b7/eng) is overridden to s86_f2b7/eng_p1r after sourcing env86.sh, and the run.log lines name the engine.
# usage: [STACK ARGS] WARM=csv FEAS=<sol> KEYS=<gkeys> XF="c6le ... p1r" bash p1r/runK86p.sh <maxit> <threads> <tag> [extra]
# maclane v2e (Opus 10 Nov): ENG=eng_p8 runs on s86_f2b7/eng_p8 (payer-8/9 keys, PAYER8SPEC W5) instead; unset = eng_p1r as before.
B=/tmp/maclane-k86/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s86_f2b7
export FAM=full KS=0; unset EGK; . $Z/env86.sh; Z=$N86; E86=$N86/${ENG:-eng_p1r}
case "${ENG:-eng_p1r}" in eng_p1r|eng_p8) ;; *) echo "runK86p: ENG must be eng_p1r or eng_p8, not $ENG" >&2; exit 2;; esac
MI=$1; TH=$2; TAG=$3; shift 3; WK=$SD/wr86K_$TAG; mkdir -p $Z/runK_$TAG $WK
[ -n "$FEAS" ] && [ -n "$KEYS" ] || { echo "runK86p: FEAS and KEYS required" >&2; exit 2; }
echo "$WARM" > $Z/runK_$TAG/warmlist.txt; cd $E86
echo "$(date -u +%H:%M:%SZ) [s86K-$TAG] start ENGINE $(basename $E86) STACK=$STACK ARGS=$(basename $ARGS) FAM=$FAM gkeys $(basename $KEYS) (md5 $(md5sum $KEYS | cut -c1-8)) flags 'gkwin gkleaf $XF' maxit $MI threads $TH feas $FEAS extra: $*" >> $Z/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=$TAG $A $CB warm=$WARM feas=$FEAS xcap=3 xpen=1e-3 lpmax=45 threads=$TH maxit=$MI work=$WK gkeys=$KEYS gkwin gkleaf $XF "$@" > $Z/runK_$TAG/K.log 2>&1
cp sol_$TAG.json rows_$TAG.txt sol_${TAG}_in.json $Z/runK_$TAG/ 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s86K-$TAG] ended ($(basename $E86)): $(grep '^iter' $Z/runK_$TAG/K.log | tail -1 | cut -c1-120)" >> $Z/run.log
