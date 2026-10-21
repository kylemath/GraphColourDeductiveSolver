# s47 controls on the full reg_A78 V = 8 table (s47/tabV8_A78): (b') upper with l3qV=7,8, (c) hand-made V = 8 solution,
# correct sign vs brokensignV, (c3) q8 = 1 (payee side live); (s1) smoke solve: 2 separation rounds from 3000 s42a rows + lowerR2.
# usage: bash ctl47f.sh DT DQ
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s47/env47.sh
DT=${1:-0.003}; DQ=${2:-0.002}; TV=$D/tabV8_A78
until [ -e $TV/tabV8.done ]; do sleep 20; done
V8F="l3qV=7,8 l3qtab8=$TV/tabV8_1.json,$TV/tabV8_-1.json"; C=$D/ctl_c; cd $E; note "full-table controls start (DT $DT DQ $DQ)"
python3 - $TV <<'PY' > $D/ctl_tabcheck.txt
import json, sys
n = bad = 0
for sg in ('1', '-1'):
    F = json.load(open('%s/tabV8_%s.json' % (sys.argv[1], sg)))
    P = json.load(open('/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s45/tabV/tabV8cert_%s.json' % sg))
    for k, v in P.items(): n += 1; bad += F[k][0] != v[0]
    print('side', sg, 'full', len(F), 'masks; s45 cert keys', len(P))
print('s45 cert-key V = 8 masks vs full A78 table: %d keys, %d differ' % (n, bad))
PY
if [ ! -e $D/ctl_b2.done ]; then
nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8F nomax sol=$SOL $A threads=1 work=$SC/P/wr47_b2 > $D/ctl_b2_upper_V8full.log 2>&1
note "control (b'), full table: $(grep UPPER-R2 $D/ctl_b2_upper_V8full.log)"; date > $D/ctl_b2.done
nice -n 10 python3 pcheck.py lowerR2 $FQ $X $V8F cert=$CERT xcap=3 $A work=$SC/P/wr47_d2 > $D/ctl_d2_lower_V8full.log 2>&1
note "control (d'), full table: $(grep LOWER-R2 $D/ctl_d2_lower_V8full.log)"
fi
python3 $C/mksol.py $SOL $C/sol_f1.json $DT $DQ > $C/mksol_f.out
nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8F nomax sol=$C/sol_f1.json $A threads=1 vfile=$C/f1_viol.txt work=$SC/P/wr47_f1 > $D/ctl_c1f_upper.log 2>&1
nice -n 10 python3 pcheck.py upperR2 $FQ $X $V8F brokensignV nomax sol=$C/sol_f1.json $A threads=1 vfile=$C/f2_viol.txt work=$SC/P/wr47_f2 > $D/ctl_c2f_upper_broken.log 2>&1
nice -n 10 python3 pcheck.py upperR2 $FQ $X nomax sol=$SOL $A threads=1 work=$SC/P/wr47_f0 > /dev/null 2>&1
note "control (c), full table, t + $DT, q[(8,6,6,5)] = $DQ: correct sign $(grep UPPER-R2 $D/ctl_c1f_upper.log) | brokensignV $(grep UPPER-R2 $D/ctl_c2f_upper_broken.log)"
echo DONE > $D/ctl47f.done
