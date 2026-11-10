# eng_p8 validation chain 3 (9 Nov 17:58Z): gkwintest rerun (d >= 10 IN comparison made informational) on both key sets.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13K3gB5m.txt
KEYS=$N/p8test/keys_p8test.txt T86CMD=gkwintest bash $N/T86.sh p8win2 - 1 $XF N=1500
KEYS=$N/p8test/keys_p8s_test.txt T86CMD=gkwintest bash $N/T86.sh p8swin - 1 $XF N=1500 seed=7
echo "$(date -u +%H:%M:%SZ) [s86P8] eng_p8 test chain 3 done" >> $N/run.log
