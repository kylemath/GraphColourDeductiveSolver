#!/bin/zsh
R=/tmp/beat_633_repro; cd $R
for e in new old; do echo "== engine $e $(date -u +%H:%M:%S)"; nice -n 15 ./bin/fast_compress_$e --mode sep --pool $R/data/pool_input.txt --rules $R/data/synth_rules_588.txt --active $R/data/synth_active_588.txt --out $R/sep_588_$e.jsonl --cert-dir $R/certdir_$e --threads 3 > $R/run_$e.log 2>&1; echo "exit $?"; done
echo "== NC (new engine, 598 rules) $(date -u +%H:%M:%S)"; nice -n 15 ./bin/fast_compress_new --mode sep --pool $R/data/pool_input.txt --rules $R/data/synth_rules_598.txt --active $R/data/synth_active_588.txt --out $R/sep_nc.jsonl --cert-dir $R/certdir_nc --threads 3 > $R/run_nc.log 2>&1; echo "exit $?"
echo ST130DONE $(date -u +%H:%M:%S)
