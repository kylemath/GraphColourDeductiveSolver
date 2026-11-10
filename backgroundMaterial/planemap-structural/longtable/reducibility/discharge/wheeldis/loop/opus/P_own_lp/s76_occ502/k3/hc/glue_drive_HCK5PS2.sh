#!/bin/zsh
# HCK5PS2 glue (Opus): after K5PS2VAll builds, compile HK5PS2_00, COccHK5PS2_00, then HK5PS2Occ.
# Job-root relative: run it from the job root (the folder that holds lean/ and the glue folder), or pass that folder as $1.
# It copies the three glue .lean files from the glue folder (this script's own folder name: glue_hc) into lean/ unless they are already there.
ROOT=${1:-$PWD}; cd "$ROOT/lean" || { echo "glue_drive: no lean/ under $ROOT (run from the job root or pass it as \$1)" >&2; exit 2; }
for f in HK5PS2_00.lean COccHK5PS2_00.lean HK5PS2Occ.lean; do [ -e $f ] || cp "$ROOT/glue_hc/$f" .; done
until grep -q "^K5PS2VAll exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK5PS2_00; ./run.sh COccHK5PS2_00; ./run.sh HK5PS2Occ; echo GLUEDONE >> status.txt
