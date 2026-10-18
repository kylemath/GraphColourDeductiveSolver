#!/bin/zsh
# Night batch n1, row R (the 7/27 certificate's receiver d=7 5675765/6577575): cfast on explore's 3 kc-not-D windows,
# one core each, nice 20. Caps: ring 16 6 h, ring 17 8 h.
cd "$(dirname $0)"; CF=../../../../studio15/cfast
one() { # line cap tag
  sed -n "$1p" rowR.txt > $3.in; s=$(date +%s)
  nice -n 20 perl -e 'alarm shift; exec @ARGV' $2 $CF $3.in --search --limit 1 > $3.cfast 2>&1; rc=$?
  echo "$(date '+%m-%d %H:%M') $3 $(cut -d' ' -f1 $3.in) rc=$rc $(( $(date +%s)-s ))s $(grep -q C-REDUCIBLE $3.cfast && echo C || (grep -q 'search |X|' $3.cfast && echo neither || echo TIMEOUT))" >> n1.log
}
one 1 21600 R16 &; one 2 28800 R17a &; one 3 28800 R17b &
wait; echo done > R.DONE
