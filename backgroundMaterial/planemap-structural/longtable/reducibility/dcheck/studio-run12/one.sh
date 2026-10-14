#!/bin/zsh
cd "$(dirname $0)/.."
s=$(date +%s); nice -n 10 lake build $1 > studio-run12/$1.log 2>&1; rc=$?
echo "$1 rc=$rc $(( $(date +%s) - s ))s" >> studio-run12/timings.txt
