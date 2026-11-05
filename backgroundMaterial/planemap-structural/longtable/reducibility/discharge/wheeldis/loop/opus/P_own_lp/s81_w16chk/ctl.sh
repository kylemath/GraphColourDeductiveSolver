B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s81_w16chk
lw() { # tag cert KS STACK ARGS
  ( export ARGS=$5 STACK=$4 FAM=full KS=$3; . $B/s78_kstar/env78.sh; WK=$SD/wr81_$1; mkdir -p $WK; cd $B/s78_kstar/eng
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$R/$2 xcap=3 $A work=$WK > $R/lower_$1.log 2>&1; rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s81-$1] STACK=$4 ARGS=$(basename $5) FAM=full KS=$3 cert $2: $(grep 'LOWER-R2' $R/lower_$1.log | tail -1 | cut -c1-200)" >> $R/run.log )
}
A97=$B/s33z/reg_A97/args_A97.txt
lw ctl_all_s75 x567SO_all_cert.json 0 s75 $A97
lw ctl_all_s77 x567SO_all_cert.json 0 s77 $A97
lw ctl_allK_s75 x567SO_allK_cert.json 1 s75 $A97
echo "$(date -u +%H:%M:%SZ) [s81] CTL DONE" >> $R/run.log
