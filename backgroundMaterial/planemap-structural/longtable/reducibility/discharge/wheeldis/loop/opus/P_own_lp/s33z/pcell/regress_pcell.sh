# s33z pcell port regression (s36g privcell.py + pcell=FILE, a9da7812): cert_s28A60L (l3q, 7360eb92) and cert_st24bL (s25 A59), off / empty / k3p name.
# Separate work dir (the class-table cache in WORK does not key on pcell).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Z=$B/s33z; cd $Z/eng; export OMP_NUM_THREADS=1
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SW=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33pc
A6="root=$M args=$B/s29/argsA60.txt rpat=$B/rpatD.txt threads=1"; F="xon apexcls filt16 killtab=$B/s29/f/kill/kill6 hat5 consall l3q l3qtab=$B/s28q/tab60_1.json,$B/s28q/tab60_-1.json lqcap=3"
nice -n 5 python3 pcheck.py lowerR2 $F pcell=$Z/pcell/empty.txt cert=$B/s28q/eng/cert_s28A60L.json xcap=3 $A6 work=${SW}e > $Z/pcell/reg_s28A60L_empty.log 2>&1
nice -n 5 python3 pcheck.py lowerR2 $F pcell=$Z/pcell/k3p.txt cert=$B/s28q/eng/cert_s28A60L.json xcap=3 $A6 work=${SW}k > $Z/pcell/reg_s28A60L_k3p.log 2>&1
A="root=$M args=$B/s25/argsA59.txt rpat=$B/rpatD.txt threads=1"; F0="xon apexcls filt16 killtab=$B/s25/f/kill/kill6 hat5 consall"
nice -n 5 python3 pcheck.py lowerR2 $F0 pcell=$Z/pcell/empty.txt cert=$B/s24d/cert_st24bL.json xcap=3 $A work=${SW}e2 > $Z/pcell/reg_st24bL_empty.log 2>&1
nice -n 5 python3 pcheck.py lowerR2 $F0 pcell=$B/s36g/g7_q.txt cert=$B/s24d/cert_st24bL.json xcap=3 $A work=${SW}g > $Z/pcell/reg_st24bL_g7.log 2>&1
echo DONE > $Z/pcell/regress_done.txt
