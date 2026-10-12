#!/bin/sh
cd "$(dirname "$0")"
C=../Census29/out
( nice -n 10 python3 tj_struct.py ../TrackF/graphs/frame22_28.txt 1 0 100000 > out/struct_frame22_28.log
  nice -n 10 python3 tj_struct.py $C/frame-29.txt 1 0 100000 > out/struct_frame29.log
  nice -n 10 python3 tj_struct.py ../TrackF/graphs/fall_20_46.txt 4 0 100000 > out/struct_fullerene.log ) &
( nice -n 10 python3 tj_struct.py $C/frame-30.txt 4 0 100000 > out/struct_frame30_s4.log
  nice -n 10 python3 tj_struct.py ../TrackF/graphs/plantri24.txt 20 0 100000 > out/struct_plantri24_s20.log ) &
wait
