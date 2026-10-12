#!/bin/sh
# Track L: sigma-type proof check on sphere sets (2 workers, nice 10)
cd "$(dirname "$0")"
( for f in 27 28; do nice -n 10 python3 tl_sigma_check.py ../Census29/out/frame-$f.txt 1 0 100000; done > out/sigma_w1.log 2>&1 ) &
( nice -n 10 python3 tl_sigma_check.py ../Census29/out/frame-29.txt 1 0 100000; nice -n 10 python3 tl_sigma_check.py ../TrackF/graphs/plantri24.txt 10 3 100000; nice -n 10 python3 tl_sigma_check.py ../TrackF/graphs/fall_20_46.txt 2 1 100000 ) > out/sigma_w2.log 2>&1 &
wait
