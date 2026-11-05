# s81: lowerR2 replays of W16's 5/6/7-world certificates on our current stack (A97 + patched-298 kill6 + B3 route F), s78 engine (K*/EDGE).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; R=$B/s81_w16chk
lw() { # tag cert KS EGK FAM
  ( export ARGS=$B/s79_routeF/args_A97_F.txt STACK=s77 FAM=$5 KS=$3; [ -n "$4" ] && export EGK=$4; . $B/s78_kstar/env78.sh; WK=$SD/wr81_$1; mkdir -p $WK; cd $B/s78_kstar/eng
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$R/$2 xcap=3 $A work=$WK > $R/lower_$1.log 2>&1; rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s81-$1] STACK=s77+routeF FAM=$5 KS=$3 EGK=$(basename ${4:-none}) cert $2 (md5 $(md5sum < $R/$2 | cut -c1-8)): $(grep 'LOWER-R2' $R/lower_$1.log | tail -1 | cut -c1-200)" >> $R/run.log )
}
EG=$B/s78_kstar/eng/edgekeys_r4.txt
lw all_full x567SO_all_cert.json 0 "" full
lw allK_ks x567SO_allK_cert.json 1 "" full
lw allK_ksEG x567SO_allK_cert.json 1 $EG full
lw all_ksEG x567SO_all_cert.json 1 $EG full
echo "$(date -u +%H:%M:%SZ) [s81] DONE" >> $R/run.log
