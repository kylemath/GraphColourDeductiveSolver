# s42a A78 lower cert re-checked on registry A83 (no fb): does 44/421 survive the A83 admissions?
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
Q=$S/reg_A83; A="root=$M args=$Q/args_A83.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
cd $E; nice -n 10 python3 pcheck.py lowerR2 $FQ $X cert=$B/s42a/run_A78/cert_q42aA78L.json xcap=3 $A work=$SC/P/wr_chk42a > $D/chk42a_A83.log 2>&1
note "s42a cert on A83: $(grep LOWER-R2 $D/chk42a_A83.log | tail -1 | cut -c1-120)"
