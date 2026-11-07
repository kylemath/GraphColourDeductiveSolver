#!/bin/zsh
# HDK3c: after HCK3C4 (K3CHK4 lean GLUEDONE), build HDK3C, HDK3CV00, HDK3CAll
cd $(dirname $0)
until grep -q GLUEDONE ../job_K3CHK4/lean/status.txt 2>/dev/null; do sleep 60; done
cd lean; ./run.sh HDK3C; ./run.sh HDK3CV00; ./run.sh HDK3CAll; echo ALLDONE >> status.txt
