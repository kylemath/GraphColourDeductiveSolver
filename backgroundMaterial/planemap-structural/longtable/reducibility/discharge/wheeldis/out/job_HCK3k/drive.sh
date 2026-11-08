#!/bin/zsh
# HCK3k: CK3K, K3KV00, K3KVAll (Fin 1), alongside the Lean queue
cd $(dirname $0)/lean; ./run.sh CK3K; ./run.sh K3KV00; ./run.sh K3KVAll; echo ALLDONE >> status.txt
