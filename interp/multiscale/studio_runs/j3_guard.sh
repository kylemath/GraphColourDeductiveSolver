#!/bin/zsh
# J3 guard (coordinator 22 Oct 22:35Z): stop a taskB run past 3 h or 32 GB (python + its bfs child); keep 20 GB free overall
R=${0:A:h}
while true; do
  alive=0
  for L in 14 15 16 17 18; do
    p=$(cat $R/J3_L$L.pid 2>/dev/null); [ -z "$p" ] && continue; ps -p $p >/dev/null 2>&1 || continue; alive=1
    et=$(ps -o etimes= -p $p 2>/dev/null | tr -d ' '); [ -z "$et" ] && et=$(ps -o etime= -p $p | awk -F'[-:]' '{n=NF; s=$n+60*$(n-1); if(n>=3)s+=3600*$(n-2); if(n==4)s+=86400*$1; print s}')
    kb=$(( $(ps -o rss= -p $p) + $(for c in $(pgrep -P $p); do ps -o rss= -p $c; done | awk '{s+=$1} END{print s+0}') ))
    if [ $et -gt 10800 ] || [ $kb -gt 33554432 ]; then pkill -P $p; kill $p; echo "$(date -u +%H:%MZ) stopped L$L: elapsed ${et}s rss ${kb}KB" >> $R/j3_guard.log; fi
  done
  free=$(vm_stat | awk '/Pages free/{print int($3*16384/2^30)}')
  if [ $free -lt 20 ]; then big=0; bp=""; for L in 14 15 16 17 18; do p=$(cat $R/J3_L$L.pid); ps -p $p >/dev/null 2>&1 || continue; k=$(( $(ps -o rss= -p $p) + $(for c in $(pgrep -P $p); do ps -o rss= -p $c; done | awk '{s+=$1} END{print s+0}') )); [ $k -gt $big ] && { big=$k; bp=$p; bl=$L; }; done; [ -n "$bp" ] && { pkill -P $bp; kill $bp; echo "$(date -u +%H:%MZ) free ${free}GB < 20: stopped L$bl (rss ${big}KB)" >> $R/j3_guard.log; }; fi
  [ $alive = 0 ] && exit 0
  sleep 60
done
