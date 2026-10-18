#!/bin/zsh
# Job 31 first solve: after the rzero validation converges at 7/27, run the 6-relay on the 1/4 registry.
cd "$(dirname $0)/../.."
until grep -q "^# wlp3x" out/job31/r6zero.log; do python3 -c 'import time; time.sleep(120)'; done
if ! grep -q "t\* = 0.259259" out/job31/r6zero.log; then echo "rzero did not reproduce 7/27; first solve NOT started" > out/job31/run31.status; exit 1; fi
echo "rzero reproduced 7/27; first solve started $(date -u '+%m-%d %H:%MZ')" > out/job31/run31.status
until [ $(ps -axo %cpu=,command= | awk '$1>40' | wc -l) -le 15 ]; do python3 -c "import time; time.sleep(120)"; done
WLP3X_DEF=1 WLP_SEPF=1 nice -n 19 python3 wlp3r6.py tag=j31 warm=out/wlp3x_j30A_x_rows.txt $(cat loop/studio/opus_check/argsNoT_local.txt) > out/job31/j31.log 2>&1
echo done > out/job31/j31.DONE
