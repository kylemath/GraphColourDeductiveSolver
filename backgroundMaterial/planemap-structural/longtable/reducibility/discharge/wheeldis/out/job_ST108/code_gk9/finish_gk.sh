#!/bin/bash
# W17 round 4 (round 5 copy in code_gk7): wait for one w17_upper.sh run to end, then write its VERDICT.md and copy its logs to the deliverable folder.
# usage: bash finish_gk.sh TAG OUTDIR "COMMAND LINE" [RUNPID]
set -u
TAG=$1; OUT=$2; CMD=$3; PID=${4:-}
L=/tmp/swarm-W17/logs/$TAG; R=/tmp/swarm-W17/logs/${TAG}_run.out
mkdir -p "$OUT"
until grep -q "^RESULT:" $L/summary.txt 2>/dev/null || { [ -n "$PID" ] && ! kill -0 $PID 2>/dev/null && ! grep -q "step 4" $R 2>/dev/null; }; do sleep 60; done
sleep 5
RES=$(grep -h "^RESULT:" $L/summary.txt 2>/dev/null | tail -1); [ -z "$RES" ] && RES="RESULT: NOT ESTABLISHED (the run ended without a summary; see run.out)"
{
  echo "# ${TAG} upper check, Studio-side second engine (W17 code_gk7: GK keys + f2b7), written $(date -u +%Y-%m-%dT%H:%M:%SZ) by finish_gk.sh"
  echo
  echo "**$RES**"
  echo
  echo "Label: [E2] if FEASIBLE here and Opus's upperR2 also FEASIBLE (two engines; the generic-key rows and separator credit are W17's own,"
  echo "written from KEYSPEC.md + DUAL_EXPORT.md gkwin; the f2b7 q7m masks from from_opus/f2b7/SPEC.md; no Opus code). Otherwise the"
  echo "arrangements reported below are the disagreement. A run with DLIST set (a partial degree list) is NOT a full check: see the d list in"
  echo "the run start line."
  echo
  echo "Command:"
  echo
  echo '```'
  echo "$CMD"
  echo '```'
  echo
  echo "Run start / end: $(head -1 $R | cut -c1-400)"
  echo "$(grep -h 'step [1-4]' $R | tr '\n' ';')"
  echo
  echo "## Summary (summarize17.py)"
  echo
  echo '```'
  cat $L/summary.txt 2>/dev/null
  echo '```'
  echo
  echo "## Separator jobs (sep.log)"
  echo
  echo '```'
  cat $L/sep.log 2>/dev/null
  echo '```'
  if [ -s $L/reported.txt ]; then echo; echo "## Reported arrangements (first 50 of $(wc -l < $L/reported.txt))"; echo; echo '```'; head -50 $L/reported.txt; echo '```'; fi
} > "$OUT/VERDICT.md"
mkdir -p "$OUT/logs"; cp $L/p0.log $L/sep.log $L/summary.txt $L/killmd5.log $R "$OUT/logs/" 2>/dev/null; [ -s $L/reported.txt ] && cp $L/reported.txt "$OUT/logs/"; [ -f $L/replay.log ] && cp $L/replay.log "$OUT/logs/"
(cd "$OUT" && md5sum VERDICT.md logs/* > MD5SUMS)
echo "finish_gk: wrote $OUT/VERDICT.md: $RES"
