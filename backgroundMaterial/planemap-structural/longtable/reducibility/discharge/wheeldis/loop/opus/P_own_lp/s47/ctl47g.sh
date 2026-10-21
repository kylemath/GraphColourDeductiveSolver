# s47 control (c) scan: t + DT, q[(8,6,6,5)] = DQ with DT = 2 DQ (the tight d = 8 rows carry lQ (8,6,6,31) twice), correct vs brokensignV
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s47/env47.sh
TV=$D/tabV8_A78; V8F="l3qV=7,8 l3qtab8=$TV/tabV8_1.json,$TV/tabV8_-1.json"; C=$D/ctl_c; cd $E
for p in "0.4 0.2" "1.0 0.5"; do set -- $p; n=g_$1_$2
  python3 $C/mksol.py $SOL $C/sol_$n.json $1 $2 >> $C/mksol_g.out
  nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8F nomax sol=$C/sol_$n.json $A threads=1 vfile=$C/${n}_ok_viol.txt work=$SC/P/wr47_g > $D/ctl_c_${n}_upper.log 2>&1
  nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8F brokensignV nomax sol=$C/sol_$n.json $A threads=1 vfile=$C/${n}_br_viol.txt work=$SC/P/wr47_g > $D/ctl_c_${n}_upper_broken.log 2>&1
  note "control (c) scan t + $1, q[(8,6,6,5)] = $2: correct $(grep UPPER-R2 $D/ctl_c_${n}_upper.log) | brokensignV $(grep UPPER-R2 $D/ctl_c_${n}_upper_broken.log)"
done; echo DONE > $D/ctl47g.done
