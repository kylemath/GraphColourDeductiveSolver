# s47: full V = 8 l3q payee mask tables for reg_A92 (main e3d45d7d) with s45/l3qtabV.py (RELAY_SPEC_s45 45.3), both sides,
# 128 exname hold-outs (as s45/tabV_cert.sh did for the A78 cert keys); nice 10, one thread per side.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Q=$B/s33z/reg_A92; EX=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex_A92
TD=$Q/k3x_D_A92.out; TC=$Q/k3x_C_A92.cfast; XN=exname=$B/s40f/exname_rm128.txt
export OMP_NUM_THREADS=1; cd $B/s47/tabV8_A92
for sg in 1 -1; do nice -n 10 python3 $B/s45/l3qtabV.py $EX $TD $TC tabV8_$sg.json $sg 8 $XN > tabV8_$sg.log 2>&1 & done; wait
md5sum tabV8_*.json > md5.txt; echo DONE > tabV8.done
