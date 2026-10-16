#!/bin/bash
# append cfast verdicts (C / noC) of OUT to vcache.txt.  Usage: cparse.sh CFASTOUT
awk '/ r=/ && !/^ /{cur=$1} /C-REDUCIBLE/{if(cur!=""){print cur"C C cfast"; c[cur]=1}} /search \|X\|/{if(cur!="" && !(cur in c)) print cur"C noC cfast"}' $1 | sort -u >> $(dirname $(readlink -f $0))/vcache.txt
