B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; P=$B/s83_cons6
AF=$B/s79_routeF/args_A97_F.txt; AC=$B/s82_w13C/args_A97_F_C3.txt
run() {  # tag args fam ks
  ( export STACK=s77 ARGS=$2 FAM=$3 KS=$4; . $P/env83.sh; WK=$SD/wr83r4_$1; mkdir -p $WK; cd $E83
    nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$P/w16r4/$1_cert.json xcap=3 $A work=$WK c6le > $P/lower_w16r4_$1.log 2>&1; rm -rf $WK
    echo "$(date -u +%H:%M:%SZ) [s83-w16r4-$1] c6le STACK=s77 ARGS=$(basename $2) FAM=$3 KS=$4 cert W16 round4 $1 (md5 $(md5sum $P/w16r4/$1_cert.json | cut -c1-8)): $(grep 'LOWER-R2' $P/lower_w16r4_$1.log | tail -1 | cut -c1-200) | wrong-sign $(grep -c 'WRONG SIGN' $P/lower_w16r4_$1.log)" >> $P/run.log )
}
run x4_P_all $AF full 0
run x4_P_allK $AF full 1
run x4_C_all $AC full 0
run x4_C_allK $AC full 1
run x4_P_rrz $AF rrz 0
run x4_P_base $AF base 0
echo "$(date -u +%H:%M:%SZ) [s83] R4 DONE" >> $P/run.log
