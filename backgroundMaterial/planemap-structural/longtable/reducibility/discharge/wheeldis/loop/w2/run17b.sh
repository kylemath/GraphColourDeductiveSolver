#!/bin/bash
# round 17 rerun with dfast18 (dfast caps at ring 16): one line at a time, timed
cd "$(dirname "$0")"
: > win17.out
while read -r line; do s=$(date +%s); echo "$line" > z17.in; nice -n 5 ../../bin/dfast18 z17.in >> win17.out 2>&1; echo "$(echo $line|cut -d' ' -f1) $(( $(date +%s)-s ))s" >> run17b.times; done < win17.txt
rm -f z17.in; echo "win17 (dfast18): D $(grep -c D=true win17.out) of $(wc -l < win17.txt)" > run17b.log
kill -CONT 17301 2>/dev/null
