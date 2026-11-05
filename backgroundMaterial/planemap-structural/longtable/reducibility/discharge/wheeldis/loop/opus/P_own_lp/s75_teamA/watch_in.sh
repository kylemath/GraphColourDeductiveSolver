# s75 Team A: every new in-point candidate eng/sol_<tag>_inNN.json is copied to cand/ and checked by upperR2 (upper75.sh, 1 thread). usage: nohup bash watch_in.sh <tag> &
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA; TAG=$1
while true; do
  for f in $(ls $N/eng/sol_${TAG}_in[0-9][0-9].json 2>/dev/null); do
    b=$(basename $f .json); [ -e $N/cand/$b.json ] && continue
    cp $f $N/cand/$b.json; t=$(python3 -c "import json; print(json.load(open('$N/cand/$b.json'))['t'])")
    echo "$(date -u +%H:%M:%SZ) [watch-$TAG] candidate $b t=$t -> upperR2" >> $N/run.log
    python3 -c "import json; s=json.load(open('$N/cand/$b.json')); s['q7'] = True if not s.get('q') else s['q7']; s['q7m'] = True if not s.get('q') else s['q7m']; json.dump(s, open('$N/cand/${b}_full.json', 'w'))"   # q = 0 (or q7 run): full-stack flags (flags-on-at-zero is a passed control)
    bash $N/upper75.sh $b $N/cand/${b}_full.json 1
  done
  pgrep -f "tag=$TAG " > /dev/null || { sleep 30; ls $N/eng/sol_${TAG}_in[0-9][0-9].json 2>/dev/null | while read f; do [ -e $N/cand/$(basename $f) ] || echo "$(date -u +%H:%M:%SZ) [watch-$TAG] unchecked $f at exit" >> $N/run.log; done; exit 0; }
  sleep 60
done
