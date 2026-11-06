#!/bin/zsh
# KS5 driver (Studio): mscreen.py per batch, one core each at nice 20, up to NP at once, in the coordinator's priority order
cd $(dirname $0); NP=${NP:-8}
export KC=$PWD/bin/kc DF18=$PWD/bin/dfast18 CF=$PWD/bin/cfast; unset DF
mkdir -p results
for t in r15_01 r15_02 k85r14 r15_03 k85r13 r15_05 r15_08 r15_06 r15_07 r15_04; do echo $t; done | \
  xargs -P $NP -I{} zsh -c 'nice -n 20 python3 mscreen.py famR5_{}.tsv results/res_W13b_{}.tsv >> results/log_{}.txt 2>&1; echo "{} $(tail -1 results/log_{}.txt) $(date -u +%H:%M)" >> results/driver_done.txt'
echo ALLDONE >> results/driver_done.txt
