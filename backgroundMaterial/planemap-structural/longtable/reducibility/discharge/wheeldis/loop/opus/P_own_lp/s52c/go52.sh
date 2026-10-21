# s52c driver: the s46c steps in order (noC upper + ccover52 -> tabnames -> batch2 per-name tables -> final52 -> check52)
O=$(cd $(dirname $0) && pwd)
bash $O/run52_noC.sh > $O/run52_noC.out 2>&1
[ -e $O/run52_noC.done ] || exit 3
python3 -I $O/tabname.py list > $O/tabname_list.out 2>&1
bash $O/batch2.sh > $O/batch2.out 2>&1
python3 -I $O/final52.py > $O/final52.log 2>&1
bash $O/check52.sh > $O/check52.out 2>&1
echo DONE > $O/go52.done
