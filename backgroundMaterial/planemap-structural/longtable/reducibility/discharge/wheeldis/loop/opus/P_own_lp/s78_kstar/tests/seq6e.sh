# s78 test 6e: pointer LPs with the generic EDGE keys (A1 C1 E1, eng/edgekeys_r4.txt): W6 pool (rrz, s77) and the b77U6 dual support (base, s75);
# EDGE alone, and EDGE + K*; caps 3 and 0.125.  nosep, no lowerR2.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; cd $N; EK=$N/eng/edgekeys_r4.txt
P1=$N/tests/t6/pool_W6support_floor.txt; P2=$N/tests/t6/pool_b77U6dual_floor.txt
for cfg in "s77 rrz 0 3 $P1 w6" "s77 rrz 1 3 $P1 w6" "s77 rrz 0 0.125 $P1 w6" "s75 base 0 3 $P2 u6" "s75 base 1 3 $P2 u6" "s75 base 0 0.125 $P2 u6" "s75 base 1 0.125 $P2 u6"; do set -- $cfg
  tg=t6e_$6_$2_ks$3_cap$4
  NOLOWER=1 STACK=$1 FAM=$2 KS=$3 EGK=$EK KSCAP=$4 bash runL78.sh $tg $5 1
  echo "$(date -u +%H:%M:%SZ) seq6e $tg done: $(grep -h '^nosep\|kstar it' $N/runL_$tg/L.log | tr '\n' ' ' | cut -c1-400)"
done
