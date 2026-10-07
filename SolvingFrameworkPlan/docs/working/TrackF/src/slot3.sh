#!/bin/sh
# Track F slot 3: frame-class adversarial witnesses (Track B; none has a 66666 hole), n <= 49, all holes, lock-parity check; then long tubes (sampling)
cd "$(dirname "$0")/.."
awk '$2<=49' graphs/witness.txt > out/wit/small.in
nice -n 10 ./src/f66_w1_new out/wit/small.in --lockparity --dump 10 --dumpfile out/wit/small.runs.jsonl > out/wit/small.holes.jsonl 2> out/wit/small.err
awk '$2>62' graphs/tubes.txt | sort -k2 -n > out/tubes/big.in
nice -n 10 ./src/f66_w4_new out/tubes/big.in --sample 200000 --budget 200000 --dump 12 --dumpfile out/tubes/big.runs.jsonl > out/tubes/big.holes.jsonl 2> out/tubes/big.err
echo done > out/tubes/DONE
