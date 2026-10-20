# ccover prep: D-only tables for A66 (all C out): kill6 (U=7,8,9) with s30t s16_filter donly=1 (RSST D2 only) + k3x_D_A66, k3x_C empty;
# l3q tables likewise (l3qtab_noC.py); args = args_A66 (cpat files are dropped by the noC flag at run time).
set -e
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Z=$P/s33z; A=$Z/reg_A66; Q=$Z/ccover; cd $Q; mkdir -p f/kill
until [ -e $A/prep_done.txt ] && [ -e $Z/m89/A66/prep_done.txt ]; do sleep 60; done
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; EX=$S/ex_A66
date -u +%H:%M:%SZ > prep_start.txt
cp $P/s30t/f/s16_filter.py $P/s30t/f/s16_killnpy.py f/
TD=$A/k3x_D_A66.out; TC=$Q/k3x_C_empty.cfast
{ for U in 7 8 9; do echo "cd $Q/f && nice -n 10 python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U donly=1 > kill/kill6_U$U.log 2>&1"; done
  for sg in 1 -1; do echo "cd $Q && nice -n 10 python3 $Q/l3qtab_noC.py $EX $TD $TC tab_$sg.json $sg > tab_$sg.log 2>&1"; done; } | OMP_NUM_THREADS=1 xargs -P1 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy tab_*.json $A/f/kill/*.npy $A/tab_*.json > md5_prep.txt
date -u +%H:%M:%SZ > prep_end.txt; echo DONE > prep_done.txt
