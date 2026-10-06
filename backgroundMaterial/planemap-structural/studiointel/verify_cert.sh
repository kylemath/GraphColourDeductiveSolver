#!/bin/sh
# studiointel verify_cert.sh TAG HOLE [K] -- independent verification of a radius certificate: core class, r(s) >= K, and r(s) < K+1. Uses only core_check.py and check.py.
cd "$(dirname "$0")"; D=${CERTDIR:-run-C-2026-10-06/cert}; K=${3:-5}
python3 core_check.py $D/$1.graph.json $2
python3 check.py lb $D/$1.graph.json $2 $D/$1.hole$2.state.json $K
python3 check.py lb $D/$1.graph.json $2 $D/$1.hole$2.state.json $((K+1))
