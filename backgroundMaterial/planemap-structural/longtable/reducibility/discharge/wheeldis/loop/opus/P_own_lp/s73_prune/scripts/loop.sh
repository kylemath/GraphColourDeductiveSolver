# iterate add-back: loop.sh START_SET_TAG(=sets/NAME.json) ; produces sets/g<i>.json
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s73_prune
cur=$1; i=${2:-1}; K=${3:-1}
while true; do
  python3 -c "
import sys,json; sys.path.insert(0,'scripts'); from lib import *
L,off=load_uni(); write_rules('sets/cur.rules.json',L,json.load(open('$cur')))"
  VCAND=1 bash scripts/run73.sh it$i $PWD/sets/cur.rules.json set711 100000000
  echo "iter $i set $cur: $(grep -c . $cur | head -1) $(python3 -c "import json;print(len(json.load(open('$cur'))))") $(tail -1 run/it$i.log)" >> run/loop.log
  grep -q "FEASIBLE at" run/it$i.log && ! grep -q INFEASIBLE run/it$i.log && break
  python3 scripts/greedy.py run/c_it$i.txt $cur sets/g$i.json $K > run/greedy_$i.log
  cur=sets/g$i.json; i=$((i+1))
done
