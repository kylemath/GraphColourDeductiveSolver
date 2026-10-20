# s44 control (a): fb OFF on the s44 engine reproduces the A74 n3 pair (lowerR2 VALID 20/183, upperR2 FEASIBLE 1/9)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
cd $E; dfok; note "control (a) start"
nice -n 10 python3 pcheck.py lowerR2 $FQ $X cert=$N3/cert_q39n3A74L.json xcap=3 $A work=$SC/P/wr44_ctl > $D/ctl_lower_off.log 2>&1
cmp $D/ctl_lower_off.log $N3/lower.log && note "lower log byte-identical to s39o" || note "lower log differs from s39o"
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$N3/sol_q39n3A74.json $A threads=1 work=$SC/P/wr44_ctlu > $D/ctl_upper_off.log 2>&1
note "control (a): $(grep -h 'LOWER-R2\|UPPER-R2' $D/ctl_lower_off.log $D/ctl_upper_off.log | tr '\n' ' ')"
echo DONE > $D/ctl.done
