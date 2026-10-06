#!/bin/bash
# wait for the order<=26 census to finish, then run order 27 with the same driver
while kill -0 $(python3 -c "import json;print(json.load(open('$HOME/studio-scratch/census/census.pid'))['pid'])") 2>/dev/null; do sleep 30; done
MAX=27 bash $HOME/studio-scratch/census/run_census.sh
