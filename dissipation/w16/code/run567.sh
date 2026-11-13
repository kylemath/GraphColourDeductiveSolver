#!/bin/bash
# sequential (one core, nice 19): row generation on the 5/6/7 world with the lazy Opus filter, exact certs, Opus lowerR2 checks
cd /tmp/swarm-W16; D=/tmp/swarm-W16/data
for fam in all base rrz; do
  OPUSF=1 timeout 1700 nice -n 19 python3 -I code/rowgen.py $D/world_567_7_std.pkl $fam $D/rg567_SO_$fam.pkl > logs/rg567_SO_$fam.log 2>&1
  OPUSQ=1 timeout 900 nice -n 19 python3 -I code/cert.py $D/rg567_SO_$fam.pkl $fam $D/c567SO_$fam > logs/c567SO_$fam.log 2>&1
  OFAM=$fam timeout 1500 nice -n 19 python3 -I code/opus_lower.py $D/c567SO_${fam}_cert.json > logs/olow567SO_$fam.log 2>&1
done
for v in std SO; do
  if [ $v = SO ]; then E="OPUSF=1"; else E="OPUSF=0"; fi
  env $E timeout 1700 nice -n 19 python3 -I code/rowgen.py $D/world_567_7_std.pkl allK $D/rg567_${v}_allK.pkl > logs/rg567_${v}_allK.log 2>&1
done
echo ALLDONE > logs/run567.done
