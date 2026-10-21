# Finish a prep_tag.sh run that was stopped after kill6 and tab_1: redo tab_-1 and dcount, then killnpy, md5s, done flag.
set -e
TAG=$1
R=/home/claude/GraphColourDeductiveSolver
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
P=$R/$W/loop/opus/P_own_lp; Z=$P/s33z; Q=$Z/reg_$TAG; cd $Q
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/$W; EX=$S/ex_$TAG
TD=$Q/k3x_D_$TAG.out; TC=$Q/k3x_C_$TAG.cfast
{ echo "cd $Q && nice -n 5 python3 $Z/l3qtab.py $EX $TD $TC tab_-1.json -1 > tab_-1.log 2>&1"
  echo "cd $Q && nice -n 5 python3 $P/s31/dcount.py args_$TAG.txt $M > dcount.txt 2>&1"; } | OMP_NUM_THREADS=1 xargs -P2 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy $P/s31/f/kill/*.npy tab_*.json $P/s28q/tab62_*.json k3x_* args_$TAG.txt > md5_prep.txt
date -u +%H:%M:%SZ > prep_end.txt
echo DONE > prep_done.txt
