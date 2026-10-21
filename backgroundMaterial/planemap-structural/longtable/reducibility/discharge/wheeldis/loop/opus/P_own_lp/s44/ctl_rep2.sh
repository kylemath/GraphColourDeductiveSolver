# s44 (cont.) control M2: as ctl_rep.sh (M), but the PAYER sign is flipped in the solve (+1 in u's receiver row; engine copy eng_mis2),
# fb uncapped. The mis-signed LP gets no use out of fb, so its cert is a no-fb cert; checked with the true engine (fb uncapped) it must be INVALID
# (fb6 prices negative on it, cf. pricer44_q42a.out) and the repair must refuse (|rc| far beyond reptol).
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
Q=$S/reg_A78; A="root=$M args=$Q/args_A78.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
C=$D/ctl_rep; EM=$SC/P/eng_mis2; WS=$C/rows_small.txt; dfok; note "repair control M2 start"
cd $EM; nice -n 10 python3 pcheck.py solveR2 $FQ fb fbdir=6 $X nosep tag=ctlrepM2 $A $CB warm=$WS K=300 xcap=3 threads=1 work=$SC/P/wr44_cM2 > $C/M2_solve.log 2>&1
mv sol_ctlrepM2.json cert_ctlrepM2.json $C/; rm -f rows_ctlrepM2.txt
cd $E; nice -n 10 python3 pcheck.py lowerR2 $FQ fb fbdir=6 $X cert=$C/cert_ctlrepM2.json xcap=3 $A work=$SC/P/wr44_cM2 > $C/M2_lower.log 2>&1
note "repair control M2: $(tail -n 1 $C/M2_lower.log | cut -c1-20)"; echo DONE > $C/done2
