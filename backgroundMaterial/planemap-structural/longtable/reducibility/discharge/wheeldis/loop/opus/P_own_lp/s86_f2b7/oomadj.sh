# s86: make checker processes the OOM killer's first choice so a memory spike never takes a long LP solve (we cannot lower the LPs' score).
# upperR2 (cheap to redo) 600, lowerR2/dualexport 300; LP solves keep 0.
while true; do
  for p in $(pgrep -f "pcheck.py upperR2"); do [ "$(cat /proc/$p/oom_score_adj 2>/dev/null)" = 600 ] || echo 600 > /proc/$p/oom_score_adj 2>/dev/null; done
  for p in $(pgrep -f "pcheck.py (lowerR2|dualexport)"); do [ "$(cat /proc/$p/oom_score_adj 2>/dev/null)" = 300 ] || echo 300 > /proc/$p/oom_score_adj 2>/dev/null; done
  sleep 10
done
