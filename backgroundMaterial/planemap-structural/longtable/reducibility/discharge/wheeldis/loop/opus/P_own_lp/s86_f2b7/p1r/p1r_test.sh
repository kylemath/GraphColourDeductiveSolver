# s86 p1r acceptance tests (p1r_test.py: (a) W6b test vectors, (b) GL2 cert coefficient changes vs p1r_changes.json + brute force,
# (c) restricted primal LP current vs p1r) on the eng_p1r engine.  Family = k86GL2's (cert f8893e87): K3g args, rules 2db75746, rpatN3.
# usage: [KEYS=<gkeys>] [P1R_NEWKEYS=w6b16f_] [P1R_LP=0] [P1R_WARM=<rows file>] bash p1r_test.sh <tag> [cert]
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13K3g.txt KEYS=${KEYS:-$B/s85_edge56/keys/cg_keys_r13w16.txt}
export FAM=full KS=0; unset EGK; . $N/env86.sh; N=$N86; E86=$N/eng_p1r
TAG=$1; CERT=${2:-$N/lext_k86GL2/cert_p1_00_f8893e87.json}; WK=$SD/wr86p_$TAG; mkdir -p $WK $N/p1r/logs; cd $E86
XFT="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
P1R_OUT=$N/p1r/logs/p1rtest_$TAG.json ROWDBG=$N/p1r/p1r_test.py nice -n 10 python3 pcheck_dbg.py lowerR2 $F $X $A threads=1 work=$WK cert=$CERT xcap=3 gkeys=$KEYS gkwin gkleaf $XFT p1r > $N/p1r/logs/p1rtest_$TAG.log 2>&1
echo "exit $?"; grep -E '^P1R-' $N/p1r/logs/p1rtest_$TAG.log; grep -c Traceback $N/p1r/logs/p1rtest_$TAG.log
rm -rf $WK
