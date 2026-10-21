# s47 controls (a) (b) (d) on the s42a A78 solution / cert; nice 10, threads=1
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s47/env47.sh
cd $E; note "controls a b d start"
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$SOL $A threads=1 work=$SC/P/wr47_a > $D/ctl_a_upper_default.log 2>&1
if diff <(strip < $B/s42a/run_A78/upper.log) <(strip < $D/ctl_a_upper_default.log) > $D/ctl_a_diff.txt; then ra="byte-identical to s42a/run_A78/upper.log (timings stripped)"; else ra="DIFFERS (ctl_a_diff.txt)"; fi
note "control (a): $ra; $(grep UPPER-R2 $D/ctl_a_upper_default.log)"
nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8A78 nomax sol=$SOL $A threads=1 work=$SC/P/wr47_b > $D/ctl_b_upper_V8.log 2>&1
note "control (b): l3qV=7,8 $(grep UPPER-R2 $D/ctl_b_upper_V8.log); s42a $(grep UPPER-R2 $B/s42a/run_A78/upper.log)"
nice -n 10 python3 pcheck.py lowerR2 $FQ $X $V8A78 cert=$CERT xcap=3 $A work=$SC/P/wr47_d > $D/ctl_d_lower_V8.log 2>&1
note "control (d): l3qV=7,8 $(grep LOWER-R2 $D/ctl_d_lower_V8.log); s45 l3qV=7,8,9 $(grep -h LOWER-R2 $B/s45/pricer45_q42a.out)"
echo DONE > $D/ctl47.done
