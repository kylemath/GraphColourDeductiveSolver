#!/bin/sh
# Track G data collection: 2 single-threaded workers under nice -n 10.
cd "$(dirname "$0")"
C=../Census29/out
F=../TrackF
( for n in 22 23 24 25 26 27 28 29; do nice -n 10 python3 tg_collect.py $C/frame-$n.txt out/census$n > out/census$n.log 2>&1; done; echo done > out/W1.done ) &
( nice -n 10 python3 tg_collect.py $F/graphs/fall_30.txt out/c30 --names 'C30#0' --homology > out/c30.log 2>&1
  nice -n 10 python3 tg_collect.py $F/graphs/fall_40.txt out/c40 --names 'C40#0' --homology > out/c40.log 2>&1
  for n in 30 31 32; do nice -n 10 python3 tg_collect.py $C/frame-$n.txt out/cyc$n --names 'p30.r10#1252,p31.r1#7302,p31.r12#19956,p31.r13#292235,p31.r19#11250,p32.r11#14729,p32.r111#946067,p32.r124#210513,p32.r17#261286,p32.r29#12613,p32.r68#2466,p32.r85#113993,p32.r96#9744' --homology > out/cyc$n.log 2>&1; done
  nice -n 10 python3 tg_collect.py $F/out/lpc/cyc_graphs.txt out/off --holes-from $F/out/lpc/cyc_graphs.kclass3.jsonl --homology > out/off.log 2>&1
  nice -n 10 python3 tg_collect.py $F/out/lpc/cyc555_graphs.txt out/off555 --holes-from $F/out/lpc/cyc555_graphs.kclass3.jsonl --homology > out/off555.log 2>&1
  echo done > out/W2.done ) &
wait
