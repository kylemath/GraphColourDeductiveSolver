# waits for the running prep_tag.sh A67 2c97e14d, then the resumable pipeline (re-run "bash resume_s33.sh A67 2c97e14d" after any restart)
S=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s33z
until [ -e $S/reg_A67/prep_done.txt ]; do sleep 60; done
cd $S && bash resume_s33.sh A67 2c97e14d > $S/resume_A67.out 2>&1
