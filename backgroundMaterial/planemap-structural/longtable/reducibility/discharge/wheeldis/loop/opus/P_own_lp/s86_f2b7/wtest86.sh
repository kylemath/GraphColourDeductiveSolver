# s86 tests: STACK=s77 ARGS=<args> bash wtest86.sh <tag> <cmd> <args...>
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export FAM=full KS=0; . $N/env86.sh; N=$N86
TG=$1; CM=$2; shift 2; WK=$SD/wr86t_$TG; mkdir -p $WK; cd $E86
nice -n 10 python3 pcheck.py $CM $F $X $A threads=1 work=$WK "$@" > $N/logs/$TG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s86T-$TG] $CM $*: $(grep -E '^(GKSELFTEST|F2B-SELFTEST|UPPER-R2|LOWER-R2)' $N/logs/$TG.log | tail -2 | tr '\n' ' ') $(grep -c Traceback $N/logs/$TG.log) tracebacks" >> $N/run.log
rm -rf $WK
