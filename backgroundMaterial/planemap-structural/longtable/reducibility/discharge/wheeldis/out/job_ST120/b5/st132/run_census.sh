#!/bin/zsh
# ST-132: rotation-aware failure census with K783 (every failing leaf), d7, d8 (rotmin) and d9..14 (c+ survivors); 1 core, nice 15
cd $(dirname $0)/..
K=kc:st132/k783_kc.txt; P=cert/parts79.txt
for d in 7 8; do
  nice -n 15 python3 -I py/export_cert.py $d st132/cert${d}_census.txt --model $K --parts $P --rot --rotmin --census st132/census$d.tsv > st132/export$d.log 2>&1
done
for d in 9 10 11 12 13 14; do
  nice -n 15 python3 -I py/export_cert.py $d st132/cert${d}_census.txt --model $K --parts $P --rot --links-file cert/links${d}_lean.txt --census st132/census$d.tsv > st132/export$d.log 2>&1
done
echo CENSUSDONE > st132/DONE
