# s53c batch 2 (= s52c/batch2.sh): per-name table attribution. For each C name behind a table kill (tabnames.txt: kill6, l3q, V8): tables = D-only + that
# name's kills, upper noC noCw with every violated row listed; covered_by(name) = V(noC) minus V(name). Two names at a time (nice 10).
O=$(cd $(dirname $0) && pwd); SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; T=$SC/s53c_tab; mkdir -p $T
one() { n=$1; [ -s $T/v_$n.txt ] && [ -e $T/v_$n.done ] && return
  python3 $O/tabname.py build $T/$n $n
  bash $O/run53u.sh "t_$n" $T/$n "noC noCw" $T/v_$n.txt && touch $T/v_$n.done
  rm -rf $T/$n; }
export -f one; export O T
grep -v '^#' $O/tabnames.txt | awk '{print $1}' | xargs -P2 -I{} bash -c 'one {}'
echo DONE > $O/batch2.done
