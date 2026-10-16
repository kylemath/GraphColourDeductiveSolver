#!/bin/bash
# run dfast on a list file (name line per config), append verdicts to vcache.txt.  Usage: runlist.sh LIST OUT
B=$(dirname $(dirname $(dirname $(readlink -f $0))))/bin
nice -n 10 $B/dfast $1 > $2 2>&1
awk '/D=true/{print $1, "D", $2, "list"} /D=false/{print $1, "notD", $2, "list"}' $2 >> $(dirname $(readlink -f $0))/vcache.txt
