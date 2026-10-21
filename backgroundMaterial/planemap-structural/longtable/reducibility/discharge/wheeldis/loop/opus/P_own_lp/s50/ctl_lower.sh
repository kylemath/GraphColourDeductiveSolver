# control: engine lowerR2 on a cert (args: REG CERT TAG)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s50/env50.sh
reg $1; cd $E
nice -n 10 python3 pcheck.py lowerR2 $FQ $X cert=$2 xcap=3 $A threads=1 work=$SC/P/wr50_$3 > $D/ctl_lower_$3.log 2>&1
