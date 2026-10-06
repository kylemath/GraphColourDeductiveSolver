#!/bin/bash
# WP21 version 2 pipeline: sharded runner + sharded independent checker. Idempotent and resumable.
# Waits until the WP20 pipeline (wp_pipeline.sh) has finished P1, so the CPUs are free, then:
#   phase A (order-26 sample) -> subset-rule check -> sharded check -> report numbers
#   -> phase-B seeds -> phase B (chains) -> sharded check -> report numbers.
# Start detached:  python3 wp_launch.py start wp21pipe --dir wp21 -- bash wp21_pipeline.sh
cd "$(dirname "$0")" || exit 1
LOG=wp21/pipeline.log
say() { echo "$(date '+%F %T') $*" >> "$LOG"; }
fail() { say "FAILED: $*"; exit 1; }
mkdir -p wp21
W=12
FULLSHA=88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8
SELSHA=24e381cbc4a0a65092fb2689f57bbb8163fad2d17573bf552a2ffcc42964ba31

# ---- wait for the WP20 pipeline to finish completely (it holds the CPUs for P1)
while pgrep -f "wp_pipeline.sh" > /dev/null; do sleep 60; done
grep -q "P1 report numbers written" wp20/pipeline.log 2>/dev/null || fail "the WP20 pipeline ended without writing the P1 report numbers; see wp20/pipeline.log"
say "WP20 pipeline finished; starting WP21 version 2"

# ---- inputs
[ -s wp21/full-m5-26.txt ] || { [ -s wp21/full-m5-26.txt.hold ] && mv wp21/full-m5-26.txt.hold wp21/full-m5-26.txt; }
[ "$(shasum -a 256 wp21/full-m5-26.txt | cut -d' ' -f1)" = "$FULLSHA" ] || fail "full order-26 list hash differs"
[ "$(shasum -a 256 wp21/sample-A-m5-26.txt | cut -d' ' -f1)" = "$SELSHA" ] || fail "phase-A selection hash differs"

# ---- phase A
if [ ! -s wp21/A-m5-26.json ]; then
  [ -s wp21/A-run/plan.json ] || python3 wp_shard_runner.py plan wp21/A-run --mode graphs --input wp21/sample-A-m5-26.txt \
      --decl WP21-declaration.md --wp WP20 --phase A --order 26 --shard-size 100 \
      --cpu-cap 43200 --timeout 14400 --max-attempts 3 >> "$LOG" 2>&1 || fail "plan phase A"
  say "phase A run start"
  python3 wp_shard_runner.py run wp21/A-run --workers $W >> wp21/A-run.log 2>&1
  say "phase A run ended (exit $?): $(python3 wp_shard_runner.py status wp21/A-run 2>&1 | tail -1 | cut -c1-200)"
  python3 wp_shard_runner.py merge wp21/A-run wp21/A-m5-26.json >> "$LOG" 2>&1 || fail "phase A is not complete (partial, capped or failed): inconclusive, not merged"
fi
python3 d1_check21.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md --range 0 0 \
    --subset-of wp21/full-m5-26.txt --full-sha $FULLSHA > wp21/A-subset-check.log 2>&1
grep -q "subset rule verified" wp21/A-subset-check.log || fail "phase-A subset rule not verified; see wp21/A-subset-check.log"
python3 wp_check_shards.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md \
    --ledger-dir wp21/A-check-ledger --range-size 200 --workers 14 --timeout 1800 --retries 2 > wp21/A-check.log 2>&1
tail -1 wp21/A-check.log | grep -q "^CHECK OK" || fail "phase A check: $(tail -1 wp21/A-check.log)"
say "phase A check OK: $(tail -1 wp21/A-check.log)"
python3 wp_report.py wp21/A-m5-26.json --title "WP21 phase A (order 26, hash-split sample)" > wp21/A-report-numbers.md 2>> "$LOG"
say "phase A report numbers written"

# ---- phase B
python3 wp21_seeds.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt wp21/seeds-B.txt >> "$LOG" 2>&1 || fail "seeds"
if [ ! -s wp21/B.json ]; then
  [ -s wp21/B-run/plan.json ] || python3 wp_shard_runner.py plan wp21/B-run --mode chains --seeds wp21/seeds-B.txt --chains 12 \
      --steps 400 --seed-tag WP21 --chain-cpu 6000 --cpu-cap 86400 --timeout 43200 --max-attempts 2 >> "$LOG" 2>&1 || fail "plan phase B"
  say "phase B run start"
  python3 wp_shard_runner.py run wp21/B-run --workers $W >> wp21/B-run.log 2>&1
  say "phase B run ended (exit $?): $(python3 wp_shard_runner.py status wp21/B-run 2>&1 | tail -1 | cut -c1-200)"
  python3 wp_shard_runner.py merge wp21/B-run wp21/B >> "$LOG" 2>&1 || fail "phase B is not complete (partial, capped or failed): inconclusive, not merged"
fi
python3 wp_check_shards.py wp21/B.json wp21/B-evaluated.txt WP21-declaration.md \
    --ledger-dir wp21/B-check-ledger --range-size 200 --workers 14 --timeout 1800 --retries 2 > wp21/B-check.log 2>&1
tail -1 wp21/B-check.log | grep -q "^CHECK OK" || fail "phase B check: $(tail -1 wp21/B-check.log)"
say "phase B check OK: $(tail -1 wp21/B-check.log)"
python3 wp_report.py wp21/B.json --title "WP21 phase B (order 26, adversarial search)" > wp21/B-report-numbers.md 2>> "$LOG"
say "ALL DONE (WP21 version 2)"
