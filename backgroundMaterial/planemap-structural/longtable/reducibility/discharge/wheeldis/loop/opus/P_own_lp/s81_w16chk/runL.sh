B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s81_w16chk; K=$B/s78_kstar
A97=$B/s33z/reg_A97/args_A97.txt; AF=$B/s79_routeF/args_A97_F.txt; EG=$K/eng/edgekeys_r4.txt; W=$R/rows_x567_recv.txt
cd $K
STACK=s75 ARGS=$A97 FAM=full KS=0 bash runL78.sh w567_s75_full $W 1
STACK=s77 ARGS=$AF FAM=full KS=0 bash runL78.sh w567_s77F_full $W 1
STACK=s75 ARGS=$A97 FAM=full KS=1 bash runL78.sh w567_s75_ks $W 1
STACK=s77 ARGS=$AF FAM=full KS=1 bash runL78.sh w567_s77F_ks $W 1
STACK=s77 ARGS=$AF FAM=full KS=1 EGK=$EG bash runL78.sh w567_s77F_ksEG $W 1
echo "$(date -u +%H:%M:%SZ) [s81] L DONE" >> $R/run.log
