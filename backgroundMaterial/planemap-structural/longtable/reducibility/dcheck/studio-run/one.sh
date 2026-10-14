#!/bin/zsh
# build one theorem library, log and time it
cd "$(dirname $0)/.."
s=$(date +%s); nice -n 10 lake build $1 > studio-run/$1.log 2>&1; rc=$?
echo "$1 rc=$rc $(( $(date +%s) - s ))s" >> studio-run/timings.txt
