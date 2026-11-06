# s85 tests: STACK=s77 ARGS=<args> bash wtest.sh <tag> <cmd> <args...>   (env as world85: FAM=full KS=0)
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56
export FAM=full KS=0; . $Z/env85.sh
TG=$1; CM=$2; shift 2; WK=$SD/wr85t_$TG; mkdir -p $WK; cd $E85
nice -n 10 python3 pcheck.py $CM $F $X $A threads=1 work=$WK "$@" > $Z/logs/$TG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s85T-$TG] $CM $*: $(grep -E '^(GKSELFTEST|GKWINTEST|WORLD0|F2B-SELFTEST|UPPER-R2)' $Z/logs/$TG.log | tail -2 | tr '\n' ' ') $(grep -c Traceback $Z/logs/$TG.log) tracebacks" >> $Z/run.log
rm -rf $WK
