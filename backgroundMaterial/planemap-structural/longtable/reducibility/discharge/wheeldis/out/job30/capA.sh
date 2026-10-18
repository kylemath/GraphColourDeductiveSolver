#!/bin/zsh
# Long Table 17:16Z: cap run A at iteration 20 (stop it, keep its log and last row dump).
cd "$(dirname $0)/../.."
until grep -q "^iter 20 " out/job30/j30A.log || ! kill -0 22240 2>/dev/null; do python3 -c 'import time; time.sleep(120)'; done
if kill -0 22240 2>/dev/null; then pkill -P 22240; kill 22240; echo "$(date -u '+%m-%d %H:%MZ') run A stopped at its iteration-20 cap" >> out/job30/capA.log; fi
