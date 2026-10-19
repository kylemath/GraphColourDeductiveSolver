cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s31
for i in $(seq 1 240); do [ -f prep_done.txt ] && break; sleep 30; done
[ -f prep_done.txt ] && bash cmd_s31.sh > run.log 2>&1
