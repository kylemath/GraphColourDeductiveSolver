# s45 control (a): default l3qV (=7) on s45/eng reproduces s42a lowerR2 VALID 44/421 on cert_q42aA78L; also explicit l3qV=7
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s45/env45.sh
cd $E; note "control (a) start"
nice -n 10 python3 pcheck.py lowerR2 $FQ $X cert=$CERT xcap=3 $A work=$SC/P/wr45_ctl > $D/ctl_lower_default.log 2>&1
nice -n 10 python3 pcheck.py lowerR2 $FQ $X l3qV=7 cert=$CERT xcap=3 $A work=$SC/P/wr45_ctl7 > $D/ctl_lower_V7.log 2>&1
note "control (a): default $(grep -h LOWER-R2 $D/ctl_lower_default.log); l3qV=7 $(grep -h LOWER-R2 $D/ctl_lower_V7.log); s42a $(grep -h LOWER-R2 $B/s42a/run_A78/lower.log)"
echo DONE > $D/ctl45a.done
