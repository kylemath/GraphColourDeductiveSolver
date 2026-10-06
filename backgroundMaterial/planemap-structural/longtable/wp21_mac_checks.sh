#!/bin/bash
# Independent checks, on the machine that did NOT produce them, of WP21 phase A and B outputs that arrived from the
# other machine: the subset-rule check (needs the full order-26 list), then the sharded checker over every graph.
# Run after wp21/A-m5-26.json, wp21/B.json and wp21/B-evaluated.txt are in place. Idempotent and resumable.
cd "$(dirname "$0")" || exit 1
mkdir -p wp21/mac-check
LOG=wp21/mac-check/checks.log
say() { echo "$(date '+%F %T') $*" >> "$LOG"; }
fail() { say "FAILED: $*"; exit 1; }
FULLSHA=88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8
shasum -a 256 -c wp21/PACKAGE-SHA256SUMS >> "$LOG" 2>&1 || fail "package hashes differ"
[ -s wp21/full-m5-26.txt ] || { [ -s wp21/full-m5-26.txt.hold ] && mv wp21/full-m5-26.txt.hold wp21/full-m5-26.txt; }
[ "$(shasum -a 256 wp21/full-m5-26.txt | cut -d' ' -f1)" = "$FULLSHA" ] || fail "full order-26 list missing or hash differs"
[ -s wp21/A-m5-26.json ] && [ -s wp21/B.json ] && [ -s wp21/B-evaluated.txt ] || fail "phase A/B outputs not present"
python3 d1_check21.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md --range 0 0 --subset-of wp21/full-m5-26.txt --full-sha $FULLSHA > wp21/mac-check/A-subset.log 2>&1
grep -q "subset rule verified" wp21/mac-check/A-subset.log || fail "phase-A subset rule: see wp21/mac-check/A-subset.log"
python3 wp_check_shards.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md --ledger-dir wp21/mac-check/A-ledger --range-size 200 --workers ${WP_WORKERS:-14} --timeout 1800 --retries 2 > wp21/mac-check/A-check.log 2>&1
tail -1 wp21/mac-check/A-check.log | grep -q "^CHECK OK" || fail "phase A: $(tail -1 wp21/mac-check/A-check.log)"
say "phase A: subset rule verified and sharded check OK"
python3 wp_check_shards.py wp21/B.json wp21/B-evaluated.txt WP21-declaration.md --ledger-dir wp21/mac-check/B-ledger --range-size 200 --workers ${WP_WORKERS:-14} --timeout 1800 --retries 2 > wp21/mac-check/B-check.log 2>&1
tail -1 wp21/mac-check/B-check.log | grep -q "^CHECK OK" || fail "phase B: $(tail -1 wp21/mac-check/B-check.log)"
say "phase B: sharded check OK"
python3 wp_report.py wp21/A-m5-26.json --title "WP21 phase A (order 26 sample)" > wp21/mac-check/A-report-numbers.md 2>> "$LOG"
python3 wp_report.py wp21/B.json --title "WP21 phase B (order 26 adversarial search)" > wp21/mac-check/B-report-numbers.md 2>> "$LOG"
say "MAC CHECKS DONE"
