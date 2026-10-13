#!/bin/sh
# re-run every quick experiment quoted in R0-ATTEMPT-1.md, logging to out/quick.txt
P="nice -n 10 python3"
for n in 8 10 12 14; do $P core.py $n 10; done
for n in 8 10 12 14 16; do $P depth.py $n; done
for n in 8 10 12 14 16; do $P l5_probe.py $n; done
for n in 8 10 12 14 16; do $P order_test.py $n 10; done; for n in 10 14; do $P order_test.py $n 5; done
for n in 8 10 12 14 16; do $P order_cegar.py $n 10 120; done; for n in 12 14 16; do $P order_cegar.py $n 5 120; done
for n in 12 16 20; do $P order_cegar.py $n 6 60 poscontrol; done
$P sigsum.py c30; for n in 8 10 12; do $P sigsum.py $n; done
$P c30.py; $P hamcheck.py; $P c30_anat.py; $P winding.py; $P poscontrol.py
for n in 8 10 12; do $P linpot.py $n; done; $P linpot.py 14 400
$P featpot.py 8; $P featpot.py 8 10; $P featpot2.py 10
for n in 10 12 14; do $P hdist.py $n; done
$P cubic_sig.py
for n in 8 10 12 14; do $P r0sat.py r0 $n 5 nonplanar t=60 | head -1; $P r0sat.py r0 $n 5 t=60 | head -1; done
for n in 8 10 12; do $P r0sat.py r0 $n 10 | head -1; $P r0sat.py r0 $n 10 nonplanar | head -1; done
for n in 10 14 18; do $P r0sat.py adj $n 5 t=120 | head -1; done
for n in 8 10 12 14; do $P r0sat.py adj $n 10 t=100 | head -1; done
for n in 14 16 18; do $P r0sat.py star $n 10 t=280 | head -1; done
