# validation step 3 queue (after rlp_queue.sh): lowerR2 exactbasis on the v2 restricted-LP dual, planted-bug rechecks, controls, test vectors.
# One process at a time, each memory gated by v2r_run.sh.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; cd $N; R=$N/v2r/rlp
while pgrep -f "v2r/rlp_queue.sh" > /dev/null; do sleep 10; done
# 3a: exact basis + norepair recheck of the exact cert (VALID expected)
bash v2r/v2r_run.sh lx_rlp_v2 lowerR2 v2r cert=$R/cert_rlp_v2.json xcap=3 exactbasis exbmu=0 exbtol=1e-10
# 3b: planted bug (every 7's two privates swapped in the rebuild) on the exact cert, norepair (must fail)
bash v2r/v2r_run.sh lx_rlp_v2_bug lowerR2 v2r v2bug=p1p2 cert=$R/cert_rlp_v2_exb.json xcap=3 norepair
# 3c: the same bug inside exactbasis (weights re-optimised over the wrong rows; reported for information)
cp $R/cert_rlp_v2.json $R/cert_rlp_v2_bugsrc.json
bash v2r/v2r_run.sh lx_rlp_v2_bugexb lowerR2 v2r v2bug=p1p2 cert=$R/cert_rlp_v2_bugsrc.json xcap=3 exactbasis exbmu=0 exbtol=1e-10
# 3d: controls: the v2 exact cert without the v2r flag (receiverV2 rows refused); the mask-mode dual under v2r (masked d = 7 / 8 rows refused)
bash v2r/v2r_run.sh lx_rlp_v2_noflag lowerR2 cert=$R/cert_rlp_v2_exb.json xcap=3 norepair
bash v2r/v2r_run.sh lx_rlp_mask_v2r lowerR2 v2r cert=$R/cert_rlp_mask.json xcap=3 norepair
# test vectors for V2ROW_SPEC.md
bash v2r/v2r_run.sh v2rshow v2rshow v2r v2rows=$N/v2r/V2ROW_vectors_rows.txt v2show=$N/v2r/V2ROW_vectors.json
python3 -I $N/v2r/spec_check.py $N/v2r/V2ROW_vectors.json $N/p1r/cg_keys_r13w16_16fi.txt > $N/v2r/logs/spec_check.log 2>&1
echo "$(date -u +%H:%M:%SZ) spec_check: $(tail -1 $N/v2r/logs/spec_check.log)" >> $N/v2r/logs/runs.txt
echo "$(date -u +%H:%M:%SZ) lx_queue done" >> $N/v2r/logs/runs.txt
