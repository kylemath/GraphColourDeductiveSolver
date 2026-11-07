#!/bin/zsh
# HCK63 driver 2: keeps at most NL K63HV builds running in total (including those the first driver already started), skips done/running modules
cd $(dirname $0); NL=${NL:-10}
running() { ps -axo command | grep -c "[r]un.sh K63HV" }
for i in $(seq 0 113); do
  m=$(printf "K63HV%03d" $i)
  grep -q "^$m exit=" status.txt && continue
  ps -axo command | grep -q "[r]un.sh $m\$" && continue
  while [ $(running) -ge $NL ]; do sleep 20; done
  ./run.sh $m &
  sleep 1
done
wait
while [ $(running) -gt 0 ]; do sleep 20; done
./run.sh K63HVAll; echo ALLDONE >> status.txt
