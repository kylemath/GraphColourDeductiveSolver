# Post-solve upper check against the NEWEST origin/main head (coordinator: heads move; fetch at this step). Waits for the A66 stacked solve  [main stack includes k3p #1 [E2 guard]: pcell=k3p.txt]
# (done_s33.txt), fetches origin/main, builds reg_H<sha> with prep_tag.sh (unless its k3x files are byte-identical to A66's, in which case
# upper_s33.log already answers it), runs upperR2 of sol_s33.json there. Then the minus-89 checks on A66 (m89/run_m89_A66.sh).
R=/home/claude/GraphColourDeductiveSolver
B=$R/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S=$B/s33z
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
until [ -e $S/done_s33.txt ]; do sleep 60; done
git -C $R fetch -q origin main; SHA=$(git -C $R rev-parse --short=8 origin/main)
dm=$(git -C $R show $SHA:$W/out/job30/k3x_D.out | md5sum | cut -c1-32); cm=$(git -C $R show $SHA:$W/out/job30/k3x_C.cfast | md5sum | cut -c1-32)
echo "$(date -u +%H:%M:%SZ) newest origin/main = $SHA (k3x_D $dm, k3x_C $cm)" >> $S/wait.log
if [ "$dm $cm" = "$(md5sum < $S/reg_A66/k3x_D_A66.out | cut -c1-32) $(md5sum < $S/reg_A66/k3x_C_A66.cfast | cut -c1-32)" ]; then
  echo "head $SHA: k3x identical to A66 -> upper_s33.log is the check" > $S/upper_newest.txt
else
  TAG=H$SHA; cd $S; bash prep_tag.sh $TAG $SHA > prep_$TAG.out 2>&1
  Q=$S/reg_$TAG; cd $S/eng
  M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/$W
  F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 pcell=$S/pcell/k3p.txt"
  OMP_NUM_THREADS=1 timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_s33.json root=$M args=$Q/args_$TAG.txt rpat=$B/rpatD.txt threads=2 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33u$SHA > $S/upper_s33_$TAG.log 2>&1 || echo "upper exit $?" >> $S/upper_s33_$TAG.log
  { echo "head $SHA ($(head -1 $Q/reg_check.txt))"; tail -n 1 $S/upper_s33_$TAG.log; } > $S/upper_newest.txt
fi
echo "$(date -u +%H:%M:%SZ) upper newest: $(tail -1 $S/upper_newest.txt)" >> $S/wait.log
echo DONE > $S/done_up_newest.txt
