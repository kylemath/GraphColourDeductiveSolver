#!/bin/zsh
# Restart w17L_5 (f7_.556858_.56.67., 8 h cap, nice 20) once the xcap=1000 test (pid 9796) ends and at most 15
# runnable jobs besides k19 remain (core counting, 18 Oct).
cd "$(dirname $0)"; CF=../../../../studio15/cfast
while kill -0 9796 2>/dev/null; do python3 -c 'import time; time.sleep(120)'; done
until [ $(ps -axo state= | grep -c '^R') -le 16 ]; do python3 -c 'import time; time.sleep(120)'; done
sed -n 5p w17.txt > w17L_5.in; s=$(date +%s)
nice -n 20 perl -e 'alarm shift; exec @ARGV' 28800 $CF w17L_5.in --search --limit 1 > w17L_5.cfast 2>&1; rc=$?
echo "$(date '+%m-%d %H:%M') w17L_5 $(cut -d' ' -f1 w17L_5.in) rc=$rc $(( $(date +%s)-s ))s $(grep -q C-REDUCIBLE w17L_5.cfast && echo C || (grep -q 'search |X|' w17L_5.cfast && echo neither || echo TIMEOUT)) (restart)" >> n1.log
