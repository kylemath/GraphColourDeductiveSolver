#!/bin/bash
# EXPLORE rounds 15-17 chain (restarted after round 18): after round 15, run round 17 (6 ring-17 windows), then round 16
cd "$(dirname "$0")"
until [ -f run8.log ]; do sleep 15; done
./run17.sh
./run89.sh
