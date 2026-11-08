#!/bin/zsh
# HCK3GX glue (Opus): after K3GXVAll builds, compile HK3GX_kk then COccHK3GX_kk for kk = 00..68, then HK3GXOcc.
# Job-root relative: run it from the job root (the folder that holds lean/ and the glue folder), or pass that folder as $1.
# It copies the glue .lean files from the glue folder (glue_hc) into lean/ unless they are already there.
ROOT=${1:-$PWD}; cd "$ROOT/lean" || { echo "glue_drive: no lean/ under $ROOT (run from the job root or pass it as \$1)" >&2; exit 2; }
for f in "$ROOT"/glue_hc/*.lean; do b=${f:t}; [ -e $b ] || cp "$f" .; done
until grep -q "^K3GXVAll exit=0" status.txt 2>/dev/null; do sleep 30; done
for k in $(seq -w 0 68); do ./run.sh HK3GX_$k; ./run.sh COccHK3GX_$k; done
./run.sh HK3GXOcc; echo GLUEDONE >> status.txt
