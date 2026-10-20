# s40f: newest-head checks on A78 (b6dc7610) with the 128 ring-merge cpat hold-outs (exname_rm127.txt): sol/cert of the A74 n3 pair (no fy).
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s40f/env.sh
Q=$S/reg_A78; A="root=$M args=$Q/args_A78.txt rpat=$B/rpatD.txt exname=$D/exname_rm127.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
cd $E; dfok
nice -n 5 python3 pcheck.py lowerR2 $FQ $X cert=$N3/cert_q39n3A74L.json xcap=3 $A work=$SC/P/wr40_a78 > $D/a78_lower_n3cert.log 2>&1
nice -n 5 python3 pcheck.py upperR2 $FQ $X nomax sol=$N3/sol_q39n3A74.json $A threads=2 work=$SC/P/wr40_a78u > $D/a78_upper_n3sol.log 2>&1
note "A78+exname on the A74 n3 pair: $(grep -h 'exname\|LOWER-R2\|UPPER-R2' $D/a78_lower_n3cert.log $D/a78_upper_n3sol.log | tr '\n' ' ')"
