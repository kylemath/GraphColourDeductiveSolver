# wait for reg_A64 prep, then run the stacked chain on A64 at threads=2
S=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s33z
until [ -e $S/reg_A64/prep_done.txt ]; do sleep 60; done
bash $S/cmd_s33.sh A64 2
