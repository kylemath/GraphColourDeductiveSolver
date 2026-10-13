#!/bin/sh
# Lemma E, Fisk degree and level-model runs quoted in R0-ATTEMPT-1.md -> out/lemmaE.txt
P="nice -n 10 python3"
for n in 8 10 12 14; do $P step_mod8.py $n; done
for n in 10 12 14; do $P lemmaE_parts.py $n; done
$P fisk.py c30; $P fisk.py 10; $P fisk.py 12
for n in 8 10 12 14 16 18 20 24 28; do $P l5_levels.py $n; done
for n in 8 10 12 14 16 18; do $P l5_levels.py $n nonplanar | cut -c 1-60; $P l5_levels.py $n noparity | cut -c 1-60; done
for n in 10 14 18; do for v in free1 free3 free4 crossI crossO; do $P l5_levels.py $n $v | cut -c 1-70; done; done
for n in 10 12 14 16 18 20; do $P l5_levels.py $n free1 free3 free4 | cut -c 1-70; done
