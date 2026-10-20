# s37c: cluster rows for d7 binder 8666655/5677657 (route b). threads=1, no solve.  bash run37.sh
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
X=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex37; SW=$X/work; mkdir -p $SW
# 0. inputs: explore's tree at 4770a564 (loop/k[0-9]*, discharge/b8b, discharge/ball.py, studiointel/routeb/rsst) under $X,
#    registry = main 3d6c4f9a out/job30/k3x_D.out, k3x_C.cfast under $X/adm54p (git archive / git show; see cyl37.log)
K=$X/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/k53
# 1. census cylinders (cen54's registry + cached two-engine window kills), coverage must equal explore's 86.68 %
(cd $X && nice python3 -I $B/s37c/cyl37.py $K $X/adm54p $B/s37c/cyl37.json > $B/s37c/cyl37.log 2>&1)
# 2. window kills -> q-names + absorption class
python3 $B/s37c/conv37.py $B/s37c/cyl37.json $B/s37c/eng/privcell.py $B/s37c/census_q.txt > $B/s37c/conv37.log
# 3. pricing on the l3q cert (A62 setup), lifting + restricted duals + primal load
F="xon apexcls filt16 killtab=$B/s31/f/kill/kill6 hat5 consall l3q l3qtab=$B/s28q/tab62_1.json,$B/s28q/tab62_-1.json lqcap=3"; A="root=$M args=$B/s31/argsA62.txt rpat=$B/rpatD.txt threads=1 work=$SW"
WARM=$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
cd $B/s37c/eng && nice python3 pcheck.py price37 $F cert=$B/s28q/eng/cert_s28A62L.json sol=$B/s28q/eng/sol_s28A62L.json cyl=$B/s37c/cyl37.json consbasis=$B/s21/cf/cons2basis_cls.json warm=$WARM xcap=3 tag=A62L outdir=$B/s37c $A > /dev/null 2>&1
