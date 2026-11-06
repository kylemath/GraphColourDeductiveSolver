#!/bin/bash
# EXPLORE round 34 part A: kc on the 7/27 certificate row's three open windows, one per core
cd "$(dirname "$0")"
i=0
while read -r line; do
  echo "$line" > a$i.in
  python3 ../kc/runrss.py a$i.kc a$i.kc.err ../kc/kc -v a$i.in &
  i=$((i+1))
done < binA.txt
wait
cat a?.kc > binA_kc.out
echo done > A.DONE
