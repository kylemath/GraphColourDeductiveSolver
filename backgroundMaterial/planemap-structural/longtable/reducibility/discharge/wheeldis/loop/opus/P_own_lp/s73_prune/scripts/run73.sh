# usage: run73.sh TAG RULES.json set711|a97 [vK]   (threads=1, nice 15); outputs run/TAG.log, run/v_TAG.txt, run/c_TAG.txt
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s64_keep95p131f/env64.sh
S73=$B/s73_prune; K=/mnt/project-files/swarm/round6/W1-minimal-set/k95f_patterns; tag=$1; R=$2; s=$3; vk=${4:-20}
F="$FUP f2b=$R"; W=$S73/work/$tag; mkdir -p $W; rm -f $S73/run/v_$tag.txt $S73/run/c_$tag.txt
cd $S73/eng
VC="vK=$vk vfile=$S73/run/v_$tag.txt"
[ -n "$VCAND" ] && VC="$VC vcand=$S73/run/c_$tag.txt fullrules=$B/s72_weighted/rules_drop276.json"
if [ $s = a97 ]; then
  nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$N/val/sol_c_repaired_opusfmt.json $A $VC threads=1 work=$W > $S73/run/$tag.log 2>&1
else
  echo "pat=$K/$s/D_patterns.out cpat=$K/$s/C_patterns.cfast" | tr ' ' '\n' > $S73/run/args_$s.txt
  nice -n 15 python3 pcheck.py upperR2 $F rpatN=$K/$s/rpatN.txt nomax sol=$N/val/sol_c_repaired_opusfmt.json root=$M args=$S73/run/args_$s.txt rpat=$K/$s/rpat_raw.txt $VC threads=1 work=$W > $S73/run/$tag.log 2>&1
fi
date -u > $S73/run/$tag.done
