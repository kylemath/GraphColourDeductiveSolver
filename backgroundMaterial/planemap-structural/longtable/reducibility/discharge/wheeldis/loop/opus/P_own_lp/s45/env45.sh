# s45 common settings (sourced): engine s45/eng = s44/eng + port_l3qV.py (l3qV); A78 tables, exname_rm128 (as s42a / s44 run44)
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; H=$B/s39o; D=$B/s45; E=$D/eng
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
Q=$S/reg_A78; A="root=$M args=$Q/args_A78.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
CERT=$B/s42a/run_A78/cert_q42aA78L.json
note() { echo "$(date -u +%H:%M:%SZ) [s45] $*" >> $D/run.log; }
