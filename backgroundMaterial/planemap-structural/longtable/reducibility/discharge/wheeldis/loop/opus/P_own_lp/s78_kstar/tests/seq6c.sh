# s78 test 6c: pointer LP over a real binding set with t > 0: the 293 receiver rows of the dual support of s77 L b77U6 (nosep, FAM=base,
# unpatched kill6, C627 args, t* 0.026384) + the 3 floor receivers; our A97 args, s75 stack; FAM base and full, K* off vs on.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; P=$N/tests/t6/pool_b77U6dual_floor.txt; cd $N
for cfg in "base 0" "base 1" "full 0" "full 1"; do set -- $cfg
  echo "$(date -u +%H:%M:%SZ) seq6c FAM=$1 KS=$2 start"
  NOLOWER=1 STACK=s75 FAM=$1 KS=$2 bash runL78.sh t6c_s75_$1_ks$2 $P 1
  echo "$(date -u +%H:%M:%SZ) seq6c FAM=$1 KS=$2 done: $(grep -h '^nosep\|kstar it' $N/runL_t6c_s75_$1_ks$2/L.log | tr '\n' ' ')"
done
