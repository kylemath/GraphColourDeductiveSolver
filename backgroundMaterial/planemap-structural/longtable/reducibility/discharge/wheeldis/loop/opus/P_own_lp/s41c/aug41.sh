# s41c: the cover check left rows violated (jointly table-killed rows). Try each table name outside the cover added to it.
O=$(cd $(dirname $0) && pwd); SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; T=$SC/s41c_tab
BASE=${1:-$O/ckeep_A74.txt}; TAGP=${2:-aug}
TN=$(grep -v '^#' $O/tabnames.txt | awk '{print $1}' | grep -xF -f $BASE | paste -sd,)
for n in $(grep -v '^#' $O/tabnames.txt | awk '{print $1}' | grep -vxF -f $BASE); do
  python3 $O/tabname.py build $T/aug $TN,$n; { cat $BASE; echo $n; } > $SC/ckeep_aug.txt
  bash $O/run41u.sh ${TAGP}_$n $T/aug "noC noCw ckeep=$SC/ckeep_aug.txt" $T/vaug_$n.txt; rm -rf $T/aug
done
echo DONE > $O/${TAGP}.done
