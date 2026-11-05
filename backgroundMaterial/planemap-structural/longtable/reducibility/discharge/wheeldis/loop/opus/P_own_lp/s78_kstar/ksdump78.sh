# s78: K* / EDGE row-value dump (eng/ksdump.py via upperR2 ksdump=) on a seeded sample of receiver rows, for row-by-row comparison.
# usage: [ARGS=..] [STACK=s75|s77] [FAM=full] [KS=1] [EGK=eng/edgekeys_r4.txt] bash ksdump78.sh <sol json> <out .tsv> [seed, default 7900] [extra pcheck opts]
#   (KS defaults to 1 and EGK to eng/edgekeys_r4.txt here; a relative EGK is taken relative to s78_kstar/.)  Log: <out>.log; one line in run.log.
N0=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar
KS=${KS:-1}; EGK=${EGK:-eng/edgekeys_r4.txt}; case $EGK in /*) ;; *) EGK=$N0/$EGK;; esac
. $N0/env78.sh
SOL=$1; OUT=$2; SEED=${3:-7900}; shift $(( $# < 3 ? $# : 3 ))
case $OUT in /*) ;; *) OUT=$PWD/$OUT;; esac
WK=$SD/wr78d_$(basename $OUT .tsv)_$$; mkdir -p $WK $(dirname $OUT); cd $N/eng
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=1 work=$WK ksdump=$OUT seed=$SEED "$@" > ${OUT%.tsv}.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s78D-$(basename $OUT .tsv)] STACK=${STACK:-s75} FAM=${FAM:-full} KS=$KS EGK=$(basename $EGK) ARGS=$(basename ${ARGS:-args_A97.txt}) $SOL (md5 $(md5sum < $SOL | cut -c1-32)) seed $SEED: $(grep 'KSDUMP\|ksdump: [0-9]' ${OUT%.tsv}.log | tr '\n' ' ' | cut -c1-200)" >> $N/run.log
rm -rf $WK
