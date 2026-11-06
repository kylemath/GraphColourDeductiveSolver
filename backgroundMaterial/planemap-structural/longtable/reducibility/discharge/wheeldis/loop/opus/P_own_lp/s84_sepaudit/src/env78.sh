# s78_kstar (Team D) common environment (source me).  Engine = $N/eng (copy of s75_teamA/eng + the K* family: kstar.py, jsepf argv[13]).
# STACK selects the tables: s75 (unpatched, = s75_teamA/tab, kill6 U7 md5 c0527d29) or s77 (B1-patched, = s77_k6patch/tab, kill6 U7 md5 b493a0ce);
#   every other table file (l3q V=7/8 masks, f2b rules, exname) is byte-identical in the two stacks.
# FAM selects the families (as env77): base (= $FUP f2b=$RULES), rrz (+ hatrr zh zr zcap=3), full (+ q7 q7m q7rc q7cap=3; = s75 upper75/runK75 set).
# EGK=<keys file> adds the generic EDGE keys (eng/edgefam.py, jsepf argv[14]).
# KS=1 adds the K* family: "kstar kscap=3" (amount column ks[K1] in [0, 3]; under keeppen it carries xpen like lq).
# RSST 2.126 / 8406.123 and the held-out names stay out through exname= (same file as s75/s77) and the A97 args.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W; SD=$SC/sD
N=$B/s78_kstar; S=$B/s33z; H=$B/s39o; Q=$S/reg_A97; N75=$B/s75_teamA; N77=$B/s77_k6patch; O=$B/s70_inout
case ${STACK:-s75} in
  s75) T=$N75/tab;;
  s77) T=$N77/tab;;
  *) echo "env78: STACK must be s75 or s77" >&2; return 1;;
esac
KT=${KT:-$T/kill/kill6}; RULES=$T/rules_studio_keep95p131f.json
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"; CB=consbasis=$B/s21/cf/cons2basis_cls.json
A="root=$M args=${ARGS:-$Q/args_A97.txt} rpat=$B/rpatD.txt exname=$T/exname_keep95p131f.txt"
FCOM="xon apexcls filt16 hat5 consall l3q lqcap=3 l3qV=7,8"
FUP="$FCOM killtab=$KT l3qtab=$T/tab_1.json,$T/tab_-1.json l3qtab8=$T/tabV8_1.json,$T/tabV8_-1.json"
case ${FAM:-full} in
  base) F="$FUP f2b=$RULES";;
  rrz)  F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3";;
  full) F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3";;
esac
[ "${KS:-0}" = 1 ] && F="$F kstar kscap=${KSCAP:-3}"
[ -n "$EGK" ] && F="$F edgekeys=$EGK kscap=${KSCAP:-3}"   # generic EDGE keys file (eng/edgekeys_r4.txt = A1 C1 E1); amounts share the ks column namespace / cap
# warm row lists (as runK75.sh / env77.sh)
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
W53=$B/s53/run_A97/rows_q53A97.txt
WK75=$O/warm/rows_q69rrz_snap2.txt,$O/warm/rows_q70t.txt,$O/warm/rows_q70inoutB.txt,$O/warm0_rows.txt,$B/s60_f2b/eng/rows_q60K95.txt,$B/s60_f2b/eng/rows_q60A97.txt,/mnt/project-files/swarm/teamA/R4-A1-motifs/cutP1_d7.txt,$W53,$WA83,$W47,$W51
WX75=$N75/warm/rows_tight3_feas.txt,$N75/warm/rows_q75B_snap2.txt,$N75/warm/rows_q70inoutC_final.txt
W7POOL=$N77/warm/pool_all_W7rows.txt
