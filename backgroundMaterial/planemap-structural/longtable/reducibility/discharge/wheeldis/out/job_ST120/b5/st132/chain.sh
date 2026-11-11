#!/bin/zsh
# wait for the ST-131 K768 census, then run the ST-132 K783 census (1 core at a time)
cd $(dirname $0)/..
until [ -f st131/DONE ]; do sleep 30; done
st132/run_census.sh > st132/run.log 2>&1
