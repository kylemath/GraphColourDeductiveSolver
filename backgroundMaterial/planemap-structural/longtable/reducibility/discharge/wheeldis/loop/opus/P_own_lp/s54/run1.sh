# s54 run1.sh TAG PM [extra solveR2 args...]: parametric solveR2 (engine s54/eng) on A97 with the s53 flags, warm = the converged
# A97 row pool, then upperR2 on the written sol.  Output: s54/runs/TAG/{solve.log,sol_TAG.json,cert_TAG.json,rows_TAG.txt,upper.log}
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
S=$B/s33z; Q=$S/reg_A97; E=$B/s54/eng; export OMP_NUM_THREADS=1
TAG=$1; PM=$2; shift 2
OD=$B/s54/runs/$TAG; WK=$SC/s54w/$TAG; mkdir -p $OD $WK
A="root=$M args=$Q/args_A97.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 l3qV=7,8 l3qtab8=$B/s47/tabV8_A97/tabV8_1.json,$B/s47/tabV8_A97/tabV8_-1.json"
X="rpatN=$B/s39o/rpatN3.txt"; CB=consbasis=$B/s21/cf/cons2basis_cls.json
WARM=${WARM:-$B/s51/eng/rows_q53A97.txt}
cd $E
if [ "${NOSOLVE:-0}" != 1 ]; then
nice -n 10 python3 pcheck.py solveR2 $F $X pm=$PM tag=$TAG outdir=$OD $A $CB warm=$WARM K=300 xcap=3 lpmax=${LPMAX:-1800} maxit=${MAXIT:-60} threads=1 work=$WK "$@" > $OD/solve.log 2>&1
fi
if [ "${NOUPPER:-0}" != 1 ] && [ -s $OD/sol_$TAG.json ]; then
nice -n 10 python3 pcheck.py upperR2 $F $X nomax sol=$OD/sol_$TAG.json $A threads=1 work=$WK vfile=$OD/viol.txt > $OD/upper.log 2>&1
fi
rm -rf $WK; echo "$TAG $PM $(grep -h 'LP t\*' $OD/solve.log | cut -c1-40) | $(grep -h UPPER-R2 $OD/upper.log 2>/dev/null)" >> $B/s54/runs/summary.txt
