# s28q: l3q V = 7 solve (RELAY_SPEC_s21). REG=A60 (7360eb92, first run), A61 (7a3857a0), A62 (3cfd7f18; warm rows_s28A60 + st24b_final), st24b flags + l3q, warm s24d/rows_st24b_final.txt,
# threads=2, keeppen timeout 3 h, then nosep, lowerR2, upperR2 on the keeppen solution. Engine s28q/eng.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s28q; cd $S/eng
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr28
REG=${REG:-A60}
if [ $REG = A60 ]; then ARGS=$B/s29/argsA60.txt; KT=$B/s29/f/kill/kill6; TAB=$S/tab60_1.json,$S/tab60_-1.json
elif [ $REG = A61 ]; then ARGS=$B/s30h/r7a/argsA61.txt; KT=$B/s30h/r7a/f/kill/kill6; TAB=$S/tab61_1.json,$S/tab61_-1.json
elif [ $REG = A62 ]; then ARGS=$B/s31/argsA62.txt; KT=$B/s31/f/kill/kill6; TAB=$S/tab62_1.json,$S/tab62_-1.json
else ARGS=$B/s25/argsA59.txt; KT=$B/s25/f/kill/kill6; TAB=$S/tab59_1.json,$S/tab59_-1.json; fi
A="root=$M args=$ARGS rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$KT hat5 consall l3q l3qtab=$TAB lqcap=3"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WARM=$B/s24d/rows_st24b_final.txt
[ $REG != A60 ] && WARM=$S/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
tag=s28$REG
date -u +%H:%M:%SZ > $S/${tag}_start.txt
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 threads=2 work=${WK}s > $S/$tag.log 2>&1 || echo "solve exit $?" >> $S/$tag.log
date -u +%H:%M:%SZ > $S/${tag}_end.txt
nice -n 5 python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$WARM K=300 xcap=3 threads=2 work=${WK}L > $S/${tag}L.log 2>&1
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 $A work=${WK}L > $S/lower_${tag}L.log 2>&1
nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json $A threads=2 work=${WK}u > $S/upper_$tag.log 2>&1
md5sum sol_$tag.json sol_${tag}L.json cert_${tag}L.json rows_$tag.txt > $S/md5_$tag.txt 2>&1
echo DONE > $S/done_$tag.txt
