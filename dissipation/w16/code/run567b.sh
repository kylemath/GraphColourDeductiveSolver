#!/bin/bash
cd /tmp/swarm-W16; D=/tmp/swarm-W16/data
DROPLINK=5556676,5556677,5757677 OPUSF=1 timeout 1700 nice -n 19 python3 -I code/rowgen.py $D/world_567_7_std.pkl all $D/rg567_SO_all_drop3.pkl > logs/rg567_SO_all_drop3.log 2>&1
OPUSF=1 timeout 1700 nice -n 19 python3 -I code/rowgen.py $D/world_567_7_std.pkl allK $D/rg567_SO_allK.pkl > logs/rg567_SO_allK.log 2>&1
echo done > logs/run567b.done
