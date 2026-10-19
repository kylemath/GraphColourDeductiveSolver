#!/bin/zsh
# Requeue (19 Oct ~01:55Z, after Job 24b DONE): w17L_3 and w17L_4 (terminated 18 Oct 11:12Z for the 24b remainder),
# again with an 8 h cap, nice 20, one core each. Same hypothesis and kill lines as the w17L table in RUNLOG.md.
cd "$(dirname $0)"; CF=../../../../studio15/cfast
one() { # line tag
  sed -n "$1p" w17.txt > $2.in; s=$(date +%s)
  nice -n 20 perl -e 'alarm shift; exec @ARGV' 28800 $CF $2.in --search --limit 1 > $2.cfast 2>&1; rc=$?
  echo "$(date '+%m-%d %H:%M') $2 $(cut -d' ' -f1 $2.in) rc=$rc $(( $(date +%s)-s ))s $(grep -q C-REDUCIBLE $2.cfast && echo C || (grep -q 'search |X|' $2.cfast && echo neither || echo TIMEOUT)) (requeue)" >> n1.log
}
until [ $(ps -axo %cpu= | awk '$1>40' | wc -l) -le 14 ]; do python3 -c 'import time; time.sleep(120)'; done
one 3 w17L_3 &; one 4 w17L_4 &
wait; echo done > R34.DONE
