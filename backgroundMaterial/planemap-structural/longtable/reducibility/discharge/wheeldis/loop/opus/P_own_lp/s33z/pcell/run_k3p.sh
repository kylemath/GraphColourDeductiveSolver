# k3p, pending Studio guard. Variant kept separate from the main stacked number: the stacked A66 solution plus the one absorbable
# private-cell kill q7-_....556_....56._::::::5 (g7 #1) through the pcell mask (s36g privcell.py / pcell=FILE, a9da7812, ported).
# Runs only after the main result, the minus-89 checks and the C-cover outputs (done_ccover.txt). Tags s33p*, work dirs wr33p*.
# 1) lowerR2 of cert_s33L with the name (ucap=100 as the main lower). 2) If INVALID: warm re-solve (keeppen 3 h, then nosep ipm0 polish,
# lowerR2, upperR2), warm rows_s33 + the main warm set. 3) t* with / without the name.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; O=$S/pcell; Q=$S/reg_A66; cd $S/eng
until [ -e $S/ccover/done_ccover.txt ] && [ -e $O/regress_done.txt ]; do sleep 60; done
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=$SC/P/wr33p; export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A66.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 pcell=$O/k3p.txt"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WARM=rows_s33.txt,rows_s33A64.txt,rows_q64A64.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt
echo "$(date -u +%H:%M:%SZ) k3p variant start" >> $S/wait.log
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_s33L.json xcap=3 ucap=100 $A work=${WK}c > $O/lower_s33L_k3p.log 2>&1
if ! grep -q "LOWER-R2: VALID" $O/lower_s33L_k3p.log; then
  date -u +%H:%M:%SZ > $O/s33p_start.txt
  timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=s33p $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 threads=2 work=${WK}s > $O/s33p.log 2>&1 || echo "solve exit $?" >> $O/s33p.log
  timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F nosep ipm0 polish tag=s33pL $A $CB warm=rows_s33p.txt,$WARM K=300 xcap=3 threads=2 work=${WK}L > $O/s33pL.log 2>&1 || echo "solve exit $?" >> $O/s33pL.log
  nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_s33pL.json xcap=3 ucap=100 $A work=${WK}L > $O/lower_s33pL.log 2>&1
  timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_s33p.json $A threads=2 work=${WK}u > $O/upper_s33p.log 2>&1 || echo "upper exit $?" >> $O/upper_s33p.log
  md5sum sol_s33p.json sol_s33pL.json cert_s33pL.json rows_s33p.txt > $O/md5_s33p.txt 2>&1
  date -u +%H:%M:%SZ > $O/s33p_end.txt
fi
echo "$(date -u +%H:%M:%SZ) k3p variant done" >> $S/wait.log
echo DONE > $O/done_k3p.txt
