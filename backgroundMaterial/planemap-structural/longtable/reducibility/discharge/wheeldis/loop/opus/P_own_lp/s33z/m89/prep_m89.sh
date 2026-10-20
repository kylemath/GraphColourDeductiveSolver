# m89 prep: registry A64 minus the 89 CGLUE-XRING C entries (27964810 list). Only k3x_C changes (k3x_C_A64m89.cfast, 992 C).
# Rebuild kill6 (U=7,8,9), killnpy, l3q tables, dcount; md5 compare against reg_A64.
set -e
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Z=$P/s33z; Q=$Z/m89; A=$Z/reg_A64; cd $Q; mkdir -p f/kill
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; EX=$S/ex_A64
date -u +%H:%M:%SZ > prep_start.txt
cp $P/s31/f/s16_filter.py $P/s31/f/s16_killnpy.py f/
TD=$A/k3x_D_A64.out; TC=$Q/k3x_C_A64m89.cfast
{ for U in 7 8 9; do echo "cd $Q/f && nice -n 10 python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1"; done
  for sg in 1 -1; do echo "cd $Q && nice -n 10 python3 $Z/l3qtab.py $EX $TD $TC tab_$sg.json $sg > tab_$sg.log 2>&1"; done
  echo "cd $Q && nice -n 10 python3 $P/s31/dcount.py args_A64m89.txt $M > dcount.txt 2>&1"; } | OMP_NUM_THREADS=1 xargs -P1 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
{ echo "# m89 vs A64"; for f in f/kill/kill6_U7.npy f/kill/kill6_U8.npy f/kill/kill6_U9.npy tab_1.json tab_-1.json; do a=$(md5sum < $A/$f | cut -c1-32); b=$(md5sum < $f | cut -c1-32); [ $a = $b ] && s=SAME || s=DIFF; echo "$f A64 $a m89 $b $s"; done; } > md5_compare.txt
date -u +%H:%M:%SZ > prep_end.txt
echo DONE > prep_done.txt
