# eng_p8 / eng_p8l validation of the 357-key file (9 Nov 23:15Z): 347 (0a66b3c0) + W6b-16w (32b2adae; payer 7 x4, payer 8 x6), on K3gB5n.
# Through T86.sh (gated, FIFO).  p8reftest + gkwintest on the 10 + every 12th old key; F2B self-test on all 357 with amounts on the 18 + 10;
# p1rordtest (eng_p8l) on all 357.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt
E86OVR=$N/eng_p8 KEYS=$N/p8test/keys_p8w_test.txt T86CMD=p8reftest bash $N/T86.sh p8wref - 1 $XF N=1500 seed=11
E86OVR=$N/eng_p8 KEYS=$N/p8test/keys_p8w_test.txt T86CMD=gkwintest bash $N/T86.sh p8wwin - 1 $XF N=1500 seed=11
E86OVR=$N/eng_p8 KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt bash $N/T86.sh p8wself $N/p8test/sol_GS14in01_p8w_amt.json 2 $XF f2bself=600 seed=11
E86OVR=$N/eng_p8l KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstw.txt T86CMD=p1rordtest bash $N/T86.sh p1rordw - 1 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r N=1500 seed=11 vecout=$N/p8test/p1rord_vectors_357.json
for f in p8wref p8wwin p8wself p1rordw; do echo "$f: $(grep -E 'P8REFTEST:|GKWINTEST:|F2B-SELFTEST|P1RORDTEST:' $N/logs/t86_$f.log | tail -2 | tr '\n' ' ') $(grep -c Traceback $N/logs/t86_$f.log) tracebacks"; done > $N/p8test/tests7.out
echo "$(date -u +%H:%M:%SZ) [s86P8] 357-key test chain done: $(tr '\n' ' ' < $N/p8test/tests7.out | cut -c1-600)" >> $N/run.log
