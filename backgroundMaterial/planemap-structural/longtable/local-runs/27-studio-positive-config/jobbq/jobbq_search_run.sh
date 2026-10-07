#!/bin/sh
cd "$(dirname "$0")"
sleep 30; while pgrep -f "jobbq_run.sh" > /dev/null; do sleep 30; done
nice -n 10 python3 jobbq_search.py 500 > jobbq-search.log 2>&1
