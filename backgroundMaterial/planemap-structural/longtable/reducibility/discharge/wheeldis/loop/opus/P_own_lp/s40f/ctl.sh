# s40f controls: (a) fy off reproduces the A74 n3 pair; (b) fy on priced against cert_q39n3A74L (pricer40.py, full negative list)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s40f/env.sh
cd $E; dfok; note "controls start"
nice -n 5 python3 pcheck.py lowerR2 $FQ $X cert=$N3/cert_q39n3A74L.json xcap=3 $A work=$SC/P/wr40_ctl > $D/ctl_lower_nofy.log 2>&1 &
nice -n 5 python3 $D/pricer40.py > $D/pricer40.out 2>&1 &
wait
nice -n 5 python3 pcheck.py upperR2 $FQ $X nomax sol=$N3/sol_q39n3A74.json $A threads=2 work=$SC/P/wr40_ctlu > $D/ctl_upper_nofy.log 2>&1
note "controls: $(grep -h 'LOWER-R2\|UPPER-R2' $D/ctl_lower_nofy.log $D/ctl_upper_nofy.log $D/pricer40.out | tr '\n' ' ')"
echo DONE > $D/ctl.done
