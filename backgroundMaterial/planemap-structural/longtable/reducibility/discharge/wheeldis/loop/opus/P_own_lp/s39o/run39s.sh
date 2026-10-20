# s39o stacked warm solve on A67: the full s33z flag set (l3q + zh/zr (Z+-) + hatrr (RR) + l6r (z6) + pcell k3p #1) + rpatN [+ offc].
# usage: [NICE=n] [XWARM=f1,f2] bash run39s.sh V [REG]    V = sn (rpatN) | son (offc + rpatN) | s2 (rpatN2) | s3 (rpatN3) | s2o (offc + rpatN2).  Warm from s33z's K rows (run_A67/rows_s33.txt + its snapshots + BASE).
V=$1; REG=${2:-A67}; NI=${NICE:-10}   # REG: registry tag (s33z/reg_REG); NICE: nice level
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; SE=$S/eng; Q=$S/reg_$REG; H=$B/s39o; E=$H/eng; RD=$H/run_$V; [ $REG = A67 ] || RD=$H/run_${V}_$REG; mkdir -p $RD; cd $E
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W; WK=$SC/P/wr39_${V}_$REG
export OMP_NUM_THREADS=1
case $V in sn) X="rpatN=$H/rpatN.txt";; son) X="offc rpatN=$H/rpatN.txt";; s2) X="rpatN=$H/rpatN2.txt";; s3) X="rpatN=$H/rpatN3.txt";; s2o) X="offc rpatN=$H/rpatN2.txt";; *) echo bad V; exit 2;; esac
A="root=$M args=$Q/args_$REG.txt rpat=$B/rpatD.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
F="$FQ zh zr hatrr zcap=3 l6r z6cap=3 pcell=$S/pcell/k3p.txt"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
BASE=$SE/rows_s33A66a.txt,$SE/rows_s33A64.txt,$SE/rows_q64A64.txt,$SE/rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt
WS=$S/run_A67/rows_s33.txt,$SE/rows_s33_rK2a.txt,$SE/rows_s33_rK1p3.txt,$SE/rows_s33_r1020061819.txt,$SE/rows_s33_r1020031622.txt,$BASE
note() { echo "$(date -u +%H:%M:%SZ) [s39o $V $REG] $*" >> $H/wait39.log; }
dfok() { a=$(df -BG --output=avail $SC | tail -1 | tr -dc 0-9); [ "$a" -gt 10 ] || { note "df: only ${a}G free, stopping"; exit 5; }; }
T=q39$V; [ $REG = A67 ] || T=q39${V}$REG
WS=${XWARM:+$XWARM,}$WS   # XWARM: extra warm files (e.g. the A67 run's rows)
dfok
if [ ! -e $RD/K.done ]; then
  [ -s rows_$T.txt ] && cp rows_$T.txt rows_${T}_r$(date -u +%m%d%H%M%S).txt
  WR=$(ls rows_${T}_r*.txt 2>/dev/null | paste -sd, -); WARM=${WR:+$WR,}$WS
  note "K start ($X, full s33z flags)"; date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout ${TO:-10800} nice -n $NI python3 pcheck.py solveR2 $F $X keeppen tag=$T $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=${LPMAX:-60} threads=2 work=${WK}k > $RD/K.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_$T.json -nt $RD/K_start.txt ]; then cp sol_$T.json rows_$T.txt $RD/; date -u > $RD/K.done; note "K converged: $(grep '^iter' $RD/K.log | tail -1 | cut -c1-40)"
  else note "K exit $ec (not converged)"; exit 4; fi
fi
dfok
WARM=rows_$T.txt,$WS
if [ ! -e $RD/L.done ]; then
  timeout 10800 nice -n $NI python3 pcheck.py solveR2 $F $X nosep ipm0 polish tag=${T}L $A $CB warm=$WARM K=300 xcap=3 threads=2 work=${WK}L > $RD/L.log 2>&1
  nice -n $NI python3 pcheck.py lowerR2 $F $X cert=cert_${T}L.json xcap=3 ucap=100 $A work=${WK}L > $RD/lower.log 2>&1
  cp sol_${T}L.json cert_${T}L.json $RD/; date -u > $RD/L.done; note "L: $(tail -1 $RD/lower.log | cut -c1-90)"
fi
if [ ! -e $RD/U.done ]; then
  timeout 7200 nice -n $NI python3 pcheck.py upperR2 $F $X nomax sol=sol_$T.json $A threads=2 work=${WK}u > $RD/upper.log 2>&1
  date -u > $RD/U.done; note "U: $(grep UPPER-R2 $RD/upper.log)"
fi
if [ ! -e $RD/B.done ]; then
  nice -n $NI python3 pcheck.py binderR2 $F $X $A sol=sol_${T}L.json cert=cert_${T}L.json row=7:8666655:5677657 top=15 work=${WK}bd > $RD/binders.log 2>&1
  date -u > $RD/B.done
fi
md5sum $RD/*.json > $RD/md5.txt; rm -rf ${WK}k ${WK}L ${WK}u ${WK}bd; note "all stages done (work dirs removed)"; echo DONE > $RD/ALL.done
