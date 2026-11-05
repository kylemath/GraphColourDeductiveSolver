# s77 Team B2 (copy of s75_teamA/env75.sh) common environment (source me).  T = s77 patched tables (kill6_U7 = keep95p131f U7 + the 7 B1 configs
# through our spec derivation, 298 new bits, md5 b493a0ce...; U8/U9, l3q, rules, exname = keep95p131f unchanged).  TB1 = B1's own 222-bit U7 (tab_b1/kill).
# FAM selects the families: base (default; = s64 run64.sh: $FUP f2b=$RULES), rrz (+ hatrr zh zr zcap=3), full (+ q7 q7m q7rc q7cap=3).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W; S7=$SC/s77
N=$B/s77_k6patch; S=$B/s33z; H=$B/s39o; Q=$S/reg_A97; T=$N/tab; KT=${KT:-$T/kill/kill6}
RULES=$T/rules_studio_keep95p131f.json
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"; CB=consbasis=$B/s21/cf/cons2basis_cls.json
A="root=$M args=${ARGS:-$Q/args_A97.txt} rpat=$B/rpatD.txt exname=$T/exname_keep95p131f.txt"
FCOM="xon apexcls filt16 hat5 consall l3q lqcap=3 l3qV=7,8"
FUP="$FCOM killtab=$KT l3qtab=$T/tab_1.json,$T/tab_-1.json l3qtab8=$T/tabV8_1.json,$T/tabV8_-1.json"
case ${FAM:-base} in
  base) F="$FUP f2b=$RULES";;
  rrz)  F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3";;
  full) F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3";;
esac
O=$B/s70_inout; N75=$B/s75_teamA
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
W53=$B/s53/run_A97/rows_q53A97.txt
# warm list of s75 runK75.sh (default WARM0 + fixed list) + the s75 q75D extras (tight3, q75B snap2, q70inoutC final); W7POOL = B1's W7 pool (uncompressed copy in warm/)
WK75=$O/warm/rows_q69rrz_snap2.txt,$O/warm/rows_q70t.txt,$O/warm/rows_q70inoutB.txt,$O/warm0_rows.txt,$B/s60_f2b/eng/rows_q60K95.txt,$B/s60_f2b/eng/rows_q60A97.txt,/mnt/project-files/swarm/teamA/R4-A1-motifs/cutP1_d7.txt,$W53,$WA83,$W47,$W51
WX75=$N75/warm/rows_tight3_feas.txt,$N75/warm/rows_q75B_snap2.txt,$N75/warm/rows_q70inoutC_final.txt
W7POOL=$N/warm/pool_all_W7rows.txt
