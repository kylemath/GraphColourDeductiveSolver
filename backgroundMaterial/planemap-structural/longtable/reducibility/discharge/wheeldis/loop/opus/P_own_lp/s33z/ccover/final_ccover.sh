# After the A66 stacked solve, the newest-head upper and the m89 checks: (1) upperR2 of sol_s33.json with ALL C out (noC noCw, D-only  [main stack includes k3p #1 [E2 guard]: pcell=k3p.txt]
# kill6/l3q tables of prep_noC_A66.sh), every violated receiver row listed (vK=1e12 -> vfile in the scratchpad); (2) ccover.py: sole-cover
# set, greedy cover, overlap with the 89 XRing entries; (3) binderR2: d7 8666655/5677657 dual + family split, top 15 receiver binders.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; Q=$S/ccover; A6=$S/reg_A66; cd $S/eng
until [ -e $S/done_s33.txt ] && [ -e $S/m89/A66/done_m89_1.txt ] && [ -e $Q/prep_done.txt ]; do sleep 60; done
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
export OMP_NUM_THREADS=1; VF=$SC/ccover_A66_vrows.txt; : > $VF
A="root=$M args=$A6/args_A66.txt rpat=$B/rpatD.txt"
FN="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 pcell=$S/pcell/k3p.txt"
F="xon apexcls filt16 killtab=$A6/f/kill/kill6 hat5 consall l3q l3qtab=$A6/tab_1.json,$A6/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 pcell=$S/pcell/k3p.txt"
echo "$(date -u +%H:%M:%SZ) ccover: noC upper start" >> $S/wait.log
timeout 14400 nice -n 5 python3 pcheck.py upperR2 $FN noC noCw nomax vK=1e12 vfile=$VF sol=sol_s33.json $A threads=2 work=$SC/P/wr33nc > $Q/upper_s33_noC.log 2>&1 || echo "upper exit $?" >> $Q/upper_s33_noC.log
wc -l $VF > $Q/vrows_count.txt; md5sum $VF >> $Q/vrows_count.txt
nice -n 5 python3 -I $Q/ccover.py $VF $A6/args_A66.txt $M $S/m89/CGLUE-XRING-ENTRIES_27964810.txt $Q > $Q/ccover.log 2>&1
nice -n 5 python3 pcheck.py binderR2 $F $A sol=sol_s33L.json cert=cert_s33L.json row=7:8666655:5677657 top=15 work=$SC/P/wr33bd > $S/binders_s33L.log 2>&1
nice -n 5 python3 pcheck.py binderR2 $F $A sol=sol_s33.json cert=cert_s33L.json row=7:8666655:5677657 work=$SC/P/wr33bd > $S/binder_s33_upper.log 2>&1
echo "$(date -u +%H:%M:%SZ) ccover + binders done" >> $S/wait.log
echo DONE > $Q/done_ccover.txt
