#!/bin/sh
cd "$(dirname "$0")"
sleep 60; while pgrep -f jobbk_run.sh > /dev/null; do sleep 30; done
nice -n 10 python3 jobbj_c.py 600 > jobbj-c-search.log 2>&1
