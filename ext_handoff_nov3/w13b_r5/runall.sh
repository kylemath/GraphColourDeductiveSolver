#!/bin/bash
# W13b round 5 (K-2): run every famR5_*.tsv batch in this folder, NP at a time (default 10), each on one core at nice 20.
# usage:  KC=/path/kc DF18=/path/dfast18 CF=/path/cfast [DF=/path/dfast] bash runall.sh [NP]
# Results: results/res_W13b_<tag>.tsv and results/log_<tag>.txt (<tag> = file name without famR5_ and .tsv).
# Resumable: rerunning skips the windows already in each res file.  Uses python3 if present, else mscreen.sh.
cd "$(dirname "$0")" || exit 1
NP=${1:-10}; mkdir -p results
: "${KC:?set KC to the kc binary}" "${DF18:?set DF18 to the dfast18 binary}" "${CF:?set CF to the cfast binary}"
export KC DF18 CF DF
if command -v python3 >/dev/null 2>&1; then export SCR="python3 mscreen.py"; else export SCR="bash mscreen.sh"; fi
ls famR5_r15_0[1-8].tsv famR5_k85r14.tsv famR5_k85r13.tsv | xargs -P "$NP" -I{} sh -c \
  't=$(basename {} .tsv); t=${t#famR5_}; nice -n 20 $SCR {} results/res_W13b_$t.tsv >> results/log_$t.txt 2>&1; echo "$t $(tail -1 results/log_$t.txt)"'
echo ALLDONE
