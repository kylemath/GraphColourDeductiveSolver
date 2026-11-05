# usage: serve73.sh NAME set711|a97  -> persistent server, dir srv/NAME (req_*.json -> res_*.txt)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s64_keep95p131f/env64.sh
S73=$B/s73_prune; K=/mnt/project-files/swarm/round6/W1-minimal-set/k95f_patterns; n=$1; s=$2
D=$S73/srv/$n; rm -rf $D; mkdir -p $D $S73/work/srv_$n
R=$S73/sets/feas961.rules.json
F="$FUP f2b=$R"; W=$S73/work/srv_$n; cd $S73/eng
echo "pat=$K/$s/D_patterns.out cpat=$K/$s/C_patterns.cfast" | tr ' ' '\n' > $S73/run/args_$s.txt
if [ $s = a97 ]; then
  nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$N/val/sol_c_repaired_opusfmt.json $A serve=$D threads=1 work=$W > $S73/run/srv_$n.log 2>&1
else
  nice -n 15 python3 pcheck.py upperR2 $F rpatN=$K/$s/rpatN.txt nomax sol=$N/val/sol_c_repaired_opusfmt.json root=$M args=$S73/run/args_$s.txt rpat=$K/$s/rpat_raw.txt serve=$D threads=1 work=$W > $S73/run/srv_$n.log 2>&1
fi
