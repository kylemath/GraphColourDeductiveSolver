# upperR2 of the stacked A64 keeppen solution (sol_s33.json) on registry A65 = main 15bc20c7 (args/kill6/l3q tables from prep_A65.sh).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng; Q=$S/reg_A65
until [ -e $S/done_s33.txt ] && [ -e $Q/prep_done.txt ]; do sleep 60; done
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A65.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3"
echo "$(date -u +%H:%M:%SZ) upperR2 sol_s33 on A65 start" >> $S/wait.log
timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_s33.json $A threads=2 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33u65 > $S/upper_s33_A65.log 2>&1 || echo "upper exit $?" >> $S/upper_s33_A65.log
echo DONE > $S/done_up_A65.txt
