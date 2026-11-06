# s84_sepaudit: upperR2 at d = 7 only (dmax=7 dtail=7) with the AUDIT COPY of the s78 engine ($S84/eng, bin/jsepf built from src/jsepf_audit.cpp).
#   The work directory is kept ($S84/work/<tag>): it holds the d = 7 query files (hdr_7_m0.txt, win_d7.bin, f2b/q7m/kstar/edge/l3q/bonus files).
#   usage: STACK=s77 FAM=full KS=1 EGK=<keys> ARGS=<args> bash upper84.sh <tag> <sol json> [extra pcheck options]
#   The UPPER-R2 verdict line of such a run is NOT a verdict (d = 8..17 and the Karp tail are skipped on purpose); only the d = 7 line counts.
#   env78.sh is sourced read-only from s78_kstar (it only sets shell variables, including A = the root/args/rpat/exname options, as upper78.sh uses it).
S84=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s84_sepaudit
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar/env78.sh
TAG=$1; SOL=$2; shift 2; WK=$S84/work/$TAG; mkdir -p $WK $S84/logs; cd $S84/eng
export SEPA_ARGVLOG=$S84/logs/argv_$TAG.txt
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=1 work=$WK dmax=7 dtail=7 "$@" > $S84/logs/upper_$TAG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s84U-$TAG] STACK=${STACK:-s75} FAM=${FAM:-full} KS=${KS:-0} EGK=$(basename ${EGK:-none}) ARGS=${ARGS:-default} $SOL (md5 $(md5sum < $SOL | cut -c1-32)) extra: $*: $(grep '^d=7' $S84/logs/upper_$TAG.log | tail -1)" >> $S84/run.log
