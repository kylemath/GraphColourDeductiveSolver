# s53c common settings (= s52c/env.sh for A97): the s53 stack (l3q lqcap 3 + l3qV=7,8 V8 tables + rpatN3, NO fb) with the 128 exname
# hold-outs on reg_A97 (main 8ec00aea), solution s53/run_A97/sol_q53A97.json (t = 0.098789365409); engine s53c/eng (= s51/eng + the s52c ckeep= hunks).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; Q=$S/reg_A97; H=$B/s39o; O=$B/s53c; E=$O/eng; RD=$B/s53/run_A97; V8=$B/s47/tabV8_A97
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
EXN=$B/s40f/exname_rm128.txt
A="root=$M args=$Q/args_A97.txt rpat=$B/rpatD.txt exname=$EXN"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 l3qV=7,8 l3qtab8=$V8/tabV8_1.json,$V8/tabV8_-1.json"   # = s53/u53.sh F
fq() { echo "xon apexcls filt16 killtab=$1/f/kill/kill6 hat5 consall l3q l3qtab=$1/tab_1.json,$1/tab_-1.json lqcap=3 l3qV=7,8 l3qtab8=$1/tabV8_1.json,$1/tabV8_-1.json"; }   # same flags, all tables from dir $1
SOL=$RD/sol_q53A97.json
