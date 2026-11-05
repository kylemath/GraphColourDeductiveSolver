cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s73_prune
cur=$1; i=1
while true; do
  python3 -c "
import sys,json; sys.path.insert(0,'scripts'); from lib import *
L,off=load_uni(); write_rules('sets/curA.rules.json',L,json.load(open('$cur')))"
  VCAND=1 bash scripts/run73.sh ia$i $PWD/sets/curA.rules.json a97 100000000
  echo "iter $i set $cur: $(python3 -c "import json;print(len(json.load(open('$cur'))))") $(tail -1 run/ia$i.log)" >> run/loopA.log
  rm -rf work/ia$i
  grep -q "FEASIBLE at" run/ia$i.log && ! grep -q INFEASIBLE run/ia$i.log && break
  python3 scripts/greedy.py run/c_ia$i.txt $cur sets/ga$i.json 1 > run/greedyA_$i.log
  cur=sets/ga$i.json; i=$((i+1))
done
cp $cur sets/bothok.json
