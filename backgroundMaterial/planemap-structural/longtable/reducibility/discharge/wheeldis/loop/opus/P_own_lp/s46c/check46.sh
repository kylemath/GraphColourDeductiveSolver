# s46c deliverable check (= s41c/check41.sh for A78): upper on sol_q42aA78 keeping ONLY the cover's C entries (ckeep_A78.txt): cpat names +
# C wheels via the engine's ckeep= (with noC noCw; exname hold-outs still applied), kill6/l3q tables = D-only + the cover names' table kills.
# Negative control: the same with the first sole entry dropped (must be INFEASIBLE). Then the ckeep control (every name kept + full tables).
O=$(cd $(dirname $0) && pwd); SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; T=$SC/s46c_tab; mkdir -p $T
TN=$(grep -v '^#' $O/tabnames.txt | awk '{print $1}' | grep -xF -f $O/ckeep_A78.txt | paste -sd,)
echo "cover names with table kills: $TN" > $O/check46_tables.txt
python3 $O/tabname.py build $T/cover ${TN:-none}; md5sum $T/cover/f/kill/*.npy $T/cover/tab_*.json >> $O/check46_tables.txt
bash $O/run46u.sh check_cover $T/cover "noC noCw ckeep=$O/ckeep_A78.txt" $SC/s46c_v_check.txt
cp $SC/s46c_v_check.txt $O/check_cover_vrows.txt
tail -n +2 $O/ckeep_A78.txt > $SC/s46c_ckeep_neg.txt; D1=$(head -1 $O/ckeep_A78.txt)
TN2=$(echo $TN | tr , '\n' | grep -vxF "$D1" | paste -sd,); python3 $O/tabname.py build $T/neg ${TN2:-none}
bash $O/run46u.sh check_neg_minus_$D1 $T/neg "noC noCw ckeep=$SC/s46c_ckeep_neg.txt"
if [ "$1" != noctl ]; then
  bash $O/run46u.sh ctl_ckeep_all $O/../s33z/reg_A78 "noC noCw ckeep=$O/ckeep_all.txt"
  cmp <(sed 's/([^)]*s)//' $O/upper_ctl_ckeep_all.log) <(sed 's/([^)]*s)//' $O/upper_base.log) > $O/ctl_ckeep_all_cmp.txt 2>&1 && echo "CONTROL ckeep_all: identical to upper_base.log (timings stripped)" > $O/ctl_ckeep_all_cmp.txt
fi
rm -rf $T/cover $T/neg; echo DONE > $O/check46.done
