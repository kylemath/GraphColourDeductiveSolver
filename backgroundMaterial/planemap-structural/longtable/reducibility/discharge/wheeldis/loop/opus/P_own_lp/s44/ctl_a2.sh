# s44 (cont.): control (a) lower half rerun on the repaired engine: fb off, A74 n3 cert -> byte-identical to s39o lower.log
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
cd $E; nice -n 10 python3 pcheck.py lowerR2 $FQ $X cert=$N3/cert_q39n3A74L.json xcap=3 $A work=$SC/P/wr44_ctla2 > $D/ctl_rep/a2_lower_off.log 2>&1
cmp $D/ctl_rep/a2_lower_off.log $N3/lower.log && r="byte-identical to s39o" || r="DIFFERS from s39o"; note "control (a) lower rerun on repaired engine: $r"; echo "$r" > $D/ctl_rep/a2.done
