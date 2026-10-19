# run 1 (st17f, cmd_st17f.sh) stopped after iteration 0: the warm-row LP (a relaxation of the face5 class) already gives t = 6/37.
# Exact lower cert over the same warm rows, no x penalty, no separation:
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P; M=$S/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s17d
W0="warm=../rows_st16ap2.txt,../rows_st16ap_run1.txt,../rows_st15f.txt,../rows_st15_run2.txt,../rows_st15_run1.txt,../rows_s12r50.txt,../rows_st14q.txt"
python3 pcheck.py solveR2 xon apexcls v6 filt16 killtab=../s16ap/kill6 face5 nosep tag=st17fL root=$M args=../s19/argsA52.txt rpat=../rpatD.txt consbasis=../cons2basis_v6.json $W0 K=300 xcap=3 threads=1 work=$S/wr17L > st17fL.log 2>&1
python3 pcheck.py lowerR2 apexcls v6 xon filt16 killtab=../s16ap/kill6 face5 cert=cert_st17fL.json xcap=3 root=$M args=../s19/argsA52.txt rpat=../rpatD.txt work=$S/wr17L > lower_st17fL.log 2>&1
