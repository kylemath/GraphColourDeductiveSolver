#!/bin/zsh
# k47c starts when k47b has finished (A.DONE)
H=${0:A:h}; K=$H/../job_k47b
until [ -f $K/A.DONE ]; do sleep 30; done
cd $H; echo 3 > NW.txt; STOPKILL=1 python3 drive_k47c.py win52_7_7676655_6667656_todo.txt > drive.log 2>&1
