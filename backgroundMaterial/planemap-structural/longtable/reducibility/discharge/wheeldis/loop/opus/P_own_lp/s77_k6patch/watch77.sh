# s77: every new in-point candidate eng/sol_<tag>_inNN.json -> cand/ -> upperR2 on the patched stack (upper77.sh, 1 thread, same FAM as the K).
# Waits while a file s77_k6patch/HOLD_WATCH exists (keeps my total at 2 threads while an L runs).  usage: FAM=.. nohup bash watch77.sh <tag> &
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch; TAG=$1
while true; do
  for f in $(ls $N/eng/sol_${TAG}_in[0-9][0-9].json 2>/dev/null); do
    [ -e $N/HOLD_WATCH ] && break
    b=$(basename $f .json); [ -e $N/cand/$b.json ] && continue
    cp $f $N/cand/$b.json; t=$(python3 -c "import json; print(json.load(open('$N/cand/$b.json'))['t'])")
    echo "$(date -u +%H:%M:%SZ) [watch77-$TAG] candidate $b t=$t -> upperR2 (FAM=${FAM:-base})" >> $N/run.log
    bash $N/upper77.sh $b $N/cand/$b.json 1
  done
  pgrep -f "tag=$TAG " > /dev/null || { [ -e $N/HOLD_WATCH ] || { sleep 30; ls $N/eng/sol_${TAG}_in[0-9][0-9].json 2>/dev/null | while read f; do [ -e $N/cand/$(basename $f) ] || echo "$(date -u +%H:%M:%SZ) [watch77-$TAG] unchecked $f at exit" >> $N/run.log; done; exit 0; }; }
  sleep 60
done
