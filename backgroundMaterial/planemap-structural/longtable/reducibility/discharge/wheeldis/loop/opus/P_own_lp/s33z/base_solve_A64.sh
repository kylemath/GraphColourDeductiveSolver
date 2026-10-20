# l3q-only reference solve on A64 (the s28A62L cert is INVALID on A64: 6 receiver rows newly killed). Same pipeline as s28q/cmd_s28.sh, threads=1,
# s33z engine, flags l3q only; waits for smoke_pol to end so the box stays at <= 4 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S=$B/s33z; cd $S/eng; Q=$S/reg_A64
until [ -s $S/smoke_pol_lower.log ]; do sleep 60; done
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33q; export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A64.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WARM=$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
tag=q64
date -u +%H:%M:%SZ > $S/${tag}_start.txt
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 threads=1 work=${WK}s > $S/$tag.log 2>&1 || echo "solve exit $?" >> $S/$tag.log
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$WARM K=300 xcap=3 threads=1 work=${WK}L > $S/${tag}L.log 2>&1 || echo "solve exit $?" >> $S/${tag}L.log
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 $A work=${WK}L > $S/lower_${tag}L.log 2>&1
timeout 3600 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json $A threads=1 work=${WK}u > $S/upper_$tag.log 2>&1
date -u +%H:%M:%SZ > $S/${tag}_end.txt
echo DONE > $S/done_$tag.txt
