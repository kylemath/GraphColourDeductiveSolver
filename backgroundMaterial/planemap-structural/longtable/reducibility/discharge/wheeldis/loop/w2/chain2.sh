#!/bin/bash
# EXPLORE rounds 17/16 chain (requeued behind round 20 H-L2): after round 15 and ../l2/l2.done, run round 17 then round 16
cd "$(dirname "$0")"
until [ -f run8.log ] && [ -f ../l2/l2.done ]; do sleep 15; done
./run17.sh
./run89.sh
