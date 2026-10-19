# s30h: upper check of sol_st24b (2/13, s24d run1) on (a) 0125c46b minus the 3 ring-merge C entries and (b) Studio head 7a3857a0.
# Engine = s24d copy (pcheck cf4eb14c). Kill tables rebuilt (s16_filter strict, wj=6) on each variant. Max 2 processes / 2 threads.
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
H=$P/s30h
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd $H
TDa=$P/s25/k3x_D_0125c46b.out; TCa=$H/k3x_C_0125c46b_m3.cfast; EXa=$S/ex59
TDb=$H/r7a/k3x_D_7a3857a0.out; TCb=$H/r7a/k3x_C_7a3857a0.cfast; EXb=$S/ex60
date -u +%H:%M:%SZ > kill_start.txt
{ for U in 7 8 9; do echo "cd $H/f && python3 s16_filter.py $EXa $TDa $TCa kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1"; done
  for U in 7 8 9; do echo "cd $H/r7a/f && python3 s16_filter.py $EXb $TDb $TCb kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1"; done
  echo "cd $H && python3 dcount.py argsA59m3.txt $M > dcount.txt 2>&1"; } | xargs -P2 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1); (cd r7a/f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy r7a/f/kill/*.npy $P/s25/f/kill/*.npy $P/s29/f/kill/*.npy > kill_md5.txt
date -u +%H:%M:%SZ > kill_end.txt
CB=consbasis=$P/s21/cf/cons2basis_cls.json
Aa="root=$M args=$H/argsA59m3.txt rpat=$P/rpatD.txt"
Ab="root=$M args=$H/r7a/argsA61.txt rpat=$P/rpatD.txt"
python3 pcheck.py upperR2 xon apexcls filt16 killtab=$H/f/kill/kill6 hat5 consall nomax sol=$P/s24d/sol_st24b.json dcap=3 $Aa threads=2 work=$S/P/wr30h_u > upper_st24b_m3.log 2>&1
date -u +%H:%M:%SZ > upperA_end.txt
python3 pcheck.py upperR2 xon apexcls filt16 killtab=$H/r7a/f/kill/kill6 hat5 consall nomax sol=$P/s24d/sol_st24b.json dcap=3 $Ab threads=2 work=$S/P/wr30h_u7a > r7a/upper_st24b_7a3857a0.log 2>&1
date -u +%H:%M:%SZ > upperB_end.txt
echo DONE > done_upper.txt
# extra (after B): lower check of the published cert_st24bL against 7a3857a0 (more D than 0125c46b, so rows could die)
python3 pcheck.py lowerR2 xon apexcls filt16 killtab=$H/r7a/f/kill/kill6 hat5 consall cert=$P/s24d/cert_st24bL.json xcap=3 dcap=3 root=$M args=$H/r7a/argsA61.txt rpat=$P/rpatD.txt work=$S/P/wr30h_L7a > r7a/lower_st24bL_7a3857a0.log 2>&1
python3 pcheck.py lowerR2 xon apexcls filt16 killtab=$H/f/kill/kill6 hat5 consall cert=$P/s24d/cert_st24bL.json xcap=3 dcap=3 root=$M args=$H/argsA59m3.txt rpat=$P/rpatD.txt work=$S/P/wr30h_Lm3 > lower_st24bL_m3.log 2>&1
# extra: upper of s29's solution (7360eb92) on 7a3857a0 (s29 upper flags)
python3 pcheck.py upperR2 xon apexcls filt16 killtab=$H/r7a/f/kill/kill6 hat5 consall nomax sol=$P/s29/sol_s29.json root=$M args=$H/r7a/argsA61.txt rpat=$P/rpatD.txt threads=2 work=$S/P/wr30h_u29 > r7a/upper_s29_7a3857a0.log 2>&1
# extra: lower of s29's cert on 7a3857a0 (s29 lower flags)
python3 pcheck.py lowerR2 xon apexcls filt16 killtab=$H/r7a/f/kill/kill6 hat5 consall cert=$P/s29/cert_s29L.json xcap=3 root=$M args=$H/r7a/argsA61.txt rpat=$P/rpatD.txt work=$S/P/wr30h_L29 > r7a/lower_s29L_7a3857a0.log 2>&1
