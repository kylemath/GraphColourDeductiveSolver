# l3q-only baseline on A64 (c6395bf1): the s28q A62 l3q-only cert / solution re-checked on the A64 registry (s33z engine, flags as s28q).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S=$B/s33z; cd $S/eng; Q=$S/reg_A64
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33b; export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A64.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
nice -n 5 python3 pcheck.py lowerR2 $F cert=$B/s28q/eng/cert_s28A62L.json xcap=3 $A work=$WK > $S/base_A64_lower.log 2>&1
timeout 3600 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=$B/s28q/eng/sol_s28A62.json $A threads=1 work=${WK}u > $S/base_A64_upper.log 2>&1
echo DONE > $S/base_A64_done.txt
