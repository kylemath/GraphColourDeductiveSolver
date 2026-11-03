# s60_f2b: K -> L -> upperR2 on registry A97 with the outside team's upgraded kill6 + l3q (V7,V8) tables and the 2-ball private-letter rules (f2b=).
# Same stack as s53/run53.sh (only killtab/l3qtab/l3qtab8 swapped, f2b= added, engine = s60_f2b/eng).  usage: bash run60.sh [RD-suffix]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s60_f2b/env60k.sh
RD=$Z/run_keep95; mkdir -p $RD; WK=$SC/P/wr60k; T=q60K95; TH=${TH:-1}; NI=10
note() { echo "$(date -u +%H:%M:%SZ) [s60k] $*" >> $Z/run.log; }
F="$FUP f2b=$RULES"
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
W53=$B/s53/run_A97/rows_q53A97.txt   # the rows s53 added on top of the warm set (the s53 warm set is the A83 + A84 + A87 files)
W51=$W53,$WA83,$W47,$W51
cd $E
if [ ! -e $RD/K.done ]; then
  [ -s rows_$T.txt ] && cp rows_$T.txt rows_${T}_r$(date -u +%m%d%H%M%S).txt
  WR=$(ls rows_${T}_r*.txt 2>/dev/null | paste -sd, -); WARM=${WR:+$WR,}$W51
  note "K start (upgraded tables + f2b; warm $WARM)"; date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout ${TO:-15000} nice -n $NI python3 pcheck.py solveR2 $F $X keeppen tag=$T $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=${LPMAX:-45} threads=$TH work=${WK}k > $RD/K.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_$T.json -nt $RD/K_start.txt ]; then cp sol_$T.json rows_$T.txt $RD/; date -u > $RD/K.done
    note "A97 upgraded keeppen t = $(python3 -c "import json; print('%.12f' % json.load(open('$RD/sol_$T.json'))['t'])") ($(grep '^iter' $RD/K.log | tail -1 | cut -c1-60))"
  else cp rows_$T.txt $RD/rows_${T}_partial.txt 2>/dev/null; note "K exit $ec (not converged; rows checkpointed): $(grep '^iter' $RD/K.log | tail -1 | cut -c1-80)"; exit 4; fi
fi
WARM=rows_$T.txt,$W51
if [ ! -e $RD/L1.done ]; then
  nice -n $NI python3 pcheck.py solveR2 $F $X nosep tag=${T}L $A $CB warm=$WARM K=300 xcap=3 threads=$TH work=${WK}L > $RD/L.log 2>&1
  cp sol_${T}L.json cert_${T}L.json $RD/; python3 $H/binder_keys.py $RD/cert_${T}L.json "s60_f2b/run_A97/cert_${T}L.json (A97, upgraded tables + 2-ball masks)" > $RD/binders_canon.txt
  date -u > $RD/L1.done; note "L nosep cert ready ($(grep '^nosep' $RD/L.log | cut -c1-80))"
fi
if [ ! -e $RD/L.done ]; then
  nice -n $NI python3 pcheck.py lowerR2 $F $X cert=$RD/cert_${T}L.json xcap=3 $A work=${WK}L > $RD/lower.log 2>&1
  date -u > $RD/L.done; note "lower: $(grep LOWER-R2 $RD/lower.log | tail -1 | cut -c1-90)"
fi
if [ ! -e $RD/U.done ]; then
  timeout 14400 nice -n $NI python3 pcheck.py upperR2 $F $X nomax sol=$RD/sol_$T.json $A threads=$TH work=${WK}u > $RD/upper.log 2>&1
  date -u > $RD/U.done; note "upper: $(grep UPPER-R2 $RD/upper.log || echo 'no UPPER-R2 line (timeout?)')"
fi
if [ ! -e $RD/B.done ]; then
  nice -n $NI python3 pcheck.py binderR2 $F $X $A sol=$RD/sol_${T}L.json cert=$RD/cert_${T}L.json top=15 work=${WK}bd > $RD/binders.log 2>&1
  date -u > $RD/B.done
fi
note "all stages done"; echo DONE > $RD/ALL.done
