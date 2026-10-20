# waits for round 2 (resume_s35f.sh -> done.txt), then runs round 3 on A67 (a67/resume_a67.sh) at nice 15
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s35f
for i in $(seq 1 1440); do [ -f done.txt ] && break; sleep 60; done
[ -f done.txt ] && nice -n 15 bash a67/resume_a67.sh > a67/run.log 2>&1
