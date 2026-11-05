# s78 test 6: nosep LP (runL78 style, no x penalty) over W6's round-3 dual support receivers (297) + the 3 floor-cert receivers, every
# sender row, the engine's conservation basis, mrow closures; family sets full (engine q7) and rrz (no q7); K* off vs on.  B1-patched stack (s77).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; P=$N/tests/t6/pool_W6support_floor.txt; cd $N
for cfg in "full 0" "full 1" "rrz 0" "rrz 1"; do set -- $cfg
  echo "$(date -u +%H:%M:%SZ) seq6 FAM=$1 KS=$2 start"
  STACK=${T6STACK:-s77} FAM=$1 KS=$2 bash runL78.sh t6_${T6STACK:-s77}_$1_ks$2 $P 1
  echo "$(date -u +%H:%M:%SZ) seq6 FAM=$1 KS=$2 done: $(grep -h '^nosep\|kstar it' $N/runL_t6_${T6STACK:-s77}_$1_ks$2/L.log | tr '\n' ' ') $(grep -h 'LOWER-R2' $N/runL_t6_${T6STACK:-s77}_$1_ks$2/lower.log | tail -1)"
done
