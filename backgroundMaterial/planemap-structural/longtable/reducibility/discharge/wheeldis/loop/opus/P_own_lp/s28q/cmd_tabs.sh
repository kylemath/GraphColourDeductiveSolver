# l3q mask tables for 7a3857a0 (ex60 + s30h/r7a k3x) then 3cfd7f18 (ex62 + s31 k3x); 2 processes at a time
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s28q
for sg in 1 -1; do nice -n 5 python3 l3qtab.py /tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex60 ../s30h/r7a/k3x_D_7a3857a0.out ../s30h/r7a/k3x_C_7a3857a0.cfast tab61_$sg.json $sg > tab61_$sg.log 2>&1 & done; wait
for sg in 1 -1; do nice -n 5 python3 l3qtab.py /tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex62 ../s31/k3x_D_3cfd7f18.out ../s31/k3x_C_3cfd7f18.cfast tab62_$sg.json $sg > tab62_$sg.log 2>&1 & done; wait
echo DONE > tabs_done.txt
