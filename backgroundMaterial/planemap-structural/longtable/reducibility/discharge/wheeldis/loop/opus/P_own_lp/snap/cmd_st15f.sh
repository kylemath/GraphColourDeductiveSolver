# st15f: stage 15 with the soundness fix (v6: conservation over ALL 1424 non-R6 6-types, incl. no-five ones). Engine snap/st15f (md5 snap/st15f_md5.txt).
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P; M=$S/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
python3 pcheck.py consbasisR2 apexcls v6 out=cons2basis_v6.json root=$M args=s17/argsA50.txt work=$S/wr21
python3 pcheck.py solveR2 xon apexcls v6 dbg tag=st15f root=$M args=s17/argsA50.txt rpat=rpatD.txt consbasis=cons2basis_v6.json warm=rows_st15_run2.txt,rows_st15_run1.txt,rows_s12r50.txt,rows_st14q.txt K=300 xcap=3 xpen=1e-3 threads=3 work=$S/wr30
python3 pcheck.py lowerR2 apexcls v6 xon cert=cert_st15f.json xcap=3 root=$M args=s17/argsA50.txt rpat=rpatD.txt work=$S/wr30
python3 pcheck.py upperR2 apexcls v6 xon nomax sol=sol_st15f.json root=$M args=s17/argsA50.txt rpat=rpatD.txt threads=2 work=$S/wr29
