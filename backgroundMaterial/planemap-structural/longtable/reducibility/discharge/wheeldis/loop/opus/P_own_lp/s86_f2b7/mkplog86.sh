# s86 (9 Nov 13:50Z): the EXPECT log for mkfam.py: an upperR2 start on <args> + 240 keys with the fam flags, stopped once "patterns:" is
# out (no slot needed: it stops before any LP or separation).  usage: bash mkplog86.sh <K3l5x|K3gB5x>   -> logs/upper_P_<fam>.log
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13$1.txt KEYS=$N/p1r/cg_keys_r13w16_16fik.txt E86OVR=$N/eng_p1r FAM=full KS=0; unset EGK; . $N/env86.sh; N=$N86
[ -s $ARGS ] || { echo "mkplog86: no $ARGS" >&2; exit 2; }
WK=$SD/wr86p_$1; mkdir -p $WK; cd $E86; L=$N/logs/upper_P_$1.log
python3 pcheck.py upperR2 $F $X nomax sol=$N/cand/sol_repS6MW_01__K3l5j.json $A threads=1 work=$WK gkeys=$KEYS gkwin gkleaf c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt > $L 2>&1 &
P=$!; for i in $(seq 600); do grep -q '^patterns: ' $L && break; kill -0 $P 2>/dev/null || break; sleep 1; done
kill $P 2>/dev/null; wait $P 2>/dev/null; rm -rf $WK; grep -c '^patterns: ' $L
