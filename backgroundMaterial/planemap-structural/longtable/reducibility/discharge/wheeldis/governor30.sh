#!/bin/zsh
# Alarm-only governor (18 Oct 10:5xZ; replaces governor28.sh, whose SIGSTOP pauses were not delivered to nohup-started
# jobs). Every 10 min: log k19's CPU share over the interval. If it is below 92% for two readings in a row, terminate
# the newest low-priority job (cfast other than R17a/R17b, dfast18, kc, lean) and log it for re-queueing. Never
# touches k19, R17a, R17b or run A (tag=j30A). Log: out/job28/governor.log.
cd "$(dirname $0)"; LOG=out/job28/governor.log; K19=${1:-7776}
secs() { ps -o time= -p $K19 | awk -F'[:.]' '{ if (NF==4) print $1*3600+$2*60+$3; else print $1*60+$2 }'; }
low=0
while kill -0 $K19 2>/dev/null; do
  a=$(secs); t0=$(date +%s); python3 -c 'import time; time.sleep(600)'; b=$(secs); t1=$(date +%s)
  sh=$(( (b - a) * 100 / (t1 - t0) )); nr=$(ps -axo state= | grep -c '^R')
  echo "$(date '+%m-%d %H:%M') k19 ${sh}% runnable $nr" >> $LOG
  if [ $sh -lt 92 ]; then low=$((low + 1)); else low=0; fi
  if [ $low -ge 2 ]; then
    v=$(ps -axo pid=,etime=,command= | awk '($0 ~ /studio15\/cfast/ && $0 !~ /R17[ab]\.in/) || $0 ~ /dfast18 / || $0 ~ /loop\/kc\/kc / || $0 ~ /bin\/lean / {print}' \
        | grep -v "tag=j30A" | python3 -c 'import sys
def s(e):
    d=0
    if "-" in e: d,e=e.split("-"); d=int(d)
    p=[int(x) for x in e.split(":")]
    while len(p)<3: p=[0]+p
    return d*86400+p[0]*3600+p[1]*60+p[2]
L=[l.split(None,2) for l in sys.stdin if l.strip()]
L.sort(key=lambda x:s(x[1]))
print(L[0][0]+" "+L[0][2][:160] if L else "")')
    if [ -n "$v" ]; then kill -TERM ${v%% *}; echo "$(date '+%m-%d %H:%M') k19 below 92% twice: terminated ${v} (re-queue it)" >> $LOG; fi
    low=0
  fi
done
echo "$(date '+%m-%d %H:%M') k19 ended" >> $LOG
