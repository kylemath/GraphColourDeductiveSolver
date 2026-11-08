# s86 v2r helper: one pcheck command on the eng_v2 engine with the k86GL5 family flags (K3g args, rules 2db75746, rpatN3 + offc_K3g, c6le, f2b7)
# + gkwin gkleaf + extra args.  Waits until MemAvailable >= 5,000,000 kB (the machine runs live LP jobs), runs under nice -n 19.
# usage: [KEYS=<gkeys>] [ARGS=<args file>] [PY=pcheck_dbg.py ROWDBG=<file>] bash v2r/v2r_run.sh <tag> <cmd> [args...]     log: v2r/logs/<tag>.log
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export STACK=s77 ARGS=${ARGS:-$N/args_A97_F_W13K3g.txt} KEYS=${KEYS:-$N/p1r/cg_keys_r13w16_16fi.txt}
export FAM=full KS=0; unset EGK; . $N/env86.sh; N=$N86; E86=$N/eng_v2
TG=$1; CM=$2; shift 2; WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/v2r/work_$TG; mkdir -p $WK $N/v2r/logs; cd $E86
XFT="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt"
while [ $(awk '/MemAvailable/{print $2}' /proc/meminfo) -lt ${MEMMIN:-5000000} ]; do sleep 30; done
echo "$(date -u +%H:%M:%SZ) start $TG $CM (MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB)" >> $N/v2r/logs/runs.txt
PYF=${PY:-pcheck.py}
ROWDBG=$ROWDBG nice -n 19 python3 $PYF $CM $F $X $A threads=1 work=$WK gkeys=$KEYS gkwin gkleaf $XFT "$@" > $N/v2r/logs/$TG.log 2>&1
rc=$?
echo "$(date -u +%H:%M:%SZ) end $TG exit $rc: $(grep -E '^(V2R-TEST|V2RESTRICTED|LOWER-R2|GKSELFTEST|DUALEXPORT)' $N/v2r/logs/$TG.log | tail -3 | tr '\n' ' ') $(grep -c Traceback $N/v2r/logs/$TG.log) tracebacks" | tee -a $N/v2r/logs/runs.txt
rm -rf $WK
