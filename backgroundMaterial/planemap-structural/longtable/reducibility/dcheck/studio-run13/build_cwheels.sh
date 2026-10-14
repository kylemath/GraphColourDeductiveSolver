#!/bin/zsh
# Job 21: build CWheels once the 47-key dfast18 parts are all done (49 D= lines), nice 10
cd "$(dirname $0)/.."
until [ $(cat ../discharge/studio14b/part*.out 2>/dev/null | grep -c D=) -ge 49 ]; do sleep 60; done
s=$(date +%s); nice -n 10 lake build CWheels > studio-run13/cwheels.log 2>&1; echo "rc=$? $(( $(date +%s)-s ))s" > studio-run13/cwheels.done
