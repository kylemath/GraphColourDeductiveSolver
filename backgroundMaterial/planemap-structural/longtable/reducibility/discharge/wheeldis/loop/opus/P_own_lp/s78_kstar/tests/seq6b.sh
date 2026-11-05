# s78 test 6b: the rrz pointer LP (seq6) with the K* cap lowered to W6's amount (0.125) and to 0.0625, then the full-engine pointer over
# the q75B K-run rows (warm/rows_q75B_snap78.txt, 3832 rows separated during the s75 K run) + the W6 pool: K* off vs on (s75 stack, FAM=full).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; P=$N/tests/t6/pool_W6support_floor.txt; cd $N
for cap in 0.125 0.0625; do
  echo "$(date -u +%H:%M:%SZ) seq6b rrz cap $cap start"
  NOLOWER=1 STACK=s77 FAM=rrz KS=1 KSCAP=$cap bash runL78.sh t6_s77_rrz_cap$cap $P 1
  echo "$(date -u +%H:%M:%SZ) seq6b rrz cap $cap done: $(grep -h '^nosep\|kstar it' $N/runL_t6_s77_rrz_cap$cap/L.log | tr '\n' ' ')"
done
for ks in 0 1; do
  echo "$(date -u +%H:%M:%SZ) seq6b q75Brows full KS=$ks start"
  NOLOWER=1 STACK=s75 FAM=full KS=$ks bash runL78.sh t6b_s75_full_ks$ks $N/warm/rows_q75B_snap78.txt,$P 1
  echo "$(date -u +%H:%M:%SZ) seq6b q75Brows full KS=$ks done: $(grep -h '^nosep\|kstar it' $N/runL_t6b_s75_full_ks$ks/L.log | tr '\n' ' ')"
done
