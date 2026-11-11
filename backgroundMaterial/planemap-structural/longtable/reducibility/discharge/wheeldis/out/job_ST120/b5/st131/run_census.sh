#!/bin/zsh
# ST-131: rotation-aware failure census (every failing leaf), d7, d8 (rotmin) and d9..14 (c+ survivors); 1 core, nice 15
cd $(dirname $0)/..
K=kc:st127/k767_kc.txt; P=cert/parts79.txt
for d in 7 8; do
  nice -n 15 python3 -I py/export_cert.py $d st131/cert${d}_census.txt --model $K --parts $P --rot --rotmin --census st131/census$d.tsv > st131/export$d.log 2>&1
done
for d in 9 10 11 12 13 14; do
  nice -n 15 python3 -I py/export_cert.py $d st131/cert${d}_census.txt --model $K --parts $P --rot --links-file cert/links${d}_lean.txt --census st131/census$d.tsv > st131/export$d.log 2>&1
done
echo CENSUSDONE > st131/DONE
