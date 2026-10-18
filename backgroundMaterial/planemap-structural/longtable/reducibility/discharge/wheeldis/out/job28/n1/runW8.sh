#!/bin/zsh
# n1 follow-up (18 Oct 10:41Z, Long Table go): the 5 win17 2 h TIMEOUTs again with an 8 h cap, nice 20, one core each.
cd "$(dirname $0)"; CF=../../../../studio15/cfast
one() { # line tag
  sed -n "$1p" w17.txt > $2.in; s=$(date +%s)
  nice -n 20 perl -e 'alarm shift; exec @ARGV' 28800 $CF $2.in --search --limit 1 > $2.cfast 2>&1; rc=$?
  echo "$(date '+%m-%d %H:%M') $2 $(cut -d' ' -f1 $2.in) rc=$rc $(( $(date +%s)-s ))s $(grep -q C-REDUCIBLE $2.cfast && echo C || (grep -q 'search |X|' $2.cfast && echo neither || echo TIMEOUT))" >> n1.log
}
for i in 1 2 3 4 5; do one $i w17L_$i &; done
wait; echo done > W8.DONE
