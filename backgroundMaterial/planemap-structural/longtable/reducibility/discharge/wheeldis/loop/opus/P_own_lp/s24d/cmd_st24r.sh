# Stage 24 re-run, one solve at a time, 4 threads, cap 3 h each. Engine P_own_lp/s24d (consall, big2 with dcap=3 dpen=1e-3).
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s24d
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
A="root=$M args=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s25/argsA59.txt rpat=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/rpatD.txt"
F0="xon apexcls filt16 killtab=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s25/f/kill/kill6 hat5 consall"
CB=consbasis=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s21/cf/cons2basis_cls.json
run1(){ tag=$1; warm=$2; shift 2; F="$*"
  date -u +%H:%M:%SZ > ${tag}_start.txt
  timeout 10800 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$warm K=300 xcap=3 xpen=1e-3 dcap=3 dpen=1e-3 threads=4 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr24r_$tag > $tag.log 2>&1 || echo "solve exit $?" >> $tag.log
  date -u +%H:%M:%SZ > ${tag}_end.txt
  python3 pcheck.py solveR2 $F nosep tag=${tag}L $A $CB warm=rows_$tag.txt,$warm K=300 xcap=3 dcap=3 threads=4 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr24r_${tag}L > ${tag}L.log 2>&1
  python3 pcheck.py lowerR2 $F cert=cert_${tag}L.json xcap=3 dcap=3 $A work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr24r_${tag}L > lower_${tag}L.log 2>&1
  python3 pcheck.py upperR2 $F nomax sol=sol_$tag.json dcap=3 $A threads=4 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr24r_${tag}u > upper_$tag.log 2>&1
}
run1 st24b /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s22/hf/rows_s22h.txt,/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s23/hf/rows_s23h.txt,/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s24d/rows_st24b_run1.txt $F0
cp rows_st24b.txt rows_st24b_final.txt
run1 st24d /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s24d/rows_st24b_final.txt,/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s24d/rows_st24d_run1.txt $F0 big2
echo DONE > done_r.txt
