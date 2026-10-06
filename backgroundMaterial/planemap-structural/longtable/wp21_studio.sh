#!/bin/bash
# Mac Studio run of WP21 version 2: phase A -> sharded independent check -> seeds -> phase B -> sharded check.
# Idempotent and resumable (re-run the same command after any interruption). Needs no plantri.
# Start detached:  python3 wp_launch.py start wp21studio --dir wp21/studio -- bash wp21_studio.sh
cd "$(dirname "$0")" || exit 1
mkdir -p wp21/studio
LOG=wp21/studio/pipeline.log
say() { echo "$(date '+%F %T') $*" >> "$LOG"; }
fail() { say "FAILED: $*"; exit 1; }
W=${WP_WORKERS:-16}
shasum -a 256 -c wp21/PACKAGE-SHA256SUMS >> "$LOG" 2>&1 || fail "package hashes differ from the announced ones; do not run"
[ -s wp21/studio/RECORD.txt ] || {
  { echo "started: $(date '+%F %T %Z')"; echo "machine: $(uname -a)"; echo "cpu: $(sysctl -n machdep.cpu.brand_string 2>/dev/null)"
    echo "cores: $(sysctl -n hw.ncpu 2>/dev/null)"; echo "memory bytes: $(sysctl -n hw.memsize 2>/dev/null)"; echo "python: $(python3 --version 2>&1)"
    echo "git head: $(git rev-parse HEAD 2>/dev/null)"; echo "workers: $W"; } > wp21/studio/RECORD.txt; }
say "package hashes verified; WP21 version 2 on this machine; workers $W"

# ---------------- phase A
if [ ! -s wp21/A-m5-26.json ]; then
  [ -s wp21/A-run/plan.json ] || python3 wp_shard_runner.py plan wp21/A-run --mode graphs --input wp21/sample-A-m5-26.txt \
      --decl WP21-declaration.md --wp WP20 --phase A --order 26 --shard-size 100 --cpu-cap 43200 --timeout 14400 --max-attempts 3 >> "$LOG" 2>&1 || fail "plan A"
  say "phase A run start"
  python3 wp_shard_runner.py run wp21/A-run --workers $W >> wp21/studio/A-run.log 2>&1
  say "phase A run ended (exit $?): $(python3 wp_shard_runner.py status wp21/A-run 2>&1 | tail -1 | cut -c1-200)"
  python3 wp_shard_runner.py merge wp21/A-run wp21/A-m5-26.json >> "$LOG" 2>&1 || fail "phase A not complete (partial, capped or failed): inconclusive, not merged"
fi
python3 wp_check_shards.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md --ledger-dir wp21/studio/A-check-ledger \
    --range-size 200 --workers $W --timeout 1800 --retries 2 > wp21/studio/A-check.log 2>&1
tail -1 wp21/studio/A-check.log | grep -q "^CHECK OK" || fail "phase A sharded check: $(tail -1 wp21/studio/A-check.log)"
say "phase A sharded check OK (the subset-rule check needs the full order-26 list and is done on the other machine)"
python3 wp_report.py wp21/A-m5-26.json --title "WP21 phase A (order 26, hash-split sample), Mac Studio" > wp21/studio/A-report-numbers.md 2>> "$LOG"

# ---------------- phase B
python3 wp21_seeds.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt wp21/seeds-B.txt >> "$LOG" 2>&1 || fail "seeds"
if [ ! -s wp21/B.json ]; then
  [ -s wp21/B-run/plan.json ] || python3 wp_shard_runner.py plan wp21/B-run --mode chains --seeds wp21/seeds-B.txt --chains 12 --steps 400 \
      --seed-tag WP21 --chain-cpu 6000 --cpu-cap 86400 --timeout 43200 --max-attempts 2 >> "$LOG" 2>&1 || fail "plan B"
  say "phase B run start"
  python3 wp_shard_runner.py run wp21/B-run --workers 12 >> wp21/studio/B-run.log 2>&1
  say "phase B run ended (exit $?): $(python3 wp_shard_runner.py status wp21/B-run 2>&1 | tail -1 | cut -c1-200)"
  python3 wp_shard_runner.py merge wp21/B-run wp21/B >> "$LOG" 2>&1 || fail "phase B not complete (partial, capped or failed): inconclusive, not merged"
fi
python3 wp_check_shards.py wp21/B.json wp21/B-evaluated.txt WP21-declaration.md --ledger-dir wp21/studio/B-check-ledger \
    --range-size 200 --workers $W --timeout 1800 --retries 2 > wp21/studio/B-check.log 2>&1
tail -1 wp21/studio/B-check.log | grep -q "^CHECK OK" || fail "phase B sharded check: $(tail -1 wp21/studio/B-check.log)"
say "phase B sharded check OK"
python3 wp_report.py wp21/B.json --title "WP21 phase B (order 26, adversarial search), Mac Studio" > wp21/studio/B-report-numbers.md 2>> "$LOG"
{ echo "finished: $(date '+%F %T %Z')"; for f in wp21/A-m5-26.json wp21/B.json wp21/B-evaluated.txt wp21/B-log.json wp21/seeds-B.txt; do echo "$(shasum -a 256 $f | cut -d' ' -f1)  $f"; done; } >> wp21/studio/RECORD.txt
say "STUDIO WP21 DONE"
