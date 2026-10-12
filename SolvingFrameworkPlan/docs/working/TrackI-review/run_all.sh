#!/bin/sh
# two workers, nice'd
cd "$(dirname "$0")"
( nice -n 10 python3 ri_run.py sphere5 11 300 out/sphere5.json --tait > out/sphere5.log 2>&1 ;
  nice -n 10 python3 ri_run.py census 12 300 out/census.json --tait > out/census.log 2>&1 ) &
( nice -n 10 python3 ri_run.py sphere3 13 400 out/sphere3.json --tait > out/sphere3.log 2>&1 ;
  nice -n 10 python3 ri_run.py rp2 14 200 out/rp2.json --tait > out/rp2.log 2>&1 ;
  nice -n 10 python3 ri_run.py torus 15 200 out/torus.json --tait > out/torus.log 2>&1 ) &
wait
