# eng_p8 / eng_p8l / eng_p8h validation of the 365-key file (10 Nov 10:20Z): 357 (449bf4dd) + the 8 W6b bb-variant payer-8 keys (as in
# maclane v2e b5875bfe), on K3gB5n.  Through T86.sh, one at a time (U86_MAXCHK=2 so a test may run beside one upperR2 check).
# p8reftest + gkwintest on keys_p8bb_test.txt (v2e's 30 test keys: the 8 + 22 old); F2B self-test on all 365 with amounts on the 8
# (MK1 in23 + bb amounts); the same on eng_p8h with HATBB (GS21 in02 + bb amounts); p1rordtest (eng_p8l) on all 365.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"; HB="hatbb hbkeys=$N/hatbb/cg_keys_w6b16x_hatbb.txt"
K365=$N/p1r/cg_keys_r13w16_16fikpqrstwb.txt
export STACK=s77 ARGS=$N/args_A97_F_W13K3gB5n.txt U86_MAXCHK=2
E86OVR=$N/eng_p8 KEYS=$N/p8test/keys_p8bb_test.txt T86CMD=p8reftest bash $N/T86.sh bbref - 1 $XF N=1500 seed=11
E86OVR=$N/eng_p8 KEYS=$N/p8test/keys_p8bb_test.txt T86CMD=gkwintest bash $N/T86.sh bbwin - 1 $XF N=1500 seed=11
E86OVR=$N/eng_p8 KEYS=$K365 bash $N/T86.sh bbself $N/p8test/sol_MK1in23_p8bb_amt.json 2 $XF f2bself=600 seed=11
E86OVR=$N/eng_p8h KEYS=$K365 bash $N/T86.sh bbhbself $N/p8test/sol_GS21in02_hb_bb_amt.json 2 $XF $HB f2bself=600 seed=11
E86OVR=$N/eng_p8l KEYS=$K365 T86CMD=p1rordtest bash $N/T86.sh bbp1rord - 1 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r N=1500 seed=11 vecout=$N/p8test/p1rord_vectors_365.json
for f in bbref bbwin bbself bbhbself bbp1rord; do echo "$f: $(grep -E 'P8REFTEST:|GKWINTEST:|F2B-SELFTEST|P1RORDTEST:' $N/logs/t86_$f.log | tail -2 | tr '\n' ' ') $(grep -c Traceback $N/logs/t86_$f.log) tracebacks"; done > $N/p8test/tests8.out
OK=1; grep -q '^bbref: .*P8REFTEST: PASS.* 0 tracebacks' $N/p8test/tests8.out || OK=0; grep -q '^bbwin: .*GKWINTEST: PASS.* 0 tracebacks' $N/p8test/tests8.out || OK=0
grep -q '^bbself: .*F2B-SELFTEST: PASS.* 0 tracebacks' $N/p8test/tests8.out || OK=0; grep -q '^bbhbself: .*F2B-SELFTEST: PASS.* 0 tracebacks' $N/p8test/tests8.out || OK=0
grep -q '^bbp1rord: .*P1RORDTEST: PASS.* 0 tracebacks' $N/p8test/tests8.out || OK=0
[ $OK = 1 ] && echo "P365OK $(date -u +%H:%M:%SZ) 365 keys p1r/cg_keys_r13w16_16fikpqrstwb.txt ($(md5sum < $K365 | cut -c1-8) = 357 449bf4dd + 8 bb) on eng_p8 / eng_p8h / eng_p8l, K3gB5n" > $N/p8test/VERDICT_365 || echo "P365BAD $(date -u +%H:%M:%SZ)" > $N/p8test/VERDICT_365
cat $N/p8test/tests8.out >> $N/p8test/VERDICT_365
echo "$(date -u +%H:%M:%SZ) [s86P8] 365-key test chain done: $(head -1 $N/p8test/VERDICT_365 | cut -c1-80); $(tr '\n' ' ' < $N/p8test/tests8.out | cut -c1-600)" >> $N/run.log
