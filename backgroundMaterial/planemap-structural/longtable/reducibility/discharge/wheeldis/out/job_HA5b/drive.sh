#!/bin/zsh
# HA5b: after HA5 finishes (both hd and hc GLUEDONE), build HDA5B hD and A5BV hC; glue added when Opus delivers
cd $(dirname $0)
until grep -q GLUEDONE ../job_HA5/hd/status.txt 2>/dev/null && grep -q GLUEDONE ../job_HA5/hc/status.txt 2>/dev/null; do sleep 60; done
(cd hd; ./run.sh HDA5B; for i in $(seq 0 44); do printf "HDA5BV%02d\n" $i; done | xargs -P 6 -n 1 ./run.sh; ./run.sh HDA5BAll; echo ALLDONE >> status.txt) &
(cd hc; for i in $(seq 0 8); do printf "A5BV%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; ./run.sh A5BVAll; echo ALLDONE >> status.txt) &
wait
