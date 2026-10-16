#!/bin/bash
# EXPLORE rounds 10-11: K = ${KK:-4} completions of each LP binder's 2-ball (centre 7), 3 at a time, CAP seconds each.
# usage: [KK=5] [FIX=fix4.txt] loop/b7/runk4.sh MAXL CAP
cd "$(dirname "$0")"; M=$1; CAP=$2; KK=${KK:-4}
xargs -P 3 -I{} bash -c 'f={}; n=${f%%:*}; timeout '"$CAP"' nice -n 5 ./defectb7 ../g9/defect_tables8.txt 7 '"$KK"' 1 '"$M"' 1000000000 60 "" "$f" > k'"$KK"'_m'"$M"'_$n.out 2> k'"$KK"'_m'"$M"'_$n.err; echo "$n exit $?" >> k'"$KK"'_m'"$M"'.done' < ${FIX:-fix.txt}
echo all done >> k${KK}_m$M.done
