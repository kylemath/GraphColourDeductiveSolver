# If K2 (xpen=1e-5 keeppen, k2_A67.sh) ends unconverged: (1) nosep over ALL rows incl. K2's -> tighter lower (tag s33L2, run_A67/lower_s33L2.log);
# (2) resume_s33.sh continues N, U, X, C, B on the converged xpen=1e-3 solution (sol_s33.json 5ecddc80, cert_s33L 6811771a; L.done kept).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; RD=$S/run_A67; Q=$S/reg_A67; cd $S/eng
until grep -q "K2 exit\|K2 converged" $S/wait.log; do sleep 60; done
grep -q "K2 converged" $S/wait.log && exit 0
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A67.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 pcell=$S/pcell/k3p.txt"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
cp rows_s33.txt rows_s33_rK2b.txt; md5sum sol_s33.json cert_s33L.json > $RD/fallback_md5.txt
WARM=rows_s33_rK2b.txt,$(cat $RD/warm_K.txt)
nice -n 5 python3 pcheck.py solveR2 $F nosep ipm0 polish tag=s33L2 $A $CB warm=$WARM K=300 xcap=3 threads=2 work=$SC/P/wr_A67L2 > $RD/s33L2.log 2>&1
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_s33L2.json xcap=3 ucap=100 $A work=$SC/P/wr_A67L2 > $RD/lower_s33L2.log 2>&1
cp cert_s33L2.json $RD/
echo "$(date -u +%H:%M:%SZ) [A67] fallback: nosep over all rows incl. K2: $(tail -1 $RD/lower_s33L2.log | cut -c1-60) ... $(grep -o '= 0\.[0-9]*  ([0-9]* rows)' $RD/lower_s33L2.log)" >> $S/wait.log
cp $RD/rows_s33.txt rows_s33.txt   # the xpen=1e-3 K rows, for resume's L warm list consistency
cd $S && bash resume_s33.sh A67 2c97e14d > $S/resume_A67.out 2>&1
