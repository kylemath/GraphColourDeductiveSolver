# s33z: signed Z± (zh + zr, RELAY_SPEC_s22) + hatrr + l3q on 3cfd7f18 (s31/argsA62, killtab s31/f/kill/kill6, l3q tab62).
# 1) bounded wait (5-min checks) for the l3q worker's A62 solve (s28q/done_s28A62.txt); after 03:00Z run anyway at threads=1.
# 2) keeppen solve (3 h cap) -> nosep L solve (3 h cap) -> lowerR2 on the L cert -> upperR2 on the keeppen solution.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33
export OMP_NUM_THREADS=1
TH=2
while [ ! -e $B/s28q/done_s28A62.txt ]; do
  if [ $(date -u +%H%M) -ge 0300 ] && [ $(date -u +%H%M) -lt 1200 ]; then TH=1; echo "03:00Z reached without done_s28A62; running at threads=1" >> $S/wait.log; break; fi
  echo "$(date -u +%H:%M:%SZ) waiting for s28q/done_s28A62.txt" >> $S/wait.log; sleep 300
done
echo "$(date -u +%H:%M:%SZ) start, threads=$TH" >> $S/wait.log
A="root=$M args=$B/s31/argsA62.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$B/s31/f/kill/kill6 hat5 consall l3q l3qtab=$B/s28q/tab62_1.json,$B/s28q/tab62_-1.json lqcap=3 zh zr hatrr zcap=3"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WARM=$B/s28q/eng/rows_s28A60.txt
[ -s $B/s28q/eng/rows_s28A62.txt ] && WARM=$B/s28q/eng/rows_s28A62.txt,$WARM
echo "warm: $WARM" >> $S/wait.log
tag=s33
date -u +%H:%M:%SZ > $S/${tag}_start.txt
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 threads=$TH work=${WK}s > $S/$tag.log 2>&1 || echo "solve exit $?" >> $S/$tag.log
date -u +%H:%M:%SZ > $S/${tag}_end.txt
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$WARM K=300 xcap=3 threads=$TH work=${WK}L > $S/${tag}L.log 2>&1 || echo "solve exit $?" >> $S/${tag}L.log
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 $A work=${WK}L > $S/lower_${tag}L.log 2>&1
timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json $A threads=$TH work=${WK}u > $S/upper_$tag.log 2>&1 || echo "upper exit $?" >> $S/upper_$tag.log
md5sum sol_$tag.json sol_${tag}L.json cert_${tag}L.json rows_$tag.txt > $S/md5_$tag.txt 2>&1
echo DONE > $S/done_$tag.txt
