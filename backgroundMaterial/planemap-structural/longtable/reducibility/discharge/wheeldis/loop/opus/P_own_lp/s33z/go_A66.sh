# s33z restart on registry A66 = main 3d6c4f9a (coordinator, 00:5xZ). Waits for prep_A66, stops the A64 stacked keeppen (iter ~5-8,
# its rows kept as rows_s33A64.txt), then: stacked keeppen on A66 (tag s33, warm rows_s33A64 + rows_q64A64 + rows_s28A62 + rows_s28A60,
# threads=2, 3 h) in parallel with the l3q-only reference q66 on A66 (threads=1). Then stacked nosep (ipm0 polish) + lowerR2 ucap=100 +
# upperR2, q66 lower/upper, then the m89 prep on A66 and the minus-89 checks.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng; Q=$S/reg_A66
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr66
export OMP_NUM_THREADS=1
until [ -e $Q/prep_done.txt ]; do sleep 60; done
a=cmd_s33k; pkill -f "bash $a.sh A64" ; p=$(pgrep -f "keeppen tag=s33 root"); [ -n "$p" ] && kill $p; sleep 5
cp rows_s33.txt rows_s33A64.txt; grep "^iter" $S/s33.log | tail -1 | cut -c1-80 > $S/s33A64_lastiter.txt; cp $S/s33.log $S/s33A64.log
echo "$(date -u +%H:%M:%SZ) A64 keeppen stopped at $(cut -c1-30 $S/s33A64_lastiter.txt); start A66" >> $S/wait.log
A="root=$M args=$Q/args_A66.txt rpat=$B/rpatD.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
F="$FQ zh zr hatrr zcap=3 l6r z6cap=3"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WARM=rows_s33A64.txt,rows_q64A64.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt
WQ=rows_q64A64.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
( date -u +%H:%M:%SZ > $S/q66_start.txt
  timeout 10800 nice -n 5 python3 pcheck.py solveR2 $FQ keeppen tag=q66 $A $CB warm=$WQ K=300 xcap=3 xpen=1e-3 threads=1 work=${WK}qs > $S/q66.log 2>&1 || echo "solve exit $?" >> $S/q66.log
  timeout 10800 nice -n 5 python3 pcheck.py solveR2 $FQ nosep tag=q66L $A $CB warm=rows_q66.txt,$WQ K=300 xcap=3 threads=1 work=${WK}qL > $S/q66L.log 2>&1 || echo "solve exit $?" >> $S/q66L.log
  nice -n 5 python3 pcheck.py lowerR2 $FQ cert=cert_q66L.json xcap=3 $A work=${WK}qL > $S/lower_q66L.log 2>&1
  timeout 3600 nice -n 5 python3 pcheck.py upperR2 $FQ nomax sol=sol_q66.json $A threads=1 work=${WK}qu > $S/upper_q66.log 2>&1
  date -u +%H:%M:%SZ > $S/q66_end.txt; echo DONE > $S/done_q66.txt ) &
date -u +%H:%M:%SZ > $S/s33_start.txt
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=s33 $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 threads=2 work=${WK}s > $S/s33.log 2>&1 || echo "solve exit $?" >> $S/s33.log
date -u +%H:%M:%SZ > $S/s33_end.txt
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F nosep ipm0 polish tag=s33L $A $CB warm=rows_s33.txt,$WARM K=300 xcap=3 threads=2 work=${WK}L > $S/s33L.log 2>&1 || echo "solve exit $?" >> $S/s33L.log
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_s33L.json xcap=3 ucap=100 $A work=${WK}L > $S/lower_s33L.log 2>&1
timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_s33.json $A threads=2 work=${WK}u > $S/upper_s33.log 2>&1 || echo "upper exit $?" >> $S/upper_s33.log
python3 -c "
import json; S=json.load(open('sol_s33.json')); print('max column value by family:', {k:(len(v), max(v.values()) if v else 0) for k,v in S.items() if isinstance(v,dict)})" >> $S/upper_s33.log 2>&1
md5sum sol_s33.json sol_s33L.json cert_s33L.json rows_s33.txt > $S/md5_s33.txt 2>&1
echo DONE > $S/done_s33.txt
echo "$(date -u +%H:%M:%SZ) A66 stacked done" >> $S/wait.log
wait
