# s42a common settings (sourced): warm l3q + rpatN3 on A78 (b6dc7610) with exname hold-outs; engine s39o/eng (+ exname port)
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
S=$B/s33z; SE=$S/eng; H=$B/s39o; E=$H/eng; D=$B/s42a; RD=$D/run_A78; mkdir -p $RD
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W; WK=$SC/P/wr42a
export OMP_NUM_THREADS=1
X="rpatN=$H/rpatN3.txt"
Q=$S/reg_A78; A="root=$M args=$Q/args_A78.txt rpat=$B/rpatD.txt exname=$D/exname_A78.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
WQ=$SE/rows_q66.txt,$SE/rows_s33A66a.txt,$SE/rows_s33A64.txt,$SE/rows_q64A64.txt,$SE/rows_q66A66a.txt,$B/s28q/eng/rows_s28A62.txt,$B/s28q/eng/rows_s28A60.txt,$B/s24d/rows_st24b_final.txt
XW=$H/run_n3_A74/rows_q39n3A74.txt,$H/run_n/rows_q39n.txt
T=q42aA78
note() { echo "$(date -u +%H:%M:%SZ) [s42a] $*" >> $D/run.log; }
dfok() { a=$(df -BG --output=avail $SC | tail -1 | tr -dc 0-9); [ "$a" -gt 10 ] || { note "df: only ${a}G free, stopping"; exit 5; }; }
