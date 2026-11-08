#!/bin/zsh
# HCK5H05 glue (Opus): after K5H05VAll builds, compile HK5H05_00, COccHK5H05_00, then HK5H05Occ (same order as HCK3l).
# Job-root relative: run it from the job root (the folder that holds lean/ and glue_hc/), or pass that folder as $1.
# It copies the three glue .lean files from glue_hc/ into lean/ unless they are already there.
ROOT=${1:-$PWD}; cd "$ROOT/lean" || { echo "glue_drive: no lean/ under $ROOT (run from the job root or pass it as \$1)" >&2; exit 2; }
for f in HK5H05_00.lean COccHK5H05_00.lean HK5H05Occ.lean; do [ -e $f ] || cp "$ROOT/glue_hc/$f" .; done
until grep -q "^K5H05VAll exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK5H05_00; ./run.sh COccHK5H05_00; ./run.sh HK5H05Occ; echo GLUEDONE >> status.txt
