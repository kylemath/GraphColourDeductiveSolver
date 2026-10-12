#!/bin/sh
# Track G: cycle anatomy (runs after worker 2 finishes, so at most 2 workers at once)
cd "$(dirname "$0")"
C=../Census29/out; F=../TrackF
until [ -f out/W2.done ]; do sleep 20; done
NAMES='p30.r10#1252,p31.r1#7302,p31.r12#19956,p31.r13#292235,p31.r19#11250,p32.r11#14729,p32.r111#946067,p32.r124#210513,p32.r17#261286,p32.r29#12613,p32.r68#2466,p32.r85#113993,p32.r96#9744'
nice -n 10 python3 tg_cycles.py $F/graphs/fall_40.txt out/cycles_c40.jsonl --names 'C40#0' --homology > /dev/null
for n in 30 31 32; do nice -n 10 python3 tg_cycles.py $C/frame-$n.txt out/cycles_sph$n.jsonl --names "$NAMES" --homology > /dev/null; done
nice -n 10 python3 tg_cycles.py $F/out/lpc/cyc_graphs.txt out/cycles_off.jsonl --holes-from $F/out/lpc/cyc_graphs.kclass3.jsonl --homology > /dev/null
nice -n 10 python3 tg_cycles.py $F/out/lpc/cyc555_graphs.txt out/cycles_off555.jsonl --holes-from $F/out/lpc/cyc555_graphs.kclass3.jsonl --homology > /dev/null
echo done > out/W3.done
