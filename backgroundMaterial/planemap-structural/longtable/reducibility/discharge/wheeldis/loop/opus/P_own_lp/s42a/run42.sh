# s42a: warm l3q + rpatN3 on A78 (b6dc7610) with 128 ring-merge hold-outs (exname_A78.txt). Template s39o/run39.sh n3 (A74), threads=2, nice 5.
# Stages: K keeppen (lpmax=300, IPM fallback) -> L nosep solve (cert) -> early binder_keys -> lowerR2 -> U upperR2 nomax -> binderR2
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s42a/env42.sh
cd $E; dfok
if [ ! -e $RD/K.done ]; then
  [ -s rows_$T.txt ] && cp rows_$T.txt rows_${T}_r$(date -u +%m%d%H%M%S).txt
  WR=$(ls rows_${T}_r*.txt 2>/dev/null | paste -sd, -); WARM=${WR:+$WR,}$XW,$WQ
  note "K start ($X, exname)"; date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout ${TO:-14400} nice -n 5 python3 pcheck.py solveR2 $FQ $X keeppen tag=$T $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=300 threads=2 work=${WK}k > $RD/K.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_$T.json -nt $RD/K_start.txt ]; then cp sol_$T.json rows_$T.txt $RD/; date -u > $RD/K.done; note "K converged: $(grep '^iter' $RD/K.log | tail -1 | cut -c1-60)"
  else note "K exit $ec (not converged)"; exit 4; fi
fi
dfok; WARM=rows_$T.txt,$XW,$WQ
if [ ! -e $RD/L1.done ]; then
  nice -n 5 python3 pcheck.py solveR2 $FQ $X nosep tag=${T}L $A $CB warm=$WARM K=300 xcap=3 threads=2 work=${WK}L > $RD/L.log 2>&1
  cp sol_${T}L.json cert_${T}L.json $RD/; python3 $H/binder_keys.py $RD/cert_${T}L.json "Opus s42a/run_A78/cert_${T}L.json (A78 b6dc7610, l3q + rpatN3, 128 exname hold-outs)" | head -11 > $RD/binders_canon.txt
  date -u > $RD/L1.done; note "L nosep cert + binders_canon ready"
fi
if [ ! -e $RD/L.done ]; then
  nice -n 5 python3 pcheck.py lowerR2 $FQ $X cert=cert_${T}L.json xcap=3 $A work=${WK}L > $RD/lower.log 2>&1
  date -u > $RD/L.done; note "L: $(tail -1 $RD/lower.log | cut -c1-90)"
fi
dfok
if [ ! -e $RD/U.done ]; then
  timeout 7200 nice -n 5 python3 pcheck.py upperR2 $FQ $X nomax sol=sol_$T.json $A threads=2 work=${WK}u > $RD/upper.log 2>&1
  date -u > $RD/U.done; note "U: $(grep UPPER-R2 $RD/upper.log)"
fi
if [ ! -e $RD/B.done ]; then
  nice -n 5 python3 pcheck.py binderR2 $FQ $X $A sol=sol_${T}L.json cert=cert_${T}L.json top=15 work=${WK}bd > $RD/binders.log 2>&1
  date -u > $RD/B.done
fi
md5sum $RD/*.json > $RD/md5.txt; rm -rf ${WK}k ${WK}L ${WK}u ${WK}bd; note "all stages done (work dirs removed)"; echo DONE > $RD/ALL.done
