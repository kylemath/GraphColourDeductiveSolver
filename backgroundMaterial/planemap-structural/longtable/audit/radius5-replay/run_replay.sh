#!/bin/bash
# Audit radius-5 replay: one command. Run from the repository root on the Studio (never on the MacBook).
#   bash backgroundMaterial/planemap-structural/longtable/audit/radius5-replay/run_replay.sh <outdir>
# One Python process at a time, nice 10, 10 CPU-minute cap per step. Stops if the self-test fails.
set -u
R=backgroundMaterial/planemap-structural/longtable/audit/radius5-replay/replay_radius.py
C=backgroundMaterial/planemap-structural/studiointel/run-C-2026-10-06/cert
O=${1:?usage: run_replay.sh OUTDIR}; mkdir -p "$O"
date '+start %F %T %Z' > "$O/times.txt"
git rev-parse HEAD > "$O/commit.txt"
shasum -a 256 "$R" $C/91a307d1852a1764.graph.json $C/91a307d1852a1764.hole22.state.json \
  $C/8a23ee3ec7b2bb33.graph.json $C/8a23ee3ec7b2bb33.hole23.state.json \
  $C/62661a3f304f4caa.graph.json $C/62661a3f304f4caa.hole23.state.json \
  $C/80b930d1540e4ee3.graph.json $C/80b930d1540e4ee3.hole23.state.json > "$O/shasums.txt"
run() { local name=$1; shift; ( ulimit -t 600; nice -n 10 python3 "$R" "$@" ) > "$O/$name.json" 2> "$O/$name.err"; echo "$name exit $?" >> "$O/times.txt"; }
run selftest selftest
if ! grep -q '"selftest_pass": true' "$O/selftest.json"; then echo "SELFTEST FAILED: stop" >> "$O/times.txt"; exit 1; fi
run cert-91a307-h22 cert $C/91a307d1852a1764.graph.json 22 $C/91a307d1852a1764.hole22.state.json 5
run cert-8a23ee-h23 cert $C/8a23ee3ec7b2bb33.graph.json 23 $C/8a23ee3ec7b2bb33.hole23.state.json 5
run cert-62661a-h23 cert $C/62661a3f304f4caa.graph.json 23 $C/62661a3f304f4caa.hole23.state.json 5
run cert-80b930-h23 cert $C/80b930d1540e4ee3.graph.json 23 $C/80b930d1540e4ee3.hole23.state.json 5
run control-91a307-expect6 cert $C/91a307d1852a1764.graph.json 22 $C/91a307d1852a1764.hole22.state.json 6
run iso-hole23 iso $C/8a23ee3ec7b2bb33.graph.json 23 $C/62661a3f304f4caa.graph.json 23
date '+end %F %T %Z' >> "$O/times.txt"
grep -h '"pass"' "$O"/cert-*.json "$O"/control-*.json | sed 's/.*"pass": \([a-z]*\).*/pass=\1/' >> "$O/times.txt"
