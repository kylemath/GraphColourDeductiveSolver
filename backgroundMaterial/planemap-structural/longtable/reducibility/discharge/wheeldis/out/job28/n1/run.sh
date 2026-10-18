#!/bin/zsh
# Night batch n1 (18 Oct, Long Table go 08:35Z): cfast --search --limit 1 on the 7/27 binder-pair windows, one core each,
# nice 20, wall caps via perl alarm. 11 jobs: ring-18 x2 (8 h), win17 ring-17 x6 (2 h), ring-16 timeouts x3 (6 h).
cd "$(dirname $0)"; CF=../../../../studio15/cfast
one() { # file line cap tag
  sed -n "$2p" $1 > $4.in; s=$(date +%s)
  nice -n 20 perl -e 'alarm shift; exec @ARGV' $3 $CF $4.in --search --limit 1 > $4.cfast 2>&1; rc=$?
  echo "$(date '+%m-%d %H:%M') $4 $(cut -d' ' -f1 $4.in) rc=$rc $(( $(date +%s)-s ))s $(grep -q C-REDUCIBLE $4.cfast && echo C || (grep -q 'search |X|' $4.cfast && echo neither || echo TIMEOUT))" >> n1.log
}
for i in 1 2; do one r18.txt $i 28800 r18_$i &; done
for i in 1 2 3 4 5 6; do one w17.txt $i 7200 w17_$i &; done
for i in 1 2 3; do one r16.txt $i 21600 r16_$i &; done
wait; echo done > n1.DONE
