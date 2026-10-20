# s42a control: s39o/eng with the exname port, no exname option, reproduces the A74 n3 lower log byte-for-byte
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s42a/env42.sh
Q4=$S/reg_A74; A4="root=$M args=$Q4/args_A74.txt rpat=$B/rpatD.txt"
F4="xon apexcls filt16 killtab=$Q4/f/kill/kill6 hat5 consall l3q l3qtab=$Q4/tab_1.json,$Q4/tab_-1.json lqcap=3"
cd $E; dfok
nice -n 5 python3 pcheck.py lowerR2 $F4 $X cert=$H/run_n3_A74/cert_q39n3A74L.json xcap=3 $A4 work=${WK}ctl > $D/ctl_lower_A74_noopt.log 2>&1
if cmp -s $D/ctl_lower_A74_noopt.log $H/run_n3_A74/lower.log; then r=BYTE-IDENTICAL; else r=DIFFERS; fi
note "control (exname port, no option, A74 n3 cert lowerR2 vs run_n3_A74/lower.log): $r"; rm -rf ${WK}ctl; echo $r > $D/ctl.done
