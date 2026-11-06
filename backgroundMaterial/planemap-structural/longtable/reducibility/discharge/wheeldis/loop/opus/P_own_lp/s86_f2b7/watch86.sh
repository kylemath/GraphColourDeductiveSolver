# s86: check every new in-point eng/sol_<tag>_inNN.json with U86.sh (STACK/ARGS/KEYS from the env; extra flags in $XF).  usage: [env] XF=c6le nohup bash watch85.sh <tag> &
Z=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; TAG=$1; mkdir -p $Z/cand
while true; do
  for f in $(ls $Z/eng/sol_${TAG}_in[0-9][0-9].json 2>/dev/null); do
    b=$(basename $f .json); [ -e $Z/cand/$b.json ] && continue
    cp $f $Z/cand/$b.json; t=$(python3 -c "import json; print(json.load(open('$Z/cand/$b.json'))['t'])")
    echo "$(date -u +%H:%M:%SZ) [watch86-$TAG] candidate $b t=$t -> upperR2 gkwin gkleaf $XF" >> $Z/run.log
    bash $Z/U86.sh $b $Z/cand/$b.json 1 $XF
  done
  pgrep -f "tag=$TAG " > /dev/null || { sleep 30; exit 0; }
  sleep 60
done
