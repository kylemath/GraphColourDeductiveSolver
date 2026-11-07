#!/bin/zsh
cd $(dirname $0)
until grep -q ALLDONE hd/status.txt 2>/dev/null && grep -q ALLDONE hc/status.txt 2>/dev/null; do sleep 60; done
(cd hd; for i in $(seq 0 44); do printf "HA5BD_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; for i in $(seq 0 44); do printf "COccHA5BD_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; ./run.sh HDA5BOcc; echo GLUEDONE >> status.txt)
(cd hc; for i in $(seq 0 8); do printf "HA5BC_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; for i in $(seq 0 8); do printf "COccHA5BC_%02d\n" $i; done | xargs -P 4 -n 1 ./run.sh; ./run.sh HA5BCOcc; echo GLUEDONE >> status.txt)
