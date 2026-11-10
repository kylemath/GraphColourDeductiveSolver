#!/bin/zsh
# HDK3GX glue (Opus): after HDK3GXAll builds, compile HK3GXD_kk then COccHK3GXD_kk for kk = 00..89, then HDK3GXOcc.
# Job-root relative: run it from the job root (the folder that holds lean/ and the glue folder), or pass that folder as $1.
# It copies the glue .lean files from the glue folder (glue_hd) into lean/ unless they are already there.
ROOT=${1:-$PWD}; cd "$ROOT/lean" || { echo "glue_drive: no lean/ under $ROOT (run from the job root or pass it as \$1)" >&2; exit 2; }
for f in "$ROOT"/glue_hd/*.lean; do b=${f:t}; [ -e $b ] || cp "$f" .; done
until grep -q "^HDK3GXAll exit=0" status.txt 2>/dev/null; do sleep 30; done
for k in $(seq -w 0 89); do ./run.sh HK3GXD_$k; ./run.sh COccHK3GXD_$k; done
./run.sh HDK3GXOcc; echo GLUEDONE >> status.txt
