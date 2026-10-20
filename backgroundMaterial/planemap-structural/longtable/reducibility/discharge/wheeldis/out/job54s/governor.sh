#!/bin/zsh
# Job 54s slot governor: NW = 15 - (CXRing lean workers) - (other Job 52 runners) - (j31r2), at least 3; not raised while
# free memory < 22 GB. Stops when A.DONE exists.
H=${0:a:h}
while [ ! -f $H/A.DONE ]; do
  ncx=$(ps -axo comm= | grep -c 'toolchains/.*/bin/lean$')
  njb=$(ps -axo command= | grep -c '[j]ob52.py')
  nj31=$(ps -axo command= | grep -c '[w]lp3r6.py tag=j31r2')
  fr=$(vm_stat | awk '/Pages free/ {gsub("\\.","",$3); print int($3*16384/1073741824)}')
  cur=$(cat $H/NW.txt 2>/dev/null || echo 3)
  n=$((15 - ncx - njb - nj31)); [ $n -lt 3 ] && n=3
  [ $n -gt $cur ] && [ $fr -lt 22 ] && n=$cur
  [ $n -ne $cur ] && { echo $n > $H/NW.txt; echo "$(date -u +%H:%M) NW $cur -> $n (lean $ncx, job52 $njb, j31r2 $nj31, free ${fr} GB)" >> $H/governor.log; }
  sleep 60
done
