# s60: independent upperR2 of the outside team's GCOct26 solutions on OUR A83 registry and OUR kill/l3q tables
# (A83 = their "A100" base minus held128/full-k3x swaps; see args diff in REPORT). usage: u60.sh <solname> <tag>
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
W=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/$W
S=$B/s33z; Q=$S/reg_A83; D=$B/s60_ext; export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A83.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 l3qV=7,8 l3qtab8=$B/s47/tabV8_A83/tabV8_1.json,$B/s47/tabV8_A83/tabV8_-1.json"
X="rpatN=$B/s39o/rpatN3.txt"
cd $B/s51/eng
nice -n 10 python3 pcheck.py upperR2 $F $X nomax sol=/mnt/user-data/uploads/GCOct26/$1 $A threads=1 work=$SC/P/wr60_$2 > $D/upper_$2.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s60] $2: $(grep UPPER-R2 $D/upper_$2.log || echo 'no UPPER-R2 line')" >> $D/run.log
rm -rf $SC/P/wr60_$2
