#!/bin/sh
# Item 2 runs: 2 workers, nice 10
cd "$(dirname "$0")"
( nice -n 10 python3 rv_h0h3.py torus 20000 12 30 101 out/h0h3_torus.json > out/h0h3_torus.log 2>&1 ;
  nice -n 10 python3 rv_h0h3.py klein 10000 16 30 103 out/h0h3_klein.json > out/h0h3_klein.log 2>&1 ) &
( nice -n 10 python3 rv_h0h3.py rp2 20000 10 30 102 out/h0h3_rp2.json > out/h0h3_rp2.log 2>&1 ;
  nice -n 10 python3 rv_h0h3.py sphere 10000 10 30 104 out/h0h3_sphere.json > out/h0h3_sphere.log 2>&1 ) &
wait
