#!/bin/bash
# EXPLORE round 33: k19 (studio14b/part00.txt) on one core, Gauss-Seidel, checkpointed (resume by rerunning).
cd "$(dirname "$0")"
python3 runrss.py k19_kc.out k19_kc.err ./kc -v -c k19.ckpt -t 6300 k19.txt
