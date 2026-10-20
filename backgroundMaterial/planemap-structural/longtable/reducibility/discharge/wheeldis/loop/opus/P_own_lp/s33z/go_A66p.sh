# s33z main stacked solve on A66 (main 3d6c4f9a), "includes k3p #1 [E2 guard]": stack l3q + zh + ZR + hatrr + l6r + pcell=k3p.txt
# (g7 #1 q7-_....556_....56._::::::5; Studio guard G0-G6 passed, coordinator 02:3xZ). Warm restart after the first A66 run died at iter 10
# in write_l3q (noise assert, now clipped): warm rows_s33A66a (A66 run 1) + rows_s33A64 + rows_q64A64 + s28 A62/A60 rows.
# In parallel (threads=1): q66 l3q-only reference (no pcell) warm from rows_q66A66a.
# After: nosep (ipm0 polish), lowerR2 ucap=100, upperR2; s33N = the same nosep LP over the final rows WITHOUT the k3p name (lower for t* without it).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng; Q=$S/reg_A66
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr66p
export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A66.txt rpat=$B/rpatD.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
F0="$FQ zh zr hatrr zcap=3 l6r z6cap=3"; F="$F0 pcell=$S/pcell/k3p.txt"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WARM=rows_s33A66a.txt,rows_s33A64.txt,rows_q64A64.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt
WQ=rows_q66A66a.txt,rows_q64A64.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
echo "$(date -u +%H:%M:%SZ) A66 stacked + k3p start" >> $S/wait.log
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
import json; S=json.load(open('sol_s33.json')); print('max column value by family:', {k:(len(v), max(v.values()) if isinstance(v, dict) else max(x[1] for x in v)) for k,v in S.items() if isinstance(v,(dict,list)) and v and k!='V'})" >> $S/upper_s33.log 2>&1
md5sum sol_s33.json sol_s33L.json cert_s33L.json rows_s33.txt > $S/md5_s33.txt 2>&1
echo DONE > $S/done_s33.txt
echo "$(date -u +%H:%M:%SZ) A66 stacked + k3p done" >> $S/wait.log
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F0 nosep ipm0 polish tag=s33N $A $CB warm=rows_s33.txt,$WARM K=300 xcap=3 threads=2 work=${WK}N > $S/pcell/s33N.log 2>&1 || echo "solve exit $?" >> $S/pcell/s33N.log
nice -n 5 python3 pcheck.py lowerR2 $F0 cert=cert_s33N.json xcap=3 ucap=100 $A work=${WK}N > $S/pcell/lower_s33N.log 2>&1
echo DONE > $S/pcell/done_s33N.txt
wait
