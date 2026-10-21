# s47 control (c): a mis-signed V = 8 term (brokensignV: the d = 7 payer term at a link 8 read as +max_a2 q instead of -q)
# must make the upper check fail on a hand-made V = 8 solution that the correct check accepts. c3: the payee side is live.
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s47/env47.sh
until [ -e $D/ctl47.done ]; do sleep 20; done
C=$D/ctl_c; cd $E; note "control (c) start"
python3 $C/mksol.py $SOL $C/sol_c1.json 0.02 0.015 > $C/mksol.out
python3 $C/mksol.py $SOL $C/sol_c3.json 0.02 1.0 >> $C/mksol.out
nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8A78 nomax sol=$C/sol_c1.json $A threads=1 work=$SC/P/wr47_c1 > $D/ctl_c1_upper_V8.log 2>&1
nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8A78 brokensignV nomax sol=$C/sol_c1.json $A threads=1 vfile=$C/c2_viol.txt work=$SC/P/wr47_c2 > $D/ctl_c2_upper_V8_broken.log 2>&1
nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8A78 nomax sol=$C/sol_c3.json $A threads=1 vfile=$C/c3_viol.txt work=$SC/P/wr47_c3 > $D/ctl_c3_upper_V8_big.log 2>&1
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$C/sol_c1.json $A threads=1 work=$SC/P/wr47_c4 > $D/ctl_c4_upper_V8off.log 2>&1
note "control (c): c1 correct sign $(grep UPPER-R2 $D/ctl_c1_upper_V8.log) | c2 brokensignV $(grep UPPER-R2 $D/ctl_c2_upper_V8_broken.log) | c3 q8 = 1 $(grep UPPER-R2 $D/ctl_c3_upper_V8_big.log) | c4 l3qV=7 on a V8 sol: $(tail -1 $D/ctl_c4_upper_V8off.log)"
echo DONE > $D/ctl47c.done
