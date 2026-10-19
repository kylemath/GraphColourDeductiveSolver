# wait for reg_A63 prep, then run the stacked chain on A63 at threads=2
S=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s33z
until [ -e $S/reg_A63/prep_done.txt ]; do sleep 60; done
bash $S/cmd_s33.sh A63 2
