. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s69_rrzq7/env69.sh
cd $N/eng; F="$FUP f2b=$RULES hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3"
for v in plain brokenkey brokensign; do ex=""; [ $v != plain ] && ex=$v
 nice -n 15 python3 pcheck.py orientR2 $F $ex $X $A work=$N/work_orient_$v threads=2 > $N/logs/orient_$v.log 2>&1; done
