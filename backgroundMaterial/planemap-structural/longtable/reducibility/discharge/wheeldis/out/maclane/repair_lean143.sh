#!/bin/bash
# Rerun Lean modules whose `time` wrapper got SIGTERM (status exit=143; the lean child survives as an orphan). Kills only that module's orphan lean (ppid 1).
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
while true; do
  for j in HCK3GX HDK3GX; do
    L=$W/out/job_$j/lean; [ -f $L/status.txt ] || continue
    for m in $(grep ' exit=143 ' $L/status.txt | cut -d' ' -f1 | sort -u); do
      last=$(grep "^$m exit=" $L/status.txt | tail -1)
      case "$last" in *" exit=143 "*) ;; *) continue ;; esac
      w=$(ps ax -o ppid,pid,command | grep 'bin/lean -o' | grep "/$m.olean" | grep -v grep)
      echo "$w" | awk '$1!=1 && NF>0{f=1} END{exit !f}' && continue      # a live wrapped run exists
      for p in $(echo "$w" | awk '$1==1{print $2}'); do kill $p; done
      echo "$(date -u +%H:%M:%SZ) rerun $j $m"
      (cd $L; nohup ./run.sh $m > /dev/null 2>&1 < /dev/null &)
    done
  done
  sleep 60
done
