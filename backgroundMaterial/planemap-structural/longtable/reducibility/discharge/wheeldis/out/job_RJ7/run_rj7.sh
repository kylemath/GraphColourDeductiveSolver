#!/bin/zsh
# RJ7 full audit (Studio): README "How to run" loop, nice 20, -P lanes
cd ~/studio_rj7/audit/work
for g in d7_w6 d8_w6 d9_w6 "d7_w7 1" "d7_w7 -1" "d8_w7 1" "d8_w7 -1"; do
  for k in 0 1 2 3 4 5 6 7; do echo "$g part=$k/8"; done
done | xargs -P ${P:-7} -I{} sh -c 'nice -n 20 python3 -I -B ../scripts/audit_any.py {} > "log_$(echo {} | tr " /=" "___").txt" 2>&1'
echo RJ7DONE > RJ7DONE
