# l3q-only reference q66 on A67 (resume_s33.sh stage Q): once converged (run_A67/Q.done), binderR2 on its cert: top 15 + 8666655/5677657.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; RD=$S/run_A67; Q=$S/reg_A67; cd $S/eng
until [ -e $RD/Q.done ]; do sleep 60; done
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
OMP_NUM_THREADS=1 nice -n 5 python3 pcheck.py binderR2 $FQ root=$M args=$Q/args_A67.txt rpat=$B/rpatD.txt sol=sol_q66L.json cert=$RD/cert_q66L.json row=7:8666655:5677657 top=15 work=$SC/P/wr_A67qbd > $RD/binders_q66L.log 2>&1
echo "$(date -u +%H:%M:%SZ) [A67] q66: $(tail -1 $RD/lower_q66L.log | cut -c1-70) | $(grep UPPER-R2 $RD/upper_q66.log) | binders done" >> $S/wait.log
