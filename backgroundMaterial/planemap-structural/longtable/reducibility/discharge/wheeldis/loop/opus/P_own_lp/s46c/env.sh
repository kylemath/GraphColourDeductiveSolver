# s46c common settings: A78 l3q + rpatN3 with the 128 exname hold-outs (= s42a/run42.sh upper stage, sol_q42aA78), engine s46c/eng
# (= s39o/eng incl. exname port + s41c ckeep= patch).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; Q=$S/reg_A78; H=$B/s39o; O=$B/s46c; E=$O/eng; RD=$B/s42a/run_A78
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
EXN=$B/s42a/exname_A78.txt   # s42a's exact argument; same 128-name set as s40f/exname_rm128.txt
A="root=$M args=$Q/args_A78.txt rpat=$B/rpatD.txt exname=$EXN"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
fq() { echo "xon apexcls filt16 killtab=$1/f/kill/kill6 hat5 consall l3q l3qtab=$1/tab_1.json,$1/tab_-1.json lqcap=3"; }   # same flags, tables from dir $1
SOL=$RD/sol_q42aA78.json
