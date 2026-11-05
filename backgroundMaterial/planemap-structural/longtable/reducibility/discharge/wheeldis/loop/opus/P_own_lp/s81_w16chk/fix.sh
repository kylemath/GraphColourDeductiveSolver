B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s81_w16chk
lw() { # tag cert KS STACK ARGS EGK
  ( export ARGS=$5 STACK=$4 FAM=full KS=$3; [ -n "$6" ] && export EGK=$6; . $B/s78_kstar/env78.sh; WK=$SD/wr81_$1; mkdir -p $WK; cd $B/s78_kstar/eng
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$R/$2 xcap=3 $A work=$WK > $R/lower_$1.log 2>&1; rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s81-$1] STACK=$4 ARGS=$(basename $5) FAM=full KS=$3 EGK=$(basename ${6:-none}) cert $2: $(grep 'LOWER-R2' $R/lower_$1.log | tail -1 | cut -c1-200)" >> $R/run.log )
}
A97=$B/s33z/reg_A97/args_A97.txt; AF=$B/s79_routeF/args_A97_F.txt; EG=$B/s78_kstar/eng/edgekeys_r4.txt
lw allK5_s75 x567SO_allK_cert_sig5.json 1 s75 $A97
lw allK5_s77F x567SO_allK_cert_sig5.json 1 s77 $AF
lw allK5_s75EG x567SO_allK_cert_sig5.json 1 s75 $A97 $EG
