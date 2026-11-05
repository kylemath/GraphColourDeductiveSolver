B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s81_w16chk; K=$B/s78_kstar
AF=$B/s79_routeF/args_A97_F.txt; AC=$B/s82_w13C/args_A97_F_C3.txt; EG=$K/eng/edgekeys_r4.txt
run() {  # tag args egk
  ( export STACK=s77 ARGS=$2 FAM=full KS=1; [ -n "$3" ] && export EGK=$3; . $K/env78.sh; WK=$SD/wr81r3_$1; mkdir -p $WK; cd $K/eng
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$R/w16r3/$1_cert.json xcap=3 $A work=$WK > $R/lower_w16r3_$1.log 2>&1; rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s81-w16r3-$1] STACK=s77 ARGS=$(basename $2) KS=1 EGK=${3:+r4} cert W16 round3 $1 (md5 $(md5sum $R/w16r3/$1_cert.json | cut -c1-8)): $(grep 'LOWER-R2' $R/lower_w16r3_$1.log | tail -1 | cut -c1-200)" >> $R/run.log )
}
run xC_allK $AC
run xC_allKE $AC $EG
run xP_allKE $AF $EG
echo "$(date -u +%H:%M:%SZ) [s81] R3 DONE" >> $R/run.log
