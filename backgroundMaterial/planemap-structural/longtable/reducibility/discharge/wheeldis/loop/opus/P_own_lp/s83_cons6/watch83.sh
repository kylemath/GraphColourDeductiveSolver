# s83: check every new in-point eng/sol_<tag>_inNN.json with U83.sh (same env + XF).  usage: [env] XF=.. nohup bash watch83.sh <tag> &
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s83_cons6; TAG=$1
while true; do
  for f in $(ls $P/eng/sol_${TAG}_in[0-9][0-9].json 2>/dev/null); do
    b=$(basename $f .json); [ -e $P/cand/$b.json ] && continue
    cp $f $P/cand/$b.json; t=$(python3 -c "import json; print(json.load(open('$P/cand/$b.json'))['t'])")
    echo "$(date -u +%H:%M:%SZ) [watch83-$TAG] candidate $b t=$t -> upperR2 flags '$XF'" >> $P/run.log
    bash $P/U83.sh $b $P/cand/$b.json "$XF"
  done
  pgrep -f "tag=$TAG " > /dev/null || { sleep 30; exit 0; }
  sleep 60
done
