# s60_f2b common environment (source me).  BASE=baseline A97 tables, UP=outside-team upgraded tables.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
N=$B/s64_keep95p131f; S=$B/s33z; H=$B/s39o; E=$B/s60_f2b/eng; Z=$B/s60_f2b; Q=$S/reg_A97; T=$N/tab
RULES=$N/tab/rules_studio_keep95p131f.json
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"; CB=consbasis=$B/s21/cf/cons2basis_cls.json
A="root=$M args=$Q/args_A97.txt rpat=$B/rpatD.txt exname=$N/tab/exname_keep95p131f.txt"
FCOM="xon apexcls filt16 hat5 consall l3q lqcap=3 l3qV=7,8"
FBASE="$FCOM killtab=$Q/f/kill/kill6 l3qtab=$Q/tab_1.json,$Q/tab_-1.json l3qtab8=$B/s47/tabV8_A97/tabV8_1.json,$B/s47/tabV8_A97/tabV8_-1.json"
FUP="$FCOM killtab=$T/kill/kill6 l3qtab=$T/tab_1.json,$T/tab_-1.json l3qtab8=$T/tabV8_1.json,$T/tabV8_-1.json"
