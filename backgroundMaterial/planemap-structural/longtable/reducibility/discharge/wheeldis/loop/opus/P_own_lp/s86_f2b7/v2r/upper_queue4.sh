# s86 v2r upper validation queue 4 (after queue 3): H = sol_S4W09k240 with lQ[(5,5,31)] + 1e-5 (masked-only column): v2 and standard checks.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; cd $N
while pgrep -f "v2r/upper_queue3.sh" > /dev/null || pgrep -f "v2r/U86v.sh" > /dev/null; do sleep 10; done
export RSSMAX=1800000 STACK=s77 ARGS=$N/args_A97_F_W13K3l5.txt KEYS=$N/p1r/cg_keys_r13w16_16fik.txt
U=$N/v2r/upper
FX="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
bash $N/v2r/U86v.sh v2H_lQ $U/sol_S4W09k240_lQ.json 2 $FX v2r v2umfile=$U/mlist_H_lQ.txt
bash $N/v2r/U86v.sh stdH_lQ $U/sol_S4W09k240_lQ.json 2 $FX vK=1000000 vfile=$U/viol_stdH_lQ.txt
echo "queue4 done"
