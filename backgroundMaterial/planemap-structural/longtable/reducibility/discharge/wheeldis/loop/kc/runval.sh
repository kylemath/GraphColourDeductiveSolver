#!/bin/bash
# EXPLORE round 33 validation with the final kc build: the 98 ring 10-16 windows, then the ring-17 not-D and D keys,
# all in Jacobi mode (depth comparable with dfast), 3 processes.
cd "$(dirname "$0")"
python3 runrss.py val_kc.txt val_kc.err ./kc -j val.txt &
python3 runrss.py r17_notD.out r17_notD.err ./kc -j -v r17_notD.txt &
python3 runrss.py r17_D.out r17_D.err ./kc -j -v r17_D.txt &
wait
python3 cmp.py val_kc.txt val_dfast.txt > cmp_val.txt
cat r17_notD.out r17_D.out > r17_kc.txt; python3 cmp.py r17_kc.txt r1718_dfast.txt > cmp_r17.txt
