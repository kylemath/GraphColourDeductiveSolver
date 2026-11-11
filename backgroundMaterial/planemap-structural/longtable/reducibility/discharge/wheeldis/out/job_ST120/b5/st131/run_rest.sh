#!/bin/zsh
# ST-131 (rerun after the aborted d8): K768 rotation-aware census d8 (rotmin), d9..14 (c+ survivors); then K783 (ST-132)
cd $(dirname $0)/..
K=kc:st127/k767_kc.txt; P=cert/parts79.txt
nice -n 15 python3 -I py/export_cert.py 8 st131/cert8_census.txt --model $K --parts $P --rot --rotmin --census st131/census8.tsv > st131/export8.log 2>&1
echo "d8 exit $?" >> st131/run.log
for d in 9 10 11 12 13 14; do
  nice -n 15 python3 -I py/export_cert.py $d st131/cert${d}_census.txt --model $K --parts $P --rot --links-file cert/links${d}_lean.txt --census st131/census$d.tsv > st131/export$d.log 2>&1
  echo "d$d exit $?" >> st131/run.log
done
echo CENSUSDONE > st131/DONE
st132/run_census.sh > st132/run.log 2>&1
