B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; P=$B/s83_cons6; W6=$P/w16r6
AC=$B/s82_w13C/args_A97_F_C3.txt
run() {  # tag cert args fam ks
  ( export STACK=s77 ARGS=$3 FAM=$4 KS=$5; . $P/env83.sh; WK=$SD/wr83r6_$1; mkdir -p $WK; cd $E83
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$W6/$2_cert.json xcap=3 $A work=$WK c6le > $W6/lower_$1.log 2>&1; rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s83-w16r6-$1] c6le STACK=s77 ARGS=$(basename $3) FAM=$4 KS=$5 cert W16 round6 $2 (md5 $(md5sum $W6/$2_cert.json | cut -c1-8)): $(grep 'LOWER-R2' $W6/lower_$1.log | tail -1 | cut -c1-200) | wrong-sign $(grep -c 'WRONG SIGN' $W6/lower_$1.log)" >> $P/run.log )
}
run a_SF x6_SF_W13 $W6/args_SF_W13.txt full 1
run b_AF x6_AF_W13 $W6/args_AF_W13.txt full 1
run c_AC x6_AF_C3 $AC full 1
run a_AF x6_SF_W13 $W6/args_AF_W13.txt full 1
run neg_b_on_SF x6_AF_W13 $W6/args_SF_W13.txt full 1
run neg_c_on_AFW13 x6_AF_C3 $W6/args_AF_W13.txt full 1
echo "$(date -u +%H:%M:%SZ) [s83] R6b DONE" >> $P/run.log
