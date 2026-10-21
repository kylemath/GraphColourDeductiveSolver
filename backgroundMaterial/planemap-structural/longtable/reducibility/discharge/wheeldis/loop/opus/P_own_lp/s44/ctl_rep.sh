# s44 (cont.) repair controls on reg_A78 (exname rm128), small warm set = the 48 receiver rows of cert_q44fbA78L, nosep, nice 10 threads 1.
# (A first try with the first 3000 A78 rows on reg_A74 gave a 2-row cert at t = -7/3 with no cons2 row: fb not exercised; replaced.)
#  (G) fb6 cap 3 solved with the s44 engine -> lowerR2 must be VALID (with or without repair).
#  (M) the same solve with the cons2 fb inflow deliberately mis-signed (-1, solve only; engine copy eng_mis), fb uncapped
#      -> lowerR2 with the true engine (fb uncapped) must be INVALID and the repair must refuse.
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
Q=$S/reg_A78; A="root=$M args=$Q/args_A78.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
C=$D/ctl_rep; EM=$SC/P/eng_mis; WS=$C/rows_small.txt; dfok; note "repair controls start"
( cd $E; nice -n 10 python3 pcheck.py solveR2 $FQ fb fbdir=6 fbcap=3 $X nosep tag=ctlrepG $A $CB warm=$WS K=300 xcap=3 threads=1 work=$SC/P/wr44_cG > $C/G_solve.log 2>&1
  mv sol_ctlrepG.json cert_ctlrepG.json $C/; rm -f rows_ctlrepG.txt
  nice -n 10 python3 pcheck.py lowerR2 $FQ fb fbdir=6 fbcap=3 $X cert=$C/cert_ctlrepG.json xcap=3 $A work=$SC/P/wr44_cG > $C/G_lower.log 2>&1 ) &
( cd $EM; nice -n 10 python3 pcheck.py solveR2 $FQ fb fbdir=6 $X nosep tag=ctlrepM $A $CB warm=$WS K=300 xcap=3 threads=1 work=$SC/P/wr44_cM > $C/M_solve.log 2>&1
  mv sol_ctlrepM.json cert_ctlrepM.json $C/; rm -f rows_ctlrepM.txt
  cd $E; nice -n 10 python3 pcheck.py lowerR2 $FQ fb fbdir=6 $X cert=$C/cert_ctlrepM.json xcap=3 $A work=$SC/P/wr44_cM > $C/M_lower.log 2>&1 ) &
wait; note "repair controls: G $(tail -n 1 $C/G_lower.log | cut -c1-20) | M $(tail -n 1 $C/M_lower.log | cut -c1-20)"; echo DONE > $C/done
