# s45: V = 8 masks for the cert's payee keys (exname held out) + V = 7 builder check on a 10-key sample of s33z/reg_A78/tab_1.json
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
D=$B/s45; Q=$B/s33z/reg_A78; EX=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex_A78
TD=$Q/k3x_D_A78.out; TC=$Q/k3x_C_A78.cfast; XN=exname=$B/s40f/exname_rm128.txt
export OMP_NUM_THREADS=1; cd $D/tabV
nice -n 10 python3 $D/l3qtabV.py $EX $TD $TC tab7_sample.json 1 7 keys=keys_V7sample.txt > tab7_sample.log 2>&1
for sg in 1 -1; do nice -n 10 python3 $D/l3qtabV.py $EX $TD $TC tabV8cert_$sg.json $sg 8 $XN keys=keys_cert_V8.txt > tabV8cert_$sg.log 2>&1; done
nice -n 10 python3 $D/l3qtabV.py $EX $TD $TC tabV8cert_noex_1.json 1 8 keys=keys_cert_V8.txt > tabV8cert_noex_1.log 2>&1
echo DONE > tabV_cert.done
