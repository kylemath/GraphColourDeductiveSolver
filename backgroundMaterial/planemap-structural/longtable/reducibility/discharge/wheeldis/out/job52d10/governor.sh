#!/bin/zsh
# job52d10 slot governor (copy of nl54e): NW = 15 - Lean workers - active nl54d windows - j31r2 - s33z checker, at least 0; not raised while
# free memory < 22 GB. nl54d keeps its own NW (11); its slots pass here as it drains, and s33z's slot when s33z ends.
H=${0:a:h}
while [ ! -f $H/A.DONE ]; do
  ncx=$(ps -axo comm= | grep -c 'toolchains/.*/bin/lean$')
  n4d=$(ps -axo command= | grep -c 'job54d/tmp[^ ]*\.in$')
  nj31=$(ps -axo command= | grep -c '[w]lp3r6.py tag=j31r2')
  ns33=$(ps -axo command= | grep -c '[s]t21_check.py')
  fr=$(vm_stat | awk '/Pages free/ {gsub("\\.","",$3); print int($3*16384/1073741824)}')
  cur=$(cat $H/NW.txt 2>/dev/null || echo 0)
  n=$((15 - ncx - n4d - nj31 - ns33)); [ $n -lt 0 ] && n=0
  [ $n -gt $cur ] && [ $fr -lt 22 ] && n=$cur
  [ $n -ne $cur ] && { echo $n > $H/NW.txt; echo "$(date -u +%H:%M) NW $cur -> $n (lean $ncx, nl54d $n4d, j31r2 $nj31, s33z $ns33, free ${fr} GB)" >> $H/governor.log; }
  sleep 30
done
