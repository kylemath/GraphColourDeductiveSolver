cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s54
while read -r c; do
  while [ $(ps -eo args | awk '$1=="python3" && $2=="pcheck.py"' | wc -l) -ge 3 ]; do sleep 10; done
  bash -c "$c" & sleep 15
done < checks/jobs.txt; wait
