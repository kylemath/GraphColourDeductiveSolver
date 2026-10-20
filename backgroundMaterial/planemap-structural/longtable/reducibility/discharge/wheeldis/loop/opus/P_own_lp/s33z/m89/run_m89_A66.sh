# m89 step 1 on A66 (registry solved on): upperR2 of sol_s33.json on A66 minus the 89 XRing C entries, then lowerR2 (ucap=100) of cert_s33L.  [main stack includes k3p #1 [E2 guard]: pcell=k3p.txt]
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; cd $S/eng; Q=$S/m89/A66
until [ -e $S/done_s33.txt ] && [ -e $S/done_up_newest.txt ] && [ -e $Q/prep_done.txt ]; do sleep 60; done
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33m; export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A66m89.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 pcell=$S/pcell/k3p.txt"
echo "$(date -u +%H:%M:%SZ) m89 (A66) upper start" >> $S/wait.log
timeout 10800 nice -n 5 python3 pcheck.py upperR2 $F nomax sol=sol_s33.json $A threads=2 work=${WK}u > $Q/upper_s33_m89.log 2>&1 || echo "upper exit $?" >> $Q/upper_s33_m89.log
nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_s33L.json xcap=3 ucap=100 $A work=${WK}L > $Q/lower_s33L_m89.log 2>&1
echo DONE > $Q/done_m89_1.txt
