# smoke of the k86GV1 setup on a SMALL warm set (the GL5 p1_00 cert's receiver and cons2 rows; full warm would need ~5 GB): GV1 family
# (K3gB5b args, 16fik keys, GL6 flags + v2r), maxit=1 (phase 1 + v2inner rounds + phase 2 + one separation round).  RSS watchdog 2.4 GB.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7; cd $N
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/v2r
while pgrep -f "v2r/lx_queue.sh" > /dev/null; do sleep 10; done
( while true; do p=$(pgrep -f "pcheck.py solveR2 .*tag=v2smoke"); if [ -n "$p" ]; then r=$(ps -o rss= -p $p | tr -d ' '); echo "$(date -u +%H:%M:%S) rss $r" >> $N/v2r/logs/smoke_rss.txt
    if [ -n "$r" ] && [ "$r" -gt 2400000 ]; then kill $p; echo "$(date -u +%H:%M:%SZ) smoke_GV1 KILLED by the RSS watchdog ($r kB)" >> $N/v2r/logs/runs.txt; fi; fi
    kill -0 $$ 2> /dev/null || exit 0; sleep 5; done ) &
ARGS=$N/args_A97_F_W13K3gB5b.txt KEYS=$N/p1r/cg_keys_r13w16_16fik.txt bash v2r/v2r_run.sh smoke_GV1 solveR2 keeppen tag=v2smoke consbasis=$B/s21/cf/cons2basis_cls.json \
  warm=$SC/warm_smoke_GL5cert.txt feas=$N/cand/sol_k85C_in03.json xcap=3 xpen=1e-3 lpmax=45 maxit=1 p1r v2r v2seed=$N/v2r/seed_sol_k86GL5_p1.json v2rescan=1 v2inner=3 \
  lext lextcert q7pen=1e-3 consk=20 consfrac=0.25
echo "$(date -u +%H:%M:%SZ) smoke_queue done" >> $N/v2r/logs/runs.txt
