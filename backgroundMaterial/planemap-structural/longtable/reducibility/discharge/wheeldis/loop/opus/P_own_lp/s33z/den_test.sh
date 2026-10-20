# lowerR2 of the smoke_pol cert (7360eb92, stacked, ipm0 polish) with wden=1e5/1e6 and with ucap=100 (noise test).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; cd $B/s33z/eng
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
F="xon apexcls filt16 killtab=$B/s29/f/kill/kill6 hat5 consall l3q l3qtab=$B/s28q/tab60_1.json,$B/s28q/tab60_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3"
A="root=$M args=$B/s29/argsA60.txt rpat=$B/rpatD.txt"; export OMP_NUM_THREADS=1
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33sm3
for o in wden=1e5 wden=1e6 ucap=100; do nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_smoke_pol.json xcap=3 $o $A work=$WK > ../den_test_$o.log 2>&1; done
echo DONE > ../den_test_done.txt
