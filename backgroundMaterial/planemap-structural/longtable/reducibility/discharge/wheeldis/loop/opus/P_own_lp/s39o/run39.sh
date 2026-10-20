# s39o warm l3q-only re-solves on A67 (the s33z Q stage with extra pattern options).  usage: [NICE=n] [LPMAX=s] [XWARM=f1,f2] bash run39.sh V [REG]   (REG: registry tag s33z/reg_REG, default A67)
#   V = n : rpatN only    V = o : offc only    V = on : offc + rpatN    V = n2 : rpatN2 only    V = n3 : rpatN3 only
# Stages (markers in run_V/): K keeppen (warm from q66's converged rows + q66's warm set), L nosep + lowerR2, U upperR2 nomax.
V=$1; REG=${2:-A67}
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; SE=$S/eng; Q=$S/reg_$REG; H=$B/s39o; E=$H/eng; RD=$H/run_$V; [ $REG = A67 ] || RD=$H/run_${V}_$REG; mkdir -p $RD; cd $E
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W; WK=$SC/P/wr39_$V; [ $REG = A67 ] || WK=${WK}_$REG
export OMP_NUM_THREADS=1
case $V in n) X="rpatN=$H/rpatN.txt";; n2) X="rpatN=$H/rpatN2.txt";; n3) X="rpatN=$H/rpatN3.txt";; o) X="offc";; on) X="offc rpatN=$H/rpatN.txt";; *) echo bad V; exit 2;; esac
A="root=$M args=$Q/args_$REG.txt rpat=$B/rpatD.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WQ=$SE/rows_q66.txt,$SE/rows_s33A66a.txt,$SE/rows_s33A64.txt,$SE/rows_q64A64.txt,$SE/rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
note() { echo "$(date -u +%H:%M:%SZ) [s39o $V $REG] $*" >> $H/wait39.log; }
T=q39$V; [ $REG = A67 ] || T=q39${V}$REG
WQ=${XWARM:+$XWARM,}$WQ
if [ ! -e $RD/K.done ]; then
  [ -s rows_$T.txt ] && cp rows_$T.txt rows_${T}_r$(date -u +%m%d%H%M%S).txt
  WR=$(ls rows_${T}_r*.txt 2>/dev/null | paste -sd, -); WARM=${WR:+$WR,}$WQ
  note "K start ($X)"; date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout 10800 nice -n ${NICE:-10} python3 pcheck.py solveR2 $FQ $X keeppen tag=$T $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=${LPMAX:-60} threads=1 work=${WK}k > $RD/K.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_$T.json -nt $RD/K_start.txt ]; then cp sol_$T.json rows_$T.txt $RD/; date -u > $RD/K.done; note "K converged: $(grep '^iter' $RD/K.log | tail -1 | cut -c1-40)"
  else note "K exit $ec (not converged)"; exit 4; fi
fi
WARM=rows_$T.txt,$WQ
if [ ! -e $RD/L.done ]; then
  nice -n ${NICE:-10} python3 pcheck.py solveR2 $FQ $X nosep tag=${T}L $A $CB warm=$WARM K=300 xcap=3 threads=1 work=${WK}L > $RD/L.log 2>&1
  nice -n ${NICE:-10} python3 pcheck.py lowerR2 $FQ $X cert=cert_${T}L.json xcap=3 $A work=${WK}L > $RD/lower.log 2>&1
  cp sol_${T}L.json cert_${T}L.json $RD/; date -u > $RD/L.done; note "L: $(tail -1 $RD/lower.log | cut -c1-90)"
fi
if [ ! -e $RD/U.done ]; then
  timeout 7200 nice -n ${NICE:-10} python3 pcheck.py upperR2 $FQ $X nomax sol=sol_$T.json $A threads=1 work=${WK}u > $RD/upper.log 2>&1
  date -u > $RD/U.done; note "U: $(grep UPPER-R2 $RD/upper.log)"
fi
if [ ! -e $RD/B.done ]; then
  nice -n ${NICE:-10} python3 pcheck.py binderR2 $FQ $X $A sol=sol_${T}L.json cert=cert_${T}L.json top=15 work=${WK}bd > $RD/binders.log 2>&1
  date -u > $RD/B.done
fi
md5sum $RD/*.json > $RD/md5.txt; note "all stages done"; echo DONE > $RD/ALL.done
