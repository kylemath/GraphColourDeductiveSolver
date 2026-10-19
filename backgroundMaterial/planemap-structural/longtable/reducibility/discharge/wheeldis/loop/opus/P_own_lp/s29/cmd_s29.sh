# s29: st24b configuration re-solved on registry 7360eb92 (argsA60). Recipe s24d/cmd_st24r.sh run1 (st24b), flags xon apexcls filt16 hat5 consall,
# dcap/dpen OFF, warm s24d/rows_st24b_final.txt, threads=2, keeppen timeout 3 h. ex60 = ex59 + git archive 3191ecf2 (explore r52k) W/loop.
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s29
EX=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex60
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
TD=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s29/k3x_D_7360eb92.out; TC=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s29/k3x_C_7360eb92.cfast
# 1) strict kill tables (2 at a time) + dcount
(cd f; python3 s16_filter.py $EX $TD $TC kill/kill6_U7.json wj=6 U=7 > kill/kill6_U7.log 2>&1 & python3 s16_filter.py $EX $TD $TC kill/kill6_U8.json wj=6 U=8 > kill/kill6_U8.log 2>&1 & wait)
(cd f && exec python3 s16_filter.py $EX $TD $TC kill/kill6_U9.json wj=6 U=9 > kill/kill6_U9.log 2>&1) &
python3 dcount.py argsA60.txt $M > dcount.txt 2>&1; wait
(cd f; python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
# 2) check 4
(cd f; python3 s16_check4.py $EX $TD $TC unk=99 > check4_unk99.log 2>&1 & python3 s16_check4.py $EX $TD $TC unk=5 > check4_unk5.log 2>&1 & wait; python3 s16_check4.py $EX $TD $TC unk=7 > check4_unk7.log 2>&1)
echo TABLES_DONE > tables_done.txt
# 3) solve
A="root=$M args=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s29/argsA60.txt rpat=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/rpatD.txt"
F="xon apexcls filt16 killtab=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s29/f/kill/kill6 hat5 consall"
CB=consbasis=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s21/cf/cons2basis_cls.json
WARM=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s24d/rows_st24b_final.txt
tag=s29
date -u +%H:%M:%SZ > ${tag}_start.txt
timeout 10800 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 threads=2 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P2work29s > $tag.log 2>&1 || echo "solve exit $?" >> $tag.log
date -u +%H:%M:%SZ > ${tag}_end.txt
python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$WARM K=300 xcap=3 threads=2 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P2work29L > ${tag}L.log 2>&1
python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 $A work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P2work29L > lower_${tag}L.log 2>&1
python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json $A threads=2 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P2work29u > upper_$tag.log 2>&1
md5sum sol_$tag.json sol_${tag}L.json cert_${tag}L.json rows_$tag.txt > md5_out.txt 2>&1
echo DONE > done.txt
