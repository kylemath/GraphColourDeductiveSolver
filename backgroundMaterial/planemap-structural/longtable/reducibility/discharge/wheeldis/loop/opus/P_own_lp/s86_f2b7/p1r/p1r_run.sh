# s86 p1r helper: one pcheck command on the eng_p1r engine with the k86GL2/K3g family flags (no offc) + gkwin gkleaf + extra args.
# usage: [KEYS=<gkeys>] [ROWDBG=<file>] bash p1r_run.sh <tag> <cmd> [args...]     log: p1r/logs/<tag>.log
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export STACK=s77 ARGS=${ARGS:-$N/args_A97_F_W13K3g.txt} KEYS=${KEYS:-$B/s85_edge56/keys/cg_keys_r13w16.txt}
export FAM=full KS=0; unset EGK; . $N/env86.sh; N=$N86; E86=$N/eng_p1r
TG=$1; CM=$2; shift 2; WK=$SD/wr86p_$TG; mkdir -p $WK $N/p1r/logs; cd $E86
XFT="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
if [ -n "$ROWDBG" ]; then PY=pcheck_dbg.py; else PY=pcheck.py; fi
ROWDBG=$ROWDBG nice -n 10 python3 $PY $CM $F $X $A threads=1 work=$WK gkeys=$KEYS gkwin gkleaf $XFT "$@" > $N/p1r/logs/$TG.log 2>&1
echo "exit $? : $(grep -E '^(GKSELFTEST|GKWINTEST|GK67|F2B-SELFTEST|UPPER-R2|LOWER-R2|P1R-TEST)' $N/p1r/logs/$TG.log | tail -4 | tr '\n' ' ') $(grep -c Traceback $N/p1r/logs/$TG.log) tracebacks"
rm -rf $WK
