#!/bin/zsh
cd $(dirname $0)
for b in A B; do n=$([ $b = A ] && echo 3 || echo 40); for i in $(seq 0 $n); do printf "HW2%s_%02d\n" $b $i; done | xargs -P 4 -n 1 ./run.sh; for i in $(seq 0 $n); do printf "COccHW2%s_%02d\n" $b $i; done | xargs -P 4 -n 1 ./run.sh; done
./run.sh HW2AOcc
until grep -q "^W2BVAll exit=0" status.txt; do sleep 300; done; ./run.sh HW2BOcc; echo GLUEDONE >> status.txt
