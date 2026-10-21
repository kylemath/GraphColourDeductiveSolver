# s44b: l3q + rpatN3 + fb6 (fbdir=6, fbcap=3) warm keeppen on A82 (main 5fa0ba6c, reg_A82) with exname = s40f/exname_rm128.txt (FAIL set rechecked at A82: unchanged).
# Engine s44/eng. Warm: s44 A78 rows + s42a A78 rows + n3 A74 rows + the s42a WQ set. Waits for run_A78/ALL.done and reg_A82/prep_done.txt; nice 5 threads 2.
# Stages: K keeppen (xpen 1e-3, lpmax=900, 4 h cap; resumes from its rows) -> L nosep + binder_keys -> lowerR2 -> U upperR2 nomax -> binderR2.
# CPU: nice 10 threads=1 while s42a runs; nice 5 threads=2 once s42a/run_A78/ALL.done exists (checked at each stage start).
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
Q=$S/reg_A82; A="root=$M args=$Q/args_A82.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
F="$FQ fb fbdir=6 fbcap=3"; T=q44fbA82; RD=$D/run_A82; WK=$SC/P/wr44b_fb; mkdir -p $RD; cd $E
WQ=$SE/rows_q66.txt,$SE/rows_s33A66a.txt,$SE/rows_s33A64.txt,$SE/rows_q64A64.txt,$SE/rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
XW=$D/run_A78/rows_q44fbA78.txt,$B/s42a/run_A78/rows_q42aA78.txt,$N3/rows_q39n3A74.txt
cpu() { NI=5; TH=2; }
until [ -e $D/run_A78/ALL.done ] && [ -e $Q/prep_done.txt ]; do sleep 60; done; note "A82 run start (run_A78 checks done, reg_A82 ready)"
dfok
if [ ! -e $RD/K.done ]; then
  cpu; [ -s rows_$T.txt ] && cp rows_$T.txt rows_${T}_r$(date -u +%m%d%H%M%S).txt
  WR=$(ls rows_${T}_r*.txt 2>/dev/null | paste -sd, -); WARM=${WR:+$WR,}$XW,$WQ
  note "K start ($F $X; nice $NI threads $TH)"; date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout ${TO:-14400} nice -n $NI python3 pcheck.py solveR2 $F $X keeppen tag=$T $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=900 threads=$TH work=${WK}k > $RD/K.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_$T.json -nt $RD/K_start.txt ]; then cp sol_$T.json rows_$T.txt $RD/; date -u > $RD/K.done; note "A82 K converged: $(grep "^iter" $RD/K.log | tail -1 | cut -c1-60)"; note "A82 keeppen t = $(grep "^iter" $RD/K.log | tail -1 | sed "s/.* t=\([0-9.]*\) .*/\1/")"
  else cp rows_$T.txt $RD/rows_${T}_partial.txt 2>/dev/null; note "K exit $ec (not converged; rows checkpointed): $(grep '^iter' $RD/K.log | tail -1 | cut -c1-60)"; exit 4; fi
fi
dfok; WARM=rows_$T.txt,$XW,$WQ
if [ ! -e $RD/L1.done ]; then
  cpu; nice -n $NI python3 pcheck.py solveR2 $F $X nosep tag=${T}L $A $CB warm=$WARM K=300 xcap=3 threads=$TH work=${WK}L > $RD/L.log 2>&1
  cp sol_${T}L.json cert_${T}L.json $RD/; python3 $H/binder_keys.py $RD/cert_${T}L.json "Opus s44/run_A78/cert_${T}L.json (A82 5fa0ba6c, l3q + rpatN3 + fb6 cap 3, 128 exname hold-outs)" > $RD/binders_canon.txt
  date -u > $RD/L1.done; note "L nosep cert + binders_canon ready"
fi
if [ ! -e $RD/L.done ]; then
  cpu; nice -n $NI python3 pcheck.py lowerR2 $F $X cert=cert_${T}L.json xcap=3 $A work=${WK}L > $RD/lower.log 2>&1
  date -u > $RD/L.done; note "L: $(tail -1 $RD/lower.log | cut -c1-90)"
fi
dfok
if [ ! -e $RD/U.done ]; then
  cpu; timeout 7200 nice -n $NI python3 pcheck.py upperR2 $F $X nomax sol=sol_$T.json $A threads=$TH work=${WK}u > $RD/upper.log 2>&1
  date -u > $RD/U.done; note "U: $(grep UPPER-R2 $RD/upper.log)"
fi
if [ ! -e $RD/B.done ]; then
  cpu; nice -n $NI python3 pcheck.py binderR2 $F $X $A sol=sol_${T}L.json cert=cert_${T}L.json top=15 work=${WK}bd > $RD/binders.log 2>&1
  date -u > $RD/B.done
fi
md5sum $RD/*.json > $RD/md5.txt; rm -rf ${WK}k ${WK}L ${WK}u ${WK}bd; note "all stages done (work dirs removed)"; echo DONE > $RD/ALL.done
