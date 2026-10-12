#!/bin/sh
# worker 1, second job: torus batch (Lemma E general form, chi_S = 0)
cd "$(dirname "$0")"
python3 -I rv_gen.py torus 800 10 30 3 505 > out/fresh_torus3.txt
nice -n 10 ./rv_eng -E 0 -s 11 -M 4000000 < out/fresh_torus3.txt > out/w1_torus3.log 2> out/w1_torus3.err
