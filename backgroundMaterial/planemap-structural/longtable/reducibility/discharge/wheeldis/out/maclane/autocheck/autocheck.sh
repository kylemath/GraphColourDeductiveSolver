#!/bin/bash
# Studio auto-check daemon (coordinator 13:59Z policy). Detached; state in files in this folder.
# - T0.txt = current best sound upper. Trigger: t < T0 * 0.9975.
# - At most one auto-check at a time. Candidates are outbox/upper points of the live lane families below the trigger,
#   lowest t first. A point is checked only if it is still below the trigger when its turn comes.
# - Each point is checked once (checked.txt). A "_tight" twin of a checked point counts as checked.
# - PASS (main RESULT: FEASIBLE): T0 := that point's t (re-armed automatically). log.txt gets "PASS ..." / "FAIL ...".
# - ST numbers come from next_st.txt.
# - queue.txt: extra points from relays, one line "NN t script arg..." (own ST number and check script). Relay entries need only t < T0
#   (not the 0.9975 trigger) and run when they are the lowest candidate; entries at or above T0 wait. Done entries go to queue_done.txt.
A=$(cd "$(dirname "$0")" && pwd); M=$(dirname "$A"); W=$(cd "$M/../.." && pwd)
O=$HOME/maclane/maclane-k86/outbox/upper/POINTS.txt
touch $A/checked.txt $A/log.txt
log(){ echo "$(date -u +%H:%M:%SZ) $*" >> $A/log.txt; }
script_for(){ case "$1" in
  K3l5r_k260) echo autost_mk6nz;;  K3l5r_k268) echo autost_mk7;;
  K3l5s_k260) echo autost_mk8nz;;  K3l5s_k268) echo autost_mk9;;
  K3l5t_k260) echo autost_mk10nz;; K3l5t_k268) echo autost_mk11;;
  K3l5u_k260) echo autost_mk12nz;; K3l5u_k268) echo autost_mk13;;
  K3l5v_k260) echo autost_mk14nz;; K3l5v_k268) echo autost_mk15;;
  *) echo "";; esac; }
log "start: T0 $(cat $A/T0.txt), trigger x0.9975, next ST $(cat $A/next_st.txt)"
judge(){ NN=$1; P=$2; T=$3; J=$W/out/job_ST$NN
    if grep -q '^RESULT: FEASIBLE' $J/main.out 2>/dev/null; then
      tn=$(grep -E '^RESULT' $J/tneg.out 2>/dev/null | cut -c1-40)
      new=$(awk -v a=$T -v b=$(cat $A/T0.txt) 'BEGIN{print (a+0 < b+0) ? a : b}')
      echo $new > $A/T0.txt
      log "PASS ST-$NN $P t=$T (tneg: $tn) commit $(grep -o 'commit [0-9a-f]*' $W/out/job_ST${NN}_run.log | tail -1); T0 -> $new, trigger $(awk -v a=$new 'BEGIN{printf "%.12f", a*0.9975}')"
    else
      log "FAIL ST-$NN $P t=$T: $(grep -E '^RESULT|refused' $J/main.out $W/out/job_ST${NN}_run.log 2>/dev/null | head -2 | cut -c1-120 | tr '\n' ' ')"
    fi; }
# ADOPT="NN POINT T": a check started by hand before the daemon; judge it when it ends
if [ -n "$ADOPT" ]; then set -- $ADOPT; echo "${2/_tight/}" >> $A/checked.txt; log "adopt ST-$1 $2 t=$3 (running)"
  while pgrep -f "autost_.*\.sh $1 " > /dev/null; do sleep 60; done; judge $1 $2 $3; fi
while true; do
  while pgrep -f 'maclane/autost_|bash autost_' > /dev/null; do sleep 60; done
  T0=$(cat $A/T0.txt); TR=$(awk -v a=$T0 'BEGIN{printf "%.12f", a*0.9975}')
  # pick the lowest unchecked candidate below the trigger
  P=""; F=""; T=""
  while read t name fam; do
    key=${name/_tight/}
    grep -qxF "$key" $A/checked.txt && continue
    [ -z "$(script_for $fam)" ] && continue
    P=$name; F=$fam; T=$t; break
  done < <(awk -v tr=$TR '$2+0 < tr+0 {print $2, $1, $4}' $O | sort -g)
  # relay queue: lowest pending entry below the trigger, if it beats the outbox candidate
  touch $A/queue.txt $A/queue_done.txt; Q=""
  while read qn qt qs qa; do
    grep -qx "$qn" $A/queue_done.txt && continue
    awk -v a=$qt -v b=$T0 'BEGIN{exit !(a+0 < b+0)}' || continue
    if [ -z "$Q" ] || awk -v a=$qt -v b=$QT 'BEGIN{exit !(a+0 < b+0)}'; then Q=$qn; QT=$qt; QS=$qs; QA=$qa; fi
  done < <(grep -v '^#' $A/queue.txt)
  if [ -n "$Q" ] && { [ -z "$P" ] || awk -v a=$QT -v b=$T 'BEGIN{exit !(a+0 <= b+0)}'; }; then
    echo $Q >> $A/queue_done.txt
    log "RUN ST-$Q (queue) $QS $QA t=$QT (trigger $TR, T0 $T0)"
    bash $M/$QS.sh $Q $QA > $W/out/job_ST${Q}_run.log 2>&1 < /dev/null
    judge $Q "$(echo $QA | awk '{print $1}' | xargs basename)" $QT
    continue
  fi
  if [ -n "$P" ]; then
    S=$(script_for $F); NN=$(cat $A/next_st.txt); echo $((NN+1)) > $A/next_st.txt
    echo "${P/_tight/}" >> $A/checked.txt
    log "RUN ST-$NN $S $P t=$T fam=$F (trigger $TR, T0 $T0)"
    bash $M/$S.sh $NN $P > $W/out/job_ST${NN}_run.log 2>&1 < /dev/null
    judge $NN $P $T
    continue
  fi
  m=$(vm_stat | awk '/free|inactive|speculative/{s+=$NF} END{print int(s*16384/1e9)}'); [ "$m" -lt 25 ] && log "LOWMEM $m GB (no new check started)"
  sleep 120
done
