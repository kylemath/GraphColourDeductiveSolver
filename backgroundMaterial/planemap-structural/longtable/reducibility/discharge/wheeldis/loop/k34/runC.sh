#!/bin/bash
# round 34: after part A's dfast18 checks (pids 1301 1302), part C = R's full-link windows (full.txt, ring order):
# kc on all; dfast on ring <= 16 (agreement check); dfast18 on kc-D windows at ring >= 17.  Then part B ring 10-14.
cd "$(dirname "$0")"
while kill -0 1301 2>/dev/null || kill -0 1302 2>/dev/null; do sleep 5; done
cat a0.df a1.df a2.df > binA_dfast.out
for p in 0 1 2; do awk -v p=$p 'NR%3==p' full.txt > c.p$p; done
for p in 0 1 2; do (
  ../kc/kc -v c.p$p > c.p$p.kc 2> c.p$p.kc.err
  awk '$2<=16' c.p$p > c.p$p.s; ../../bin/dfast c.p$p.s > c.p$p.df 2> c.p$p.df.err
  grep "D=true" c.p$p.kc | awk '{print $1}' > c.p$p.dn
  awk 'NR==FNR{d[$1]=1;next} ($1 in d) && $2>=17' c.p$p.dn c.p$p > c.p$p.big
  [ -s c.p$p.big ] && ../../bin/dfast18 c.p$p.big > c.p$p.df18 2> c.p$p.df18.err
) & done; wait
cat c.p?.kc > full_kc.out; cat c.p?.df > full_dfast.out; cat c.p?.df18 > full_dfast18.out 2>/dev/null; echo done > C.DONE
./runB.sh 10 14 b14
