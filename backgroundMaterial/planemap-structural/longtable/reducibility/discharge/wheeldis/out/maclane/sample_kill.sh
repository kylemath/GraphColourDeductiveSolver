#!/bin/bash
# Sample ps every 2 s, all minutes, keeping only young processes
while true; do
  m=$(date -u +%M); case $m in *) echo "=== $(date -u +%H:%M:%S)"; ps ax -o pid,ppid,etime,command | awk '{split($3,a,":"); if (NF>3 && length($3)<=5 && a[1]+0==0) print}' | cut -c1-150 ;; esac
  case $m in *) sleep 2;; *) sleep 20;; esac
done
