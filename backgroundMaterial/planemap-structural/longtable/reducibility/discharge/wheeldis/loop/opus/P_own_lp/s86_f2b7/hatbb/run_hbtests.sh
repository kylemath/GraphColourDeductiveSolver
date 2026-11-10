# eng_p8h HATBB integration tests (10 Nov): python rows vs C++ leaf (WIN) with HATBB amounts on (f2bself), then the planted control (must FAIL)
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"; HB="hatbb hbkeys=$N/hatbb/cg_keys_w6b16x_hatbb.txt"
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt E86OVR=$N/eng_p8h KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt U86_MINFREE_MB=${MF:-2000}
bash $N/T86.sh hbf2bself $N/hatbb/sol_test_GS20in_hb.json 2 $XF $HB f2bself=600 seed=11
bash $N/T86.sh hbf2bplant $N/hatbb/sol_test_GS20in_hb.json 2 $XF $HB hbwplant f2bself=600 seed=11
for f in hbf2bself hbf2bplant; do echo "$f: $(grep -E 'F2B-SELFTEST' $N/logs/t86_$f.log | tail -4 | tr '\n' ' ') $(grep -c Traceback $N/logs/t86_$f.log) tracebacks"; done > $N/hatbb/tests_f2b.out
echo "$(date -u +%H:%M:%SZ) [s86HB] eng_p8h HATBB f2bself tests done: $(tr '\n' ' ' < $N/hatbb/tests_f2b.out | cut -c1-500)" >> $N/run.log
