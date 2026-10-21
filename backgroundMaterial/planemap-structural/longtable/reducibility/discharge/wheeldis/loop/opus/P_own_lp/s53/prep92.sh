# A92 (main e3d45d7d): registry prep, then V=8 tables
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
cd $B/s33z && bash prep_tag.sh A92 e3d45d7d > prep_A92.out 2>&1 && cd $B/s47 && bash tabV8_A92.sh > tabV8_A92/nohup.out 2>&1
