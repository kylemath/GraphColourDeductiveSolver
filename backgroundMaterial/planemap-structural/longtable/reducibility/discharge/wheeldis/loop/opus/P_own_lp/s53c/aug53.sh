# s53c (= s52c/aug52.sh): if the cover check leaves rows violated (jointly table-killed rows), try each table name outside the cover added to it.
# usage: bash aug53.sh [BASE_CKEEP] [TAGPREFIX]
O=$(cd $(dirname $0) && pwd); SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; T=$SC/s53c_tab; mkdir -p $T
BASE=${1:-$O/ckeep_A97.txt}; TAGP=${2:-aug}
TN=$(grep -v '^#' $O/tabnames.txt | awk '{print $1}' | grep -xF -f $BASE | paste -sd,)
for n in $(grep -v '^#' $O/tabnames.txt | awk '{print $1}' | grep -vxF -f $BASE); do
  python3 $O/tabname.py build $T/aug ${TN:+$TN,}$n; { cat $BASE; echo $n; } > $SC/s53c_ckeep_aug.txt
  bash $O/run53u.sh ${TAGP}_$n $T/aug "noC noCw ckeep=$SC/s53c_ckeep_aug.txt" $T/vaug_$n.txt; rm -rf $T/aug
done
echo DONE > $O/${TAGP}.done
