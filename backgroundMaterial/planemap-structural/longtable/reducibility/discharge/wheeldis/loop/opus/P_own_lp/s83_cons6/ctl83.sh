B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; P=$B/s83_cons6; R=$B/s81_w16chk
AF=$B/s79_routeF/args_A97_F.txt; EG=$B/s78_kstar/eng/edgekeys_r4.txt; CE=$R/exact_xPK_s77F_ksEG/cert_z_exb.json; RW=$R/rows_xP_allK_recv.txt
chk() { # tag flags
  ( export STACK=s77 ARGS=$AF FAM=full KS=1 EGK=$EG; . $P/env83.sh; WK=$SD/wr83c_$1; mkdir -p $WK; cd $E83
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$CE xcap=3 $A work=$WK $2 norepair > $P/ctl_$1.log 2>&1; rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s83-ctl-$1] s83 eng lowerR2 '$2 norepair' on the equality floor cert xPK_s77F_ksEG exb (0.005802654): $(grep LOWER-R2 $P/ctl_$1.log | tail -1 | cut -c1-120); wrong-sign rows $(grep -c 'WRONG SIGN' $P/ctl_$1.log) ($(grep 'WRONG SIGN' $P/ctl_$1.log | awk '{print $3}' | sort | uniq -c | tr '\n' ' '))" >> $P/run.log )
}
chk reg ""
chk neg "c6le"
( export STACK=s77 ARGS=$AF FAM=full KS=1 EGK=$EG; bash $P/L83.sh xPK_c6_ksEG $RW "c6le conssep" )
( export STACK=s77 ARGS=$AF FAM=full KS=1 EGK=$EG; bash $P/L83.sh xPK_eq_ksEG $RW "conssep" )
( export STACK=s77 ARGS=$AF FAM=full KS=0; bash $P/L83.sh xPK_c6_full $RW "c6le conssep" )
echo "$(date -u +%H:%M:%SZ) [s83] CTL DONE" >> $P/run.log
