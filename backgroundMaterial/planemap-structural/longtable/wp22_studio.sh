#!/bin/bash
# wp22_studio.sh -- WP22 (S2) launcher: verify the hashed package, then s2c, s2b, s2a; merge each; stop at the first
# failure.  Idempotent and resumable (re-run the same command after an interruption).
#
#   wp22_studio.sh make-sums          write $WP22_DIR/PACKAGE-SHA256SUMS for the package (the lead does this once and
#                                     announces the hash of that file)
#   wp22_studio.sh                    verify, run s2c, s2b, s2a, merge, write $WP22_DIR/RECORD.txt
#   WORKERS=14 (default) | WP22_DIR=wp22 | S2C_EXTRA_DIRS="dir dir"  (more certificate directories, e.g. Math's second
#   search) | S2A_TAG_CPU=120 | S2A_CPU_CAP=6000 | S2A_TAGS=40 | SUMS=path (the sums file to verify)
# Work happens in $WP22_DIR (default: wp22/ next to this script): run-s2c/, run-s2b/, run-s2a/, out/, RECORD.txt.
set -euo pipefail
cd "$(dirname "$0")"
WORKERS=${WORKERS:-14}
WP22_DIR=${WP22_DIR:-wp22}
SUMS=${SUMS:-$WP22_DIR/PACKAGE-SHA256SUMS}
S2A_TAG_CPU=${S2A_TAG_CPU:-120}
S2A_CPU_CAP=${S2A_CPU_CAP:-6000}
S2A_TAGS=${S2A_TAGS:-40}
PKG="wp22_radius.py wp22_search.py wp22_census.py wp22_s2c.py wp22_runner.py wp22_studio.sh wp22_tests.py WP22-S2-preregistration.md WP22-interface.md"
PY=${PYTHON:-python3}
mkdir -p "$WP22_DIR"
if [ "${1:-}" = "make-sums" ]; then
  shasum -a 256 $PKG > "$SUMS"
  echo "wrote $SUMS"; shasum -a 256 "$SUMS"; exit 0
fi
[ -f "$SUMS" ] || { echo "FAIL: $SUMS missing (run: $0 make-sums, and announce its hash)"; exit 2; }
shasum -a 256 -c "$SUMS" || { echo "FAIL: package files differ from $SUMS"; exit 2; }
START="$(date '+%Y-%m-%d %H:%M:%S %z')"
OUT="$WP22_DIR/out"; mkdir -p "$OUT"
finish() {
  rc=$?
  $PY wp22_runner.py record "$WP22_DIR/RECORD.txt" --workers "$WORKERS" --start "$START" \
      --end "$(date '+%Y-%m-%d %H:%M:%S %z') (script exit status $rc)" \
      --run "$WP22_DIR/run-s2c" --run "$WP22_DIR/run-s2b" --run "$WP22_DIR/run-s2a" \
      --hash-file "$SUMS" --hash-file "$OUT/s2c.jsonl" --hash-file "$OUT/s2c-summary.json" \
      --hash-file "$OUT/s2b.jsonl" --hash-file "$OUT/s2b-summary.json" --hash-file "$OUT/s2a-summary.json" \
      2>/dev/null || true
  exit $rc
}
trap finish EXIT
CERT_ARGS=""
for d in ${S2C_EXTRA_DIRS:-}; do CERT_ARGS="$CERT_ARGS --cert-dir $d"; done
if [ -n "$CERT_ARGS" ]; then   # defaults must then be named explicitly
  CERT_ARGS="--cert-dir ../../../SolvingFrameworkPlan/docs/working/MathChainSearch/certs_len_ge6 --cert-dir ../../../SolvingFrameworkPlan/docs/working/MathChainSearch/lt_certs $CERT_ARGS"
fi
phase() {  # name, plan args...
  name=$1; shift
  echo "== $name: plan"; $PY wp22_runner.py plan "$WP22_DIR/run-$name" "$@"
  echo "== $name: run";  $PY wp22_runner.py run "$WP22_DIR/run-$name" --workers "$WORKERS"
  echo "== $name: status"; $PY wp22_runner.py status "$WP22_DIR/run-$name" --verify
  echo "== $name: merge"; $PY wp22_runner.py merge "$WP22_DIR/run-$name" "$OUT/$name"
}
phase s2c --mode s2c $CERT_ARGS
phase s2b --mode s2b
phase s2a --mode s2a --tags "$S2A_TAGS" --tag-cpu "$S2A_TAG_CPU" --cpu-cap "$S2A_CPU_CAP"
echo "WP22 complete: $OUT"
