#!/bin/sh
# full-cycle L1-normalised price certificates for every data file, 4 at a time
cd "$(dirname "$0")"
ls data/*_data.json | xargs -P 4 -I{} sh -c 'b=$(basename {} _data.json); nice -n 10 ../TrackQ/.venv/bin/python tr_lag.py {} --out out/full_$b.json > out/full_$b.log 2>&1'
