#!/bin/zsh
# HDK3b: after HA5b (hd and hc GLUEDONE), build HDK3B, HDK3BV00, HDK3BAll
cd $(dirname $0)
until grep -q GLUEDONE ../job_HA5b/hd/status.txt 2>/dev/null && grep -q GLUEDONE ../job_HA5b/hc/status.txt 2>/dev/null; do sleep 60; done
cd lean; ./run.sh HDK3B; ./run.sh HDK3BV00; ./run.sh HDK3BAll; echo ALLDONE >> status.txt
