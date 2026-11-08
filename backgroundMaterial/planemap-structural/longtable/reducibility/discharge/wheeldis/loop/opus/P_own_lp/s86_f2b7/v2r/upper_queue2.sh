# s86 v2r upper validation queue 2 (after queue 1): G = worked receivers at the probe (v2rupshow); E = the k86GL5 phase-1 sol (lext seed,
# family K3g + 220 keys 16fi + offc_K3g) under v2r and the standard check (masked vs v2 counts).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; cd $N
while pgrep -f "v2r/upper_queue1.sh" > /dev/null || pgrep -f "v2r/U86v.sh" > /dev/null; do sleep 10; done
export RSSMAX=1800000 STACK=s77
U=$N/v2r/upper
FX="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
ARGS=$N/args_A97_F_W13K3l5.txt KEYS=$N/p1r/cg_keys_r13w16_16fik.txt CMD=v2rupshow bash $N/v2r/U86v.sh v2G_upshow_probe $U/sol_S4W09k240_probe.json 2 $FX v2r v2urows=$U/v2urows_probe.txt v2ushow=$U/V2UPPER_vectors.json
FXG="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt"
ARGS=$N/args_A97_F_W13K3g.txt KEYS=$N/p1r/cg_keys_r13w16_16fi.txt bash $N/v2r/U86v.sh v2E_GL5p1 $N/v2r/seed_sol_k86GL5_p1.json 2 $FXG v2r v2uK=500000 v2unbr=0 vfile=$U/viol_v2E_GL5p1.txt v2umfile=$U/mlist_E_GL5p1.txt
ARGS=$N/args_A97_F_W13K3g.txt KEYS=$N/p1r/cg_keys_r13w16_16fi.txt bash $N/v2r/U86v.sh stdE_GL5p1 $N/v2r/seed_sol_k86GL5_p1.json 2 $FXG vK=500000 vfile=$U/viol_stdE_GL5p1.txt
echo "queue2 done"
