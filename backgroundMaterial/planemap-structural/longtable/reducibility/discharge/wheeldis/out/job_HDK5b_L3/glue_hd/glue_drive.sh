#!/bin/zsh
# HDK5b_L3 glue (Opus): after HDK5BL3All builds, compile HK5BL3D_00, COccHK5BL3D_00, then HDK5BL3Occ.
# Job-root relative: run it from the job root (the folder that holds lean/ and the glue folder), or pass that folder as $1.
# It copies the three glue .lean files from the glue folder (this script's own folder name: glue_hd) into lean/ unless they are already there.
ROOT=${1:-$PWD}; cd "$ROOT/lean" || { echo "glue_drive: no lean/ under $ROOT (run from the job root or pass it as \$1)" >&2; exit 2; }
for f in HK5BL3D_00.lean COccHK5BL3D_00.lean HDK5BL3Occ.lean; do [ -e $f ] || cp "$ROOT/glue_hd/$f" .; done
until grep -q "^HDK5BL3All exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK5BL3D_00; ./run.sh COccHK5BL3D_00; ./run.sh HDK5BL3Occ; echo GLUEDONE >> status.txt
