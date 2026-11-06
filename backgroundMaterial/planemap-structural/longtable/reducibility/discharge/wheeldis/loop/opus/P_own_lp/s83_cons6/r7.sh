B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; P=$B/s83_cons6; W7D=$P/w16r7
run() {  # tag cert args fam ks
  ( export STACK=s77 ARGS=$3 FAM=$4 KS=$5; . $P/env83.sh; WK=$SD/wr83r7_$1; mkdir -p $WK; cd $E83
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$W7D/$2_cert.json xcap=3 $A work=$WK c6le > $W7D/lower_$1.log 2>&1; rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s83-w16r7-$1] c6le STACK=s77 ARGS=$(basename $3) FAM=$4 KS=$5 cert W16 round7 $2 (md5 $(md5sum $W7D/$2_cert.json | cut -c1-8)): $(grep 'LOWER-R2' $W7D/lower_$1.log | tail -1 | cut -c1-200) | wrong-sign $(grep -c 'WRONG SIGN' $W7D/lower_$1.log) | patterns $(grep -o "by kind {[^}]*}" $W7D/lower_$1.log | head -1)" >> $P/run.log )
}
run SF108 x7_SF_108 $W7D/args_SF_108.txt full 1
run AF108 x7_AF_108 $W7D/args_AF_108.txt full 1
run SF99 x7_SF_99 $W7D/args_SF_99.txt full 1
run AF99 x7_AF_99 $W7D/args_AF_99.txt full 1
run neg_SF99_on_SF108 x7_SF_99 $W7D/args_SF_108.txt full 1
run neg_SF108_on_SFbase x7_SF_108 $B/s79_routeF/args_studio_full_F.txt full 1
echo "$(date -u +%H:%M:%SZ) [s83] R7 DONE" >> $P/run.log
