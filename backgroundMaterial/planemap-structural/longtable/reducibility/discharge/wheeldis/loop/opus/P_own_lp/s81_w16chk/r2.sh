B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s81_w16chk; K=$B/s78_kstar
AF=$B/s79_routeF/args_A97_F.txt; EG=$K/eng/edgekeys_r4.txt
( export STACK=s77 ARGS=$AF FAM=full KS=1; . $K/env78.sh; WK=$SD/wr81r2; mkdir -p $WK; cd $K/eng
  nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$R/xP_allK_cert.json xcap=3 $A work=$WK > $R/lower_xP_allK_s77F.log 2>&1; rm -rf $WK
  echo "$(date -u +%H:%M:%SZ) [s81-xP_allK_s77F] STACK=s77+F FAM=full KS=1 cert xP_allK (md5 172e4a8e): $(grep 'LOWER-R2' $R/lower_xP_allK_s77F.log | tail -1 | cut -c1-200)" >> $R/run.log )
cd $K && STACK=s77 ARGS=$AF FAM=full KS=1 EGK=$EG bash runL78.sh xPK_s77F_ksEG $R/rows_xP_allK_recv.txt 1
echo "$(date -u +%H:%M:%SZ) [s81] R2 L DONE" >> $R/run.log
