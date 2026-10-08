#!/bin/bash
# Track U launch: 4 workers, nice -n 10, ~60 min wall total
cd "$(dirname "$0")"
E=./tu_eng; O=out
( for nn in 16 18 20 22 24 26; do nice -n 10 $E anneal 11$nn $nn 360 B 1 > $O/annB_n$nn.jsonl; done ) &
( nice -n 10 $E anneal 2032 32 1200 A 1 > $O/annA_n32.jsonl; nice -n 10 $E anneal 2040 40 1200 A 1 > $O/annA_n40.jsonl; nice -n 10 $E anneal 2036 36 900 B 1 > $O/annB_n36.jsonl ) &
( nice -n 10 $E anneal 31 0 1200 B 1 $O/seed_c30.txt 0 > $O/seedB_c30.jsonl; nice -n 10 $E anneal 32 0 1200 B 1 $O/seed_surf.txt 1 > $O/seedB_klein.jsonl; nice -n 10 $E anneal 35 0 900 A 1 $O/seed_c30.txt 0 > $O/seedA_c30.jsonl ) &
( nice -n 10 $E anneal 41 0 1200 B 1 $O/seed_surf.txt 5 > $O/seedB_rp2w501.jsonl; nice -n 10 $E anneal 42 0 1200 B 1 $O/seed_surf.txt 0 > $O/seedB_rp2w664.jsonl; nice -n 10 $E anneal 2028 28 900 A 1 > $O/annA_n28.jsonl ) &
wait
