# s50 common settings (sourced): engine s50/eng = copy of s44/eng (incl. port_repair), fb OFF, s42a family flags
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
D=$B/s50; E=$D/eng; S=$B/s33z; H=$B/s39o
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
reg() { Q=$S/reg_$1; A="root=$M args=$Q/args_$1.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
  FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"; }
