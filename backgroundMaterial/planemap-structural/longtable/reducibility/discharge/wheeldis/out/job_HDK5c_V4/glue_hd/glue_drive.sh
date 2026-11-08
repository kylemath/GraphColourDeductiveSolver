#!/bin/zsh
# HDK5c_V4 glue (Opus): after HDK5CV4All builds, compile HK5CV4D_00, COccHK5CV4D_00, then HDK5CV4Occ.
# Job-root relative: run it from the job root (the folder that holds lean/ and the glue folder), or pass that folder as $1.
# It copies the three glue .lean files from the glue folder (this script's own folder name: glue_hd) into lean/ unless they are already there.
ROOT=${1:-$PWD}; cd "$ROOT/lean" || { echo "glue_drive: no lean/ under $ROOT (run from the job root or pass it as \$1)" >&2; exit 2; }
for f in HK5CV4D_00.lean COccHK5CV4D_00.lean HDK5CV4Occ.lean; do [ -e $f ] || cp "$ROOT/glue_hd/$f" .; done
until grep -q "^HDK5CV4All exit=0" status.txt 2>/dev/null; do sleep 30; done
./run.sh HK5CV4D_00; ./run.sh COccHK5CV4D_00; ./run.sh HDK5CV4Occ; echo GLUEDONE >> status.txt
