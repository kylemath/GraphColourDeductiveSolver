# s41c prep: D-only kill6 (U=7,8,9) and l3q tables for A74 (all C out), as s33z/ccover/prep_noC_A66.sh:
# s30t s16_filter donly=1 (RSST D2 only) + k3x_D_A74, k3x_C empty; l3q tables via s33z/ccover/l3qtab_noC.py.
# usage: bash prep_noC_A74.sh OUTDIR [TC]   (TC default: empty C file; the cover check passes the cover-only C file)
set -e
R=/home/claude/GraphColourDeductiveSolver; W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
P=$R/$W/loop/opus/P_own_lp; Z=$P/s33z; A=$Z/reg_A74
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; EX=$SC/ex_A74
O=$1; TC=${2:-$Z/ccover/k3x_C_empty.cfast}; mkdir -p $O/f/kill; cd $O
if [ ! -e $EX/.done ]; then rm -rf $EX; cp -r $SC/ex60 $EX
  git -C $R archive 09a6a667 $W/loop | tar -x -C $EX; git -C $R archive 95ba762d $W/loop | tar -x -C $EX; touch $EX/.done; fi
date -u +%H:%M:%SZ > prep_start.txt
cp $P/s30t/f/s16_filter.py $P/s30t/f/s16_killnpy.py f/
TD=$A/k3x_D_A74.out
for U in 7 8 9; do (cd f && OMP_NUM_THREADS=1 nice -n 10 python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U donly=1 > kill/kill6_U$U.log 2>&1); done
for sg in 1 -1; do OMP_NUM_THREADS=1 nice -n 10 python3 $Z/ccover/l3qtab_noC.py $EX $TD $TC tab_$sg.json $sg > tab_$sg.log 2>&1; done
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy tab_*.json $TC > md5_prep.txt
date -u +%H:%M:%SZ > prep_end.txt; echo DONE > prep_done.txt
