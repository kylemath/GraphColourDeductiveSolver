# s52c common settings: A83 l3q + rpatN3 + fb6 (fbdir=6 fbcap=3) with the 128 exname hold-outs (= s44/run44c.sh upper stage, sol_q44fbA83),
# engine s52c/eng (= s44/eng + the s41c/s46c ckeep= patch, same hunks).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; Q=$S/reg_A83; H=$B/s39o; O=$B/s52c; E=$O/eng; RD=$B/s44/run_A83
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
EXN=$B/s40f/exname_rm128.txt   # s44/run44c.sh's exact argument (128 names)
A="root=$M args=$Q/args_A83.txt rpat=$B/rpatD.txt exname=$EXN"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 fb fbdir=6 fbcap=3"
fq() { echo "xon apexcls filt16 killtab=$1/f/kill/kill6 hat5 consall l3q l3qtab=$1/tab_1.json,$1/tab_-1.json lqcap=3 fb fbdir=6 fbcap=3"; }   # same flags, tables from dir $1
SOL=$RD/sol_q44fbA83.json
