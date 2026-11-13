#!/bin/bash
cd /tmp/swarm-W16; D=/tmp/swarm-W16/data
until [ -e logs/run567c.done ]; do sleep 15; done
timeout 900 nice -n 19 python3 -I code/exact_dual.py $D/rg567_SO_allK.pkl allK $D/x567SO_allK > logs/x567SO_allK.log 2>&1
echo done > logs/run567d.done
