# s44 (cont.): rerun lowerR2 (with the exact repair of port_repair.py) on a run's nosep cert.  bash low44.sh TAGREG CERT OUT [extra]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s44/env.sh
R=$1; CERT=$2; OUT=$3; shift 3
Q=$S/reg_$R; A="root=$M args=$Q/args_$R.txt rpat=$B/rpatD.txt exname=$B/s40f/exname_rm128.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
F="$FQ fb fbdir=6 fbcap=3"; cd $E
nice -n 10 python3 pcheck.py lowerR2 $F $X cert=$CERT xcap=3 $A "$@" work=$SC/P/wr44_low_$R > $OUT 2>&1
