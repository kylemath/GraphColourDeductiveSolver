#!/bin/zsh
# Keep the ring-19 key (k19, studio14d) at >= ~92% of a core (coordinator, 15 Oct): pause the lowest-priority work when
# it drops, resume it when k19 is above 97% and there is room. Order of pausing: Job 27 (c) Lean (wheelcheck16), then
# the K = 4 defect searches (defectc). Log: out/job28/governor.log. Exits (resuming everything) when k19 ends.
cd "$(dirname $0)"; LOG=out/job28/governor.log
K19=${1:-42778}   # pid of studio14d's wheelcheck18 k19 (started 14 Oct 23:41)
secs() { ps -o time= -p $K19 | awk -F'[:.]' '{ if (NF==4) print $1*3600+$2*60+$3; else print $1*60+$2 }'; }
order=(wheelcheck16 defectc cfast dfast18)
while kill -0 $K19 2>/dev/null; do
  # Job 27/28 engines below nice 20 compete with k19 (nice 15): push them to 20
  for p in $(ps -axo pid=,nice=,comm= | awk '$3 ~ /(cfast|dfast18|sep3|defectc)$/ && $2 < 20 {print $1}'); do renice -n 20 -p $p >/dev/null 2>&1; done
  a=$(secs); sleep 120; b=$(secs); sh=$(( (b - a) * 100 / 120 ))
  ld=$(sysctl -n vm.loadavg | awk '{print int($2)}')
  if [ $sh -lt 92 ]; then
    for n in $order; do r=$(ps -axo pid=,state=,comm= | awk -v n=$n '$3 ~ n"$" && $2 !~ /T/ {print $1}'); if [ -n "$r" ]; then kill -STOP ${=r}; echo "$(date '+%m-%d %H:%M') k19 ${sh}% load $ld: paused $n" >> $LOG; break; fi; done
  elif [ $sh -ge 97 ] && [ $ld -lt 16 ]; then
    for n in ${(Oa)order}; do r=$(ps -axo pid=,state=,comm= | awk -v n=$n '$3 ~ n"$" && $2 ~ /T/ {print $1}'); if [ -n "$r" ]; then kill -CONT ${=r}; echo "$(date '+%m-%d %H:%M') k19 ${sh}% load $ld: resumed $n" >> $LOG; break; fi; done
  fi
  sleep 180
done
for n in $order; do r=$(ps -axo pid=,state=,comm= | awk -v n=$n '$3 ~ n"$" && $2 ~ /T/ {print $1}'); [ -n "$r" ] && kill -CONT ${=r}; done
echo "$(date '+%m-%d %H:%M') k19 ended; resumed all" >> $LOG
