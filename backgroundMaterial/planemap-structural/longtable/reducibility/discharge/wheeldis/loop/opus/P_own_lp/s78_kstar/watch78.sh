# s78: every new in-point candidate eng/sol_<tag>_inNN.json of a runK78 run is copied to cand/ and checked by upperR2 (upper78.sh, 1 thread,
# the SAME STACK/FAM/KS/EGK as the K run: pass them in the environment).  usage: STACK=.. FAM=full KS=1 EGK=.. nohup bash watch78.sh <tag> > logs/watch_<tag>.out 2>&1 &
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar; TAG=$1
while true; do
  for f in $(ls $N/eng/sol_${TAG}_in[0-9][0-9].json 2>/dev/null); do
    b=$(basename $f .json); [ -e $N/cand/$b.json ] && continue
    cp $f $N/cand/$b.json; t=$(python3 -c "import json; print(json.load(open('$N/cand/$b.json'))['t'])")
    echo "$(date -u +%H:%M:%SZ) [watch78-$TAG] candidate $b t=$t -> upperR2 (STACK=${STACK:-s75} FAM=${FAM:-full} KS=${KS:-0} EGK=$(basename ${EGK:-none}))" >> $N/run.log
    bash $N/upper78.sh $b $N/cand/$b.json 1
  done
  pgrep -f "tag=$TAG " > /dev/null || { sleep 30; ls $N/eng/sol_${TAG}_in[0-9][0-9].json 2>/dev/null | while read f; do [ -e $N/cand/$(basename $f) ] || echo "$(date -u +%H:%M:%SZ) [watch78-$TAG] unchecked $f at exit" >> $N/run.log; done; exit 0; }
  sleep 60
done
