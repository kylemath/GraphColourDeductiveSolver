#!/bin/bash
# usage: gen_shards.sh N MOD PAR  -- plantri -m5 -c4 N res/MOD piped into TrackB frame.c (copy in bin/), PAR shards at a time, nice 10
# graphs named pN.rRES#k (k = index within shard res/MOD). Output out/shards/N/RES.{txt,count,plog}; DONE marker when finished.
N=$1; MOD=$2; PAR=${3:-8}; cd "$(dirname "$0")/.."; D=out/shards/$N; mkdir -p $D
run() { r=$1; nice -n 10 ./bin/plantri -m5 -c4 $N $r/$MOD 2>$D/$r.plog | nice -n 10 ./bin/frame p$N.r$r > $D/$r.txt 2> $D/$r.count; echo "$(date +%T) shard $r done" >> $D/progress; }
export -f run; export N MOD D
seq 0 $((MOD-1)) | xargs -P $PAR -I{} bash -c 'run {}'
touch $D/DONE
