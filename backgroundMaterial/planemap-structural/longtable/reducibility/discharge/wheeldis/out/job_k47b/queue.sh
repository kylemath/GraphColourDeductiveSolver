#!/bin/zsh
# k47b starts when k47 has finished (A.DONE) or stopped at a kill (KILL non-empty and no k47 windows active)
H=${0:A:h}; K=$H/../job_k47
until [ -f $K/A.DONE ]; do sleep 30; done
cd $H; echo 5 > NW.txt; STOPKILL=1 python3 drive_k47b.py win52_7_9656775_5556655_todo.txt > drive.log 2>&1
