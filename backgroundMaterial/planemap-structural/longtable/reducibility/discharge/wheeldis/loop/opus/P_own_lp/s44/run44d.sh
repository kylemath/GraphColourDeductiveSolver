# s44d (RELAY_SPEC_s47): l3q + l3qV = 8 + rpatN3 + fb6 (fbdir=6, fbcap=3) warm keeppen on A84 (main 517b0129, reg_A84;
# 2,707 D / 1,218 C), exname = s40f/exname_rm128.txt (FAIL set rechecked at A84: out/job30/ringmerge_cpat_sweep.out at 517b0129
# is md5 a2ec92e5, identical to 618c0899 / 240b5a08, 129 FAIL lines; minus f9_....5565B_....6655. = exname_rm128, unchanged;
# rechecked again below at start). Engine s47/eng, tag q47A84, outputs s47/run_A84/.
# Waits for s33z/reg_A84/prep_done.txt, then builds the reg_A84 V = 8 tables (s47/tabV8_A84.sh, in the background, while run44c
# runs); waits for run44c to finish: s44/run_A83/ALL.done exists, or the run44c.sh PID taken once at start (pgrep) is gone
# (kill -0); then waits for s47/tabV8_A84/tabV8.done. Warm: run44c's rows (s44/eng/rows_q44fbA83*.txt, s44/run_A83/rows_*)
# + run44c's warm list. Stages as run44c: K keeppen -> L nosep + binder_keys -> lowerR2 -> U upperR2 nomax -> binderR2.
# CPU: nice 10, threads 1 (TH=2 in the environment raises it).
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
D44=$D; E=$B/s47/eng; RD=$B/s47/run_A84; R44=$D44/run_A83; TV=$B/s47/tabV8_A84
Q=$S/reg_A84; A="root=$M args=$Q/args_A84.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
F="$FQ fb fbdir=6 fbcap=3 l3qV=7,8 l3qtab8=$TV/tabV8_1.json,$TV/tabV8_-1.json"; T=q47A84; WK=$SC/P/wr44d; mkdir -p $RD
WQ=$SE/rows_q66.txt,$SE/rows_s33A66a.txt,$SE/rows_s33A64.txt,$SE/rows_q64A64.txt,$SE/rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
XW=$D44/run_A78/rows_q44fbA78.txt,$B/s42a/run_A78/rows_q42aA78.txt,$N3/rows_q39n3A74.txt
note() { echo "$(date -u +%H:%M:%SZ) [s44d] $*" >> $B/s47/run.log; }
NI=10; TH=${TH:-1}
P44=$(pgrep -f run44c.sh | head -1)
note "run44d launched (pid $$); waiting for reg_A84 prep, run44c (pid ${P44:-none}) and the A84 V = 8 tables"
R=/home/claude/GraphColourDeductiveSolver; JW=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job30/ringmerge_cpat_sweep.out
if ! diff <(git -C $R show 517b0129:$JW | grep '^FAIL' | awk '{print $2}' | grep -vxF 'f9_....5565B_....6655.' | sort -u) <(grep -v '^#' $B/s40f/exname_rm128.txt | awk 'NF{print $1}' | sort -u) > /dev/null; then note "A84 ring-merge FAIL set differs from exname_rm128: stopping"; exit 6; fi
note "A84 ring-merge FAIL set (517b0129) = exname_rm128 + the kept f9 name: unchanged"
until [ -e $Q/prep_done.txt ]; do sleep 60; done; note "reg_A84 prep done"
[ -e $TV/tabV8.done ] || { mkdir -p $TV; nohup bash $B/s47/tabV8_A84.sh > $TV/nohup.out 2>&1 & note "A84 V = 8 tables started (pid $!)"; }
while [ ! -e $R44/ALL.done ] && [ -n "$P44" ] && kill -0 $P44 2>/dev/null; do sleep 60; done
note "run44c finished or gone (ALL.done: $([ -e $R44/ALL.done ] && echo yes || echo no))"
until [ -e $TV/tabV8.done ]; do sleep 60; done
cd $E; dfok
if [ ! -e $RD/K.done ]; then
  [ -s rows_$T.txt ] && cp rows_$T.txt rows_${T}_r$(date -u +%m%d%H%M%S).txt
  WR=$(ls rows_${T}_r*.txt 2>/dev/null | paste -sd, -)
  W44=$(ls $D44/eng/rows_q44fbA83*.txt $R44/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
  WARM=${WR:+$WR,}${W44:+$W44,}$XW,$WQ
  note "K start ($F $X; nice $NI threads $TH; warm $WARM)"; date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout ${TO:-14400} nice -n $NI python3 pcheck.py solveR2 $F $X keeppen tag=$T $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=900 threads=$TH work=${WK}k > $RD/K.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_$T.json -nt $RD/K_start.txt ]; then cp sol_$T.json rows_$T.txt $RD/; date -u > $RD/K.done; note "A84 K converged: $(grep "^iter" $RD/K.log | tail -1 | cut -c1-60)"
  else cp rows_$T.txt $RD/rows_${T}_partial.txt 2>/dev/null; note "K exit $ec (not converged; rows checkpointed): $(grep '^iter' $RD/K.log | tail -1 | cut -c1-60)"; exit 4; fi
fi
dfok; WARM=rows_$T.txt,${W44:-$(ls $D44/eng/rows_q44fbA83*.txt $R44/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)},$XW,$WQ; WARM=${WARM//,,/,}
if [ ! -e $RD/L1.done ]; then
  nice -n $NI python3 pcheck.py solveR2 $F $X nosep tag=${T}L $A $CB warm=$WARM K=300 xcap=3 threads=$TH work=${WK}L > $RD/L.log 2>&1
  cp sol_${T}L.json cert_${T}L.json $RD/; python3 $H/binder_keys.py $RD/cert_${T}L.json "Opus s47/run_A84/cert_${T}L.json (A84 517b0129, l3q + l3qV 8 + rpatN3 + fb6 cap 3, 128 exname hold-outs)" > $RD/binders_canon.txt
  date -u > $RD/L1.done; note "L nosep cert + binders_canon ready"
fi
if [ ! -e $RD/L.done ]; then
  nice -n $NI python3 pcheck.py lowerR2 $F $X cert=cert_${T}L.json xcap=3 $A work=${WK}L > $RD/lower.log 2>&1
  date -u > $RD/L.done; note "L: $(tail -1 $RD/lower.log | cut -c1-90)"
fi
dfok
if [ ! -e $RD/U.done ]; then
  timeout 7200 nice -n $NI python3 pcheck.py upperR2 $F $X nomax sol=sol_$T.json $A threads=$TH work=${WK}u > $RD/upper.log 2>&1
  date -u > $RD/U.done; note "U: $(grep UPPER-R2 $RD/upper.log)"
fi
if [ ! -e $RD/B.done ]; then
  nice -n $NI python3 pcheck.py binderR2 $F $X $A sol=sol_${T}L.json cert=cert_${T}L.json top=15 work=${WK}bd > $RD/binders.log 2>&1
  date -u > $RD/B.done
fi
md5sum $RD/*.json > $RD/md5.txt; rm -rf ${WK}k ${WK}L ${WK}u ${WK}bd; note "all stages done (work dirs removed)"; echo DONE > $RD/ALL.done
