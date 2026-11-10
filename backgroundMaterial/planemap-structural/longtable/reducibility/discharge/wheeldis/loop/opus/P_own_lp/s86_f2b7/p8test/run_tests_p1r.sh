# eng_p8l (GL16) validation (9 Nov 19:50Z): p1r coefficient <= upper coefficient with the 329 keys (payer-8/9), and the p1rplant control
# (d = 8 payer-8/9 OUT read as 0) must FAIL.  Through T86.sh (gated, FIFO).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r"
export E86OVR=$N/eng_p8l STACK=s77 ARGS=$N/args_A97_F_W13K3gB5m.txt
KEYS=$N/p1r/cg_keys_r13w16_16fikpqrs.txt T86CMD=p1rordtest bash $N/T86.sh p1rord - 1 $XF N=1500
KEYS=$N/p1r/cg_keys_r13w16_16fikpqrs.txt T86CMD=p1rordtest bash $N/T86.sh p1rordCTL - 1 $XF N=600 p1rplant
echo "$(date -u +%H:%M:%SZ) [s86P8] eng_p8l p1r test chain done" >> $N/run.log
