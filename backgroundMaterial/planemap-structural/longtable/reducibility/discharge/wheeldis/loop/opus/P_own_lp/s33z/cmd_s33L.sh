# s33L: after cmd_s33k.sh (keeppen) on SHA: nosep LP over rows_s33 + warm with ipm0 polish (simplex on the stacked LP is too slow),
# lowerR2 with ucap=100 (IPM duals leave ~1e-13 negative rcs on uncapped y/r/g columns; priced at a cap of 100 -> the bound holds
# for the family with every column <= 100; cost ~1e-9), upperR2 on the keeppen solution (also checked against 100 below).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33
export OMP_NUM_THREADS=1
SHA=$1; TH=${2:-2}; Q=${3:-$S/reg_$SHA}; ARGS=${4:-$Q/args_$SHA.txt}; tag=${5:-s33}; SOLW=${6:-rows_s33.txt}
until [ -e $S/done_s33k.txt ]; do sleep 60; done
A="root=$M args=$ARGS rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WARM=$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt
echo "$(date -u +%H:%M:%SZ) $tag nosep/lower/upper start" >> $S/wait.log
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F nosep ipm0 polish tag=${tag}L $A $CB warm=$SOLW,$WARM K=300 xcap=3 threads=$TH work=${WK}L > $S/${tag}L.log 2>&1 || echo "solve exit $?" >> $S/${tag}L.log
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 ucap=100 $A work=${WK}L > $S/lower_${tag}L.log 2>&1
timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_s33.json $A threads=$TH work=${WK}u > $S/upper_$tag.log 2>&1 || echo "upper exit $?" >> $S/upper_$tag.log
python3 -c "
import json; S=json.load(open('sol_s33.json')); print('max column value by family:', {k:(len(v), max(v.values()) if v else 0) for k,v in S.items() if isinstance(v,dict)})" >> $S/upper_$tag.log 2>&1
md5sum sol_s33.json sol_${tag}L.json cert_${tag}L.json rows_s33.txt > $S/md5_$tag.txt 2>&1
echo DONE > $S/done_$tag.txt
