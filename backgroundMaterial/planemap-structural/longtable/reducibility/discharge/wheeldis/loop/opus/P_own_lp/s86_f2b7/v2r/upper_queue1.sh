# s86 v2r upper validation queue 1 (one run at a time, after any running U86v.sh): on K3l5 + 240 keys (16fik), the S4W09k240 family.
#   B: sol_S4W09k240 (t = 0.028372061), v2r, masked list down to 0.002 below the cap, sym / brute / 1-site checks, every listed row to a file
#   C: the probe (t - 0.003), v2r, the same checks
#   D: the probe, standard upperR2 on eng_v2 without v2r (the masked counts to compare)
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; cd $N
while pgrep -f "v2r/U86v.sh" > /dev/null; do sleep 10; done
export RSSMAX=1800000 STACK=s77 ARGS=$N/args_A97_F_W13K3l5.txt KEYS=$N/p1r/cg_keys_r13w16_16fik.txt
FX="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
U=$N/v2r/upper
bash $N/v2r/U86v.sh v2B_S4W09k240_m002 $N/cand/sol_S4W09k240.json 2 $FX v2r v2umargin=0.002 v2usym=20 v2ubrute=10 v2unbr=1 v2umfile=$U/mlist_B_S4W09k240_m002.txt
bash $N/v2r/U86v.sh v2C_S4W09k240_probe $U/sol_S4W09k240_probe.json 2 $FX v2r vfile=$U/viol_v2C_probe.txt v2usym=20 v2ubrute=20 v2unbr=1 v2umfile=$U/mlist_C_probe.txt
bash $N/v2r/U86v.sh stdD_S4W09k240_probe $U/sol_S4W09k240_probe.json 2 $FX vK=1000000 vfile=$U/viol_stdD_probe.txt
echo "queue1 done"
