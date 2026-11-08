#!/bin/zsh
# HDK5d_B1: after the K5b jobs (out/job_K3CHK9/LEANDONE), side by side with the K5c jobs: HDK5DB1, HDK5DB1V00, HDK5DB1All
cd $(dirname $0)
until [ -f ../job_K3CHK9/LEANDONE ]; do sleep 60; done
cd lean; ./run.sh HDK5DB1; ./run.sh HDK5DB1V00; ./run.sh HDK5DB1All; echo ALLDONE >> status.txt
