# after lx_queue.sh step 3a / 3b (3c, the bug inside exactbasis, dropped: ~40 min of exact elimination that only re-certifies the wrong rows):
# controls, V2ROW_SPEC test vectors + spec-only re-derivation, then the k86GV1 smoke.  One process at a time, memory gated (v2r_run.sh).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7; cd $N; R=$N/v2r/rlp
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/v2r
while pgrep -f "v2r/v2r_run.sh" > /dev/null || pgrep -f "scratchpad/v2r/work_" > /dev/null; do sleep 10; done   # any run of this build still running (3b)
bash v2r/v2r_run.sh lx_rlp_v2_noflag lowerR2 cert=$R/cert_rlp_v2_exb.json xcap=3 norepair
bash v2r/v2r_run.sh lx_rlp_mask_v2r lowerR2 v2r cert=$R/cert_rlp_mask.json xcap=3 norepair
bash v2r/v2r_run.sh v2rshow v2rshow v2r v2rows=$N/v2r/V2ROW_vectors_rows.txt v2show=$N/v2r/V2ROW_vectors.json
python3 -I $N/v2r/spec_check.py $N/v2r/V2ROW_vectors.json $N/p1r/cg_keys_r13w16_16fi.txt > $N/v2r/logs/spec_check.log 2>&1
echo "$(date -u +%H:%M:%SZ) spec_check: $(tail -1 $N/v2r/logs/spec_check.log)" >> $N/v2r/logs/runs.txt
( while true; do p=$(pgrep -f "pcheck.py solveR2 .*tag=v2smoke"); if [ -n "$p" ]; then r=$(ps -o rss= -p $p | tr -d ' '); echo "$(date -u +%H:%M:%S) rss $r" >> $N/v2r/logs/smoke_rss.txt
    if [ -n "$r" ] && [ "$r" -gt 2400000 ]; then kill $p; echo "$(date -u +%H:%M:%SZ) smoke_GV1 KILLED by the RSS watchdog ($r kB)" >> $N/v2r/logs/runs.txt; fi; fi
    kill -0 $$ 2> /dev/null || exit 0; sleep 5; done ) &
ARGS=$N/args_A97_F_W13K3gB5b.txt KEYS=$N/p1r/cg_keys_r13w16_16fik.txt bash v2r/v2r_run.sh smoke_GV1 solveR2 keeppen tag=v2smoke consbasis=$B/s21/cf/cons2basis_cls.json \
  warm=$SC/warm_smoke_GL5cert.txt feas=$N/cand/sol_k85C_in03.json xcap=3 xpen=1e-3 lpmax=45 maxit=1 p1r v2r v2seed=$N/v2r/seed_sol_k86GL5_p1.json v2rescan=1 v2inner=3 \
  lext lextcert q7pen=1e-3 consk=20 consfrac=0.25
echo "$(date -u +%H:%M:%SZ) rest_queue done" >> $N/v2r/logs/runs.txt
