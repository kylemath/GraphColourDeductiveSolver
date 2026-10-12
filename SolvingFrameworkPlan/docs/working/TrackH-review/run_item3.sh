#!/bin/sh
# Item 3 runs (rigid isolation, sphere): 2 workers, nice 10
cd "$(dirname "$0")"
C=../Census29/out
X=out/exclude_trackH.txt
( for o in 22 23 24 25 26 27 28 29; do nice -n 10 python3 rv_ri.py out/ri_frame$o.json $C/frame-$o.txt 1 0 1000000000 $X > /dev/null 2>out/ri_frame$o.err; done
  nice -n 10 python3 rv_ri.py out/ri_frame30.json $C/frame-30.txt 10 3 1000000000 $X > /dev/null 2>out/ri_frame30.err ) &
( for f in m3_12 m3_14 m4_15 m4_17 m5_20 m5_22; do nice -n 10 python3 rv_ri.py out/ri_pl_$f.json out/pl/$f.txt > /dev/null 2>out/ri_pl_$f.err; done
  nice -n 10 python3 rv_ri.py out/ri_frame31.json $C/frame-31.txt 40 7 1000000000 $X > /dev/null 2>out/ri_frame31.err
  nice -n 10 python3 rv_ri.py out/ri_frame32.json $C/frame-32.txt 160 11 1000000000 $X > /dev/null 2>out/ri_frame32.err ) &
wait
