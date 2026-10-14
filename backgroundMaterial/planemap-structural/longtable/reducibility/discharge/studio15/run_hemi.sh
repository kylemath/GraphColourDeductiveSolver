#!/bin/zsh
# Job 15: C-candidate search on the hemi8 key (ring 15) then the hemi9 key (ring 16); waits for a free core (cap 14)
cd "$(dirname $0)"
while [ $(( $(pgrep -f dfast18 | wc -l) + $(pgrep -f 'wheelcheck16 v_' | wc -l) )) -ge 14 ]; do sleep 30; done
nice -n 10 ./cfast hemi8.txt --search --limit 1000000 > hemi8_search.out 2>&1
nice -n 10 ./cfast hemi9.txt --search --limit 1000000 > hemi9_search.out 2>&1
echo DONE > hemi.DONE
