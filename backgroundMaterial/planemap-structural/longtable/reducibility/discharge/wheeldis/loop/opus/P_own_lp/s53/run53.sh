# s53 run53 (RELAY_SPEC_s51 + RELAY_SPEC_s47): the stacked solve LT asked for: s42a family (l3q lqcap 3 + rpatN3, xcap 3, 128 exname hold-outs)
# + xo (s51) + l3qV=7,8 (s47 V=8 tables built on A91, s47/tabV8_A91), fb off, on registry A91 (main 76148fb1). Engine s51/eng.
# Waits for s51's first result (s51/run_A87/K.done, or run51p.sh PID 708 gone), then K keeppen -> L nosep -> lowerR2 -> U upperR2 -> binderR2.
# Writes "[s53] A91 xo+V8 keeppen t = ...", "xo+V8 U: ...", "xo+V8 L: ..." to s53/run.log.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; H=$B/s39o; D=$B/s51; E=$D/eng; Z3=$B/s53
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"; CB=consbasis=$B/s21/cf/cons2basis_cls.json
note() { echo "$(date -u +%H:%M:%SZ) [s53] $*" >> $Z3/run.log; }
dfok() { a=$(df -BG --output=avail $SC | tail -1 | tr -dc 0-9); [ "$a" -gt 10 ] || { note "df: only ${a}G free, stopping"; exit 5; }; }
NI=10; TH=${TH:-1}
note "run53 launched (pid $$); waiting for s51 K (s51/run_A87/K.done or run51p pid 708 gone)"
while [ ! -e $D/run_A87/K.done ] && kill -0 708 2>/dev/null; do sleep 120; done
note "s51 state: $(grep -E 'xo keeppen t|xo+V8 K exit' $D/run.log | tail -1 | cut -c1-120)"
RG=A91
[ -e $S/reg_$RG/prep_done.txt ] && [ -e $B/s47/tabV8_A91/tabV8.done ] || { note "reg_A91 or tabV8_A91 not ready: stopping"; exit 3; }
Q=$S/reg_$RG; SHA=$(head -1 $Q/reg_check.txt | sed -E 's/.*\(main ([0-9a-f]+).*/\1/')
SKIP=$(for n in 85 86 87 88 89; do [ -d $S/reg_A$n ] && [ ! -e $S/reg_A$n/prep_done.txt ] && echo -n "A$n(no prep_done) "; done)
note "REGISTRY USED: $RG (main $SHA; $(sed -n 1p $Q/reg_check.txt | cut -d: -f2- | cut -c1-60); prep_done $(cat $Q/prep_end.txt 2>/dev/null)); not used: ${SKIP:-none}"
R=/home/claude/GraphColourDeductiveSolver; JW=$W/out/job30/ringmerge_cpat_sweep.out
if ! diff <(git -C $R show $SHA:$JW | grep '^FAIL' | awk '{print $2}' | grep -vxF 'f9_....5565B_....6655.' | sort -u) <(grep -v '^#' $B/s40f/exname_rm128.txt | awk 'NF{print $1}' | sort -u) > /dev/null; then note "$RG ring-merge FAIL set differs from exname_rm128: stopping"; exit 6; fi
note "$RG ring-merge FAIL set ($SHA, sweep md5 $(git -C $R show $SHA:$JW | md5sum | cut -c1-8)) = exname_rm128 + the kept f9 name: unchanged"
A="root=$M args=$Q/args_$RG.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 l3qV=7,8 l3qtab8=$B/s47/tabV8_A91/tabV8_1.json,$B/s47/tabV8_A91/tabV8_-1.json xo"
T=q53$RG; RD=$Z3/run_$RG; WK=$SC/P/wr53r; mkdir -p $RD
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $D/run_A87/rows_q51A87*.txt $E/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -); [ -n "$W47" ] || W47=$(ls $B/s47/eng/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
cd $E; dfok
if [ ! -e $RD/K.done ]; then
  [ -s rows_$T.txt ] && cp rows_$T.txt rows_${T}_r$(date -u +%m%d%H%M%S).txt
  WR=$(ls rows_${T}_r*.txt 2>/dev/null | paste -sd, -)
  WARM=${WR:+$WR,}$WA83,$W47,$W51; WARM=${WARM//,,/,}
  note "K start ($F $X; nice $NI threads $TH; warm $WARM)"; date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout ${TO:-28800} nice -n $NI python3 pcheck.py solveR2 $F $X keeppen tag=$T $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=900 threads=$TH work=${WK}k > $RD/K.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_$T.json -nt $RD/K_start.txt ]; then cp sol_$T.json rows_$T.txt $RD/; date -u > $RD/K.done
    note "$RG xo+V8 keeppen t = $(python3 -c "import json; print('%.12f' % json.load(open('$RD/sol_$T.json'))['t'])") ($(grep '^iter' $RD/K.log | tail -1 | cut -c1-60); $(grep '  xo:' $RD/K.log | tail -1 | cut -c3-120))"
  else cp rows_$T.txt $RD/rows_${T}_partial.txt 2>/dev/null; note "$RG xo+V8 K exit $ec (not converged; rows checkpointed): $(grep '^iter' $RD/K.log | tail -1 | cut -c1-60)"; exit 4; fi
fi
dfok; WARM=rows_$T.txt,$WA83,$W47,$W51; WARM=${WARM//,,/,}
if [ ! -e $RD/L1.done ]; then
  nice -n $NI python3 pcheck.py solveR2 $F $X nosep tag=${T}L $A $CB warm=$WARM K=300 xcap=3 threads=$TH work=${WK}L > $RD/L.log 2>&1
  cp sol_${T}L.json cert_${T}L.json $RD/; python3 $H/binder_keys.py $RD/cert_${T}L.json "Opus s51/run_$RG/cert_${T}L.json ($RG $SHA, s42a family + xo + l3qV=7,8, xcap 3, 128 exname hold-outs)" > $RD/binders_canon.txt
  date -u > $RD/L1.done; note "$RG xo+V8 L nosep cert + binders_canon ready ($(grep '^nosep' $RD/L.log | cut -c1-80))"
fi
if [ ! -e $RD/L.done ]; then
  nice -n $NI python3 pcheck.py lowerR2 $F $X cert=$RD/cert_${T}L.json xcap=3 $A work=${WK}L > $RD/lower.log 2>&1
  date -u > $RD/L.done; note "xo+V8 L: $RG $(grep LOWER-R2 $RD/lower.log | tail -1 | cut -c1-90)"
fi
dfok
if [ ! -e $RD/U.done ]; then
  timeout 7200 nice -n $NI python3 pcheck.py upperR2 $F $X nomax sol=$RD/sol_$T.json $A threads=$TH work=${WK}u > $RD/upper.log 2>&1
  date -u > $RD/U.done; note "xo+V8 U: $RG $(grep UPPER-R2 $RD/upper.log || echo 'no UPPER-R2 line (timeout?)')"
fi
if [ ! -e $RD/B.done ]; then
  nice -n $NI python3 pcheck.py binderR2 $F $X $A sol=$RD/sol_${T}L.json cert=$RD/cert_${T}L.json top=15 work=${WK}bd > $RD/binders.log 2>&1
  date -u > $RD/B.done
fi
md5sum $RD/*.json > $RD/md5.txt; rm -rf ${WK}k ${WK}L ${WK}u ${WK}bd; note "$RG all stages done (work dirs removed)"; echo DONE > $RD/ALL.done
