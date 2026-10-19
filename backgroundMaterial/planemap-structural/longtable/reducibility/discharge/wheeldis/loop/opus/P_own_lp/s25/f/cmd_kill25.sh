# s25 strict kill tables + check 4 on 0125c46b (ex59 = ex58 [ex57 + 03c34729 W/loop] + git archive 0125c46b W/loop)
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s25/f
EX=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex59
for U in 7 8 9; do python3 s16_filter.py $EX ../k3x_D_0125c46b.out ../k3x_C_0125c46b.cfast kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1 & done; wait
python3 s16_killnpy.py kill > kill/killnpy.log 2>&1
for K in 99 5 7; do python3 s16_check4.py $EX ../k3x_D_0125c46b.out ../k3x_C_0125c46b.cfast unk=$K > check4_unk$K.log 2>&1 & done; wait
echo DONE
