#!/bin/bash
# K-3 Mac runner (macOS bash 3.2 safe: no arrays, no case inside $( ), no bash-4 features).
# Runs famK3_r15_01..12 (value order: highest-excess BINDING classes first), NP at a time (default 10), one core each at nice 20.
# usage:  KC=/path/kc DF18=/path/dfast18 CF=/path/cfast [DF=/path/dfast] [SKIP=/path/skip_k3.txt] bash runk3.sh [NP]
# Results: results/res_K3_<tag>.tsv + results/log_<tag>.txt.  Resumable: rerun skips windows already in each res file.
cd "$(dirname "$0")" || exit 1
NP=${1:-10}; mkdir -p results
: "${KC:?set KC to the kc binary}" "${DF18:?set DF18 to the dfast18 binary}" "${CF:?set CF to the cfast binary}"
if [ -z "$SKIP" ] && [ -f skip_k3.txt ]; then SKIP="$PWD/skip_k3.txt"; fi
export KC DF18 CF DF SKIP
ls famK3_r15_*.tsv | xargs -P "$NP" -I{} sh -c \
  't=$(basename {} .tsv); t=${t#famK3_}; nice -n 20 python3 mscreen.py {} results/res_K3_$t.tsv >> results/log_$t.txt 2>&1; echo "$t $(tail -1 results/log_$t.txt)"'
echo ALLDONE
