# usage: run72.sh set711|a97  (threads=1, nice 15); rules = s72 rules_drop276.json
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s64_keep95p131f/env64.sh
S72=$B/s72_weighted; K=/mnt/project-files/swarm/round6/W1-minimal-set/k95f_patterns; s=$1
R72=$S72/rules_drop276.json; F="$FUP f2b=$R72"; mkdir -p $S72/work_$s; rm -f $S72/run/v_$s.txt
cd $S72/eng
if [ $s = a97 ]; then
  nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$N/val/sol_c_repaired_opusfmt.json $A vout=$S72/run/v_$s.txt threads=1 work=$S72/work_$s > $S72/run/upper_$s.log 2>&1
else
  echo "pat=$K/$s/D_patterns.out cpat=$K/$s/C_patterns.cfast" | tr ' ' '\n' > $S72/run/args_$s.txt
  nice -n 15 python3 pcheck.py upperR2 $F rpatN=$K/$s/rpatN.txt nomax sol=$N/val/sol_c_repaired_opusfmt.json root=$M args=$S72/run/args_$s.txt rpat=$K/$s/rpat_raw.txt vout=$S72/run/v_$s.txt threads=1 work=$S72/work_$s > $S72/run/upper_$s.log 2>&1
fi
date -u > $S72/run/$s.done
