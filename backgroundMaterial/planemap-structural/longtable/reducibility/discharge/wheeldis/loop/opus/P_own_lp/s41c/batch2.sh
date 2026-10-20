# s41c batch 2: per-name table attribution. For each C name behind a table kill (tabnames.txt): tables = D-only + that name's kills,
# upper noC noCw with every violated row listed; covered_by(name) = V(noC) minus V(name).
O=$(cd $(dirname $0) && pwd); SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; T=$SC/s41c_tab; mkdir -p $T
for n in $(grep -v '^#' $O/tabnames.txt | awk '{print $1}'); do
  [ -s $T/v_$n.txt ] && [ -e $T/v_$n.done ] && continue
  python3 $O/tabname.py build $T/$n $n
  bash $O/run41u.sh "t_$n" $T/$n "noC noCw" $T/v_$n.txt && touch $T/v_$n.done
  rm -rf $T/$n
done
echo DONE > $O/batch2.done
