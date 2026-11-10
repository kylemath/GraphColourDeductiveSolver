#!/bin/bash
# K-5 Mac runner (macOS bash 3.2 safe: no arrays, no case inside $( ), no bash-4 features).
# Runs famK5_r1516_t102_00..03 (ring 15 first, then ring 16; smallest m first), NP at a time (default 4), one core each at nice 20.
# usage:  KC=/path/kc DF18=/path/dfast18 CF=/path/cfast [DF=/path/dfast] [SKIP=/path/skip_none.txt] bash runt102.sh [NP]
# Results: results/res_K5_<tag>.tsv + results/log_<tag>.txt.  Resumable: rerun skips windows already in each res file.
cd "$(dirname "$0")" || exit 1
NP=${1:-4}; mkdir -p results
: "${KC:?set KC to the kc binary}" "${DF18:?set DF18 to the dfast18 binary}" "${CF:?set CF to the cfast binary}"
if [ -z "$SKIP" ] && [ -f skip_none.txt ]; then SKIP="$PWD/skip_none.txt"; fi
export KC DF18 CF DF SKIP
ls famK5_r1516_t102_*.tsv | xargs -P "$NP" -I{} sh -c \
  't=$(basename {} .tsv); t=${t#famK5_}; nice -n 20 python3 mscreen.py {} results/res_K5_$t.tsv >> results/log_$t.txt 2>&1; echo "$t $(tail -1 results/log_$t.txt)"'
echo ALLDONE
