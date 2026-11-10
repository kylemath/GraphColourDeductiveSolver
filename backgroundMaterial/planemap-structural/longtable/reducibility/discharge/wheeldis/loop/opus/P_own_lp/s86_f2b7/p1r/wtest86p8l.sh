# eng_p8l copy (9 Nov 19:55Z) of wtest86p.sh: every eng_p1r replaced by eng_p8l (GL16: p1r with payer-8/9 keys).
# s86 p1r: wtest86.sh on the engine copy eng_p8l (E86 overridden after sourcing env86.sh; logs to s86_f2b7/logs as wtest86.sh).
# usage: STACK=s77 ARGS=<args> bash p1r/wtest86p.sh <tag> <cmd> <args...>
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export FAM=full KS=0; . $N/env86.sh; N=$N86; E86=$N86/eng_p8l
echo 900 > /proc/self/oom_score_adj 2>/dev/null   # s86 (10 Nov 03:25Z): beside GS20 + GL20 this check is the OOM victim, never the LPs
TG=$1; CM=$2; shift 2; WK=$SD/wr86t_$TG; mkdir -p $WK; cd $E86
nice -n 10 python3 pcheck.py $CM $F $X $A threads=1 work=$WK "$@" > $N/logs/$TG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s86T-$TG] (eng_p8l) $CM $*: $(grep -E '^(GKSELFTEST|F2B-SELFTEST|UPPER-R2|LOWER-R2)' $N/logs/$TG.log | tail -2 | tr '\n' ' ') $(grep -c Traceback $N/logs/$TG.log) tracebacks" >> $N/run.log
rm -rf $WK
