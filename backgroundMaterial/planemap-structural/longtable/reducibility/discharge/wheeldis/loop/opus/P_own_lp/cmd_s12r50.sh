# s12r50: reduced 6-centred relay (apexcls) on argsA50 (d43ba26a). Engines snapshotted in snap/s12r50_solve (solve; reconstructed:
# prelay2 = prelay2_s13_backup.py, the file as it was at launch; pcheck = current minus the later jsep4 hook) and snap/s12r50_check (checks).
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P; M=$S/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
python3 pcheck.py solveR2 xon apexcls tag=s12r50 root=$M args=s17/argsA50.txt rpat=rpatD.txt consbasis=cons2basis_cls.json warm=rows_s12r47.txt,rows_s15c.txt,s14/rows_s14r.txt K=300 xcap=3 xpen=1e-3 threads=3 work=$S/wr24
python3 pcheck.py lowerR2 apexcls xon cert=cert_s12r50.json xcap=3 root=$M args=s17/argsA50.txt rpat=rpatD.txt work=$S/wr24
python3 pcheck.py upperR2 apexcls xon nomax consbasis=cons2basis_cls.json sol=sol_s12r50.json root=$M args=s17/argsA50.txt rpat=rpatD.txt threads=2 work=$S/wr26
# consbasis file: python3 pcheck.py consbasisR2 apexcls out=cons2basis_cls.json root=$M args=s9/argsA44.txt
