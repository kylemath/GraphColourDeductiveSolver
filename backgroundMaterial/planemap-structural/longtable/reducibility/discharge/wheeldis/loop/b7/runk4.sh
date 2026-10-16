#!/bin/bash
# EXPLORE round 10: K = 4 completions of each LP binder's 2-ball (centre 7), 3 at a time, CAP seconds each.
# usage: loop/b7/runk4.sh MAXL CAP
cd "$(dirname "$0")"; M=$1; CAP=$2
xargs -P 3 -I{} bash -c 'f={}; n=${f%%:*}; timeout '"$CAP"' nice -n 5 ./defectb7 ../g9/defect_tables8.txt 7 4 1 '"$M"' 1000000000 60 "" "$f" > k4_m'"$M"'_$n.out 2> k4_m'"$M"'_$n.err; echo "$n exit $?" >> k4_m'"$M"'.done' < ${FIX:-fix.txt}
echo all done >> k4_m$M.done
