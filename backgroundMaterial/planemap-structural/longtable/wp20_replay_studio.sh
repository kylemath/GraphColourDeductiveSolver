#!/bin/bash
# Independent replay of WP20 P1 (order 25, every graph) on a second machine, as 254 shards of 100 graphs, with the
# unchanged producer and declaration. The result is compared with the first machine by content digest, so the
# ~100 MB output need not be shipped: after it finishes run
#   python3 wp_compare_outputs.py digest wp20/replay-P1-m5-25.json > wp20/replay/DIGEST.json
# and compare it with the digest of the original merged output (same --block 2539).
# Idempotent and resumable. Start detached:  python3 wp_launch.py start wp20replay --dir wp20/replay -- bash wp20_replay_studio.sh
cd "$(dirname "$0")" || exit 1
mkdir -p wp20/replay
LOG=wp20/replay/pipeline.log
say() { echo "$(date '+%F %T') $*" >> "$LOG"; }
fail() { say "FAILED: $*"; exit 1; }
W=${WP_WORKERS:-16}
shasum -a 256 -c wp21/PACKAGE-SHA256SUMS >> "$LOG" 2>&1 || fail "package hashes differ; do not run"
[ "$(shasum -a 256 wp20/input-m5-25.txt | cut -d' ' -f1)" = "92e482edefb9ff4c5fbb77b2121366b2c3a88cf8001fecafa1ae29025e60d989" ] || fail "order-25 input hash differs"
if [ ! -s wp20/replay-P1-m5-25.json ]; then
  [ -s wp20/replay-run/plan.json ] || python3 wp_shard_runner.py plan wp20/replay-run --mode graphs --input wp20/input-m5-25.txt \
      --decl WP20-D1-declaration.md --wp WP20 --phase P1 --order 25 --shard-size 100 --cpu-cap 216000 --timeout 14400 --max-attempts 3 >> "$LOG" 2>&1 || fail "plan"
  say "replay run start (workers $W)"
  python3 wp_shard_runner.py run wp20/replay-run --workers $W >> wp20/replay/run.log 2>&1
  say "replay run ended (exit $?): $(python3 wp_shard_runner.py status wp20/replay-run 2>&1 | tail -1 | cut -c1-200)"
  python3 wp_shard_runner.py merge wp20/replay-run wp20/replay-P1-m5-25.json >> "$LOG" 2>&1 || fail "replay not complete: inconclusive, not merged"
fi
python3 wp_compare_outputs.py digest wp20/replay-P1-m5-25.json > wp20/replay/DIGEST.json 2>> "$LOG"
say "REPLAY DONE; digest in wp20/replay/DIGEST.json"
