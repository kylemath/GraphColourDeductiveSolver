#!/bin/zsh
# HDK5c_V1 glue (Opus): after HDK5CV1All builds, compile HK5CV1D_00, COccHK5CV1D_00, then HDK5CV1Occ.
# Job-root relative: run it from the job root (the folder that holds lean/ and the glue folder), or pass that folder as $1.
# It copies the three glue .lean files from the glue folder (this script's own folder name: glue_hd) into lean/ unless they are already there.
ROOT=${1:-$PWD}; cd "$ROOT/lean" || { echo "glue_drive: no lean/ under $ROOT (run from the job root or pass it as \$1)" >&2; exit 2; }
for f in HK5CV1D_00.lean COccHK5CV1D_00.lean HDK5CV1Occ.lean; do [ -e $f ] || cp "$ROOT/glue_hd/$f" .; done
until grep -q "^HDK5CV1All exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK5CV1D_00; ./run.sh COccHK5CV1D_00; ./run.sh HDK5CV1Occ; echo GLUEDONE >> status.txt
