# s53: early upperR2 on the A97 K solution, in parallel with run53's L stage (same flags as run53's U stage). Writes run_A97/upper_early.log.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
S=$B/s33z; Q=$S/reg_A97; RD=$B/s53/run_A97; export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A97.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 l3qV=7,8 l3qtab8=$B/s47/tabV8_A97/tabV8_1.json,$B/s47/tabV8_A97/tabV8_-1.json"
X="rpatN=$B/s39o/rpatN3.txt"
cd $B/s51/eng
nice -n 10 python3 pcheck.py upperR2 $F $X nomax sol=$RD/sol_q53A97.json $A threads=1 work=$SC/P/wr53ue > $RD/upper_early.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s53] early U: A97 $(grep UPPER-R2 $RD/upper_early.log || echo 'no UPPER-R2 line')" >> $B/s53/run.log
rm -rf $SC/P/wr53ue
