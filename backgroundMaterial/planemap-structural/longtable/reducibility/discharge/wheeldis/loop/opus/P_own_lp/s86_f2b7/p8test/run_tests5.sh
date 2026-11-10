# eng_p8 validation chain 5 (9 Nov 18:25Z, rerun of chain 4: its run was OOM-killed at 18:21Z): d = 7 leaf control (gkinplant: payer-8/9 keys read as payer 7 in the leaf; F2B-SELFTEST must FAIL).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export E86OVR=$N/eng_p8 STACK=s77 ARGS=$N/args_A97_F_W13K3gB5m.txt
KEYS=$N/p1r/cg_keys_r13w16_16fikpqrs.txt bash $N/T86.sh p8sselfINCTL2 $N/p8test/sol_GS14in01_p8s_amt.json 2 $XF f2bself=600 seed=7 gkinplant
echo "$(date -u +%H:%M:%SZ) [s86P8] eng_p8 test chain 5 done" >> $N/run.log
