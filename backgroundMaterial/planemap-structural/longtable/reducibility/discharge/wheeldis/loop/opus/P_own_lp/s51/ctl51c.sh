# s51 control (c), upper part: the s42a A78 solution converted to xo (conv51.py; old x on every outer-letter completion)
# checked by upperR2 xo: correct build, xobroken=sign (receiver gets -XQ), xobroken=end (u reads the far outer letter).
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s51/env51.sh
cd $E; SV=$D/sol_conv_q42aA78.json; note "control (c) upper start"
for b in none sign end; do
  BF=; [ $b != none ] && BF=xobroken=$b
  nice -n 10 python3 pcheck.py upperR2 $FQ $X xo $BF nomax sol=$SV $A threads=1 work=$SC/P/wr51_c$b > $D/ctl_c_upper_$b.log 2>&1
done
note "control (c) upper, converted s42a sol: correct $(grep UPPER-R2 $D/ctl_c_upper_none.log) | sign-broken $(grep UPPER-R2 $D/ctl_c_upper_sign.log) | end-broken $(grep UPPER-R2 $D/ctl_c_upper_end.log)"
echo DONE > $D/ctl51c.done
