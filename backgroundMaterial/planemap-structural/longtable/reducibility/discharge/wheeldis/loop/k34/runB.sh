#!/bin/bash
# EXPLORE round 34 part B: kc then dfast on the untested windows of the tight d=7 family with ring LO..HI, 3 streams
# usage: runB.sh LO HI TAG   (dfast caps at ring 16; dfast18 for 17+)
cd "$(dirname "$0")"
LO=$1; HI=$2; T=$3; DF=../../bin/dfast; [ "$HI" -gt 16 ] && DF=../../bin/dfast18
awk -v lo=$LO -v hi=$HI '$2>=lo && $2<=hi' t13_r18.txt > $T.txt
for p in 0 1 2; do awk -v p=$p 'NR%3==p' $T.txt > $T.p$p; done
for p in 0 1 2; do ( ../kc/kc $T.p$p > $T.p$p.kc 2> $T.p$p.kc.err; $DF $T.p$p > $T.p$p.df 2> $T.p$p.df.err ) & done; wait
cat $T.p0.kc $T.p1.kc $T.p2.kc > ${T}_kc.out; cat $T.p0.df $T.p1.df $T.p2.df > ${T}_dfast.out
rm -f $T.p? ; echo done > $T.DONE
