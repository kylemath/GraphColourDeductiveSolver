# s43 common settings (sourced): engine s44/eng = s43/eng + port_fb.py (fb)
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; SE=$S/eng; Q=$S/reg_A74; H=$B/s39o; D=$B/s44; E=$D/eng
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
A="root=$M args=$Q/args_A74.txt rpat=$B/rpatD.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
N3=$H/run_n3_A74
note() { echo "$(date -u +%H:%M:%SZ) [s44] $*" >> $D/run.log; }
dfok() { a=$(df -BG --output=avail $SC | tail -1 | tr -dc 0-9); [ "$a" -gt 10 ] || { note "df: only ${a}G free, stopping"; exit 5; }; }
