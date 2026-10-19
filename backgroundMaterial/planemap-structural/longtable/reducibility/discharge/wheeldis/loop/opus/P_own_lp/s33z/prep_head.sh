# s33z prep for a Studio head SHA (as s31/cmd_s31_prep.sh): registry = ex60 + git archive SHA W/loop; k3x_{D,C} = SHA's out/job30 files;
# args = s31/argsA62.txt with the k3x lines replaced; ring-merge 3 must be absent; strict kill6 tables, dcount, l3q tables. -P2.
# usage: bash prep_head.sh SHA
set -e
SHA=$(git -C /home/claude/GraphColourDeductiveSolver rev-parse --short=8 $1)
R=/home/claude/GraphColourDeductiveSolver
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
P=$R/$W/loop/opus/P_own_lp; Z=$P/s33z; Q=$Z/reg_$SHA; mkdir -p $Q/f/kill; cd $Q
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/$W
EX=$S/ex_$SHA
date -u +%H:%M:%SZ > prep_start.txt
git -C $R show $SHA:$W/out/job30/k3x_D.out > k3x_D_$SHA.out
git -C $R show $SHA:$W/out/job30/k3x_C.cfast > k3x_C_$SHA.cfast
{ echo "head $SHA: $(grep -c 'D=true' k3x_D_$SHA.out) D lines, $(grep -c ' r=' k3x_C_$SHA.cfast) C entries"
  for n in 'f7_..56757_...5...' 'f7_..65757_..55...' 'f7_..65757_..65...'; do echo "ring-merge $n: $(grep -cF "$n " k3x_C_$SHA.cfast || true) in C, $(grep -cF "$n " k3x_D_$SHA.out || true) in D"; done; } > ringmerge_check.txt
cat ringmerge_check.txt
if grep -q "ring-merge .*: [1-9]" ringmerge_check.txt; then echo "RING-MERGE NAME PRESENT: stop" >> ringmerge_check.txt; exit 3; fi
sed "s#$P/s31/k3x_D_3cfd7f18.out#$Q/k3x_D_$SHA.out#; s#$P/s31/k3x_C_3cfd7f18.cfast#$Q/k3x_C_$SHA.cfast#" $P/s31/argsA62.txt > args_$SHA.txt
grep -c "k3x_._$SHA" args_$SHA.txt
rm -rf $EX; cp -r $S/ex60 $EX
git -C $R archive $SHA $W/loop | tar -x -C $EX
cp $P/s31/f/s16_filter.py $P/s31/f/s16_killnpy.py f/
TD=$Q/k3x_D_$SHA.out; TC=$Q/k3x_C_$SHA.cfast
{ for U in 7 8 9; do echo "cd $Q/f && nice -n 5 python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1"; done
  for sg in 1 -1; do echo "cd $Q && nice -n 5 python3 $Z/l3qtab.py $EX $TD $TC tab_$sg.json $sg > tab_$sg.log 2>&1"; done
  echo "cd $Q && nice -n 5 python3 $P/s31/dcount.py args_$SHA.txt $M > dcount.txt 2>&1"; } | OMP_NUM_THREADS=1 xargs -P2 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy $P/s31/f/kill/*.npy tab_*.json $P/s28q/tab62_*.json k3x_* args_$SHA.txt > md5_prep.txt
date -u +%H:%M:%SZ > prep_end.txt
echo DONE > prep_done.txt
