# s35f: our own whole-face rule fy (RELAY_SPEC_s20, engine = s25c copy) converged on origin/main 413ba030 (registry 2,555 D / 1,097 C,
# ring-merge 3 held). s24d flags + fy, no l3q. keeppen (cap 5 h) -> nosep (cap 5 h) -> lowerR2 -> upperR2.
# Warm: s25c/rows_st25y.txt + s28q/eng/rows_s28A62.txt (receiver rows; each re-checked admissible on load).
# CPU gate: threads=1 while s33z's solve (pcheck ... tag=s33) runs, else 2; re-checked before each stage.
# Optional second pass (fy + g7, EXPLORATORY: g7 names are not in the registry) with tag s35g if GO_G7=1.
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Q=$P/s35f; cd $Q
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
EX=$S/ex63; TD=$Q/k3x_D_413ba030.out; TC=$Q/k3x_C_413ba030.cfast
gate(){ if pgrep -f 'pcheck.py .*tag=s33' > /dev/null; then TH=1; else TH=2; fi; echo "$(date -u +%H:%M:%SZ) $1 threads=$TH" >> gate.log; }
if [ ! -f tables_done.txt ]; then
  date -u +%H:%M:%SZ > kill_start.txt
  for U in 7 8 9; do (cd f && nice -n 5 python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1); done
  (cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
  nice -n 5 python3 dcount.py argsA63.txt $M > dcount.txt 2>&1
  md5sum f/kill/*.npy $P/s25/f/kill/*.npy $P/s31/f/kill/*.npy > kill_md5.txt
  date -u +%H:%M:%SZ > tables_done.txt
fi
A="root=$M args=$Q/argsA63.txt rpat=$P/rpatD.txt"
CB=consbasis=$P/s21/cf/cons2basis_cls.json
WARM=$P/s25c/rows_st25y.txt,$P/s28q/eng/rows_s28A62.txt
run(){ tag=$1; F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall $2"
  gate ${tag}_solve; date -u +%H:%M:%SZ > ${tag}_start.txt
  timeout 18000 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 threads=$TH work=$S/P/wr35_$tag > $tag.log 2>&1 || echo "solve exit $?" >> $tag.log
  date -u +%H:%M:%SZ > ${tag}_end.txt
  gate ${tag}L_solve
  timeout 18000 nice -n 5 python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$WARM K=300 xcap=3 threads=$TH work=$S/P/wr35_${tag}L > ${tag}L.log 2>&1 || echo "solve exit $?" >> ${tag}L.log
  date -u +%H:%M:%SZ > ${tag}L_end.txt
  nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 $A work=$S/P/wr35_${tag}L > lower_${tag}L.log 2>&1
  gate ${tag}_upper
  nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json $A threads=$TH work=$S/P/wr35_${tag}u > upper_$tag.log 2>&1
  md5sum sol_$tag.json sol_${tag}L.json cert_${tag}L.json rows_$tag.txt rows_${tag}L.txt > md5_$tag.txt 2>&1
  echo DONE > done_$tag.txt; }
run s35f fy
[ "$GO_G7" = 1 ] && run s35g "fy g7"
echo DONE > done.txt
