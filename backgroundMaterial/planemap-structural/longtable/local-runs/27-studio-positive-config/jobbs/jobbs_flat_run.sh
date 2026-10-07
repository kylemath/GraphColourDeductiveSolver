#!/bin/sh
cd "$(dirname "$0")"
sleep 60; while pgrep -f "jobbj_c.py|jobbj_c_run.sh" > /dev/null; do sleep 30; done
nice -n 10 python3 jobbs_flat.py > jobbs-flat.log 2>&1
