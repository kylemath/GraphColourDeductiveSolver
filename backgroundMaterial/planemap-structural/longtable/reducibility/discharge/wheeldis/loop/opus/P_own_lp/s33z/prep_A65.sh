# s33z prep for registry A65 = main 15bc20c7 (2,544 D / 1,094 C; adds r54n over A64), files W/out/job30/k3x_{D,C} of 15bc20c7.
# argsA65 = s31/argsA62.txt with only the k3x lines changed. ex_A65 = ex60 + git archive 09a6a667 W/loop + git archive 15bc20c7 W/loop
# (main last). Checks: 3 ring-merge names absent; the 89 CGLUE-XRING names (27964810 list) present. Then kill6, l3q masks, dcount (-P2).
set -e
TAG=A65; SRC=15bc20c7; MAIN=09a6a667
R=/home/claude/GraphColourDeductiveSolver
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
P=$R/$W/loop/opus/P_own_lp; Z=$P/s33z; Q=$Z/reg_$TAG; mkdir -p $Q/f/kill; cd $Q
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/$W; EX=$S/ex_$TAG
date -u +%H:%M:%SZ > prep_start.txt
git -C $R show $SRC:$W/out/job30/k3x_D.out > k3x_D_$TAG.out
git -C $R show $SRC:$W/out/job30/k3x_C.cfast > k3x_C_$TAG.cfast
{ echo "registry $TAG (main $SRC out/job30): $(grep -c 'D=true' k3x_D_$TAG.out) D lines, $(grep -c ' r=' k3x_C_$TAG.cfast) C entries"; md5sum k3x_D_$TAG.out k3x_C_$TAG.cfast
  for n in 'f7_..56757_...5...' 'f7_..65757_..55...' 'f7_..65757_..65...'; do echo "ring-merge $n: $(grep -cF "$n " k3x_C_$TAG.cfast || true) in C, $(grep -cF "$n " k3x_D_$TAG.out || true) in D"; done
  np=0; nm=0; for n in $(grep -E '^[epf][0-9]+_' $Z/m89/CGLUE-XRING-ENTRIES_27964810.txt | awk '{print $1}'); do if grep -qF "$n r=" k3x_C_$TAG.cfast; then np=$((np+1)); else nm=$((nm+1)); echo "XRING MISSING $n"; fi; done
  echo "XRING names (89 listed): present in C $np, missing $nm"; } > reg_check.txt
cat reg_check.txt
if grep -q "ring-merge .*: [1-9]" reg_check.txt; then echo "RING-MERGE NAME PRESENT: stop" >> reg_check.txt; exit 3; fi
sed "s#$P/s31/k3x_D_3cfd7f18.out#$Q/k3x_D_$TAG.out#; s#$P/s31/k3x_C_3cfd7f18.cfast#$Q/k3x_C_$TAG.cfast#" $P/s31/argsA62.txt > args_$TAG.txt
cp args_$TAG.txt $Z/argsA65.txt
diff <(tr ' ' '\n' < $P/s31/argsA62.txt) <(tr ' ' '\n' < args_$TAG.txt) > args_diff.txt || true
rm -rf $S/ex_A65; cp -r $S/ex60 $S/ex_A65
git -C $R archive $MAIN $W/loop | tar -x -C $EX
git -C $R archive $SRC $W/loop | tar -x -C $EX
cp $P/s31/f/s16_filter.py $P/s31/f/s16_killnpy.py f/
TD=$Q/k3x_D_$TAG.out; TC=$Q/k3x_C_$TAG.cfast
{ for U in 7 8 9; do echo "cd $Q/f && nice -n 5 python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1"; done
  for sg in 1 -1; do echo "cd $Q && nice -n 5 python3 $Z/l3qtab.py $EX $TD $TC tab_$sg.json $sg > tab_$sg.log 2>&1"; done
  echo "cd $Q && nice -n 5 python3 $P/s31/dcount.py args_$TAG.txt $M > dcount.txt 2>&1"; } | OMP_NUM_THREADS=1 xargs -P1 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy $P/s31/f/kill/*.npy tab_*.json $P/s28q/tab62_*.json k3x_* args_$TAG.txt > md5_prep.txt
date -u +%H:%M:%SZ > prep_end.txt
echo DONE > prep_done.txt
