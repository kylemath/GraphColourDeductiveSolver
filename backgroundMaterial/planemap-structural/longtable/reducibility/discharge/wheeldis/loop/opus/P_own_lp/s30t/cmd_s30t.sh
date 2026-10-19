# s30t (T1): upper check of sol_st24b (2/13) with ALL C entries excluded (D only), registry 0125c46b. No re-solve.
# Engine = s24d copy with three opt-in flags (default behaviour unchanged): noC (drop every cpat= file and the
# def_*.cfast C 7-wheels from RBIG), noCw (also drop C wheel verdicts from R5/R6), vK (max violated rows listed, VROW lines).
# Kill tables: s16_filter donly=1 (RSST D2 verdicts only, 249 of 582) + k3x_D_0125c46b names, k3x_C empty.
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
T=$P/s30t
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
cd $T
TD=$P/s25/k3x_D_0125c46b.out; TC=$T/k3x_C_empty.cfast; EX=$S/ex59
date -u +%H:%M:%SZ > kill_start.txt
for U in 7 8 9; do echo "cd $T/f && python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U donly=1 > kill/kill6_U$U.log 2>&1"; done | xargs -P2 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
md5sum f/kill/*.npy $P/s25/f/kill/*.npy > kill_md5.txt
date -u +%H:%M:%SZ > kill_end.txt
F="xon apexcls filt16 hat5 consall nomax sol=$P/s24d/sol_st24b.json dcap=3 threads=2 vK=100000"
A="root=$M rpat=$P/rpatD.txt"
# regression: patched engine, full registry, s25 kill tables (must match s24d/upper_st24b.log)
grep -q UPPER-R2 upper_regress.log 2>/dev/null || python3 pcheck.py upperR2 $F killtab=$P/s25/f/kill/kill6 $A args=$P/s25/argsA59.txt work=$S/P/wr30t_reg > upper_regress.log 2>&1
# T1: D only (cpat files out, cfast 7-wheels out, kill tables D only)
python3 pcheck.py upperR2 $F noC killtab=$T/f/kill/kill6 $A args=$T/argsA59D.txt work=$S/P/wr30t_u > upper_st24b_Donly.log 2>&1
# T1': additionally C wheel verdicts out of R5/R6
python3 pcheck.py upperR2 $F noC noCw killtab=$T/f/kill/kill6 $A args=$T/argsA59D.txt work=$S/P/wr30t_uw > upper_st24b_Donly_noCw.log 2>&1
echo DONE > done.txt
