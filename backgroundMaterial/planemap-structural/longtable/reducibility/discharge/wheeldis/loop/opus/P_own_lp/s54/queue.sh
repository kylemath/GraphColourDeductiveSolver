# s54 queue.sh "cmd" ...: run each command when fewer than 3 engine processes (pcheck.py) are running
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s54
for c in "$@"; do
  sleep $((RANDOM % 20 + 5))
  while [ $(pgrep -fc "python3 pcheck.py") -ge 3 ]; do sleep 30; done
  bash -c "$c"
done
