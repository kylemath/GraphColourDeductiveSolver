# s78 test 6d: the 6c base-family pointer (b77U6 dual-support receivers + floor) with the K* cap at W6's amount 0.125 and at 0.0625
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; P=$N/tests/t6/pool_b77U6dual_floor.txt; cd $N
for cap in 0.125 0.0625; do
  NOLOWER=1 STACK=s75 FAM=base KS=1 KSCAP=$cap bash runL78.sh t6c_s75_base_cap$cap $P 1
  echo "$(date -u +%H:%M:%SZ) seq6d base cap $cap done: $(grep -h '^nosep\|kstar it' $N/runL_t6c_s75_base_cap$cap/L.log | tr '\n' ' ')"
done
