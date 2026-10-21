# s51 control (a): default flags (no xo) reproduce s42a/run_A78/upper.log and lower.log (timings stripped); nice 10, threads 1
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s51/env51.sh
cd $E; note "control (a) start"
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$SOL $A threads=1 work=$SC/P/wr51_a > $D/ctl_a_upper.log 2>&1
nice -n 10 python3 pcheck.py lowerR2 $FQ $X cert=$CERT xcap=3 $A work=$SC/P/wr51_al > $D/ctl_a_lower.log 2>&1
ru=$(diff <(strip < $B/s42a/run_A78/upper.log) <(strip < $D/ctl_a_upper.log) > $D/ctl_a_upper_diff.txt && echo identical || echo DIFFERS)
rl=$(diff <(strip < $B/s42a/run_A78/lower.log) <(strip < $D/ctl_a_lower.log) > $D/ctl_a_lower_diff.txt && echo identical || echo DIFFERS)
note "control (a): upper $ru to s42a/run_A78/upper.log ($(grep UPPER-R2 $D/ctl_a_upper.log)); lower $rl to s42a/run_A78/lower.log ($(grep LOWER-R2 $D/ctl_a_lower.log))"
echo DONE > $D/ctl51a.done
