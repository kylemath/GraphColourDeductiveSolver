#!/bin/bash
# EXPLORE round 7 (exploratory): iterate the lone-five family.  Each step n: lone.py (pattern-free arrangements with more
# than d-6 lone fives, all known patterns + every u*.pat so far) -> ufree.py (receiver-free configurations of their lone
# fives, ring <= RMAX, arc <= ARC; if none is new, B-fixed sets of lone fives via bfix.py) -> dfast on the untested ones (2 processes) -> u<n>.pat.  Stops when no arrangement
# is left or no new configuration is written.  usage: loop/lone/iter.sh START STEPS RMAX ARC [DLIST]
cd "$(dirname "$0")"; W=../..; n=$1; last=$(( $1 + $2 )); R=$3; A=$4; DL=${5:-9,10,11,12,13,14,15}
while [ $n -lt $last ]; do
  P="$(cat pats0.txt | sed 's#\(c\?pat=\)#\1#g')"; for f in u*.pat b*.out; do [ -e "$f" ] && P="$P pat=loop/lone/$f"; done
  (cd $W && nice -n 5 python3 loop/lone/lone.py d=$DL many=300 out=loop/lone/lone$n.txt $P > /dev/null 2>&1)
  grep "^d=" lone$n.txt | sed "s/^/step $n: /" >> iter.log
  left=$(grep -c receiver lone$n.txt); [ "$left" = 0 ] && { echo "step $n: no arrangement left" >> iter.log; break; }
  python3 ufree.py u${n}all.txt $R $A lone$n.txt > /dev/null 2>&1
  cat u*.out 2>/dev/null | awk '{print $1}' | sort -u > tested.txt
  awk 'NR==FNR{t[$1]=1; next} !($1 in t)' tested.txt u${n}all.txt > u$n.txt; rm -f u${n}all.txt
  new=$(wc -l < u$n.txt); kind=u
  if [ "$new" = 0 ]; then   # no new receiver-free window: B-fixed (receiver at exact degree) sets of lone fives
    python3 bfix.py b$n.txt $R lone$n.txt > /dev/null 2>&1; rm -f u$n.txt; new=$(wc -l < b$n.txt); kind=b
  fi
  echo "step $n: $left arrangements, $new new $kind configurations (ring <= $R)" >> iter.log
  [ "$new" = 0 ] && break
  k=$kind$n; awk 'NR%2==1' $k.txt > $k.p0; awk 'NR%2==0' $k.txt > $k.p1
  nice -n 5 $W/bin/dfast $k.p0 > $k.p0.o 2>&1 & p0=$!
  nice -n 5 $W/bin/dfast $k.p1 > $k.p1.o 2>&1; wait $p0
  cat $k.p0.o $k.p1.o > $k.out; rm -f $k.p0 $k.p1 $k.p0.o $k.p1.o
  echo "step $n: D $(grep -c D=true $k.out) of $new" >> iter.log
  [ $kind = u ] && python3 ufree.py mkpat u$n.out u$n.pat 17 > /dev/null
  n=$((n + 1))
done
echo "done at step $n" >> iter.log
