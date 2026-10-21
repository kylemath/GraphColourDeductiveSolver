# s47 common settings (sourced): engine s47/eng = s44/eng (with 44.8 repair) + s45/port_l3qV.py + s47/port_s47.py
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; H=$B/s39o; D=$B/s47; E=$D/eng
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
Q=$S/reg_A78; A="root=$M args=$Q/args_A78.txt rpat=$B/rpatD.txt exname=$B/s42a/exname_A78.txt"   # s42a arguments
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
V8A78="l3qV=7,8 l3qtab8=$B/s45/tabV/tabV8cert_1.json,$B/s45/tabV/tabV8cert_-1.json l3qpartial"   # s45 cert-key V = 8 tables (A78)
SOL=$B/s42a/run_A78/sol_q42aA78.json; CERT=$B/s42a/run_A78/cert_q42aA78L.json
note() { echo "$(date -u +%H:%M:%SZ) [s47] $*" >> $D/run.log; }
strip() { sed -E 's/, [0-9.]+s\)/)/; s/ [0-9.]+s$//'; }
