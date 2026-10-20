# s40f: l3q + fy + rpatN3 warm re-solve on A74 (95ba762d).  Engine s40f/eng = s39o/eng + s35f/fyq/port_fy.py.
# Flags = run_n3_A74's (run39.sh n3 A74: FQ + rpatN3) + fy.  nice 5, threads=2, lpmax=300 (IPM fallback).
# Stages (markers in run/): K keeppen (warm: n3 A74 rows + fyq1 rows + run39's WQ), L nosep + lowerR2, U upperR2 nomax on K sol, B binders.
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s40f/env.sh
F="$FQ fy"; T=q40fy; RD=$D/run; WK=$SC/P/wr40_fy; mkdir -p $RD; cd $E
WQ=$N3/rows_q39n3A74.txt,$B/s35f/fyq/eng/rows_fyq1.txt,$SE/rows_q66.txt,$SE/rows_s33A66a.txt,$SE/rows_s33A64.txt,$SE/rows_q64A64.txt,$SE/rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
dfok
if [ ! -e $RD/K.done ]; then
  [ -s rows_$T.txt ] && cp rows_$T.txt rows_${T}_r$(date -u +%m%d%H%M%S).txt
  WR=$(ls rows_${T}_r*.txt 2>/dev/null | paste -sd, -); WARM=${WR:+$WR,}$WQ
  note "K start ($F $X)"; date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout ${TO:-14400} nice -n 5 python3 pcheck.py solveR2 $F $X keeppen tag=$T $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=300 threads=2 work=${WK}k > $RD/K.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_$T.json -nt $RD/K_start.txt ]; then cp sol_$T.json rows_$T.txt $RD/; date -u > $RD/K.done; note "K converged: $(grep '^iter' $RD/K.log | tail -1 | cut -c1-40)"
  else note "K exit $ec (not converged): $(grep '^iter' $RD/K.log | tail -1 | cut -c1-40)"; exit 4; fi
fi
dfok
WARM=rows_$T.txt,$WQ
if [ ! -e $RD/L.done ]; then
  timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F $X nosep tag=${T}L $A $CB warm=$WARM K=300 xcap=3 threads=2 work=${WK}L > $RD/L.log 2>&1
  nice -n 5 python3 pcheck.py lowerR2 $F $X cert=cert_${T}L.json xcap=3 $A work=${WK}L > $RD/lower.log 2>&1
  cp sol_${T}L.json cert_${T}L.json $RD/; date -u > $RD/L.done; note "L: $(tail -1 $RD/lower.log | cut -c1-90)"
fi
if [ ! -e $RD/U.done ]; then
  timeout 7200 nice -n 5 python3 pcheck.py upperR2 $F $X nomax sol=sol_$T.json $A threads=2 work=${WK}u > $RD/upper.log 2>&1
  date -u > $RD/U.done; note "U: $(grep UPPER-R2 $RD/upper.log)"
fi
if [ ! -e $RD/B.done ]; then
  nice -n 5 python3 pcheck.py binderR2 $F $X $A sol=sol_${T}L.json cert=cert_${T}L.json top=15 work=${WK}bd > $RD/binders.log 2>&1
  python3 $H/binder_keys.py $RD/cert_${T}L.json "Opus s40f/run/cert_${T}L.json (A74 95ba762d, l3q + fy + rpatN3)" > $RD/binders_canon.txt
  date -u > $RD/B.done
fi
md5sum $RD/*.json > $RD/md5.txt; rm -rf ${WK}k ${WK}L ${WK}u ${WK}bd; note "all stages done (work dirs removed)"; echo DONE > $RD/ALL.done
