# s53c deliverable check (= s52c/check52.sh for A97): upper on sol_q53A97 keeping ONLY the cover's C entries (ckeep_A97.txt): cpat names +
# C wheels via the engine's ckeep= (with noC noCw; exname hold-outs still applied), kill6/l3q/V8 tables = D-only + the cover names' table kills.
# Negative control: the same with the first sole entry dropped (must be INFEASIBLE). Then the ckeep control (every name kept + full tables).
O=$(cd $(dirname $0) && pwd); SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; T=$SC/s53c_tab; mkdir -p $T
TN=$(grep -v '^#' $O/tabnames.txt | awk '{print $1}' | grep -xF -f $O/ckeep_A97.txt | paste -sd,)
echo "cover names with table kills: $TN" > $O/check53_tables.txt
python3 $O/tabname.py build $T/cover ${TN:-none}; md5sum $T/cover/f/kill/*.npy $T/cover/tab_*.json $T/cover/tabV8_*.json >> $O/check53_tables.txt
bash $O/run53u.sh check_cover $T/cover "noC noCw ckeep=$O/ckeep_A97.txt" $SC/s53c_v_check.txt &
D1=$(head -1 $O/ckeep_A97.txt); tail -n +2 $O/ckeep_A97.txt > $SC/s53c_ckeep_neg.txt
TN2=$(echo $TN | tr , '\n' | grep -vxF "$D1" | paste -sd,); python3 $O/tabname.py build $T/neg ${TN2:-none}
bash $O/run53u.sh check_neg_minus_$D1 $T/neg "noC noCw ckeep=$SC/s53c_ckeep_neg.txt"
wait; cp $SC/s53c_v_check.txt $O/check_cover_vrows.txt
if [ "$1" != noctl ]; then
  bash $O/run53u.sh ctl_ckeep_all $O/full "noC noCw ckeep=$O/ckeep_all.txt"
  cmp <(sed 's/([^)]*s)//' $O/upper_ctl_ckeep_all.log) <(sed 's/([^)]*s)//' $O/upper_base.log) > $O/ctl_ckeep_all_cmp.txt 2>&1 && echo "CONTROL ckeep_all: identical to upper_base.log (timings stripped)" > $O/ctl_ckeep_all_cmp.txt
fi
rm -rf $T/cover $T/neg; echo DONE > $O/check53.done
