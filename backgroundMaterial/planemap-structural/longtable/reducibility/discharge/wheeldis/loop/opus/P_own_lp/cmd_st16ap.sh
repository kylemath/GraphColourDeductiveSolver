# Stage 16 A′ (RELAY_SPEC 14′). Engine snap/st16ap (md5s in snap/st16ap_md5.txt). Forbidden set: 582 RSST + 1427 twoeng k3x at 09d8ac38.
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P; M=$S/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
X=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
F="filt16 killtab=s16ap/kill6"
# kill tables + check 4
#   for U in 7 8 9: python3 s16_filter.py $X/ex52 s19/k3x_D_09d8ac38.out s19/k3x_C_09d8ac38.cfast s16ap/kill6_U$U.json wj=6 U=$U ; python3 s16_killnpy.py s16ap
#   python3 s16_check4full.py $X/ex52 s19/k3x_D_09d8ac38.out s19/k3x_C_09d8ac38.cfast   -> 3072 ;  s16_check4.py (LP projection) -> 7500
# validation 1: filter off reproduces st15f (23/134)
python3 pcheck.py lowerR2 apexcls v6 xon cert=cert_st15f.json xcap=3 root=$M args=s17/argsA50.txt rpat=rpatD.txt work=$S/wr30 > val_off_lower.log 2>&1
python3 pcheck.py upperR2 apexcls v6 xon nomax sol=sol_st15f.json root=$M args=s17/argsA50.txt rpat=rpatD.txt threads=1 work=$S/wr42 > val_off_upper.log 2>&1
# structure summary (blind, for Studio)
python3 pcheck.py structR2 apexcls v6 xon $F structout=s17_struct.txt root=$M args=s19/argsA52.txt rpat=rpatD.txt work=$S/wr43 > s17_struct.log 2>&1
# solves on argsA52: filter on (st16ap) and the same engine with the filter off (st16b0, baseline)
W="warm=rows_st15f.txt,rows_st15_run2.txt,rows_st15_run1.txt,rows_s12r50.txt,rows_st14q.txt"
python3 pcheck.py solveR2 xon apexcls v6 $F dbg tag=st16ap root=$M args=s19/argsA52.txt rpat=rpatD.txt consbasis=cons2basis_v6.json $W K=300 xcap=3 xpen=1e-3 threads=2 work=$S/wr40 > st16ap.log 2>&1
python3 pcheck.py solveR2 xon apexcls v6 dbg tag=st16b0 root=$M args=s19/argsA52.txt rpat=rpatD.txt consbasis=cons2basis_v6.json $W K=300 xcap=3 xpen=1e-3 threads=1 work=$S/wr41 > st16b0.log 2>&1
python3 pcheck.py lowerR2 apexcls v6 xon $F cert=cert_st16ap.json xcap=3 root=$M args=s19/argsA52.txt rpat=rpatD.txt work=$S/wr40 > lower_st16ap.log 2>&1
python3 pcheck.py upperR2 apexcls v6 xon nomax $F sol=sol_st16ap.json root=$M args=s19/argsA52.txt rpat=rpatD.txt threads=2 work=$S/wr44 > upper_st16ap.log 2>&1
# baseline checks
python3 pcheck.py lowerR2 apexcls v6 xon cert=cert_st16b0.json xcap=3 root=$M args=s19/argsA52.txt rpat=rpatD.txt work=$S/wr41 > lower_st16b0.log 2>&1
python3 pcheck.py upperR2 apexcls v6 xon nomax sol=sol_st16b0.json root=$M args=s19/argsA52.txt rpat=rpatD.txt threads=1 work=$S/wr45 > upper_st16b0.log 2>&1
# run 1 (st16ap) did not settle after the x penalty was removed (t = 6/37 throughout; killed at iteration 36, rows kept in rows_st16ap_run1.txt).
# run 2: restart from all rows with keeppen (stop at the penalised fixed point, where no row is violated). Engine snap/st16ap2.
python3 pcheck.py solveR2 xon apexcls v6 filt16 killtab=s16ap/kill6 keeppen dbg tag=st16ap2 root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis args=s19/argsA52.txt rpat=rpatD.txt consbasis=cons2basis_v6.json warm=rows_st16ap_run1.txt,rows_st15f.txt,rows_st15_run2.txt,rows_st15_run1.txt,rows_s12r50.txt,rows_st14q.txt K=300 xcap=3 xpen=1e-3 threads=3 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr40 > st16ap2.log 2>&1
python3 pcheck.py lowerR2 apexcls v6 xon filt16 killtab=s16ap/kill6 cert=cert_st16ap2.json xcap=3 root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis args=s19/argsA52.txt rpat=rpatD.txt work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr40 > lower_st16ap2.log 2>&1
python3 pcheck.py upperR2 apexcls v6 xon nomax filt16 killtab=s16ap/kill6 sol=sol_st16ap2.json root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis args=s19/argsA52.txt rpat=rpatD.txt threads=2 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr44 > upper_st16ap2.log 2>&1
# run 2's cert is from the penalised LP and does not certify (LOWER INVALID, 72 negative reduced costs). Exact cert: the unpenalised LP over the same rows, no separation (nosep).
python3 pcheck.py solveR2 xon apexcls v6 filt16 killtab=s16ap/kill6 nosep tag=st16ap2L root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis args=s19/argsA52.txt rpat=rpatD.txt consbasis=cons2basis_v6.json warm=rows_st16ap2.txt,rows_st16ap_run1.txt,rows_st15f.txt,rows_st15_run2.txt,rows_st15_run1.txt,rows_s12r50.txt,rows_st14q.txt K=300 xcap=3 threads=1 work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr46 > st16ap2L.log 2>&1
python3 pcheck.py lowerR2 apexcls v6 xon filt16 killtab=s16ap/kill6 cert=cert_st16ap2L.json xcap=3 root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis args=s19/argsA52.txt rpat=rpatD.txt work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr46 > lower_st16ap2L.log 2>&1
