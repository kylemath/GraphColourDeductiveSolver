# s30h re-solve (only run if an upper check of sol_st24b fails): st24b recipe (s24d/cmd_st24r.sh run1) on Studio head 7a3857a0
# (argsA61 = argsA60 with k3x_D/C of 7a3857a0), kill tables r7a/f/kill. threads=2, keeppen cap 3 h, warm st24b_final + s29 rows.
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
H=$P/s30h; cd $H
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
A="root=$M args=$H/r7a/argsA61.txt rpat=$P/rpatD.txt"
F="xon apexcls filt16 killtab=$H/r7a/f/kill/kill6 hat5 consall"
CB=consbasis=$P/s21/cf/cons2basis_cls.json
WARM=$P/s24d/rows_st24b_final.txt,$P/s29/rows_s29.txt
tag=s30r
date -u +%H:%M:%SZ > ${tag}_start.txt
timeout 10800 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 dcap=3 dpen=1e-3 threads=2 work=$S/P/wr30h_$tag > $tag.log 2>&1 || echo "solve exit $?" >> $tag.log
date -u +%H:%M:%SZ > ${tag}_end.txt
python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$WARM K=300 xcap=3 dcap=3 threads=2 work=$S/P/wr30h_${tag}L > ${tag}L.log 2>&1
python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 dcap=3 $A work=$S/P/wr30h_${tag}L > lower_${tag}L.log 2>&1
python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json dcap=3 $A threads=2 work=$S/P/wr30h_${tag}u > upper_$tag.log 2>&1
md5sum sol_$tag.json sol_${tag}L.json cert_${tag}L.json rows_$tag.txt > md5_$tag.txt 2>&1
echo DONE > done_$tag.txt
