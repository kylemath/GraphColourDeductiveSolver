# m89 step 1: upperR2 of the stacked A64 solution (sol_s33.json) on A64 minus the 89 XRing C entries; then lowerR2 of cert_s33L on m89.
# Runs after the A65 upper check (done_up_A65.txt). A re-solve, if upper is INFEASIBLE, is decided after reading this.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng; Q=$S/m89
until [ -e $S/done_s33.txt ] && [ -e $S/done_up_A65.txt ]; do sleep 60; done
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33m; export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A64m89.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3"
echo "$(date -u +%H:%M:%SZ) m89 upper start" >> $S/wait.log
timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_s33.json $A threads=2 work=${WK}u > $Q/upper_s33_m89.log 2>&1 || echo "upper exit $?" >> $Q/upper_s33_m89.log
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_s33L.json xcap=3 ucap=100 $A work=${WK}L > $Q/lower_s33L_m89.log 2>&1
echo DONE > $Q/done_m89_1.txt
