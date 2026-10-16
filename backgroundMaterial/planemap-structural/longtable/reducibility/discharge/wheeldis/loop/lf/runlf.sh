#!/bin/bash
# EXPLORE round 18 (H-LF): K = ${KK:-3} completions of each HARD28-like 2-ball (centre 7), letters 5..MAXL, 3 at a time.
# usage: [KK=3] [FM=FREEMAX] loop/lf/runlf.sh MAXL CAP   (FM: letters 5..FM on free slots of rings 2..K-1; default MAXL)
cd "$(dirname "$0")"; M=$1; CAP=$2; KK=${KK:-3}; FM=${FM:-$M}; T=k${KK}_m${M}_f${FM}
nl -nln -w1 -s' ' fix.txt | xargs -P 3 -L 1 bash -c 'n=$0; f=$1; timeout '"$CAP"' nice -n 5 ../b7/defectb9 ../g9/defect_tables9.txt 7 '"$KK"' 1 '"$M"' 1000000000 60 "" "$f" '"$FM"' > '"$T"'_$n.out 2> '"$T"'_$n.err; echo "$n $f exit $?" >> '"$T"'.done'
echo all done >> $T.done
