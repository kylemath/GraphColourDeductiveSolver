# eng_p8 validation chain 2 (9 Nov 17:35Z): the W6b-16s payer-8/9 keys (b8bcafba) on top of the 305; through T86.sh (gated, FIFO).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13K3gB5m.txt
KEYS=$N/p8test/keys_p8s_test.txt T86CMD=p8reftest bash $N/T86.sh p8sref - 1 $XF N=1500 seed=7
KEYS=$N/p1r/cg_keys_r13w16_16fikpqrs.txt bash $N/T86.sh p8sself $N/p8test/sol_GS14in01_p8s_amt.json 2 $XF f2bself=600 seed=7
echo "$(date -u +%H:%M:%SZ) [s86P8] eng_p8 test chain 2 done" >> $N/run.log
