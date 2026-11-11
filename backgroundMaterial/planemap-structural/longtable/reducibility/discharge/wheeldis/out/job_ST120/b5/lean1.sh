#!/bin/zsh
# run.sh for one module with the B5 Python exporter (if running) paused: one active process at a time
P=$(pgrep -f "py/export_cert.py" | tr '\n' ' ')
[ -n "$P" ] && kill -STOP ${=P}
$(dirname $0)/run.sh $1
[ -n "$P" ] && kill -CONT ${=P}
tail -1 $(dirname $0)/status.txt
