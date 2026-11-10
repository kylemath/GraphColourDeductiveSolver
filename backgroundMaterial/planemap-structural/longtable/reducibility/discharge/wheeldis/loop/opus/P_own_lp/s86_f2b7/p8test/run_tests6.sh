# eng_p8 / eng_p8l validation of the 347-key file (9 Nov 20:15Z): 329 (891077d7) + W6b-16t sel18 (b9440d2d; payer 8 x10, payer 7 x8).
# Through T86.sh (gated, FIFO).  p8reftest + gkwintest on the 18 + every 12th old key; F2B self-test on all 347 with amounts on the 18;
# p1rordtest (eng_p8l) on all 347.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5m.txt
E86OVR=$N/eng_p8 KEYS=$N/p8test/keys_p8t_test.txt T86CMD=p8reftest bash $N/T86.sh p8tref - 1 $XF N=1500 seed=11
E86OVR=$N/eng_p8 KEYS=$N/p8test/keys_p8t_test.txt T86CMD=gkwintest bash $N/T86.sh p8twin - 1 $XF N=1500 seed=11
E86OVR=$N/eng_p8 KEYS=$N/p1r/cg_keys_r13w16_16fikpqrst.txt bash $N/T86.sh p8tself $N/p8test/sol_GS14in01_p8t_amt.json 2 $XF f2bself=600 seed=11
E86OVR=$N/eng_p8l KEYS=$N/p1r/cg_keys_r13w16_16fikpqrst.txt T86CMD=p1rordtest bash $N/T86.sh p1rordt - 1 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r N=1500 seed=11 vecout=$N/p8test/p1rord_vectors_347.json
for f in p8tref p8twin p8tself p1rordt; do echo "$f: $(grep -E 'P8REFTEST:|GKWINTEST:|F2B-SELFTEST|P1RORDTEST:' $N/logs/t86_$f.log | tail -2 | tr '\n' ' ') $(grep -c Traceback $N/logs/t86_$f.log) tracebacks"; done > $N/p8test/tests6.out
echo "$(date -u +%H:%M:%SZ) [s86P8] 347-key test chain done: $(tr '\n' ' ' < $N/p8test/tests6.out | cut -c1-600)" >> $N/run.log
