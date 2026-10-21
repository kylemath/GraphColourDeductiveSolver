# s53c prep (= s52c/prep_noC_A83.sh for A97 + D-only V = 8 tables): D-only kill6 (U=7,8,9) and l3q tables for A97 (all C out):
# s30t s16_filter donly=1 (RSST D2 only) + k3x_D_A97, k3x_C empty; l3q tables via s33z/ccover/l3qtab_noC.py; V = 8 tables via s53c/l3qtabV_noC.py
# (s45/l3qtabV.py with donly=1, exname as s47/tabV8_A97.sh). Two streams (kill6+l3q | V8 after the base control), nice 10, one thread each.
# usage: bash prep_noC_A97.sh OUTDIR [TC]
set -e
R=/home/claude/GraphColourDeductiveSolver; W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
P=$R/$W/loop/opus/P_own_lp; Z=$P/s33z; A=$Z/reg_A97; OO=$P/s53c
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; EX=$SC/ex_A97
O=$1; TC=${2:-$Z/ccover/k3x_C_empty.cfast}; mkdir -p $O/f/kill; cd $O
[ -e $EX/$W/loop/k44/rsst_verdicts.txt ] || { echo "ex_A97 missing"; exit 3; }
date -u +%H:%M:%SZ > prep_start.txt
cp $P/s30t/f/s16_filter.py $P/s30t/f/s16_killnpy.py f/
TD=$A/k3x_D_A97.out
( for U in 7 8 9; do (cd f && OMP_NUM_THREADS=1 nice -n 10 python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U donly=1 > kill/kill6_U$U.log 2>&1); done
  for sg in 1 -1; do OMP_NUM_THREADS=1 nice -n 10 python3 $Z/ccover/l3qtab_noC.py $EX $TD $TC tab_$sg.json $sg > tab_$sg.log 2>&1; done ) &
( until [ -e $OO/base.done ]; do sleep 20; done
  for sg in 1 -1; do OMP_NUM_THREADS=1 nice -n 10 python3 $OO/l3qtabV_noC.py $EX $TD $TC tabV8_$sg.json $sg 8 exname=$P/s40f/exname_rm128.txt > tabV8_$sg.log 2>&1; done ) &
wait
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy tab_*.json tabV8_*.json $TC > md5_prep.txt
date -u +%H:%M:%SZ > prep_end.txt; echo DONE > prep_done.txt
