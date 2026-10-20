# s33z resumable main pipeline.  usage: bash resume_s33.sh TAG SHA      (e.g. A67 2c97e14d)
# Main stack "includes k3p #1 [E2 guard]": l3q + zh + ZR + hatrr + l6r + pcell=pcell/k3p.txt on reg_TAG (prep_tag.sh TAG SHA).
# Every stage leaves a marker in run_TAG/; a re-run (e.g. after a container restart) skips finished stages and restarts an unfinished
# solve warm from EVERY rows file so far: rows_s33.txt / rows_q66.txt of the interrupted run are first snapshotted to rows_*_r<time>.txt.
# Stages: P prep | (bg) M89 prep, noC prep | (bg) Q l3q-only reference q66 (threads=1) | K stacked keeppen (threads=2, 3 h) |
#         L nosep ipm0 polish + lowerR2 ucap=100 + upperR2 | N same nosep LP without the k3p name | U upper on the newest origin/main |
#         X minus-89 upper / lower | C all-C-out upper + ccover.py | B binderR2 (8666655/5677657 + top 15).
TAG=$1; SHA=$2
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
R=/home/claude/GraphColourDeductiveSolver; W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; E=$S/eng; Q=$S/reg_$TAG; RD=$S/run_$TAG; mkdir -p $RD; cd $E
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W; WK=$SC/P/wr_$TAG
export OMP_NUM_THREADS=1
note() { echo "$(date -u +%H:%M:%SZ) [$TAG] $*" >> $S/wait.log; }
done_() { [ -e $RD/$1.done ]; }
mark() { date -u +%H:%M:%SZ > $RD/$1.done; }
note "resume_s33 start (pid $$)"
# ---- P: registry
if [ ! -e $Q/prep_done.txt ]; then (cd $S && bash prep_tag.sh $TAG $SHA > prep_$TAG.out 2>&1); fi
[ -e $Q/prep_done.txt ] || { note "prep failed"; exit 3; }
grep -q "RING-MERGE NAME PRESENT" $Q/reg_check.txt && { note "ring-merge name present: stop"; exit 3; }
A="root=$M args=$Q/args_$TAG.txt rpat=$B/rpatD.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
F0="$FQ zh zr hatrr zcap=3 l6r z6cap=3"; PC="pcell=$S/pcell/k3p.txt"; F="$F0 $PC"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
snap() { [ -s $1.txt ] && cp $1.txt ${1}_r$(date -u +%m%d%H%M%S).txt; rm -f $1.txt; }
# ---- background preps: minus-89 registry, D-only tables (only k3x_C / C-sources change)
X=$S/m89/$TAG; CC=$S/ccover/$TAG
( if [ ! -e $X/prep_done.txt ]; then mkdir -p $X/f/kill; cd $X
    python3 $S/m89/m89_build.py $S/m89/CGLUE-XRING-ENTRIES_27964810.txt $Q/k3x_C_$TAG.cfast k3x_C_${TAG}m89.cfast > m89_build.txt
    sed "s#cpat=$Q/k3x_C_$TAG.cfast#cpat=$X/k3x_C_${TAG}m89.cfast#" $Q/args_$TAG.txt > args_${TAG}m89.txt
    diff <(tr ' ' '\n' < $Q/args_$TAG.txt) <(tr ' ' '\n' < args_${TAG}m89.txt) >> m89_build.txt
    cp $B/s31/f/s16_filter.py $B/s31/f/s16_killnpy.py f/
    for U in 7 8 9; do (cd f && nice -n 10 python3 s16_filter.py $SC/ex_$TAG $Q/k3x_D_$TAG.out $X/k3x_C_${TAG}m89.cfast kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1); done
    for sg in 1 -1; do nice -n 10 python3 $S/l3qtab.py $SC/ex_$TAG $Q/k3x_D_$TAG.out $X/k3x_C_${TAG}m89.cfast tab_$sg.json $sg > tab_$sg.log 2>&1; done
    (cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
    for f in f/kill/kill6_U7.npy f/kill/kill6_U8.npy f/kill/kill6_U9.npy tab_1.json tab_-1.json; do a=$(md5sum < $Q/$f | cut -c1-32); b=$(md5sum < $f | cut -c1-32); [ $a = $b ] && s=SAME || s=DIFF; echo "$f $TAG $a m89 $b $s"; done > md5_compare.txt
    echo DONE > prep_done.txt; fi
  if [ ! -e $CC/prep_done.txt ]; then mkdir -p $CC/f/kill; cd $CC
    cp $B/s30t/f/s16_filter.py $B/s30t/f/s16_killnpy.py f/
    for U in 7 8 9; do (cd f && nice -n 10 python3 s16_filter.py $SC/ex_$TAG $Q/k3x_D_$TAG.out $S/ccover/k3x_C_empty.cfast kill/kill6_U$U.json wj=6 U=$U donly=1 > kill/kill6_U$U.log 2>&1); done
    for sg in 1 -1; do nice -n 10 python3 $S/ccover/l3qtab_noC.py $SC/ex_$TAG $Q/k3x_D_$TAG.out $S/ccover/k3x_C_empty.cfast tab_$sg.json $sg > tab_$sg.log 2>&1; done
    (cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
    md5sum f/kill/*.npy tab_*.json > md5_prep.txt; echo DONE > prep_done.txt; fi ) > $RD/bgprep.log 2>&1 &
BG=$!
BASE=rows_s33A66a.txt,rows_s33A64.txt,rows_q64A64.txt,rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt
# ---- Q: l3q-only reference (background, threads=1)
( if ! done_ Q; then snap rows_q66; WQ=$(ls rows_q66_r*.txt 2>/dev/null | paste -sd, -); WQ=${WQ:+$WQ,}$BASE,$B/s24d/rows_st24b_final.txt
    date -u +%H:%M:%SZ > $RD/q66_start.txt
    timeout 10800 nice -n 5 python3 pcheck.py solveR2 $FQ keeppen tag=q66 $A $CB warm=$WQ K=300 xcap=3 xpen=1e-3 threads=1 work=${WK}qs > $RD/q66.log 2>&1; ec=$?
    if [ $ec = 0 ] && [ sol_q66.json -nt $RD/q66_start.txt ]; then
      nice -n 5 python3 pcheck.py solveR2 $FQ nosep tag=q66L $A $CB warm=rows_q66.txt,$WQ K=300 xcap=3 threads=1 work=${WK}qL > $RD/q66L.log 2>&1
      nice -n 5 python3 pcheck.py lowerR2 $FQ cert=cert_q66L.json xcap=3 $A work=${WK}qL > $RD/lower_q66L.log 2>&1
      timeout 3600 nice -n 5 python3 pcheck.py upperR2 $FQ nomax sol=sol_q66.json $A threads=1 work=${WK}qu > $RD/upper_q66.log 2>&1
      cp sol_q66.json cert_q66L.json $RD/; mark Q
    else note "q66 keeppen exit $ec (not converged); re-run resume_s33.sh to continue"; fi; fi ) &
QP=$!
# ---- K: stacked keeppen
if ! done_ K; then
  snap rows_s33; WS=$(ls rows_s33_r*.txt 2>/dev/null | paste -sd, -); WARM=${WS:+$WS,}$BASE; echo "$WARM" > $RD/warm_K.txt
  note "K keeppen start, warm $(echo $WARM | tr ',' '\n' | wc -l) files"
  date -u +%H:%M:%SZ > $RD/K_start.txt
  timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=s33 $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=1500 threads=2 work=${WK}s > $RD/s33.log 2>&1; ec=$?
  if [ $ec = 0 ] && [ sol_s33.json -nt $RD/K_start.txt ]; then cp sol_s33.json rows_s33.txt $RD/; mark K; note "K converged: $(grep '^iter' $RD/s33.log | tail -1 | cut -c1-40)"
  else note "K exit $ec (not converged); re-run resume_s33.sh $TAG $SHA to continue warm"; wait $QP; exit 4; fi
fi
WARM=rows_s33.txt,$(cat $RD/warm_K.txt)
# ---- L: lower / upper
if ! done_ L; then
  timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F nosep ipm0 polish tag=s33L $A $CB warm=$WARM K=300 xcap=3 threads=2 work=${WK}L > $RD/s33L.log 2>&1
  nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_s33L.json xcap=3 ucap=100 $A work=${WK}L > $RD/lower_s33L.log 2>&1
  timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_s33.json $A threads=2 work=${WK}u > $RD/upper_s33.log 2>&1
  python3 -c "
import json; S=json.load(open('sol_s33.json')); print('max column value by family:', {k:(len(v), max(v.values()) if isinstance(v, dict) else max(x[1] for x in v)) for k,v in S.items() if isinstance(v,(dict,list)) and v and k!='V'})" >> $RD/upper_s33.log 2>&1
  cp sol_s33L.json cert_s33L.json $RD/; md5sum sol_s33.json sol_s33L.json cert_s33L.json rows_s33.txt > $RD/md5_s33.txt; mark L
  note "L: $(tail -1 $RD/lower_s33L.log | cut -c1-90) | $(grep UPPER-R2 $RD/upper_s33.log)"
fi
# ---- N: t* without the k3p name (same final rows)
if ! done_ N; then
  nice -n 5 python3 pcheck.py solveR2 $F0 nosep ipm0 polish tag=s33N $A $CB warm=$WARM K=300 xcap=3 threads=2 work=${WK}N > $RD/s33N.log 2>&1
  nice -n 5 python3 pcheck.py lowerR2 $F0 cert=cert_s33N.json xcap=3 ucap=100 $A work=${WK}N > $RD/lower_s33N.log 2>&1; mark N
fi
wait $BG
# ---- U: upper on the newest origin/main head
if ! done_ U; then
  git -C $R fetch -q origin main; H=$(git -C $R rev-parse --short=8 origin/main)
  dm=$(git -C $R show $H:$W/out/job30/k3x_D.out | md5sum | cut -c1-32); cm=$(git -C $R show $H:$W/out/job30/k3x_C.cfast | md5sum | cut -c1-32)
  if [ "$dm $cm" = "$(md5sum < $Q/k3x_D_$TAG.out | cut -c1-32) $(md5sum < $Q/k3x_C_$TAG.cfast | cut -c1-32)" ]; then
    echo "newest origin/main $H: k3x identical to $TAG ($SHA) -> upper_s33.log is the check: $(grep UPPER-R2 $RD/upper_s33.log)" > $RD/upper_newest.txt
  else
    HT=H$H; [ -e $S/reg_$HT/prep_done.txt ] || (cd $S && bash prep_tag.sh $HT $H > prep_$HT.out 2>&1)
    HQ=$S/reg_$HT; FH="xon apexcls filt16 killtab=$HQ/f/kill/kill6 hat5 consall l3q l3qtab=$HQ/tab_1.json,$HQ/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 $PC"
    timeout 10800 nice -n 5 python3 pcheck.py upperR2 $FH nomax sol=sol_s33.json root=$M args=$HQ/args_$HT.txt rpat=$B/rpatD.txt threads=2 work=${WK}u$H > $RD/upper_s33_$HT.log 2>&1
    { echo "newest origin/main $H ($(head -1 $HQ/reg_check.txt))"; grep UPPER-R2 $RD/upper_s33_$HT.log; } > $RD/upper_newest.txt
  fi; mark U; note "U: $(tail -1 $RD/upper_newest.txt)"
fi
# ---- X: minus-89
if ! done_ X; then
  FX="xon apexcls filt16 killtab=$X/f/kill/kill6 hat5 consall l3q l3qtab=$X/tab_1.json,$X/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 $PC"
  AX="root=$M args=$X/args_${TAG}m89.txt rpat=$B/rpatD.txt"
  timeout 10800 nice -n 5 python3 pcheck.py upperR2 $FX nomax sol=sol_s33.json $AX threads=2 work=${WK}xu > $RD/upper_s33_m89.log 2>&1
  nice -n 5 python3 pcheck.py lowerR2 $FX cert=cert_s33L.json xcap=3 ucap=100 $AX work=${WK}xL > $RD/lower_s33L_m89.log 2>&1
  mark X; note "X: $(grep UPPER-R2 $RD/upper_s33_m89.log) | $(tail -1 $RD/lower_s33L_m89.log | cut -c1-80)"
fi
# ---- C: all C out + ccover
if ! done_ C; then
  VF=$SC/ccover_${TAG}_vrows.txt; : > $VF
  FN="xon apexcls filt16 killtab=$CC/f/kill/kill6 hat5 consall l3q l3qtab=$CC/tab_1.json,$CC/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 $PC"
  timeout 14400 nice -n 5 python3 pcheck.py upperR2 $FN noC noCw nomax vK=1e12 vfile=$VF sol=sol_s33.json $A threads=2 work=${WK}nc > $RD/upper_s33_noC.log 2>&1
  { wc -l < $VF; md5sum $VF; } > $RD/vrows_count.txt
  nice -n 5 python3 -I $S/ccover/ccover.py $VF $Q/args_$TAG.txt $M $S/m89/CGLUE-XRING-ENTRIES_27964810.txt $RD/ccover > $RD/ccover.log 2>&1
  mark C; note "C: $(grep -E '^sole-cover set' $RD/ccover/ccover_summary.txt)"
fi
# ---- B: binder probe
if ! done_ B; then
  nice -n 5 python3 pcheck.py binderR2 $F $A sol=sol_s33L.json cert=cert_s33L.json row=7:8666655:5677657 top=15 work=${WK}bd > $RD/binders_s33L.log 2>&1
  nice -n 5 python3 pcheck.py binderR2 $F $A sol=sol_s33.json cert=cert_s33L.json row=7:8666655:5677657 work=${WK}bd > $RD/binder_s33_upper.log 2>&1
  mark B
fi
wait $QP
note "resume_s33 all stages done"; echo DONE > $RD/ALL.done
