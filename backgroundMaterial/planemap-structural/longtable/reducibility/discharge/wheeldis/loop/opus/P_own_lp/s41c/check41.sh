# s41c deliverable 4: upper on sol_q39n3A74 keeping ONLY the cover's C entries (ckeep_A74.txt): cpat names + C wheels via the
# engine's ckeep= (with noC noCw), and kill6/l3q tables = D-only + the cover names' table kills (tabname.py).
# Negative control: the same with the first sole entry dropped (must be INFEASIBLE).
O=$(cd $(dirname $0) && pwd); SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; T=$SC/s41c_tab
TN=$(grep -v '^#' $O/tabnames.txt | awk '{print $1}' | grep -xF -f $O/ckeep_A74.txt | paste -sd,)
echo "cover names with table kills: $TN" > $O/check41_tables.txt
python3 $O/tabname.py build $T/cover ${TN:-none}; md5sum $T/cover/f/kill/*.npy $T/cover/tab_*.json >> $O/check41_tables.txt
bash $O/run41u.sh check_cover $T/cover "noC noCw ckeep=$O/ckeep_A74.txt" $SC/s41c_v_check.txt
tail -n +2 $O/ckeep_A74.txt > $SC/ckeep_neg.txt; D1=$(head -1 $O/ckeep_A74.txt)
TN2=$(echo $TN | tr , '\n' | grep -vxF "$D1" | paste -sd,); python3 $O/tabname.py build $T/neg ${TN2:-none}
bash $O/run41u.sh check_neg_minus_$D1 $T/neg "noC noCw ckeep=$SC/ckeep_neg.txt"
# ckeep control: every C name kept + full reg_A74 tables must reproduce the base upper (timings stripped)
bash $O/run41u.sh ctl_ckeep_all $O/../s33z/reg_A74 "noC noCw ckeep=$O/ckeep_all.txt"
cmp <(sed 's/([^)]*s)//' $O/upper_ctl_ckeep_all.log) <(sed 's/([^)]*s)//' $O/upper_base.log) > $O/ctl_ckeep_all_cmp.txt 2>&1 && echo "CONTROL ckeep_all: identical to upper_base.log (timings stripped)" > $O/ctl_ckeep_all_cmp.txt
rm -rf $T/cover $T/neg; echo DONE > $O/check41.done
