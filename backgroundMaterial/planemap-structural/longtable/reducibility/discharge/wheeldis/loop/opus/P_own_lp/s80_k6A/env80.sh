# s80 Team E (copy of s77_k6patch/env77.sh): common environment (source me).  T = s80 tables: tab/kill = s80 kill6 build (patched-298 + B3 route A;
# the 2 route-A configs add 0 bits, so U7/U8/U9 are md5-identical to s77 patched-298); l3q, rules, exname = s77 copies (md5-identical).
# ENG = engine dir (default s80 eng = s77 eng + f2bx support; eng_orig = byte copy of s77_k6patch/eng).  ARGS default = route-F args (local copy).
# FAM: base | rrz | full (as env77).  F2BX (optional) = extra f2b rule file(s) for routes A'/L' (comma list) -> option f2bx=...
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W; S8=$SC/s80
N=$B/s80_k6A; ENG=${ENG:-$N/eng}; S=$B/s33z; H=$B/s39o; Q=$S/reg_A97; T=$N/tab; KT=${KT:-$T/kill/kill6}
RULES=$T/rules_studio_keep95p131f.json
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"; CB=consbasis=$B/s21/cf/cons2basis_cls.json
A="root=$M args=${ARGS:-$N/args/args_A97_F.txt} rpat=$B/rpatD.txt exname=$T/exname_keep95p131f.txt"
FCOM="xon apexcls filt16 hat5 consall l3q lqcap=3 l3qV=7,8"
FUP="$FCOM killtab=$KT l3qtab=$T/tab_1.json,$T/tab_-1.json l3qtab8=$T/tabV8_1.json,$T/tabV8_-1.json"
case ${FAM:-base} in
  base) F="$FUP f2b=$RULES";;
  rrz)  F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3";;
  full) F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3";;
esac
[ -n "$F2BX" ] && F="$F f2bx=$F2BX"
