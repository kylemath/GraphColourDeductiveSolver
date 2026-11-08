#!/bin/zsh
# HDOF7 glue (Opus): after HDOF7All builds, compile HOF7_kk then COccHOF7_kk for kk = 00..64, then HDOF7Occ.
# Job-root relative: run it from the job root (the folder that holds lean/ and the glue folder), or pass that folder as $1.
# It copies the glue .lean files from the glue folder (glue_hd) into lean/ unless they are already there.
# HDOF7Occ ties hD_i to the per-key occurrence modules only; the per-line off-centre kill theorems still need Offc.OffcRotOcc (OffcOcc.lean).
ROOT=${1:-$PWD}; cd "$ROOT/lean" || { echo "glue_drive: no lean/ under $ROOT (run from the job root or pass it as \$1)" >&2; exit 2; }
for f in "$ROOT"/glue_hd/*.lean; do b=${f:t}; [ -e $b ] || cp "$f" .; done
until grep -q "^HDOF7All exit=0" status.txt 2>/dev/null; do sleep 30; done
for k in $(seq -w 0 64); do ./run.sh HOF7_$k; ./run.sh COccHOF7_$k; done
./run.sh HDOF7Occ; echo GLUEDONE >> status.txt
