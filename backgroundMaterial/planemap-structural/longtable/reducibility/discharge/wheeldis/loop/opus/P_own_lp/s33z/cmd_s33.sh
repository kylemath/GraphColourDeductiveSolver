# s33z: signed Z± (zh + zr, RELAY_SPEC_s22) + hatrr + l3q on Studio head SHA (reg_SHA from prep_head.sh: args, kill6, l3q tables).
# usage: bash cmd_s33.sh SHA [threads]   (the wait for the l3q A62 solve is done outside, by wait_s33.sh)
# keeppen solve (3 h cap) -> nosep L solve (3 h cap) -> lowerR2 on the L cert -> upperR2 on the keeppen solution.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33
export OMP_NUM_THREADS=1
SHA=$1; TH=${2:-2}; Q=$S/reg_$SHA
[ -e $Q/prep_done.txt ] || { echo "no prep for $SHA" >> $S/wait.log; exit 3; }
echo "$(date -u +%H:%M:%SZ) start on $SHA, threads=$TH" >> $S/wait.log
A="root=$M args=$Q/args_$SHA.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3"
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
