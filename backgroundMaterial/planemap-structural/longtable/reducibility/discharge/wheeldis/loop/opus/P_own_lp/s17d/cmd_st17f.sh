# Stage 17 (face pool F5, flag face5), FINDINGS stage 17. Engine: P_own_lp/s17d (prelay2.py = top-level 4f400216 + face5).
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P; M=$S/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s17d
F="filt16 killtab=../s16ap/kill6"
# validation: face5 off, filter off reproduces st16b0 (6/35) on argsA52
python3 pcheck.py lowerR2 apexcls v6 xon cert=../cert_st16b0.json xcap=3 root=$M args=../s19/argsA52.txt rpat=../rpatD.txt work=$S/wr17v > val_off_lower.log 2>&1
python3 pcheck.py upperR2 apexcls v6 xon nomax sol=../sol_st16b0.json root=$M args=../s19/argsA52.txt rpat=../rpatD.txt threads=1 work=$S/wr17v2 > val_off_upper.log 2>&1
# orientation + face5 physical test
python3 pcheck.py orientR2 xon apexcls v6 $F face5 root=$M args=../s19/argsA52.txt rpat=../rpatD.txt work=$S/wr17a > orient_st17f.log 2>&1
# solve: st16ap2 class + face5, warm from st16ap2 rows; keeppen fixed point, then exact unpenalised LP (nosep) for the cert
W="warm=../rows_st16ap2.txt,../rows_st16ap_run1.txt,../rows_st15f.txt,../rows_st15_run2.txt,../rows_st15_run1.txt,../rows_s12r50.txt,../rows_st14q.txt"
python3 pcheck.py solveR2 xon apexcls v6 $F face5 keeppen dbg tag=st17f root=$M args=../s19/argsA52.txt rpat=../rpatD.txt consbasis=../cons2basis_v6.json $W K=300 xcap=3 xpen=1e-3 threads=2 work=$S/wr17s > st17f.log 2>&1
