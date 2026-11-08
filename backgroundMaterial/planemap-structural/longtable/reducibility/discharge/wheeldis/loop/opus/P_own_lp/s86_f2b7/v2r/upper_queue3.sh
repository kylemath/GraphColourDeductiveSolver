# s86 v2r upper validation queue 3: G = worked receivers at the probe (v2rupshow); F = planted DP bug v2bug=dpin:gk03_37 (the DP drops key
# gk03_37's IN term; the row builder keeps it): F1 at the probe, F2 at sol_S4W09k240 with the masked list down to 0.002 below the cap.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; cd $N
while pgrep -f "v2r/U86v.sh" > /dev/null; do sleep 10; done
export RSSMAX=1800000 STACK=s77 ARGS=$N/args_A97_F_W13K3l5.txt KEYS=$N/p1r/cg_keys_r13w16_16fik.txt
U=$N/v2r/upper
FX="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
CMD=v2rupshow bash $N/v2r/U86v.sh v2G_upshow_probe $U/sol_S4W09k240_probe.json 2 $FX v2r v2urows=$U/v2urows_probe.txt v2ushow=$U/V2UPPER_vectors.json
bash $N/v2r/U86v.sh v2F1_bug_probe $U/sol_S4W09k240_probe.json 2 $FX v2r v2bug=dpin:gk03_37 v2umfile=$U/mlist_F1_bug_probe.txt
bash $N/v2r/U86v.sh v2F2_bug_S4W09k240_m002 $N/cand/sol_S4W09k240.json 2 $FX v2r v2bug=dpin:gk03_37 v2umargin=0.002 v2umfile=$U/mlist_F2_bug_m002.txt
bash $N/v2r/U86v.sh v2F3_bug_probe_nonbr $U/sol_S4W09k240_probe.json 2 $FX v2r v2bug=dpin:gk03_37 v2unbr=0
echo "queue3 done"
