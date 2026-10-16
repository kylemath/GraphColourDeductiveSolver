#!/bin/zsh
# perline.sh BIN IN OUT: run BIN on each line of IN separately (so every verdict is written as soon as it is found)
cd "$(dirname $0)"; T=$(mktemp -d)
while IFS= read -r l; do print -r -- "$l" > $T/x; nice -n 15 $1 $T/x >> $3 2>&1; done < $2
rm -rf $T; echo done > $2.DONE
