# s33z regressions: flags off (s28 flag set) and flags on, lowerR2 against cert_s28A60L on argsA60; orientR2 key self-tests
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33
A="root=$M args=$B/s29/argsA60.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$B/s29/f/kill/kill6 hat5 consall l3q l3qtab=$B/s28q/tab60_1.json,$B/s28q/tab60_-1.json lqcap=3"
export OMP_NUM_THREADS=1
nice -n 5 python3 pcheck.py lowerR2 $F cert=$B/s28q/eng/cert_s28A60L.json xcap=3 $A work=${WK}a > $S/reg_off_lower.log 2>&1
nice -n 5 python3 pcheck.py lowerR2 $F zh zr hatrr cert=$B/s28q/eng/cert_s28A60L.json xcap=3 $A work=${WK}b > $S/reg_on_lower.log 2>&1
nice -n 5 python3 pcheck.py orientR2 $F zh zr hatrr $A work=${WK}c > $S/reg_orient.log 2>&1
nice -n 5 python3 pcheck.py orientR2 $F zh zr hatrr brokenkey $A work=${WK}c > $S/reg_orient_broken.log 2>&1
nice -n 5 python3 pcheck.py orientR2 $F zh zr hatrr brokensign $A work=${WK}c > $S/reg_orient_brokensign.log 2>&1
