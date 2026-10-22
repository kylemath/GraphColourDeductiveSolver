# s54 ucheck.sh SOL LOG: upperR2 (s53 flags, A97, exname_rm128) on SOL, vfile LOG.viol
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
S=$B/s33z; Q=$S/reg_A97; E=$B/s54/eng; export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A97.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 l3qV=7,8 l3qtab8=$B/s47/tabV8_A97/tabV8_1.json,$B/s47/tabV8_A97/tabV8_-1.json"
X="rpatN=$B/s39o/rpatN3.txt"; WK=$SC/s54w/u_$(basename $2)
cd $E; rm -f $2.viol
nice -n 10 python3 pcheck.py upperR2 $F $X nomax sol=$1 $A threads=1 work=$WK vK=${VK:-20} vfile=$2.viol > $2 2>&1
rm -rf $WK; grep UPPER-R2 $2
