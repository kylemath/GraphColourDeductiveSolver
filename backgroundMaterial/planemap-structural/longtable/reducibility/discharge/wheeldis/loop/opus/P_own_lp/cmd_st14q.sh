# st14q: stage 14 (R77 7-inflow, q7) on top of reduced 6-centred (apexcls), argsA50 (d43ba26a). Engine snapshot: snap/st14q (md5 in snap/st14q_md5.txt)
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P; M=$S/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
python3 pcheck.py solveR2 xon apexcls q7 dbg tag=st14q root=$M args=s17/argsA50.txt rpat=rpatD.txt consbasis=cons2basis_cls.json warm=$S/rows_s12r50_partial.txt,rows_s12r47.txt K=300 xcap=3 xpen=1e-3 threads=1 work=$S/wr25
python3 pcheck.py lowerR2 apexcls q7 xon cert=cert_st14q.json xcap=3 root=$M args=s17/argsA50.txt rpat=rpatD.txt work=$S/wr25
python3 pcheck.py upperR2 apexcls q7 xon nomax sol=sol_st14q.json root=$M args=s17/argsA50.txt rpat=rpatD.txt threads=2 work=$S/wr27
