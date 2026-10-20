# Stage 25 (RELAY_SPEC_s20): fy flag on the s24d engine copy. keeppen -> nosep -> lowerR2 -> upperR2 (on the solution itself).
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s25c
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
A="root=$M args=$P/s25/argsA59.txt rpat=$P/rpatD.txt"
F="xon apexcls filt16 killtab=$P/s25/f/kill/kill6 hat5 consall fy g7"
CB=consbasis=$P/s21/cf/cons2basis_cls.json
WARM=$P/s22/hf/rows_s22h.txt,$P/s23/hf/rows_s23h.txt,$P/s24d/rows_st24b_run1.txt,$P/s24d/rows_st24b_final.txt,/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s25c/rows_st25y.txt
tag=st25yg
date -u +%H:%M:%SZ > ${tag}_start.txt
timeout 10800 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 threads=4 work=$SC/wr25_$tag > $tag.log 2>&1 || echo "solve exit $?" >> $tag.log
date -u +%H:%M:%SZ > ${tag}_end.txt
python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$WARM K=300 xcap=3 threads=4 work=$SC/wr25_${tag}L > ${tag}L.log 2>&1
python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 $A work=$SC/wr25_${tag}L > lower_${tag}L.log 2>&1
python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json $A threads=4 work=$SC/wr25_${tag}u > upper_$tag.log 2>&1
echo DONE > done25g.txt
