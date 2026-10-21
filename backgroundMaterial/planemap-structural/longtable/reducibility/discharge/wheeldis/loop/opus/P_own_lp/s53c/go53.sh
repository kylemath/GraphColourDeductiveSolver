# s53c driver: the s52c steps in order (noC upper + ccover53 -> tabnames -> batch2 per-name tables -> final53 -> check53; aug53 + final53 + check53 again if the check leaves rows)
O=$(cd $(dirname $0) && pwd)
bash $O/run53_noC.sh > $O/run53_noC.out 2>&1
[ -e $O/run53_noC.done ] || exit 3
python3 -I $O/tabname.py list > $O/tabname_list.out 2>&1 || exit 4
bash $O/batch2.sh > $O/batch2.out 2>&1
python3 -I $O/final53.py > $O/final53.log 2>&1 || exit 6
bash $O/check53.sh noctl > $O/check53.out 2>&1
echo DONE > $O/go53.done
