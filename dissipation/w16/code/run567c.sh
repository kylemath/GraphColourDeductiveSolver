#!/bin/bash
cd /tmp/swarm-W16; D=/tmp/swarm-W16/data
until [ -e logs/run567b.done ]; do sleep 15; done
for fam in rrz base; do
  OPUSF=1 timeout 1700 nice -n 19 python3 -I code/rowgen.py $D/world_567_7_std.pkl $fam $D/rg567_SO_$fam.pkl > logs/rg567_SO_$fam.log 2>&1
  OPUSQ=1 timeout 900 nice -n 19 python3 -I code/exact_dual.py $D/rg567_SO_$fam.pkl $fam $D/x567SO_$fam > logs/x567SO_$fam.log 2>&1
  OFAM=$fam timeout 1500 nice -n 19 python3 -I code/opus_lower.py $D/x567SO_${fam}_cert.json > logs/olowx567SO_$fam.log 2>&1
done
echo done > logs/run567c.done
