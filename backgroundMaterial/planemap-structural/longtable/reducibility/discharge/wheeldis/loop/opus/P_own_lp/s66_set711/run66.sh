# usage: bash run66.sh set711|set702   (threads=1, nice 15)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s64_keep95p131f/env64.sh
S66=$B/s66_set711; K=/mnt/project-files/swarm/round6/W1-minimal-set/k95f_patterns; s=$1
mkdir -p $S66/run $S66/work_$s; rm -f $S66/run/v_$s.txt
sed "s#^#pat=$K/$s/D_patterns.out #;q" /dev/null
echo "pat=$K/$s/D_patterns.out cpat=$K/$s/C_patterns.cfast" | tr ' ' '\n' > $S66/run/args_$s.txt
F="$FUP f2b=$RULES"; cd $S66/eng
nice -n 15 python3 pcheck.py upperR2 $F rpatN=$K/$s/rpatN.txt nomax sol=$N/val/sol_c_repaired_opusfmt.json root=$M args=$S66/run/args_$s.txt rpat=$K/$s/rpat_raw.txt vout=$S66/run/v_$s.txt threads=1 work=$S66/work_$s > $S66/run/upper_$s.log 2>&1
