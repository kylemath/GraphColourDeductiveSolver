#!/bin/bash
# graph-only census at orders 27-28: configuration-free graphs and those with adjacent degree-5 vertices
cd "$(dirname "$0")"
for n in 27 28; do
  ~/work/bin/plantri -m5 -c4 -a $n 2>/dev/null > /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver/d0b4209a-c287-4052-b58e-4ff5d94a2731/scratchpad/plantri-$n.txt
  python3 convert.py plantri /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver/d0b4209a-c287-4052-b58e-4ff5d94a2731/scratchpad/plantri-$n.txt | sed "s/^plantri-$n#/p$n#/" > /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver/d0b4209a-c287-4052-b58e-4ff5d94a2731/scratchpad/in-plantri-$n.txt
  nice -n 10 ./picyc /private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver/d0b4209a-c287-4052-b58e-4ff5d94a2731/scratchpad/in-plantri-$n.txt --graphonly > out/census-$n.jsonl
  grep '"cfree": true' out/census-$n.jsonl > out/cfree-$n.jsonl
  echo "order $n graphs $(wc -l < out/census-$n.jsonl) cfree $(wc -l < out/cfree-$n.jsonl) cfree+adj55 $(grep -c '"adj55": [1-9]' out/cfree-$n.jsonl)" >> out/census.log
done
echo CENSUS DONE >> out/census.log
