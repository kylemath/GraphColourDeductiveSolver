#!/bin/zsh
# HCK3i: moved up by the swarm lead (12:32Z) - build now, ahead of HA5b / HDK3b / HCK3C4 / HDK3c
cd $(dirname $0)/lean; ./run.sh K3IV00 & ./run.sh K3IV01 & wait; ./run.sh K3IVAll; echo ALLDONE >> status.txt
