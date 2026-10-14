#!/bin/zsh
# start the Job 7 census once the Job 6 walkers (Python walk.py) are gone (they are capped at 01:10)
cd "$(dirname $0)"
until [[ $(date +%H%M) -ge 0110 && $(date +%H%M) -lt 1200 ]]; do sleep 60; done
while ps -axo command | grep -v grep | grep -q "walk[.]py"; do sleep 30; done
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do ./bnd_worker.sh & done
wait
echo CENSUSDONE > out/census/DONE
