# smoke: stacked nosep LP over the s28A60 warm rows (7360eb92) with ipm0 (IPM at iteration 0), then lowerR2. Timing check for the real solve.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
cd $B/s33z/eng
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
F="xon apexcls filt16 killtab=$B/s29/f/kill/kill6 hat5 consall l3q l3qtab=$B/s28q/tab60_1.json,$B/s28q/tab60_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3"
A="root=$M args=$B/s29/argsA60.txt rpat=$B/rpatD.txt"; export OMP_NUM_THREADS=1
date -u +%T > ../smoke_ipm_start.txt
timeout 7200 nice -n 5 python3 pcheck.py solveR2 $F nosep ipm0 tag=smoke_ipm $A consbasis=$B/s21/cf/cons2basis_cls.json warm=$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt K=300 xcap=3 threads=1 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33sm2 > ../smoke_ipm.log 2>&1
date -u +%T > ../smoke_ipm_end.txt
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_smoke_ipm.json xcap=3 $A work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33sm2 > ../smoke_ipm_lower.log 2>&1
