#!/bin/zsh
# HA5: after HCK63 (ALLDONE), build hD (HDA5T) and hC (A5CV), then the Opus glue; nice 20 via run.sh
cd $(dirname $0)
until grep -q ALLDONE ../job_HCK63/lean/status.txt 2>/dev/null; do sleep 60; done
(cd hd; ./run.sh HDA5T; for i in $(seq 0 34); do printf "HDA5TV%02d\n" $i; done | xargs -P 6 -n 1 ./run.sh; ./run.sh HDA5TAll; echo ALLDONE >> status.txt) &
(cd hc; ./run.sh CA5C; for i in $(seq 0 9); do printf "A5CV%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; ./run.sh A5CVAll; echo ALLDONE >> status.txt) &
wait
(cd hd; for i in $(seq 0 34); do printf "HA5D_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; for i in $(seq 0 34); do printf "COccHA5D_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; ./run.sh HDA5TOcc; echo GLUEDONE >> status.txt)
(cd hc; for i in $(seq 0 9); do printf "HA5C_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; for i in $(seq 0 9); do printf "COccHA5C_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; ./run.sh HA5COcc; echo GLUEDONE >> status.txt)
