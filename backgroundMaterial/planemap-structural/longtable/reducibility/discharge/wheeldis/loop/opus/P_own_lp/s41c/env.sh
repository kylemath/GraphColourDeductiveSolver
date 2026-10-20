# s41c common settings: A74 l3q + rpatN3 (= s39o run39.sh V=n3 REG=A74 upper stage), engine s39o/eng.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; Q=$S/reg_A74; H=$B/s39o; E=$H/eng; RD=$H/run_n3_A74; O=$B/s41c
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
A="root=$M args=$Q/args_A74.txt rpat=$B/rpatD.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
fq() { echo "xon apexcls filt16 killtab=$1/f/kill/kill6 hat5 consall l3q l3qtab=$1/tab_1.json,$1/tab_-1.json lqcap=3"; }   # same flags, tables from dir $1
SOL=$RD/sol_q39n3A74.json
