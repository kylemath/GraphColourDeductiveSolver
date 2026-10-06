#!/bin/bash
# Unattended pipeline: WP20 P1 (chunked, resumable) -> merge -> independent check --all -> report numbers;
# then WP21 phase A -> check -> report; seeds; phase B -> check -> report.
# Idempotent: finished outputs are skipped. Stops at the first failure or checker mismatch.
# Start detached:  nohup setsid caffeinate -ims bash wp_pipeline.sh > /dev/null 2>&1 &
cd "$(dirname "$0")" || exit 1
LOG=wp20/pipeline.log
say() { echo "$(date '+%F %T') $*" >> "$LOG"; }
fail() { say "FAILED: $*"; exit 1; }
mkdir -p wp20/P1chunks wp21
W=12
N=25381; C=2539

# ---------------- WP20 P1 (rerun from scratch after the interruption; chunked so an interruption costs at most one chunk)
if [ ! -s wp20/P1-m5-25.json ]; then
  [ "$(shasum -a 256 wp20/input-m5-25.txt | cut -d' ' -f1)" = "92e482edefb9ff4c5fbb77b2121366b2c3a88cf8001fecafa1ae29025e60d989" ] || fail "order-25 input hash differs from the declared one"
  for k in 0 1 2 3 4 5 6 7 8 9; do
    out=wp20/P1chunks/P1-chunk-$k.json
    if [ ! -s "$out" ]; then
      say "P1 chunk $k start (graphs $((k*C)) .. $((k*C+C-1)))"
      python3 d1_confirm.py --phase P1 --order 25 --workers $W --out "$out.tmp" --input-file wp20/input-m5-25.txt \
              --first $((k*C)) --graph-limit $C > wp20/P1chunks/chunk-$k.log 2>&1 || fail "P1 chunk $k"
      mv "$out.tmp" "$out"
      say "P1 chunk $k done: $(tail -1 wp20/P1chunks/chunk-$k.log | cut -c1-200)"
    fi
  done
  python3 wp_merge.py wp20/P1-m5-25.json wp20/P1chunks/P1-chunk-*.json >> "$LOG" 2>&1 || fail "merge P1"
fi
if [ ! -s wp20/P1-check.log ] || ! grep -q "CHECK OK" wp20/P1-check.log; then
  say "P1 independent check --all start"
  python3 d1_check.py wp20/P1-m5-25.json wp20/input-m5-25.txt WP20-D1-declaration.md --all --workers 14 > wp20/P1-check.log 2>&1
  grep -q "CHECK OK" wp20/P1-check.log || fail "P1 check did not pass; see wp20/P1-check.log"
  say "P1 check OK"
fi
python3 wp_report.py wp20/P1-m5-25.json --title "WP20 P1 (order 25, every graph)" > wp20/P1-report-numbers.md 2>> "$LOG"
say "P1 report numbers written: wp20/P1-report-numbers.md"

# ---------------- WP21 phase A
FULL=wp21/full-m5-26.txt
[ "$(shasum -a 256 $FULL | cut -d' ' -f1)" = "88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8" ] || fail "full order-26 list hash differs"
[ "$(shasum -a 256 wp21/sample-A-m5-26.txt | cut -d' ' -f1)" = "24e381cbc4a0a65092fb2689f57bbb8163fad2d17573bf552a2ffcc42964ba31" ] || fail "phase-A selection hash differs"
if [ ! -s wp21/A-m5-26.json ]; then
  say "WP21 phase A start"
  python3 wp_cpucap.py 43200 -- python3 d1_confirm.py --phase A --order 26 --decl WP21-declaration.md --workers $W \
        --out wp21/A-m5-26.json.tmp --input-file wp21/sample-A-m5-26.txt > wp21/A-run.log 2>&1 || fail "WP21 phase A (exit $?; 3 = CPU cap reached, inconclusive)"
  mv wp21/A-m5-26.json.tmp wp21/A-m5-26.json
  say "WP21 phase A done: $(tail -1 wp21/A-run.log | cut -c1-200)"
fi
if [ ! -s wp21/A-check.log ] || ! grep -q "CHECK OK" wp21/A-check.log; then
  say "WP21 A check --all start"
  python3 d1_check21.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md --all --workers 14 \
        --subset-of $FULL --full-sha 88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8 > wp21/A-check.log 2>&1
  grep -q "CHECK OK" wp21/A-check.log || fail "WP21 A check did not pass; see wp21/A-check.log"
  say "WP21 A check OK"
fi
python3 wp_report.py wp21/A-m5-26.json --title "WP21 phase A (order 26, hash-split sample)" > wp21/A-report-numbers.md 2>> "$LOG"
say "WP21 A report numbers written"

# ---------------- WP21 phase B
python3 wp21_seeds.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt wp21/seeds-B.txt >> "$LOG" 2>&1 || fail "seeds"
if [ ! -s wp21/B.json ]; then
  say "WP21 phase B start"
  python3 wp_cpucap.py 86400 -- python3 wp21_search.py --seeds wp21/seeds-B.txt --out-prefix wp21/B --chains 12 --steps 400 \
        --seed-tag WP21 --cpu-seconds 6000 --workers $W > wp21/B-run.log 2>&1 || fail "WP21 phase B (exit $?; 3 = CPU cap reached, inconclusive)"
  say "WP21 phase B done: $(tail -1 wp21/B-run.log | cut -c1-200)"
fi
if [ ! -s wp21/B-check.log ] || ! grep -q "CHECK OK" wp21/B-check.log; then
  say "WP21 B check --all start"
  python3 d1_check21.py wp21/B.json wp21/B-evaluated.txt WP21-declaration.md --all --workers 14 > wp21/B-check.log 2>&1
  grep -q "CHECK OK" wp21/B-check.log || fail "WP21 B check did not pass; see wp21/B-check.log"
  say "WP21 B check OK"
fi
python3 wp_report.py wp21/B.json --title "WP21 phase B (order 26, adversarial search)" > wp21/B-report-numbers.md 2>> "$LOG"
say "ALL DONE"
