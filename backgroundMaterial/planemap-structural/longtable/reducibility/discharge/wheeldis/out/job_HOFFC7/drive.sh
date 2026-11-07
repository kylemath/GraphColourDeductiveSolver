#!/bin/zsh
# HOFFC7: after HDK3c (its lean/status.txt GLUEDONE): (A) OffcOcc (Opus 3731ad81, as is); (D) HDOF7 + HDOF7V00..51 + HDOF7All
cd $(dirname $0)
until grep -q GLUEDONE ../job_HDK3c/lean/status.txt 2>/dev/null; do sleep 60; done
cd lean; ./run.sh OffcOcc; echo ADONE >> status.txt
./run.sh HDOF7; for i in $(seq -f %02g 0 51); do ./run.sh HDOF7V$i; done; ./run.sh HDOF7All; echo ALLDONE >> status.txt
